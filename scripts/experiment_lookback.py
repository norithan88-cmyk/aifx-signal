#!/usr/bin/env python3
"""
AI FX研究所 - LOOKBACK比較実験ログ

2026-08-20、19ヶ月分の過去データ(HistData.com)でLOOKBACK値を10〜100まで比較検証した結果、
30を下回るあたりから「回帰チャネルの基準線が、判定対象の反発点そのものに引っ張られる」
自己参照的な問題が疑われ、数値が不自然に良く見えている可能性が高いと判断した
（本番はLOOKBACK=30を採用）。

100〜50の範囲も、なだらかだが件数・勝率・PFとも改善傾向が見られたため、疑わしい
10・現行の30に加えて、50・70・100も含めた5値を"これから"の実データ（未来のデータ）で
リアルタイムに記録し、過去データへの過剰適合が実際に問題になるのかどうかを
検証するための実験用ログ。本番のsignal.json/trade_log.jsonとは完全に別ファイル
(experiment_lookback_log.json)に記録し、サイト表示には一切使わない。

各lookback呼び出しには必ずlookback=を明示的に渡している（compute_signal.py本体の
LOOKBACK定数を関数デフォルト値経由で暗黙参照すると、本体側の値を変更した時に
挙動が変わってしまうバグを過去に踏んだため、このスクリプトでは踏襲しない設計）。

記録する内容: 各LOOKBACK値で判定したbias(WAIT/SELL/BUY)と、シグナルが出た場合の
entry/tp/slの決着(WIN/LOSS)。compute_signal.pyのtrade_logロジックと同じ考え方だが、
LOOKBACK値ごとに独立した仮想ポジション管理を行う。
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))
import compute_signal as cs

EXPERIMENT_LOOKBACKS = [10, 30, 50, 70, 100]


def compute_bias_for_lookback(m5, m15, h1, m1, lookback):
    """compute_signal.pyのbuild_signal()と同じロジックを、指定LOOKBACKで再計算する。"""
    ch_5m = cs.linear_regression_channel([b["c"] for b in m5], lookback=lookback)
    ch_15m = cs.linear_regression_channel([b["c"] for b in m15], lookback=lookback)
    ch_1h = cs.linear_regression_channel([b["c"] for b in h1], lookback=lookback)
    ch_1m = cs.linear_regression_channel([b["c"] for b in m1], lookback=lookback)

    d5 = cs.momentum_direction(ch_5m)
    d15 = cs.momentum_direction(ch_15m)
    d1h = cs.momentum_direction(ch_1h)

    if d5 == "UP" and d15 == "UP" and d1h == "UP":
        candidate = "BUY"
    elif d5 == "DOWN" and d15 == "DOWN" and d1h == "DOWN":
        candidate = "SELL"
    else:
        candidate = None

    extreme = cs.detect_reversal_setup(m1, ch_1m, candidate) if candidate else None
    bias = candidate if (candidate and extreme is not None) else "WAIT"
    return bias, extreme


def load_log(base_dir):
    path = os.path.join(base_dir, "experiment_lookback_log.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for lb in EXPERIMENT_LOOKBACKS:
            data.setdefault(str(lb), {"trades": []})
        return data
    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError):
        return {str(lb): {"trades": []} for lb in EXPERIMENT_LOOKBACKS}


def update_one_lookback(log_entry, bias, entry, tp, sl, latest_price, now_iso):
    trades = log_entry["trades"]
    open_trade = trades[-1] if trades and trades[-1].get("status") == "OPEN" else None

    if open_trade is not None:
        ob = open_trade["bias"]
        otp, osl = open_trade["take_profit"], open_trade["stop_loss"]
        hit_tp = (latest_price <= otp) if ob == "SELL" else (latest_price >= otp)
        hit_sl = (latest_price >= osl) if ob == "SELL" else (latest_price <= osl)
        if hit_tp or hit_sl:
            open_trade["status"] = "WIN" if hit_tp else "LOSS"
            open_trade["closed_at_utc"] = now_iso
            open_trade["closed_price"] = round(latest_price, 3)
            diff = (open_trade["entry"] - latest_price) if ob == "SELL" else (latest_price - open_trade["entry"])
            open_trade["pips"] = round(diff * 100, 1)
            open_trade = None

    if open_trade is None and bias in ("SELL", "BUY") and entry is not None:
        trades.append({
            "opened_at_utc": now_iso, "bias": bias, "entry": round(entry, 3),
            "take_profit": round(tp, 3), "stop_loss": round(sl, 3),
            "status": "OPEN", "closed_at_utc": None, "closed_price": None, "pips": None,
        })

    closed = [t for t in trades if t["status"] in ("WIN", "LOSS")]
    wins = [t for t in closed if t["status"] == "WIN"]
    log_entry["stats"] = {
        "total_closed": len(closed),
        "wins": len(wins),
        "win_rate_pct": round(len(wins) / len(closed) * 100, 1) if closed else None,
        "total_pips": round(sum(t["pips"] for t in closed), 1) if closed else 0.0,
    }
    log_entry["trades"] = trades


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    now = datetime.now(timezone.utc)

    m1 = cs.fetch_fx_intraday("JPY=X", "1m", "5d")
    m5 = cs.fetch_fx_intraday("JPY=X", "5m", "5d")
    m15 = cs.fetch_fx_intraday("JPY=X", "15m", "5d")
    h1 = cs.fetch_fx_intraday("JPY=X", "60m", "60d")
    latest_price = m1[-1]["c"] if m1 else None

    log = load_log(base_dir)

    for lb in EXPERIMENT_LOOKBACKS:
        try:
            bias, extreme = compute_bias_for_lookback(m5, m15, h1, m1, lb)
        except RuntimeError as e:
            print(f"[WARN] LOOKBACK={lb}の判定に失敗（続行します）: {e}", file=sys.stderr)
            continue

        entry = tp = sl = None
        if bias in ("SELL", "BUY") and extreme is not None:
            entry = latest_price
            move = abs(entry - extreme)
            if bias == "SELL":
                sl = extreme + cs.SL_BUFFER_PIPS / 100
                tp = entry - move
            else:
                sl = extreme - cs.SL_BUFFER_PIPS / 100
                tp = entry + move

        update_one_lookback(log[str(lb)], bias, entry, tp, sl, latest_price, now.isoformat())
        print(f"LOOKBACK={lb}: bias={bias}  stats={log[str(lb)]['stats']}")

    log["updated_at_utc"] = now.isoformat()
    out_path = os.path.join(base_dir, "experiment_lookback_log.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f"書き出し完了: {out_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        print(f"[WARN] 実験ログの更新に失敗しました（本番シグナルには影響しません）: {e}", file=sys.stderr)
        sys.exit(0)
