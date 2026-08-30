#!/usr/bin/env python3
"""
AI FX研究所 - 「今日の詳しい分析」自動生成スクリプト

背景:
  従来は「声掛け制」（ユーザーが「今日の分析書いて」と頼むたびにClaude Codeが
  signal.jsonの実データを見て手で書き、GitHub Contents APIでコミットする）
  だった。本スクリプトはこれを置き換え、GitHub Actionsから1日2回（東京時間
  8:00・22:00）自動実行し、LLM（Gemini API）に実データを渡して文章化させる
  「完全自動」方式。2026-08-14、ユーザーの明示的な合意により導入。

設計方針（ハルシネーション対策）:
  - LLMは「渡した事実データを言語化するだけの翻訳機」として使う。
    LLM自身の事前学習知識や推測でニュース・数値を補わせない
   （システムプロンプトで明示的に禁止）。
  - 断定・予測を避けた客観的な文体を指示する。
  - 売買に直結する数値（entry/take_profit/stop_loss）はLLMに生成させず、
    compute_signal.pyがルールベースで計算した priority_trade の値を
    Python側でそのまま差し込む（価格のハルシネーションを構造的に排除）。
  - LLMの出力はJSON Schema（Gemini APIのresponseSchema）で構造を強制した上、
    断定的な表現（「確実」「保証」等）が含まれていないかPython側で正規表現
    チェックする。どちらかに引っかかった場合は書き込みを行わず、
    直前のdaily_analysis.jsonをそのまま残す（サイトが古い情報のまま
    壊れずに動き続けることを優先する）。

経済指標カレンダー:
  ForexFactoryの週間XMLフィード（無料・キー不要・スクレイピング規約上も
  問題ない配布用フィード）から、JPY/USDの中〜高重要度イベントのみを
  抽出してLLMへの入力に含める。
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=9))

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = "gemini-flash-latest"  # Google管理のエイリアス。常時その時点のflash系最新モデルを指す
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

FF_CALENDAR_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

# 「断定」「保証」の類を検出するための簡易チェック（完璧な検知ではないが、
# 明らかにアウトな表現が混入した場合に自動反映を止める最後の砦として機能する）
BANNED_PATTERNS = [
    "確実", "保証", "絶対に", "間違いない", "必ず", "断言", "太鼓判",
    "投資助言", "買うべき", "売るべき",
]

TREND_JA = {"up": "上昇", "down": "低下", "flat": "横ばい"}
CHANNEL_TREND_JA = {"UP": "上昇", "DOWN": "下降", "FLAT": "横ばい"}

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "headline": {"type": "STRING"},
        "advice": {"type": "ARRAY", "items": {"type": "STRING"}, "minItems": 2, "maxItems": 3},
        "scenarios": {
            "type": "ARRAY",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "OBJECT",
                "properties": {
                    "label": {"type": "STRING"},
                    "probability": {"type": "INTEGER"},
                    "color": {"type": "STRING", "enum": ["buy", "sell", "neutral"]},
                    "body": {"type": "STRING"},
                },
                "required": ["label", "probability", "color", "body"],
            },
        },
        "economic_events_note": {"type": "STRING"},
        "order_plan_lead": {"type": "STRING"},
        "order_plan_sub_note": {"type": "STRING"},
        "risk_note": {"type": "STRING"},
    },
    "required": [
        "headline", "advice", "scenarios", "economic_events_note",
        "order_plan_lead", "order_plan_sub_note", "risk_note",
    ],
}

SYSTEM_PROMPT = """あなたはUSD/JPY(ドル円)を専門とする、冷静で客観的な市場解説者です。
これから渡す【提供データ】だけを根拠に、当サイト「AI FX研究所」の「今日の詳しい分析」欄の
文章をJSON形式で生成してください。

【厳守するルール】
1. 事実のみを使うこと。【提供データ】に無い数値・ニュース・出来事を、あなた自身の
   知識や推測で補ったり創作したりしないでください。分からないことは書かない。
2. 断定の禁止。「AだからBになった」のような一方的な因果の断定を避け、
   「Aとなるなか、Bが推移している」のように事象を並べる客観的な書き方にしてください。
3. 将来予測・投資助言の禁止。「今後は〜になるだろう」「〜すべきだ」等は書かないでください。
   ただし scenarios（本命／上抜け／下抜けの3パターン）は、あくまで「もし〜円を超えたら
   どちらに動きやすいか」という条件付きの構造的な整理であり、断定的な将来予測ではないので、
   この項目に限り「〜円を試す」「〜円方向へ反落」のような条件付きの記述は許可します。
4. 「確実」「保証」「絶対」等の強い断定語は一切使わないでください。
5. 簡潔でプロフェッショナルな文体。日本語。絵文字は使わない。
6. order_plan_lead / order_plan_sub_note には、具体的な価格の逆指値・利確・損切り数値を
   自分で計算して書かないでください（数値は別のルールベースの計算結果を機械的に
   使うため、あなたは方針・注意点の文章だけを書けば十分です）。

【出力するJSONの各キーについて】
- headline: 見出し（30文字程度）
- advice: 分析本文の段落（2〜3個の配列）。地合い・テクニカル・通貨強弱等を客観的に整理する。
- scenarios: 本命/上抜け/上抜け以外の3パターン（label, probability(0-100の整数,
  合計100目安), color("buy"/"sell"/"neutral"), body）
- economic_events_note: 当日の経済指標に関する客観的な注記（無ければ「特筆すべき
  重要指標はありません」等）
- order_plan_lead: 戦略の要点（1〜2文、価格の具体数値は書かない）
- order_plan_sub_note: 補足（1〜2文、価格の具体数値は書かない）
- risk_note: リスク・注意点（1〜2文）
"""


def fetch_calendar_events():
    """
    ForexFactoryの週間XMLフィードから、JPY/USDの中〜高重要度イベントのうち
    「今日（JST）」に該当するものだけを抽出する。取得・パースに失敗した場合は
    空リストを返す（経済指標欄が「特になし」相当になるだけで、本体の生成は止めない）。
    """
    try:
        req = urllib.request.Request(FF_CALENDAR_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as res:
            raw = res.read()
        root = ET.fromstring(raw)
    except (urllib.error.URLError, TimeoutError, ET.ParseError):
        return []

    today_jst = datetime.now(JST).date()
    events = []
    for e in root.findall("event"):
        country = e.findtext("country") or ""
        impact = e.findtext("impact") or ""
        if country not in ("JPY", "USD"):
            continue
        if impact not in ("High", "Medium"):
            continue
        date_str = (e.findtext("date") or "").strip()
        try:
            event_date = datetime.strptime(date_str, "%m-%d-%Y").date()
        except ValueError:
            continue
        if event_date != today_jst:
            continue
        events.append({
            "title": (e.findtext("title") or "").strip(),
            "country": country,
            "impact": impact,
            "time": (e.findtext("time") or "").strip(),
            "forecast": (e.findtext("forecast") or "").strip(),
            "previous": (e.findtext("previous") or "").strip(),
        })
    return events


def build_data_block(signal, events):
    sig = signal.get("signal", {})
    channels = signal.get("regression_channels", [])
    technical = signal.get("technical", {})
    macro = signal.get("macro", {})
    cs = signal.get("currency_strength", [])
    sr = technical.get("support_resistance") or {}
    macd = technical.get("macd") or {}
    rsi = technical.get("rsi") or {}

    lines = []
    lines.append(f"現在時刻(JST): {datetime.now(JST).strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"USD/JPY 現在値: {signal.get('latest_price')}円（直近1時間比 {signal.get('day_change_pct')}%）")
    lines.append(f"AI総合シグナル: {sig.get('bias_label')}（信頼度{sig.get('confidence')}%）")
    lines.append(f"相場モード: {signal.get('market_mode')}（{signal.get('market_mode_note')}）")

    for ch in channels:
        trend_ja = CHANNEL_TREND_JA.get(ch.get("trend"), ch.get("trend"))
        lines.append(
            f"- {ch.get('label')}: 中心線からの位置 {ch.get('position_sigma')}σ、トレンド{trend_ja}、"
            f"中心{ch.get('mid')}円/上限{ch.get('upper')}円/下限{ch.get('lower')}円"
        )

    reversal = signal.get("reversal_setup")
    if reversal:
        lines.append(
            f"1分足の反発トリガー: 直近の谷/山{reversal.get('extreme')}円から"
            f"{reversal.get('reverted_pips')}pips反発したタイミングでシグナル発動"
        )

    if sr:
        lines.append(f"サポート: {sr.get('support')}円 / レジスタンス: {sr.get('resistance')}円")
    if macd:
        lines.append(f"MACD: {macd.get('state')}（ヒストグラム{macd.get('histogram')}）")
    if rsi:
        lines.append(f"RSI(14): {rsi.get('value')}（{rsi.get('state')}）")

    if macro:
        lines.append(
            "米10年債利回り: {}%（{}基調） / 日本10年債利回り: {}%（{}基調） / "
            "DXY: {}（{}基調） / WTI原油: {}基調".format(
                macro.get("us10y_latest"), TREND_JA.get(macro.get("us10y_trend"), "横ばい"),
                macro.get("jp10y_latest"), TREND_JA.get(macro.get("jp10y_trend"), "横ばい"),
                macro.get("dxy_latest"), TREND_JA.get(macro.get("dxy_trend"), "横ばい"),
                TREND_JA.get(macro.get("wti_trend"), "横ばい"),
            )
        )

    if cs:
        cs_txt = "、".join(f"{c['code']} {c['change_pct']:+.2f}%" for c in cs)
        lines.append(f"通貨強弱（直近1日）: {cs_txt}")

    if events:
        lines.append("本日の経済指標（JPY・USD、中〜高重要度）:")
        for ev in events:
            fc = f"予想{ev['forecast']}" if ev["forecast"] else "予想非公表"
            pv = f"前回{ev['previous']}" if ev["previous"] else "前回非公表"
            lines.append(f"- {ev['time']} [{ev['country']}/{ev['impact']}] {ev['title']}（{fc}・{pv}）")
    else:
        lines.append("本日の経済指標（JPY・USD、中〜高重要度）: 該当なし")

    return "\n".join(lines)


RETRYABLE_HTTP_CODES = (429, 500, 502, 503, 504)


def call_gemini(data_block):
    if not GEMINI_API_KEY:
        raise RuntimeError("環境変数 GEMINI_API_KEY が設定されていません")

    body = json.dumps({
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"parts": [{"text": "【提供データ】\n" + data_block}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": RESPONSE_SCHEMA,
            "temperature": 0.4,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    # Gemini APIは無料枠の混雑時に503(Service Unavailable)を返すことがある
    # (Google公式にも一時的なエラーとして再試行が推奨されている)。1回失敗しただけで
    # 諦めず、数秒待って数回まで再試行することで、混雑のタイミングに毎回引っかかって
    # 何日も更新が止まる、という事態を避ける。
    attempts = 4
    delays = [5, 15, 30]  # 各リトライ前の待機秒数
    last_error = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=60) as res:
                payload = json.loads(res.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code not in RETRYABLE_HTTP_CODES:
                raise
            if attempt < attempts - 1:
                print(f"[WARN] Gemini APIがHTTP {e.code}を返したため、{delays[attempt]}秒後に再試行します（{attempt + 1}/{attempts}回目）", file=sys.stderr)
                time.sleep(delays[attempt])
            else:
                raise
    else:
        raise last_error  # 実際にはbreakかraiseで抜けるため到達しないが、念のため

    candidates = payload.get("candidates") or []
    if not candidates:
        raise RuntimeError(f"Gemini APIから候補が返りませんでした: {payload}")
    parts = candidates[0].get("content", {}).get("parts") or []
    if not parts:
        raise RuntimeError(f"Gemini APIのレスポンスにpartsがありません: {candidates[0]}")
    text = parts[0].get("text", "")
    return json.loads(text)


def list_available_models():
    """
    診断用: このAPIキーで実際に使えるモデル名の一覧をGemini APIから取得する。
    call_geminiが404を返した場合（モデル名が存在しない等）に、次回実行時の
    ログへ手がかりを残すために使う。取得に失敗しても例外は投げない。
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
        with urllib.request.urlopen(url, timeout=30) as res:
            payload = json.loads(res.read().decode("utf-8"))
        names = [
            m.get("name") for m in payload.get("models", [])
            if "generateContent" in (m.get("supportedGenerationMethods") or [])
        ]
        return names
    except Exception as e:  # noqa: BLE001
        return [f"(モデル一覧の取得にも失敗: {e})"]


def find_banned_word(obj):
    """objの中の全文字列を再帰的に走査し、禁止語を含む文字列があれば返す。無ければNone。"""
    if isinstance(obj, str):
        for w in BANNED_PATTERNS:
            if w in obj:
                return w
        return None
    if isinstance(obj, dict):
        for v in obj.values():
            hit = find_banned_word(v)
            if hit:
                return hit
        return None
    if isinstance(obj, list):
        for v in obj:
            hit = find_banned_word(v)
            if hit:
                return hit
        return None
    return None


def validate_llm_output(obj):
    for key in RESPONSE_SCHEMA["required"]:
        if key not in obj:
            raise ValueError(f"必須キー'{key}'がLLM出力にありません")
    if not isinstance(obj["advice"], list) or not obj["advice"]:
        raise ValueError("adviceが空、または配列ではありません")
    if not isinstance(obj["scenarios"], list) or len(obj["scenarios"]) != 3:
        raise ValueError("scenariosは3件である必要があります")
    for sc in obj["scenarios"]:
        if sc.get("color") not in ("buy", "sell", "neutral"):
            raise ValueError(f"scenarios.colorが不正です: {sc.get('color')}")
        prob = sc.get("probability")
        if not isinstance(prob, int) or not (0 <= prob <= 100):
            raise ValueError(f"scenarios.probabilityが不正です: {prob}")
    banned = find_banned_word(obj)
    if banned:
        raise ValueError(f"禁止語'{banned}'がLLM出力に含まれています")


def build_order_plan(llm_obj, signal):
    """
    価格に関わる数値（entry/take_profit/stop_loss）はLLMに生成させず、
    compute_signal.pyがルールベースで計算したpriority_tradeの値をそのまま使う。
    lead/sub_noteの文章部分だけLLM出力を採用する。
    """
    trade = signal.get("priority_trade", {})
    entry = trade.get("entry")
    tp = trade.get("take_profit")
    sl = trade.get("stop_loss")
    return {
        "lead": llm_obj["order_plan_lead"],
        "entry": f"{entry}円付近（現在値）" if entry is not None else "様子見（新規エントリーなし）",
        "take_profit": f"{tp}円" if tp is not None else "‒",
        "stop_loss": f"{sl}円" if sl is not None else "‒",
        "sub_note": llm_obj["order_plan_sub_note"],
    }


def load_signal(signal_path):
    with open(signal_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    signal_path = os.path.abspath(os.path.join(base_dir, "signal.json"))
    out_path = os.path.abspath(os.path.join(base_dir, "daily_analysis.json"))

    try:
        signal = load_signal(signal_path)
        events = fetch_calendar_events()
        data_block = build_data_block(signal, events)
        llm_obj = call_gemini(data_block)
        validate_llm_output(llm_obj)

        now_jst = datetime.now(JST)
        result = {
            "date": now_jst.strftime("%Y-%m-%d"),
            "updated_at_jst": now_jst.strftime("%Y-%m-%d %H:%M"),
            "headline": llm_obj["headline"],
            "advice": llm_obj["advice"],
            "scenarios": llm_obj["scenarios"],
            "economic_events_note": llm_obj["economic_events_note"],
            "order_plan": build_order_plan(llm_obj, signal),
            "risk_note": llm_obj["risk_note"],
        }
    except Exception as e:  # noqa: BLE001
        # 失敗時は既存のdaily_analysis.jsonに一切触れない
        # （直前の分析が残るだけで、サイトが空欄や壊れた状態になることはない）。
        print(f"[WARN] daily_analysis生成に失敗したため、既存ファイルを維持します: {e}", file=sys.stderr)
        if "404" in str(e):
            print("[DEBUG] このAPIキーで実際に使えるモデル一覧:", file=sys.stderr)
            for name in list_available_models():
                print(f"  - {name}", file=sys.stderr)
        sys.exit(0)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"書き出し完了: {out_path}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
