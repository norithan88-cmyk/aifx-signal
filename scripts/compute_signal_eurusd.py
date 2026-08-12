#!/usr/bin/env python3
"""
AI FX研究所 - EUR/USD 今日のAIシグナル 自動計算スクリプト

USD/JPY版（compute_signal.py）と同じ回帰チャネル・テクニカル指標ロジックを
EUR/USDに適用する。既存のUSD/JPY用スクリプトには一切手を加えず、共通の
純粋関数（データ取得・回帰チャネル計算・MACD/RSI等）だけをインポートして
再利用することで、USD/JPY側の稼働中パイプラインへの影響をゼロにしている。

USD/JPYとの主な違い:
  - 通貨ペア: EUR/USD（Yahoo Financeシンボル "EURUSD=X"）
  - 価格の丸め桁数: 3桁ではなく5桁（EUR/USDの一般的な表示精度に合わせる）。
    compute_signal.py側の移動平均・ボリンジャー・サポレジ関数は3桁固定で
    書かれているため、精度確保のためこのファイル内に5桁版を複製している
    （MACD・RSIはスケールに依存しない値のためcompute_signal.py側をそのまま再利用）。
  - 介入リスク（intervention_risk）: 日銀のドル円介入を想定した項目のため、
    EUR/USDには存在しない概念。出力に含めない。
  - 通貨強弱（currency_strength）: EUR/USD詳細ページ側では使わないため、
    このスクリプトでは計算しない。
  - 「本日の詳しい分析」は daily_analysis.json ではなく
    daily_analysis_eurusd.json を読み込む（USD/JPY版と混ざらないよう分離）。

出力先: signal_eurusd.json（signal.jsonとは別ファイル。GitHub Actionsが
USD/JPY版の直後に追加ステップとしてこのスクリプトも実行し、コミットする）。
"""

import json
import os
import sys
import time
from datetime import datetime, timezone

import compute_signal as cs

PAIR_LABEL = "EUR/USD"
SYMBOL = "EURUSD=X"
DECIMALS = 5


def compute_moving_averages_eurusd(closes):
    """compute_signal.compute_moving_averagesの5桁精度版。ロジックは同一。"""
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
        "ma5": round(mas[5], DECIMALS),
        "ma25": round(mas[25], DECIMALS),
        "ma75": round(mas[75], DECIMALS),
        "ma200": round(mas[200], DECIMALS),
        "price": round(price, DECIMALS),
        "perfect_order": perfect_order,
    }


def compute_bollinger_eurusd(closes, period=20, num_std=2):
    """compute_signal.compute_bollingerの5桁精度版。ロジックは同一。"""
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
        "mid": round(mid, DECIMALS), "upper": round(upper, DECIMALS), "lower": round(lower, DECIMALS),
        "price": round(price, DECIMALS), "state": state,
    }


def compute_support_resistance_eurusd(bars, lookback=50):
    """compute_signal.compute_support_resistanceの5桁精度版。ロジックは同一。"""
    recent = bars[-lookback:] if len(bars) > lookback else bars
    if not recent:
        return None
    resistance = max(b["h"] for b in recent)
    support = min(b["l"] for b in recent)
    return {"resistance": round(resistance, DECIMALS), "support": round(support, DECIMALS)}


def build_chart_entry_eurusd(tf):
    """compute_signal.build_chart_entryの5桁精度版。ロジックは同一。"""
    lookback = tf["lookback"]
    display_count = min(cs.DISPLAY_BARS, lookback)
    index_shift = lookback - display_count
    ch = tf["channel"]
    display_intercept = ch["intercept"] + ch["slope"] * index_shift

    return {
        "label": tf["label"],
        "state": tf["state"],
        "bars": [
            {
                "o": round(b["o"], DECIMALS), "h": round(b["h"], DECIMALS),
                "l": round(b["l"], DECIMALS), "c": round(b["c"], DECIMALS),
            }
            for b in tf["bars"][-display_count:]
        ],
        "channel": {
            "intercept": round(display_intercept, DECIMALS + 1),
            "slope": round(ch["slope"], DECIMALS + 3),
            "sigma": round(ch["sigma"], DECIMALS + 1),
        },
    }


def build_market_context_eurusd(bias, sell_count, buy_count, gate_count, latest_price,
                                 day_change_pct, us10y_trend, wti_trend):
    """compute_signal.build_market_contextのEUR/USD向け版（「円」単位を使わない等の文言違いのみ）。"""
    change_txt = f"{day_change_pct:+.2f}%"
    y = cs.TREND_JA.get(us10y_trend, "横ばい")
    w = cs.TREND_JA.get(wti_trend, "横ばい")

    if bias == "SELL":
        stance = f"{sell_count}個の時間足が上値の重さを示しており、戻り売りが優勢な地合い"
        outlook = "目先は上値の重い展開が想定され、高値を追わず戻りを待つスタンスが機能しやすい局面。"
    elif bias == "BUY":
        stance = f"{buy_count}個の時間足が下値の堅さを示しており、押し目買いが優勢な地合い"
        outlook = "目先は下値の堅い展開が想定され、押し目を焦らず拾うスタンスが機能しやすい局面。"
    else:
        stance = f"時間足ごとの判定が割れており（SELL {sell_count}／BUY {buy_count}／GATE {gate_count}）、方向感に乏しいレンジ地合い"
        outlook = "明確なブレイクが出るまでは、無理に取りにいかず様子見が無難な局面。"

    return (
        f"EUR/USDは現在{latest_price:.{DECIMALS}f}付近で推移（直近1時間比{change_txt}）。{stance}。"
        f"米10年債利回りは{y}基調、WTI原油は{w}基調で推移している。{outlook}"
        "※このまとめは実データから自動生成された定型解説です。個別の経済指標発表や"
        "ニュース速報の内容までは反映していません。"
    )


def load_daily_analysis_eurusd(base_dir):
    """daily_analysis_eurusd.json（リポジトリ直下）を読み込む。無ければNone。"""
    path = os.path.join(base_dir, "daily_analysis_eurusd.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def build_signal(out_path=None):
    if not cs.ALPHA_VANTAGE_KEY:
        raise RuntimeError("環境変数 ALPHA_VANTAGE_KEY が設定されていません")

    now = datetime.now(timezone.utc)

    # --- 為替データ: Yahoo Finance（無料・キー不要・毎回取得） ---
    m5 = cs.fetch_fx_intraday(SYMBOL, "5m", "5d")
    m15 = cs.fetch_fx_intraday(SYMBOL, "15m", "5d")
    h1 = cs.fetch_fx_intraday(SYMBOL, "60m", "60d")

    # --- 米10年債・WTI: USD/JPY版と同じ「1日1回だけ実際に取得」ロジックを流用 ---
    prev = cs.load_previous_signal(out_path) if out_path else None
    prev_macro = (prev or {}).get("macro", {})
    reuse_macro = prev and cs.is_same_utc_date(prev.get("generated_at_utc"), now) and prev_macro.get("us10y_latest") is not None

    if reuse_macro:
        yield_trend = prev_macro.get("us10y_trend", "flat")
        us10y_latest = prev_macro.get("us10y_latest")
        wti_trend = prev_macro.get("wti_trend", "flat")
    else:
        us10y = cs.fetch_treasury_yield_10y()
        time.sleep(13)
        wti = cs.fetch_wti_daily()
        yield_trend = cs.trend_direction(us10y)
        us10y_latest = us10y[-1][1] if us10y else None
        wti_trend = cs.trend_direction(wti)

    bars_4h = cs.aggregate_to_4h(h1)

    # --- テクニカル指標（1時間足基準・参考情報として表示するのみ） ---
    h1_closes = [b["c"] for b in h1]
    technical = {
        "macd": cs.compute_macd(h1_closes),
        "rsi": cs.compute_rsi(h1_closes),
        "moving_averages": compute_moving_averages_eurusd(h1_closes),
        "bollinger": compute_bollinger_eurusd(h1_closes),
        "support_resistance": compute_support_resistance_eurusd(h1),
    }

    ch_5m = cs.linear_regression_channel([b["c"] for b in m5])
    ch_15m = cs.linear_regression_channel([b["c"] for b in m15])
    ch_1h = cs.linear_regression_channel([b["c"] for b in h1])
    ch_4h = cs.linear_regression_channel([b["c"] for b in bars_4h], lookback=30)

    timeframes = [
        {"label": "5分足", "key": "m5", "channel": ch_5m, "bars": m5, "lookback": cs.LOOKBACK},
        {"label": "15分足", "key": "m15", "channel": ch_15m, "bars": m15, "lookback": cs.LOOKBACK},
        {"label": "1時間足", "key": "h1", "channel": ch_1h, "bars": h1, "lookback": cs.LOOKBACK},
        {"label": "4時間足", "key": "h4", "channel": ch_4h, "bars": bars_4h, "lookback": 30},
    ]
    for tf in timeframes:
        tf["trend"] = cs.moving_average_trend([b["c"] for b in tf["bars"]])
        tf["state"] = cs.classify_state(tf["channel"]["position"], trend=tf["trend"])

    sell_count = sum(1 for tf in timeframes if tf["state"] == "SELL")
    buy_count = sum(1 for tf in timeframes if tf["state"] == "BUY")
    gate_count = sum(1 for tf in timeframes if tf["state"] == "GATE")

    # USD/JPY版と同じ修正: Entry/TP/SLは常に1時間足チャネル基準で計算するため、
    # bias自体も「1時間足自身が同じ方向であること」を必須条件にする
    # (時間足またぎでTPがエントリーの反対側に来る矛盾を防ぐ)。
    h1_state = timeframes[2]["state"]  # {m5, m15, h1, h4}の順で並んでいる
    if sell_count >= 2 and sell_count >= buy_count and h1_state == "SELL":
        bias = "SELL"
    elif buy_count >= 2 and buy_count > sell_count and h1_state == "BUY":
        bias = "BUY"
    else:
        bias = "WAIT"

    agreeing = [tf for tf in timeframes if tf["state"] == bias] if bias in ("SELL", "BUY") else []
    if agreeing:
        avg_abs_pos = sum(abs(tf["channel"]["position"]) for tf in agreeing) / len(agreeing)
        agreement_ratio = len(agreeing) / len(timeframes)
        confidence = 50 + agreement_ratio * 30 + min(avg_abs_pos, 3.0) * 5
        confidence = max(50, min(95, round(confidence)))
        stars = max(1, min(5, round(confidence / 20)))
    else:
        confidence = 50
        stars = 2

    directional_tfs = sell_count + buy_count
    if directional_tfs >= 3:
        market_mode = "TREND"
        market_mode_note = "複数の時間足でチャネル際まで到達しており、方向感のある地合い。"
    elif gate_count >= 1:
        market_mode = "EVENT DRIVEN"
        market_mode_note = "回帰チャネルの突破が見られ、材料次第で振れやすい局面。"
    else:
        market_mode = "RANGE"
        market_mode_note = "多くの時間足が中央付近で推移しており、方向感に乏しいレンジ地合い。"

    latest_price = m5[-1]["c"] if m5 else ch_1h["latest"]
    day_change_pct = 0.0
    if len(h1) >= 24:
        base = h1[-24]["c"]
        if base:
            day_change_pct = (latest_price - base) / base * 100

    # USD/JPY版と同じ修正: GATE継続型(ブレイク継続・順張り)ではSL=中心線、
    # TP=測定値幅(エントリーから中心線までの距離を反対方向に伸ばした位置)に変更。
    ref_channel = ch_1h
    is_gate_continuation = abs(ref_channel["position"]) >= cs.GATE_THRESHOLD
    if bias == "SELL":
        entry = latest_price
        if is_gate_continuation:
            sl = ref_channel["mid"]
            tp = 2 * entry - ref_channel["mid"]
            trade_lead = "戻り売り継続 ― ブレイク方向についていく（順張り）"
        else:
            tp = ref_channel["mid"]
            sl = ref_channel["upper"] + 0.5 * ref_channel["sigma"]
            trade_lead = "戻り売り ― ただし戻りを深追いしない"
    elif bias == "BUY":
        entry = latest_price
        if is_gate_continuation:
            sl = ref_channel["mid"]
            tp = 2 * entry - ref_channel["mid"]
            trade_lead = "押し目買い継続 ― ブレイク方向についていく（順張り）"
        else:
            tp = ref_channel["mid"]
            sl = ref_channel["lower"] - 0.5 * ref_channel["sigma"]
            trade_lead = "押し目買い ― ただし高値を深追いしない"
    else:
        entry = tp = sl = None
        trade_lead = "様子見 ― チャネル中央で方向感なし"

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
            "チャネルの中央は様子見。ブレイクを待つのが賢明。",
        ],
    }
    commentary = comments.get(bias, comments["WAIT"])[0]
    market_context = build_market_context_eurusd(
        bias, sell_count, buy_count, gate_count, latest_price, day_change_pct,
        yield_trend, wti_trend,
    )

    daily_analysis = None
    if out_path:
        daily_analysis = load_daily_analysis_eurusd(os.path.dirname(out_path))

    result = {
        "generated_at_utc": now.isoformat(),
        "pair": PAIR_LABEL,
        "latest_price": round(latest_price, DECIMALS),
        "day_change_pct": round(day_change_pct, 2),
        "signal": {
            "bias": bias,
            "bias_label": {"SELL": "戻り売り優勢", "BUY": "押し目買い優勢", "WAIT": "方向感なし"}[bias],
            "stars": stars,
            "confidence": confidence,
        },
        "market_mode": market_mode,
        "market_mode_note": market_mode_note,
        "priority_trade": {
            "lead": trade_lead,
            "entry": round(entry, DECIMALS) if entry is not None else None,
            "take_profit": round(tp, DECIMALS) if tp is not None else None,
            "stop_loss": round(sl, DECIMALS) if sl is not None else None,
        },
        "regression_channels": [
            {
                "key": tf["key"],
                "label": tf["label"],
                "state": tf["state"],
                "position_sigma": round(tf["channel"]["position"], 2),
                "trend": tf["trend"],
                "mid": round(tf["channel"]["mid"], DECIMALS),
                "upper": round(tf["channel"]["upper"], DECIMALS),
                "lower": round(tf["channel"]["lower"], DECIMALS),
                "is_primary": tf["key"] == "h1",
            }
            for tf in timeframes
        ],
        "charts": [build_chart_entry_eurusd(tf) for tf in timeframes],
        "technical": technical,
        "macro": {
            "us10y_trend": yield_trend,
            "us10y_latest": round(us10y_latest, 2) if us10y_latest is not None else None,
            "wti_trend": wti_trend,
        },
        "commentary": commentary,
        "market_context": market_context,
        "disclaimer": "本データはルールベースの参考情報であり、投資成果を保証するものではありません。",
    }
    if daily_analysis is not None:
        result["daily_analysis"] = daily_analysis
    return result


def main():
    out_path = os.path.join(os.path.dirname(__file__), "..", "signal_eurusd.json")
    out_path = os.path.abspath(out_path)

    try:
        signal = build_signal(out_path=out_path)
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] EUR/USDシグナル計算に失敗しました: {e}", file=sys.stderr)
        sys.exit(1)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(signal, f, ensure_ascii=False, indent=2)
    print(f"書き出し完了: {out_path}")
    print(json.dumps(signal, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
