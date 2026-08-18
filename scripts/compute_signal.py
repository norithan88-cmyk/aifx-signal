#!/usr/bin/env python3
"""
AI FX研究所 - 本日のAIシグナル 自動計算スクリプト

やっていること（概要）:
  1. Yahoo Finance の公開チャートAPI（無料・キー不要）から
     USD/JPY の価格（1分足・5分足・15分足・1時間足）を取得する。毎回実行時に取得。
  2. Alpha Vantage（無料枠）から米10年債利回り・WTI原油（いずれも日足）を取得する。
     ただし元データが日足のため、当日分をすでに取得済みなら再取得せず使い回す
    （無料枠が1日25回までのため、頻繁な実行でも枠を消費しないようにするため）。
  3. 5分・15分・1時間足の3つで線形回帰チャネルを計算し、3つとも「チャネル中心から
     ±1.3σ以上その方向に偏っている」状態(momentum_direction)が一致した時だけ、
     上位足の方向（押し目買い/戻り売りの候補方向）を確定する。
  4. その方向候補が確定している時だけ、1分足がその方向に逆行してチャネル際まで
     達し、そこから戻り始めたタイミング(detect_reversal_setup)を検出し、
     検出できた瞬間だけ実際のSELL/BUYシグナルとして確定する（それ以外はWAIT）。
  5. Entry = 直近1分足終値。TP/SLは、1分足の逆行の谷/山（測定値幅）を基準に算出する。
  6. 結果を signal.json として書き出す（GitHub Actionsがコミットし、
     raw.githubusercontent.com経由でWordPress側から読み込む）。

設計方針:
  - ブラックボックスなAI予測ではなく、「なぜその判定になったか」を
    誰でも追える単純な統計ルール（回帰チャネル）にしている。
  - このロジック（5分・15分・1時間足の方向一致＋1分足の逆行からの戻り）は、
    2025-01〜2026-07の19ヶ月・実データでのwalk-forwardバックテストで検証済み
    （勝率70.3%・PF1.88・19ヶ月中18ヶ月がプラス）。ただし本番の自動実行は
    5分おき設定でも実際は10分〜2時間おきになることがあり、1分単位の
    反発タイミングを毎回リアルタイムで捉えられるとは限らない点に留意。
  - 実際のトレード成績を保証するものではない。あくまで
    「参考情報を自動更新する」ためのツール。
  - 為替の分足・時間足データは、Alpha Vantageの無料枠が2026年時点で
    「historical intraday」を有料化してしまったため、Yahoo Financeの
    非公式だが広く使われているチャートAPI（yfinance等でも使われているもの）
    を利用している。公式サポートのAPIではないため、将来URLの仕様が
    変わって取得できなくなる可能性はゼロではない（その場合はエラーとして
    検知され、既存の静的表示のまま維持される）。
  - 米10年債・WTIはAlpha Vantageの無料枠（日足データ）で取得。1日1回だけ
    実際にAPIを呼び、それ以外の実行では前回のsignal.jsonの値を使い回す。
    日本10年債は財務省が公開する金利情報CSV（無料・無制限、Shift-JIS）を
    直接読み込んで取得し、これも日足データのため1日1回だけ取得する。
    DXY（ドル指数）・GOLD（金、シンボル"GC=F"）はYahoo Financeの同じ非公式
    チャートAPIで取得でき、レート制限が無いため他のFXペアと同様に毎回取得する
    （Alpha Vantage無料枠ではGOLDを取得できないため、こちらを使っている）。
  - 経済指標カレンダー（今夜の重要指標）は無料で信頼できる自動取得先が
    見つからなかったため、今回は自動化していない（手動更新のまま）。
"""

import csv
import io
import json
import os
import smtplib
import statistics
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import parsedate_to_datetime

ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "").strip()
BASE_URL = "https://www.alphavantage.co/query"
YAHOO_CHART_BASE = "https://query1.finance.yahoo.com/v8/finance/chart"
MOF_JGB_CSV_URL = "https://www.mof.go.jp/jgbs/reference/interest_rate/jgbcm.csv"

# 「LATEST NEWS」欄用。ForexLive・DailyFXはRSS取得が403でブロックされたため使えず、
# 日本語サイトなので英語のInvesting.comから、日本語のザイFX！（ダイヤモンド社）に切り替えた。
# （重要度でのフィルタリングはしない。フィードに載っている見出しをそのまま使う）
NEWS_FEEDS = [
    ("ザイFX！", "https://zai.diamond.jp/list/feed/rssfxnews"),
]
MAX_NEWS_AGE_HOURS = 24  # これより古い見出しは「今日のニュース」として不適切なので除外する

# 新規シグナル(SELL/BUY)発生時のメール通知用（Gmailアプリパスワード方式）。
# いずれかが未設定なら send_signal_email は何もしない（任意機能）。
GMAIL_SENDER = os.environ.get("GMAIL_SENDER", "").strip()
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
NOTIFY_EMAIL_TO = os.environ.get("NOTIFY_EMAIL_TO", "").strip()

# 通貨強弱（簡易版）の算出に使う補助ペア。(Yahoo Financeシンボル, base通貨, quote通貨)
# USD/JPY自体は既存のh1データを流用するのでここには含めない。
STRENGTH_PAIRS = [
    ("EURUSD=X", "EUR", "USD"),
    ("GBPUSD=X", "GBP", "USD"),
    ("AUDUSD=X", "AUD", "USD"),
    ("NZDUSD=X", "NZD", "USD"),
    ("USDCHF=X", "USD", "CHF"),
    ("USDCAD=X", "USD", "CAD"),
]

# 回帰チャネル計算に使う直近バーの本数
LOOKBACK = 100

# チャネル内での位置（sigma単位）がこれを超えたら「その方向に強く偏っている」とみなす
EDGE_THRESHOLD = 1.3

# 1分足の「逆行からの戻り」判定パラメータ（2025-01〜2026-07・19ヶ月のバックテストで検証済みの値）
REVERT_WINDOW = 10       # 直近何本(分)以内に逆行の谷/山を探すか
REVERT_MIN_PIPS = 3.0    # 「戻り出した」とみなす最低反発幅(pips、ノイズ除去用)
SL_BUFFER_PIPS = 2.0     # 逆行の谷/山からSLまでの余白(pips)


def http_get_json(params, retries=3, wait_sec=15):
    """Alpha Vantage APIを呼び出してJSONを返す。レート制限時は少し待って再試行する。"""
    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{BASE_URL}?{query}&apikey={ALPHA_VANTAGE_KEY}"
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=30) as res:
                data = json.loads(res.read().decode("utf-8"))
            if "Note" in data or "Information" in data:
                # レート制限メッセージ。少し待って再試行。
                last_err = RuntimeError(data.get("Note") or data.get("Information"))
                time.sleep(wait_sec)
                continue
            return data
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            time.sleep(wait_sec)
    raise RuntimeError(f"API呼び出しに失敗しました: {params.get('function')} ({last_err})")


def fetch_fx_intraday(symbol, interval, range_):
    """
    Yahoo Financeの公開チャートAPIから指定シンボルの分足・時間足データ（ローソク足）を取得し、
    [{"t":timestamp,"o":始値,"h":高値,"l":安値,"c":終値}, ...] を古い順（null値を除く）で返す。
    symbol例: "JPY=X"（USD/JPY） "EURUSD=X" / interval例: "1m" "5m" "15m" "60m" / range例: "5d" "60d"
    """
    url = f"{YAHOO_CHART_BASE}/{symbol}?interval={interval}&range={range_}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                data = json.loads(res.read().decode("utf-8"))
            result = data.get("chart", {}).get("result")
            if not result:
                raise RuntimeError(f"{symbol} {interval} のデータが取得できませんでした: {data.get('chart', {}).get('error')}")
            r = result[0]
            timestamps = r.get("timestamp") or []
            quote = r["indicators"]["quote"][0]
            opens = quote.get("open") or []
            highs = quote.get("high") or []
            lows = quote.get("low") or []
            closes = quote.get("close") or []
            bars = []
            for i, ts in enumerate(timestamps):
                c = closes[i] if i < len(closes) else None
                if c is None:
                    continue
                o = opens[i] if i < len(opens) and opens[i] is not None else c
                h = highs[i] if i < len(highs) and highs[i] is not None else max(o, c)
                low = lows[i] if i < len(lows) and lows[i] is not None else min(o, c)
                bars.append({"t": ts, "o": o, "h": h, "l": low, "c": c})
            if not bars:
                raise RuntimeError(f"{symbol} {interval} のデータが空でした")
            return bars
        except (urllib.error.URLError, TimeoutError, RuntimeError) as e:
            last_err = e
            time.sleep(5)
    raise RuntimeError(f"Yahoo Financeからの取得に失敗しました: {symbol} {interval} ({last_err})")


def pair_change_pct(bars, lookback_bars=24):
    """
    直近バーが lookback_bars 本前の終値からどれだけ%変化したかを返す。
    1時間足で24本 = 約1日分の変化率、という使い方を想定。
    """
    if len(bars) < 2:
        return 0.0
    latest = bars[-1]["c"]
    base_idx = -lookback_bars if len(bars) > lookback_bars else 0
    base = bars[base_idx]["c"]
    if not base:
        return 0.0
    return (latest - base) / base * 100


# 通貨強弱スコアの固定スケール。この%変化で±100スコアに達する。「その日の最大変動値を
# ±100とみなす」相対正規化ではなく固定スケールにしているのは、静かな日にごく小さな変動が
# 誇張されて「非常に強い/弱い」と表示されてしまう（相対正規化の欠点）のを避けるため。
# 主要通貨ペアの日中変動が通常2%を超えることは稀（±2.5%は大きな指標発表・要人発言級の
# 動きに相当）という前提で設定している。
CURRENCY_STRENGTH_MAX_PCT = 2.5


def currency_strength_score(change_pct, max_pct=CURRENCY_STRENGTH_MAX_PCT):
    """change_pct（%）を-100〜+100のスコアに変換する（固定スケール、上下限でクランプ）。"""
    score = change_pct / max_pct * 100
    return round(max(-100.0, min(100.0, score)), 1)


def compute_currency_strength(usdjpy_bars):
    """
    通貨強弱（簡易版）。EUR/GBP/AUD/NZD/CHF/CADの主要6ペア＋USD/JPYの
    1時間足の直近1日（24本）騰落率から、8通貨それぞれの強弱スコアを算出する。

    設計上の割り切り: USDは7ペア全てに登場するため平均が取れて比較的信頼できるが、
    JPY・EUR・GBP・AUD・NZD・CHF・CADはそれぞれ1ペアのみからの算出（真のクロス通貨網羅
    ではない簡易版）。取得に失敗したペアは黙ってスキップし、成功した分だけで算出する
    （全滅した場合は空リストを返し、呼び出し側でキー自体を省略する）。
    """
    contributions = {c: [] for c in ("USD", "EUR", "GBP", "JPY", "AUD", "CHF", "CAD", "NZD")}

    usdjpy_change = pair_change_pct(usdjpy_bars)
    contributions["USD"].append(usdjpy_change)
    contributions["JPY"].append(-usdjpy_change)

    for symbol, base, quote in STRENGTH_PAIRS:
        try:
            bars = fetch_fx_intraday(symbol, "60m", "5d")
        except RuntimeError:
            continue
        change = pair_change_pct(bars)
        contributions[base].append(change)
        contributions[quote].append(-change)

    result = []
    for code, vals in contributions.items():
        if not vals:
            continue
        avg = sum(vals) / len(vals)
        result.append({
            "code": code,
            "change_pct": round(avg, 2),
            "strength_score": currency_strength_score(avg),
        })
    result.sort(key=lambda x: x["strength_score"], reverse=True)
    return result


def fetch_treasury_yield_10y():
    data = http_get_json({
        "function": "TREASURY_YIELD",
        "interval": "daily",
        "maturity": "10year",
    })
    series = data.get("data")
    if not series:
        raise RuntimeError(f"米10年債利回りが取得できませんでした: {data}")
    # 新しい順で返ってくる想定。値が "." のことがあるので除外。
    values = [(row["date"], row["value"]) for row in series if row.get("value") not in (None, ".")]
    values = [(d, float(v)) for d, v in values]
    values.sort()  # 古い順に
    return values


def fetch_wti_daily():
    data = http_get_json({
        "function": "WTI",
        "interval": "daily",
    })
    series = data.get("data")
    if not series:
        raise RuntimeError(f"WTI原油が取得できませんでした: {data}")
    values = [(row["date"], row["value"]) for row in series if row.get("value") not in (None, ".")]
    values = [(d, float(v)) for d, v in values]
    values.sort()
    return values


def fetch_dxy_daily():
    """ドル指数（DXY）。Yahoo Financeの同じ非公式チャートAPIを使い回す（無料・キー不要）。"""
    bars = fetch_fx_intraday("DX-Y.NYB", "1d", "1mo")
    return [(b["t"], b["c"]) for b in bars]


def fetch_gold_daily():
    """
    金（GOLD、COMEX先物）。Alpha Vantage無料枠では取得できないため、DXYと同じ
    Yahoo Finance非公式チャートAPI（レート制限なし）を使う。シンボルは"GC=F"。
    """
    bars = fetch_fx_intraday("GC=F", "1d", "1mo")
    return [(b["t"], b["c"]) for b in bars]


def fetch_jp10y_daily():
    """
    日本10年国債利回り。財務省が公開する金利情報CSV（Shift-JIS）を直接読み込む。
    直近営業日数件分のみを含む小さなCSVで、末尾に「ダウンロードできない場合は
    ブラウザのキャッシュを削除して…」という注意書きの行が数値なしで付いてくる
    ことがあるため、数値としてパースできた行だけを採用する。
    """
    req = urllib.request.Request(MOF_JGB_CSV_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        raw = res.read()
    text = raw.decode("shift_jis", errors="replace")
    rows = list(csv.reader(io.StringIO(text)))
    if len(rows) < 3:
        raise RuntimeError("財務省国債金利CSVの形式が想定と異なります")
    header = rows[1]
    try:
        idx_10y = header.index("10年")
    except ValueError:
        raise RuntimeError("財務省国債金利CSVに「10年」列が見つかりません")
    values = []
    for row in rows[2:]:
        if len(row) <= idx_10y:
            continue
        try:
            values.append((row[0], float(row[idx_10y].strip())))
        except ValueError:
            continue
    if not values:
        raise RuntimeError("財務省国債金利CSVから10年債データを抽出できませんでした")
    return values


def fetch_one_news_feed(source, url):
    """1つのRSSフィードを取得し、[{"source","title","link","published_at_utc"}, ...]を返す。"""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as res:
        raw = res.read()
    root = ET.fromstring(raw)
    items = []
    for item in root.findall(".//item"):
        title_el = item.find("title")
        link_el = item.find("link")
        pubdate_el = item.find("pubDate")
        if title_el is None or not title_el.text or link_el is None or not link_el.text:
            continue
        published_at = None
        if pubdate_el is not None and pubdate_el.text:
            try:
                published_at = parsedate_to_datetime(pubdate_el.text)
                if published_at.tzinfo is None:
                    published_at = published_at.replace(tzinfo=timezone.utc)
            except (TypeError, ValueError):
                published_at = None
        items.append({
            "source": source,
            "title": title_el.text.strip(),
            "link": link_el.text.strip(),
            "published_at_utc": published_at.astimezone(timezone.utc).isoformat() if published_at else None,
        })
    return items


def fetch_news_headlines(limit=6):
    """
    NEWS_FEEDSのRSSフィードから最新見出しをまとめて取得する（重要度による絞り込みはしない）。
    1つが失敗しても他のフィードだけで続行し、全て失敗した場合は空リストを返す
    （本体のシグナル計算は止めない設計）。MAX_NEWS_AGE_HOURSより古い見出しは除外する。
    """
    all_items = []
    for source, url in NEWS_FEEDS:
        try:
            all_items.extend(fetch_one_news_feed(source, url))
        except Exception as e:  # noqa: BLE001
            print(f"[WARN] {source}のRSS取得に失敗しました（続行します）: {e}", file=sys.stderr)
    all_items.sort(key=lambda it: it["published_at_utc"] or "", reverse=True)
    now = datetime.now(timezone.utc)
    fresh = []
    for it in all_items:
        if not it["published_at_utc"]:
            continue
        published_at = datetime.fromisoformat(it["published_at_utc"])
        if (now - published_at).total_seconds() <= MAX_NEWS_AGE_HOURS * 3600:
            fresh.append(it)
    return fresh[:limit]


def linear_regression_channel(closes, lookback=LOOKBACK):
    """
    直近 lookback 本の終値から線形回帰チャネルを計算する。
    戻り値: dict(mid, upper, lower, sigma, position, slope)
      position = 直近終値がチャネル中心から何sigma離れているか（+が上、-が下）
      slope    = 回帰直線の傾き（1本あたりの価格変化）
    """
    series = closes[-lookback:] if len(closes) > lookback else closes[:]
    n = len(series)
    if n < 5:
        raise RuntimeError("回帰チャネル計算に必要なデータ本数が不足しています")

    xs = list(range(n))
    x_mean = sum(xs) / n
    y_mean = sum(series) / n

    num = sum((xs[i] - x_mean) * (series[i] - y_mean) for i in range(n))
    den = sum((xs[i] - x_mean) ** 2 for i in range(n))
    slope = num / den if den else 0.0
    intercept = y_mean - slope * x_mean

    fitted = [intercept + slope * x for x in xs]
    residuals = [series[i] - fitted[i] for i in range(n)]
    sigma = statistics.pstdev(residuals) if n > 1 else 0.0
    sigma = sigma if sigma > 1e-6 else 1e-6  # ゼロ割回避

    mid = fitted[-1]
    upper = mid + 2 * sigma
    lower = mid - 2 * sigma
    latest = series[-1]
    position = (latest - mid) / sigma

    return {
        "mid": mid, "upper": upper, "lower": lower, "sigma": sigma,
        "position": position, "slope": slope, "intercept": intercept, "n": n,
        "latest": latest,
    }


def momentum_direction(ch):
    """
    5分・15分・1時間足それぞれについて、「チャネル中心から何σ離れているか」(position)が
    ±EDGE_THRESHOLD(1.3σ)を超えていれば、その方向に強く偏っている(継続方向)とみなす。
    3つの時間足がこの判定で全て同じ方向になった時だけ、上位足の方向候補が確定する
    （build_signal参照）。
    """
    pos = ch["position"]
    if pos >= EDGE_THRESHOLD:
        return "UP"
    if pos <= -EDGE_THRESHOLD:
        return "DOWN"
    return "FLAT"


def detect_reversal_setup(bars, ch, direction):
    """
    directionは上位3時間足が一致した方向候補("BUY"/"SELL")。1分足がこの方向とは
    逆に振れてチャネル際(±EDGE_THRESHOLD)まで達し、そこから戻り始めていれば、
    その谷(BUYの場合)/山(SELLの場合)の価格を返す。まだ戻り始めていない・戻り幅が
    REVERT_MIN_PIPS未満・そもそもチャネル際まで達していない場合はNoneを返す。
    """
    if len(bars) < REVERT_WINDOW:
        return None
    recent = bars[-REVERT_WINDOW:]
    closes = [b["c"] for b in recent]
    latest = closes[-1]
    sigma = ch["sigma"]
    mid = ch["mid"]

    if direction == "BUY":
        trough_idx = min(range(len(closes)), key=lambda i: closes[i])
        trough = closes[trough_idx]
        if trough_idx == len(closes) - 1:
            return None  # 最新バーがまだ谷=反発が始まっていない
        trough_position = (trough - mid) / sigma
        if trough_position > -EDGE_THRESHOLD:
            return None  # チャネル下限際まで到達していない
        if (latest - trough) * 100 < REVERT_MIN_PIPS:
            return None  # 戻り幅が不十分(ノイズ)
        return trough
    else:
        peak_idx = max(range(len(closes)), key=lambda i: closes[i])
        peak = closes[peak_idx]
        if peak_idx == len(closes) - 1:
            return None
        peak_position = (peak - mid) / sigma
        if peak_position < EDGE_THRESHOLD:
            return None
        if (peak - latest) * 100 < REVERT_MIN_PIPS:
            return None
        return peak


def moving_average_trend(closes, short=10, long=30):
    """
    短期・長期の単純移動平均のクロスからトレンド方向を判定する（参考表示用）。
    差が0.05%未満なら方向感なし（FLAT）扱い。売買判定には使用しない。
    """
    if len(closes) < long:
        return "FLAT"
    short_ma = sum(closes[-short:]) / short
    long_ma = sum(closes[-long:]) / long
    if not long_ma:
        return "FLAT"
    diff_ratio = (short_ma - long_ma) / long_ma
    if diff_ratio > 0.0005:
        return "UP"
    if diff_ratio < -0.0005:
        return "DOWN"
    return "FLAT"


# ==== テクニカル指標（1時間足を基準に計算） ====
# 「AI'S MARKET READ」等と並ぶ参考情報として表示する（売買判定ロジックには使わない）。

def ema_series(values, period):
    """
    指数移動平均（EMA）の系列を返す。最初のperiod本は単純移動平均で初期化し、
    以降はEMAの標準的な漸化式で計算する。戻り値はvalues[period-1:]に対応する。
    """
    if len(values) < period:
        return []
    k = 2 / (period + 1)
    seed = sum(values[:period]) / period
    out = [seed]
    for v in values[period:]:
        out.append(v * k + out[-1] * (1 - k))
    return out


def compute_macd(closes, fast=12, slow=26, signal=9):
    """
    MACD(12,26,9)。短期・長期EMAの差（MACD線）と、その9期間EMA（シグナル線）を比較し、
    ゴールデンクロス/デッドクロスが直近で起きたかどうかも返す。
    """
    if len(closes) < slow + signal:
        return None
    ema_fast = ema_series(closes, fast)
    ema_slow = ema_series(closes, slow)
    ema_fast_aligned = ema_fast[slow - fast:]
    macd_line = [f - s for f, s in zip(ema_fast_aligned, ema_slow)]
    signal_line = ema_series(macd_line, signal)
    if len(signal_line) < 2:
        return None
    macd_aligned = macd_line[signal - 1:]

    macd_now, macd_prev = macd_aligned[-1], macd_aligned[-2]
    signal_now, signal_prev = signal_line[-1], signal_line[-2]
    histogram = macd_now - signal_now

    if macd_prev <= signal_prev and macd_now > signal_now:
        cross = "GOLDEN_CROSS"
    elif macd_prev >= signal_prev and macd_now < signal_now:
        cross = "DEAD_CROSS"
    else:
        cross = None

    state = "BULLISH" if macd_now > signal_now else ("BEARISH" if macd_now < signal_now else "NEUTRAL")

    return {
        "macd": round(macd_now, 4),
        "signal": round(signal_now, 4),
        "histogram": round(histogram, 4),
        "state": state,
        "cross": cross,
    }


def compute_rsi(closes, period=14):
    """RSI（Wilderの平滑化方式）。70以上でOVERBOUGHT、30以下でOVERSOLD。"""
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        change = closes[i] - closes[i - 1]
        gains.append(max(change, 0.0))
        losses.append(max(-change, 0.0))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        rsi = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

    state = "OVERBOUGHT" if rsi >= 70 else ("OVERSOLD" if rsi <= 30 else "NEUTRAL")
    return {"value": round(rsi, 1), "state": state}


def compute_moving_averages(closes):
    """MA5/25/75/200と、価格を含めた並び順から「パーフェクトオーダー」を判定する。"""
    periods = [5, 25, 75, 200]
    if len(closes) < max(periods):
        return None
    mas = {p: sum(closes[-p:]) / p for p in periods}
    price = closes[-1]

    order = [price, mas[5], mas[25], mas[75], mas[200]]
    if all(order[i] > order[i + 1] for i in range(len(order) - 1)):
        perfect_order = "BULLISH"
    elif all(order[i] < order[i + 1] for i in range(len(order) - 1)):
        perfect_order = "BEARISH"
    else:
        perfect_order = None

    return {
        "ma5": round(mas[5], 3),
        "ma25": round(mas[25], 3),
        "ma75": round(mas[75], 3),
        "ma200": round(mas[200], 3),
        "price": round(price, 3),
        "perfect_order": perfect_order,
    }


def compute_bollinger(closes, period=20, num_std=2):
    """ボリンジャーバンド（20期間・±2σ）。現在値がバンドのどこにあるかも返す。"""
    if len(closes) < period:
        return None
    window = closes[-period:]
    mid = sum(window) / period
    variance = sum((c - mid) ** 2 for c in window) / period
    std = variance ** 0.5
    upper = mid + num_std * std
    lower = mid - num_std * std
    price = closes[-1]
    state = "UPPER_TOUCH" if price >= upper else ("LOWER_TOUCH" if price <= lower else "INSIDE")
    return {
        "mid": round(mid, 3), "upper": round(upper, 3), "lower": round(lower, 3),
        "price": round(price, 3), "state": state,
    }


def compute_support_resistance(bars, lookback=50):
    """直近lookback本の高値・安値から、単純なサポート/レジスタンスを算出する。"""
    recent = bars[-lookback:] if len(bars) > lookback else bars
    if not recent:
        return None
    resistance = max(b["h"] for b in recent)
    support = min(b["l"] for b in recent)
    return {"resistance": round(resistance, 3), "support": round(support, 3)}


def trend_direction(values, days=5):
    """直近days件の値から単純な向き（up/down/flat）を判定する。"""
    if len(values) < 2:
        return "flat"
    recent = [v for _, v in values[-days:]]
    if len(recent) < 2:
        return "flat"
    change = recent[-1] - recent[0]
    span = max(abs(v) for v in recent) or 1.0
    if abs(change) / span < 0.01:
        return "flat"
    return "up" if change > 0 else "down"


TREND_JA = {"up": "上昇", "down": "低下", "flat": "横ばい"}


MOMENTUM_LABEL_JA = {"UP": "上方向", "DOWN": "下方向", "FLAT": "中央"}


def build_confidence_breakdown(bias, candidate, timeframes, confidence):
    """
    「信頼度が何%で、星いくつか」だけでは根拠が見えないため、5分・15分・1時間足
    それぞれの方向(momentum_direction)と、確信度の計算根拠を短い文章にして返す。
    ユーザー向けに「なぜその数字か」を可視化する目的の、表示専用の補助データ。
    """
    tf_line = " / ".join(f"{tf['label']}:{MOMENTUM_LABEL_JA[tf['momentum']]}" for tf in timeframes)
    if bias in ("SELL", "BUY"):
        align_note = tf_line + " → 3時間足すべて一致、1分足の反発シグナルも確認済み"
        calc_note = f"基本50% + 3時間足一致30% + チャネル際からの乖離度ボーナス = {confidence}%（上限95%）"
    elif candidate is not None:
        align_note = tf_line + " → 3時間足は一致していますが、1分足の反発シグナルはまだ点灯していません"
        calc_note = "3時間足の方向一致のみでは確信度は上がらず、1分足の反発確認まで基本値50%のままです。"
    else:
        align_note = tf_line + " → 3時間足の方向が一致していません"
        calc_note = "3時間足の方向が揃っていないため、基本値50%のままです。"
    return {"timeframes_note": align_note, "calc_note": calc_note}


def build_market_context(bias, candidate, latest_price, day_change_pct, us10y_trend, wti_trend):
    """
    「直近の指標・報道まとめ」欄用の文章を、その時点の実データから自動生成する。
    固定文ではなく、価格・トレンドという生きた数値を毎回埋め込むため、
    時間が経っても内容が古びない（＝手動更新が要らない）設計にしている。

    bias: 最終的なシグナル("SELL"/"BUY"/"WAIT")
    candidate: 5分・15分・1時間足の方向一致だけで見た候補方向(一致していなければNone)。
      biasがWAITでもcandidateがある場合、「上位足は方向一致しているが1分足の
      反発シグナルがまだ点灯していない」ことを示せるため、単なるWAITより
      具体的な状況説明ができる。
    """
    change_txt = f"{day_change_pct:+.2f}%"
    y = TREND_JA.get(us10y_trend, "横ばい")
    w = TREND_JA.get(wti_trend, "横ばい")

    if bias == "SELL":
        stance = "5分・15分・1時間足が揃って上値の重さを示す中、1分足が短期的な戻りから反落したタイミング"
        outlook = "目先は上値の重い展開が想定され、高値を追わず戻りを待つスタンスが機能しやすい局面。"
    elif bias == "BUY":
        stance = "5分・15分・1時間足が揃って下値の堅さを示す中、1分足が短期的な押し目から反発したタイミング"
        outlook = "目先は下値の堅い展開が想定され、押し目を焦らず拾うスタンスが機能しやすい局面。"
    elif candidate == "SELL":
        stance = "5分・15分・1時間足は戻り売り方向で揃っているが、1分足の反落シグナルはまだ点灯していない"
        outlook = "上位足の方向感は出ているため、1分足が戻り高値から反落するタイミングを待ちたい局面。"
    elif candidate == "BUY":
        stance = "5分・15分・1時間足は押し目買い方向で揃っているが、1分足の反発シグナルはまだ点灯していない"
        outlook = "上位足の方向感は出ているため、1分足が押し目安値から反発するタイミングを待ちたい局面。"
    else:
        stance = "5分・15分・1時間足の方向が揃っておらず、方向感に乏しいレンジ地合い"
        outlook = "明確な方向一致が出るまでは、無理に取りにいかず様子見が無難な局面。"

    return (
        f"USD/JPYは現在{latest_price:.2f}円付近で推移（直近1時間比{change_txt}）。{stance}。"
        f"米10年債利回りは{y}基調、WTI原油は{w}基調で推移している。{outlook}"
        "※このまとめは実データから自動生成された定型解説です。個別の経済指標発表や"
        "ニュース速報の内容までは反映していません。"
    )


def load_previous_signal(out_path):
    """前回書き出したsignal.jsonを読む（無ければNone）。"""
    try:
        with open(out_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def load_daily_analysis(base_dir):
    """
    daily_analysis.json（リポジトリ直下、signal.jsonと同じ階層）を読み込む。
    このファイルはCIが自動生成するものではなく、Claude Codeとの会話の中で
    人が都度書いて保存する「今日の詳しい分析」用の小さなファイル。
    存在しない/壊れている場合はNoneを返し、signal.json側では
    "daily_analysis" キー自体を省略する（詳細ページ側でフォールバック表示）。
    """
    path = os.path.join(base_dir, "daily_analysis.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def load_trade_log(base_dir):
    """
    trade_log.json（リポジトリ直下、signal.jsonと同じ階層）を読み込む。
    過去のシグナル履歴（勝率・pips検証用）を蓄積するファイルで、signal.jsonとは
    別ファイルにして肥大化を防いでいる。存在しない/壊れている場合は空の履歴から始める。
    """
    path = os.path.join(base_dir, "trade_log.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data.get("trades"), list):
            raise ValueError("trade_log.jsonの形式が不正です")
        return data
    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError, AttributeError):
        return {"trades": []}


def pips_for(bias, entry, price):
    """USD/JPYの1pips=0.01円として、bias方向での損益pipsを返す（正=利益、負=損失）。"""
    diff = (entry - price) if bias == "SELL" else (price - entry)
    return round(diff * 100, 1)


def update_trade_log(trade_log, bias, priority_trade, latest_price, confidence, now_iso):
    """
    ①オープン中の取引があれば、現在値がTP/SLに到達していないか確認して決着させる。
    ②オープン中の取引が無く、今回の判定がSELL/BUYであれば、新規にオープンとして記録する。
    戻り値は (trade_log, newly_opened)。newly_openedは②で実際に新規オープンした
    場合だけTrueになり、メール通知（send_signal_email）を送るかどうかの判定に使う。
    """
    trades = trade_log.get("trades", [])
    open_trade = trades[-1] if trades and trades[-1].get("status") == "OPEN" else None

    if open_trade is not None:
        ob = open_trade["bias"]
        tp = open_trade["take_profit"]
        sl = open_trade["stop_loss"]
        hit_tp = (latest_price <= tp) if ob == "SELL" else (latest_price >= tp)
        hit_sl = (latest_price >= sl) if ob == "SELL" else (latest_price <= sl)
        if hit_tp or hit_sl:
            open_trade["status"] = "WIN" if hit_tp else "LOSS"
            open_trade["closed_at_utc"] = now_iso
            open_trade["closed_price"] = round(latest_price, 3)
            open_trade["pips"] = pips_for(ob, open_trade["entry"], latest_price)
            open_trade = None  # 決着したので、この後の新規オープン判定に進める

    newly_opened = False
    if open_trade is None and bias in ("SELL", "BUY"):
        entry = priority_trade.get("entry")
        tp = priority_trade.get("take_profit")
        sl = priority_trade.get("stop_loss")
        if entry is not None and tp is not None and sl is not None:
            trades.append({
                "id": now_iso,
                "opened_at_utc": now_iso,
                "bias": bias,
                "entry": entry,
                "take_profit": tp,
                "stop_loss": sl,
                "confidence": confidence,
                "status": "OPEN",
                "closed_at_utc": None,
                "closed_price": None,
                "pips": None,
            })
            newly_opened = True

    trade_log["trades"] = trades
    return trade_log, newly_opened


def compute_trade_stats(trades):
    """勝率・平均pips・プロフィットファクターを、決着済み（WIN/LOSS）の取引から算出する。"""
    closed = [t for t in trades if t.get("status") in ("WIN", "LOSS")]
    wins = [t for t in closed if t["status"] == "WIN"]
    losses = [t for t in closed if t["status"] == "LOSS"]
    total_closed = len(closed)

    gross_win = sum(t["pips"] for t in wins)
    gross_loss = abs(sum(t["pips"] for t in losses))

    return {
        "total_closed": total_closed,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate_pct": round(len(wins) / total_closed * 100, 1) if total_closed else None,
        "avg_win_pips": round(gross_win / len(wins), 1) if wins else None,
        "avg_loss_pips": round(-gross_loss / len(losses), 1) if losses else None,
        # 損失がまだ無い（＝分母ゼロ）場合はPF計算不能として扱い、無限大等の非JSON値を出さない。
        "profit_factor": round(gross_win / gross_loss, 2) if gross_loss > 0 else None,
        "total_pips": round(sum(t["pips"] for t in closed), 1) if closed else 0.0,
    }


def send_signal_email(bias, priority_trade, confidence, latest_price):
    """
    新規シグナル(SELL/BUY)が発動した瞬間（update_trade_logがnewly_opened=Trueを
    返した時）だけメール通知する。GMAIL_SENDER・GMAIL_APP_PASSWORD・NOTIFY_EMAIL_TOの
    いずれかが未設定なら何もしない（この機能を使わない運用でも既存の動作に影響を
    与えないようにするため）。送信に失敗してもシグナル計算本体には影響させない。
    """
    if not (GMAIL_SENDER and GMAIL_APP_PASSWORD and NOTIFY_EMAIL_TO):
        return
    label = "戻り売り" if bias == "SELL" else "押し目買い"
    subject = f"[AI FX研究所] {label}シグナル発生 - USD/JPY"
    body = (
        f"USD/JPYで{label}シグナルが発生しました。\n\n"
        f"現在値: {latest_price}円\n"
        f"ENTRY: {priority_trade.get('entry')}円\n"
        f"TAKE PROFIT: {priority_trade.get('take_profit')}円\n"
        f"STOP LOSS: {priority_trade.get('stop_loss')}円\n"
        f"信頼度: {confidence}%\n\n"
        "詳細: https://aifxlabo.com/\n\n"
        "本メールはルールベースの自動計算による参考情報であり、投資成果を保証するものではありません。"
    )
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = GMAIL_SENDER
    msg["To"] = NOTIFY_EMAIL_TO
    msg.set_content(body)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
            server.starttls()
            server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
    except Exception as e:  # noqa: BLE001
        print(f"[WARN] メール通知の送信に失敗しました（シグナル本体は継続します）: {e}", file=sys.stderr)


def is_same_utc_date(iso_ts, now):
    """iso_ts（ISO形式の日時文字列）がnowと同じUTC日付かどうか。"""
    if not iso_ts:
        return False
    try:
        dt = datetime.fromisoformat(iso_ts)
    except ValueError:
        return False
    return dt.date() == now.date()


# --- ニュース影響分析（market_events.json） ---
# ニュース見出し検出時点の相場スナップショット(price/DXY/USD強弱スコア)を基準(baseline)として
# 記録し、30分/1時間/2時間/4時間経過ごとに現在値と比較する。「因果関係の証明」ではなく、
# あくまで数値の変化を機械的に並べて見せるだけの設計（要約文は実測値をf-stringに埋め込むだけの
# テンプレート生成にし、AIに文章を書かせない＝ハルシネーションが原理的に発生しない構成）。
# AI BTC研究所（bit.aifxlabo.com）に先行導入した同名機能をFX向けに移植したもの。
# BTC版はFunding Rate・Fear & Greedを使ったが、FXにはそれらの概念が無いため、
# 代わりに「毎回取得できる」DXY（ドル指数）とUSD強弱スコア（-100〜+100固定スケール）を使う。
# 米10年債・WTIは1日1回しか取得しない（Alpha Vantage無料枠の制約）ため、数時間単位の
# before/after比較には使えず、対象から外している。
MARKET_EVENT_CHECKPOINTS = [("30m", 30 * 60), ("1h", 60 * 60), ("2h", 2 * 60 * 60), ("4h", 4 * 60 * 60)]
MARKET_EVENT_CHECKPOINT_LABEL_JA = {"30m": "30分", "1h": "1時間", "2h": "2時間", "4h": "4時間"}
MARKET_EVENTS_MAX_KEEP = 60  # 保持する最大イベント数（4時間分の決着を待つ間は必ず残し、それ以外は新しい順に間引く）

PRICE_SWING_PCT_FX = 0.3      # USD/JPYがbaselineからこれ以上動いたら「価格急変」とみなす（%）
DXY_SWING_PCT = 0.3           # DXYがbaselineからこれ以上動いたら「ドル全面高/安」とみなす（%）
USD_STRENGTH_SWING = 15.0     # USD強弱スコア(-100〜+100)がbaselineからこれ以上動いたら「転換」とみなす（ポイント）


def load_market_events(base_dir):
    """
    market_events.json（リポジトリ直下、signal.jsonと同じ階層）を読み込む。
    trade_log.jsonと同様、signal.jsonとは別ファイルにして肥大化を防いでいる。
    """
    path = os.path.join(base_dir, "market_events.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data.get("events"), list):
            raise ValueError("market_events.jsonの形式が不正です")
        return data
    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError, AttributeError):
        return {"events": []}


def classify_price_flag_fx(before, after):
    if not before or after is None:
        return None
    pct = (after - before) / before * 100
    if abs(pct) >= PRICE_SWING_PCT_FX:
        return f"価格急変（{pct:+.2f}%）"
    return None


def classify_dxy_flag(before, after):
    if not before or after is None:
        return None
    pct = (after - before) / before * 100
    if pct >= DXY_SWING_PCT:
        return "ドル全面高（DXY急伸）"
    if pct <= -DXY_SWING_PCT:
        return "ドル全面安（DXY急落）"
    return None


def classify_usd_strength_flag(before, after):
    if before is None or after is None:
        return None
    delta = after - before
    if delta >= USD_STRENGTH_SWING:
        return "USD買い優勢への転換（強弱スコア急上昇）"
    if delta <= -USD_STRENGTH_SWING:
        return "USD売り優勢への転換（強弱スコア急低下）"
    return None


def build_event_summary(event, label, checkpoint):
    """
    実測値だけをf-stringに埋め込んだ定型文を生成する（LLMを使わないため、数値の
    捏造や過度な断定が原理的に起こらない）。
    「(見出し)後、USD/JPYは(経過時間)で(価格変化)%。DXYは(前)から(後)へ(方向)、
      USD強弱スコアも(前)から(後)へ(方向)。(所見)。ただし因果関係は確定できません。」
    """
    baseline = event["baseline"]
    elapsed_ja = MARKET_EVENT_CHECKPOINT_LABEL_JA[label]
    parts = [f"「{event['title']}」の報道後、USD/JPYは{elapsed_ja}で{checkpoint['delta_price_pct']:+.2f}%。"]

    bd, ad = baseline.get("dxy"), checkpoint.get("dxy")
    if bd is not None and ad is not None:
        trend = "上昇" if ad > bd else ("低下" if ad < bd else "横ばい")
        parts.append(f"DXYは{bd:.2f}から{ad:.2f}へ{trend}、")

    bs, as_ = baseline.get("usd_strength_score"), checkpoint.get("usd_strength_score")
    if bs is not None and as_ is not None:
        trend2 = "上昇" if as_ > bs else ("低下" if as_ < bs else "横ばい")
        parts.append(f"USD強弱スコアも{bs:+.0f}から{as_:+.0f}へ{trend2}。")

    if event.get("flags"):
        parts.append("、".join(event["flags"]) + "の兆候が見られます。")

    parts.append("ただし相関の一致であり、因果関係は確定できません。")
    return "".join(parts)


def update_market_events(events_data, now, snapshot, news_headlines):
    """
    ①未追跡のニュース見出しを新規イベントとして登録（検出時点のsnapshotをbaselineに）。
    ②追跡中の各イベントについて、経過時間がチェックポイント(30分/1時間/2時間/4時間)を
      超えていれば、現在のsnapshotとbaselineを比較してdelta・フラグ・要約文を更新する。
    ③4時間チェックポイントまで埋まったイベントはfinalizedとし、保持件数の上限を超えた分は
      古いfinalized済みイベントから間引く（未決着のイベントは常に残す）。
    """
    events = events_data.get("events", [])
    known_links = {e["link"] for e in events}
    for item in news_headlines:
        if item["link"] in known_links:
            continue
        events.append({
            "title": item["title"],
            "link": item["link"],
            "source": item["source"],
            "published_at_utc": item["published_at_utc"],
            "detected_at_utc": now.isoformat(),
            "baseline": snapshot,
            "checkpoints": {},
            "flags": [],
            "relevance": "unknown",
            "summary": None,
            "finalized": False,
        })

    for event in events:
        if event.get("finalized"):
            continue
        detected_at = datetime.fromisoformat(event["detected_at_utc"])
        elapsed_sec = (now - detected_at).total_seconds()
        baseline = event["baseline"]

        for label, threshold_sec in MARKET_EVENT_CHECKPOINTS:
            if label in event["checkpoints"] or elapsed_sec < threshold_sec:
                continue
            checkpoint = dict(snapshot)
            if baseline.get("price") and snapshot.get("price") is not None:
                checkpoint["delta_price_pct"] = round((snapshot["price"] - baseline["price"]) / baseline["price"] * 100, 3)
            else:
                checkpoint["delta_price_pct"] = None
            event["checkpoints"][label] = checkpoint

            flags = []
            for flag in (
                classify_price_flag_fx(baseline.get("price"), snapshot.get("price")),
                classify_dxy_flag(baseline.get("dxy"), snapshot.get("dxy")),
                classify_usd_strength_flag(baseline.get("usd_strength_score"), snapshot.get("usd_strength_score")),
            ):
                if flag:
                    flags.append(flag)
            if flags:
                event["flags"] = list(dict.fromkeys(event.get("flags", []) + flags))

            if len(event["flags"]) >= 2:
                event["relevance"] = "high"
            elif len(event["flags"]) == 1:
                event["relevance"] = "medium"
            else:
                event["relevance"] = event.get("relevance") if event.get("relevance") != "unknown" else "low"

            if checkpoint["delta_price_pct"] is not None:
                event["summary"] = build_event_summary(event, label, checkpoint)

        if "4h" in event["checkpoints"]:
            event["finalized"] = True

    pending = [e for e in events if not e.get("finalized")]
    finalized = sorted(
        (e for e in events if e.get("finalized")),
        key=lambda e: e["detected_at_utc"], reverse=True,
    )
    keep_finalized = finalized[: max(0, MARKET_EVENTS_MAX_KEEP - len(pending))]
    events = pending + keep_finalized
    events.sort(key=lambda e: e["detected_at_utc"], reverse=True)

    events_data["events"] = events
    return events_data


def build_signal(out_path=None):
    if not ALPHA_VANTAGE_KEY:
        raise RuntimeError("環境変数 ALPHA_VANTAGE_KEY が設定されていません")

    now = datetime.now(timezone.utc)

    # --- 為替データ: Yahoo Finance（無料・キー不要・毎回取得） ---
    m1 = fetch_fx_intraday("JPY=X", "1m", "5d")
    m5 = fetch_fx_intraday("JPY=X", "5m", "5d")
    m15 = fetch_fx_intraday("JPY=X", "15m", "5d")
    h1 = fetch_fx_intraday("JPY=X", "60m", "60d")

    # --- 通貨強弱（簡易版）: 主要6ペアを追加取得。失敗しても本体の計算は止めない ---
    try:
        currency_strength = compute_currency_strength(h1)
    except Exception:  # noqa: BLE001
        currency_strength = []

    # --- 米10年債・WTI: Alpha Vantage（無料枠 25回/日のため、1日1回だけ取得して使い回す） ---
    prev = load_previous_signal(out_path) if out_path else None
    prev_macro = (prev or {}).get("macro", {})
    reuse_macro = (
        prev
        and is_same_utc_date(prev.get("generated_at_utc"), now)
        and prev_macro.get("us10y_latest") is not None
        and prev_macro.get("jp10y_latest") is not None
    )

    if reuse_macro:
        yield_trend = prev_macro.get("us10y_trend", "flat")
        us10y_latest = prev_macro.get("us10y_latest")
        wti_trend = prev_macro.get("wti_trend", "flat")
        jp10y_trend = prev_macro.get("jp10y_trend", "flat")
        jp10y_latest = prev_macro.get("jp10y_latest")
    else:
        us10y = fetch_treasury_yield_10y()
        time.sleep(13)
        wti = fetch_wti_daily()
        yield_trend = trend_direction(us10y)
        us10y_latest = us10y[-1][1] if us10y else None
        wti_trend = trend_direction(wti)
        try:
            jp10y = fetch_jp10y_daily()
            jp10y_trend = trend_direction(jp10y)
            jp10y_latest = jp10y[-1][1] if jp10y else None
        except Exception:  # noqa: BLE001
            # 財務省サイト側の一時的な不調でも、シグナル計算全体は止めない。
            jp10y_trend = prev_macro.get("jp10y_trend", "flat")
            jp10y_latest = prev_macro.get("jp10y_latest")

    # DXY（ドル指数）・GOLDはYahoo Finance側にレート制限が無いため、他のFXペアと同様に毎回取得する。
    try:
        dxy = fetch_dxy_daily()
        dxy_trend = trend_direction(dxy)
        dxy_latest = dxy[-1][1] if dxy else None
    except Exception:  # noqa: BLE001
        dxy_trend = prev_macro.get("dxy_trend", "flat")
        dxy_latest = prev_macro.get("dxy_latest")

    try:
        gold = fetch_gold_daily()
        gold_trend = trend_direction(gold)
        gold_latest = gold[-1][1] if gold else None
    except Exception:  # noqa: BLE001
        gold_trend = prev_macro.get("gold_trend", "flat")
        gold_latest = prev_macro.get("gold_latest")

    try:
        news_headlines = fetch_news_headlines()
    except Exception as e:  # noqa: BLE001
        print(f"[WARN] ニュース見出しの取得に失敗しました（続行します）: {e}", file=sys.stderr)
        news_headlines = []

    # --- テクニカル指標（1時間足基準・参考情報として表示するのみ、売買判定には使わない） ---
    h1_closes = [b["c"] for b in h1]
    technical = {
        "macd": compute_macd(h1_closes),
        "rsi": compute_rsi(h1_closes),
        "moving_averages": compute_moving_averages(h1_closes),
        "bollinger": compute_bollinger(h1_closes),
        "support_resistance": compute_support_resistance(h1),
    }

    # --- 回帰チャネル: 5分・15分・1時間足で方向一致を判定、1分足で反発を検出 ---
    ch_1m = linear_regression_channel([b["c"] for b in m1])
    ch_5m = linear_regression_channel([b["c"] for b in m5])
    ch_15m = linear_regression_channel([b["c"] for b in m15])
    ch_1h = linear_regression_channel([b["c"] for b in h1])

    timeframes = [
        {"label": "5分足", "key": "m5", "channel": ch_5m, "bars": m5},
        {"label": "15分足", "key": "m15", "channel": ch_15m, "bars": m15},
        {"label": "1時間足", "key": "h1", "channel": ch_1h, "bars": h1},
    ]
    for tf in timeframes:
        tf["trend"] = moving_average_trend([b["c"] for b in tf["bars"]])
        tf["momentum"] = momentum_direction(tf["channel"])

    dirs = [tf["momentum"] for tf in timeframes]
    if dirs[0] == "UP" and dirs[1] == "UP" and dirs[2] == "UP":
        candidate = "BUY"
    elif dirs[0] == "DOWN" and dirs[1] == "DOWN" and dirs[2] == "DOWN":
        candidate = "SELL"
    else:
        candidate = None

    # 上位3時間足の方向が一致している時だけ、1分足の逆行からの戻りを調べる。
    extreme = detect_reversal_setup(m1, ch_1m, candidate) if candidate else None
    bias = candidate if (candidate and extreme is not None) else "WAIT"

    if bias in ("SELL", "BUY"):
        # 5分・15分・1時間足が全て一致している時しかbiasは確定しないため、
        # 一致度合いは常に3/3固定。代わりに、3時間足のチャネル際からの
        # 平均乖離度(avg_abs_pos)が大きいほど「強い一致」とみなして加点する。
        avg_abs_pos = sum(abs(tf["channel"]["position"]) for tf in timeframes) / len(timeframes)
        confidence = 50 + 30 + min(avg_abs_pos, 3.0) * 5
        confidence = max(50, min(95, round(confidence)))
        stars = max(1, min(5, round(confidence / 20)))
    else:
        confidence = 50
        stars = 2

    if candidate is not None:
        market_mode = "TREND"
        market_mode_note = "5分・15分・1時間足の方向が揃っており、方向感のある地合い。"
    else:
        market_mode = "RANGE"
        market_mode_note = "時間足ごとに方向が割れており、方向感に乏しいレンジ地合い。"

    latest_price = m1[-1]["c"] if m1 else ch_1h["latest"]
    day_change_pct = 0.0
    if len(h1) >= 24:
        base = h1[-24]["c"]
        if base:
            day_change_pct = (latest_price - base) / base * 100

    intervention_risk = "HIGH" if (latest_price >= 158.5 and day_change_pct >= 0.7) else (
        "MID" if latest_price >= 155.0 else "LOW"
    )

    # Entry/TP/SLは、1分足の逆行の谷/山(extreme)を基準にした「測定値幅」で算出する。
    # SLはextremeの少し外側（このセットアップの前提が崩れる水準）、
    # TPはentryからextremeまでの距離を反対方向に伸ばした幅。
    if bias == "SELL":
        entry = latest_price
        move = abs(entry - extreme)
        sl = extreme + SL_BUFFER_PIPS / 100
        tp = entry - move
        trade_lead = "戻り売り ― 上位足の下降方向一致＋1分足の戻りからの反落"
    elif bias == "BUY":
        entry = latest_price
        move = abs(entry - extreme)
        sl = extreme - SL_BUFFER_PIPS / 100
        tp = entry + move
        trade_lead = "押し目買い ― 上位足の上昇方向一致＋1分足の押し目からの反発"
    else:
        entry = tp = sl = None
        if candidate == "SELL":
            trade_lead = "様子見 ― 上位足は戻り売り方向で一致、1分足の反落シグナル待ち"
        elif candidate == "BUY":
            trade_lead = "様子見 ― 上位足は押し目買い方向で一致、1分足の反発シグナル待ち"
        else:
            trade_lead = "様子見 ― 5分・15分・1時間足の方向が一致していない"

    reversal_setup = None
    if bias in ("SELL", "BUY"):
        reverted_pips = round((entry - extreme) * 100, 1) if bias == "BUY" else round((extreme - entry) * 100, 1)
        reversal_setup = {"extreme": round(extreme, 3), "reverted_pips": reverted_pips}

    comments = {
        "SELL": [
            "強い相場ほど、飛び乗らない。戻りを丁寧に売る一日に。",
            "上値は重い。高値づかみを避け、戻り待ちに徹する。",
        ],
        "BUY": [
            "押し目は焦らず拾う。飛び乗りより、待つ勇気を。",
            "下値は堅い。押し目待ちで、無理な高値追いはしない。",
        ],
        "WAIT": [
            "方向感のない日は、休むも相場。無理に取りにいかない。",
            "1分足のタイミングを待つのが賢明。",
        ],
    }
    if bias in ("SELL", "BUY"):
        commentary = comments[bias][0]
    elif candidate == "BUY":
        commentary = "上位足は上向き。焦らず、1分足の押し目からの反発を待つ。"
    elif candidate == "SELL":
        commentary = "上位足は下向き。焦らず、1分足の戻りからの反落を待つ。"
    else:
        commentary = comments["WAIT"][0]
    market_context = build_market_context(
        bias, candidate, latest_price, day_change_pct, yield_trend, wti_trend,
    )

    daily_analysis = None
    if out_path:
        daily_analysis = load_daily_analysis(os.path.dirname(out_path))

    result = {
        "generated_at_utc": now.isoformat(),
        "pair": "USD/JPY",
        "latest_price": round(latest_price, 3),
        "day_change_pct": round(day_change_pct, 2),
        "signal": {
            "bias": bias,
            "bias_label": {"SELL": "戻り売り優勢", "BUY": "押し目買い優勢", "WAIT": "方向感なし"}[bias],
            "stars": stars,
            "confidence": confidence,
            "confidence_breakdown": build_confidence_breakdown(bias, candidate, timeframes, confidence),
        },
        "intervention_risk": intervention_risk,
        "market_mode": market_mode,
        "market_mode_note": market_mode_note,
        "priority_trade": {
            "lead": trade_lead,
            "entry": round(entry, 3) if entry is not None else None,
            "take_profit": round(tp, 3) if tp is not None else None,
            "stop_loss": round(sl, 3) if sl is not None else None,
        },
        "reversal_setup": reversal_setup,
        "regression_channels": [
            {
                "key": tf["key"],
                "label": tf["label"],
                "position_sigma": round(tf["channel"]["position"], 2),
                "trend": tf["trend"],
                "momentum": tf["momentum"],
                "mid": round(tf["channel"]["mid"], 3),
                "upper": round(tf["channel"]["upper"], 3),
                "lower": round(tf["channel"]["lower"], 3),
            }
            for tf in timeframes
        ],
        "technical": technical,
        "macro": {
            "us10y_trend": yield_trend,
            "us10y_latest": round(us10y_latest, 2) if us10y_latest is not None else None,
            "wti_trend": wti_trend,
            "jp10y_trend": jp10y_trend,
            "jp10y_latest": round(jp10y_latest, 3) if jp10y_latest is not None else None,
            "dxy_trend": dxy_trend,
            "dxy_latest": round(dxy_latest, 2) if dxy_latest is not None else None,
            "gold_trend": gold_trend,
            "gold_latest": round(gold_latest, 2) if gold_latest is not None else None,
        },
        "commentary": commentary,
        "market_context": market_context,
        "news": news_headlines,
        "disclaimer": "本データはルールベースの参考情報であり、投資成果を保証するものではありません。",
    }
    if daily_analysis is not None:
        result["daily_analysis"] = daily_analysis
    if currency_strength:
        result["currency_strength"] = currency_strength

    # trade_log.json（実績ページ用の履歴）はsignal.jsonとは別ファイルに直接書き出す。
    # ここで失敗しても、シグナル本体の計算・書き出しには影響させない。
    if out_path:
        base_dir = os.path.dirname(out_path)
        try:
            trade_log = load_trade_log(base_dir)
            trade_log, newly_opened = update_trade_log(
                trade_log, bias, result["priority_trade"], latest_price, confidence, now.isoformat(),
            )
            trade_log["stats"] = compute_trade_stats(trade_log["trades"])
            trade_log["updated_at_utc"] = now.isoformat()
            with open(os.path.join(base_dir, "trade_log.json"), "w", encoding="utf-8") as f:
                json.dump(trade_log, f, ensure_ascii=False, indent=2)
            if newly_opened:
                send_signal_email(bias, result["priority_trade"], confidence, latest_price)
        except Exception as e:  # noqa: BLE001
            print(f"[WARN] trade_log.jsonの更新に失敗しました（シグナル本体は継続します）: {e}", file=sys.stderr)

        # market_events.json（ニュース影響分析の履歴）も同様に、失敗してもシグナル本体には影響させない。
        try:
            usd_strength_score = None
            for c in currency_strength:
                if c.get("code") == "USD":
                    usd_strength_score = c.get("strength_score")
                    break
            snapshot = {
                "t": now.isoformat(),
                "price": round(latest_price, 3),
                "dxy": round(dxy_latest, 2) if dxy_latest is not None else None,
                "usd_strength_score": usd_strength_score,
            }
            events_data = load_market_events(base_dir)
            events_data = update_market_events(events_data, now, snapshot, news_headlines)
            events_data["updated_at_utc"] = now.isoformat()
            with open(os.path.join(base_dir, "market_events.json"), "w", encoding="utf-8") as f:
                json.dump(events_data, f, ensure_ascii=False, indent=2)
        except Exception as e:  # noqa: BLE001
            print(f"[WARN] market_events.jsonの更新に失敗しました（シグナル本体は継続します）: {e}", file=sys.stderr)

    return result


def main():
    out_path = os.path.join(os.path.dirname(__file__), "..", "signal.json")
    out_path = os.path.abspath(out_path)

    try:
        signal = build_signal(out_path=out_path)
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] シグナル計算に失敗しました: {e}", file=sys.stderr)
        sys.exit(1)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(signal, f, ensure_ascii=False, indent=2)
    print(f"書き出し完了: {out_path}")
    print(json.dumps(signal, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
