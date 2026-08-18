
<style>
  .afl-top {
    --afl-ink: #171310;
    --afl-navy: #0c1526;
    --afl-navy-2: #16294a;
    --afl-paper: #f6f2e7;
    --afl-paper-line: #e6dfc9;
    --afl-surface: #fffdf8;
    --afl-line: #e3ddc9;
    --afl-muted: #74695a;
    --afl-cyan: #49b6e6;
    --afl-cyan-ink: #0d5d7a;
    --afl-brass: #a97a2f;
    --afl-good: #2f8f5b;
    --afl-good-bg: #e7f3ea;
    --afl-warn: #a97a2f;
    --afl-warn-bg: #f6ecd9;
    --afl-bad: #b8503f;
    --afl-bad-bg: #f8e9e5;
    --afl-shadow: 0 18px 40px rgba(12, 21, 38, .10);

    background: var(--afl-paper);
    color: var(--afl-ink);
    font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic Medium", "Yu Gothic", Meiryo, sans-serif;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
  }
  @media (prefers-color-scheme: dark) {
    .afl-top {
      --afl-ink: #eee9e0;
      --afl-paper: #0b0f16;
      --afl-paper-line: #1a2130;
      --afl-surface: #121a26;
      --afl-line: #253044;
      --afl-muted: #93a0b4;
      --afl-cyan: #6cd0ff;
      --afl-cyan-ink: #bdeeff;
      --afl-brass: #d7ab5f;
      --afl-good: #58c98a;
      --afl-good-bg: #123322;
      --afl-warn: #d7ab5f;
      --afl-warn-bg: #332711;
      --afl-bad: #e08674;
      --afl-bad-bg: #3a1c17;
      --afl-shadow: 0 18px 40px rgba(0, 0, 0, .35);
    }
  }

  .afl-top, .afl-top *, .afl-top *::before, .afl-top *::after { box-sizing: border-box; }
  .afl-top .afl-shell { max-width: 1160px; margin: 0 auto; padding: 0 20px 40px; }
  .afl-top .afl-mono { font-family: ui-monospace, "SF Mono", "Cascadia Code", Consolas, monospace; font-variant-numeric: tabular-nums; }
  .afl-top .afl-serif { font-family: "Hiragino Mincho ProN", "Yu Mincho", "Noto Serif JP", serif; }
  .afl-top a { color: var(--afl-cyan-ink); }

  /* ---------- HERO ---------- */
  .afl-top .afl-hero {
    position: relative;
    background: linear-gradient(160deg, var(--afl-navy), var(--afl-navy-2) 78%);
    color: #eef4fb;
    border-radius: 18px;
    padding: 22px 40px 18px;
    margin-top: 24px;
    overflow: hidden;
    box-shadow: var(--afl-shadow);
  }
  .afl-top .afl-hero-grid {
    position: absolute; inset: 0;
    background-image:
      linear-gradient(rgba(120,190,230,.10) 1px, transparent 1px),
      linear-gradient(90deg, rgba(120,190,230,.10) 1px, transparent 1px);
    background-size: 34px 34px;
    mask-image: radial-gradient(ellipse 70% 70% at 78% 15%, #000 0%, transparent 72%);
    pointer-events: none;
  }
  .afl-top .afl-hero-head {
    position: relative;
    display: flex; align-items: flex-start; justify-content: space-between; gap: 24px; flex-wrap: wrap;
  }
  .afl-top .afl-mark { flex: 0 0 auto; display: flex; align-items: center; gap: 10px; }
  .afl-top .afl-mark svg { width: 40px; height: 40px; display: block; }
  .afl-top .afl-mark-word { font-size: 13px; letter-spacing: .16em; font-weight: 700; color: #cfe6f7; }
  .afl-top .afl-mark-word small { display: block; font-size: 10px; letter-spacing: .22em; color: #7fa3c2; font-weight: 500; margin-top: 2px; }
  .afl-top .afl-live {
    display: inline-flex; align-items: center; gap: 7px;
    font-size: 11px; letter-spacing: .08em; color: #a9c4dc;
    border: 1px solid rgba(255,255,255,.18); border-radius: 999px; padding: 5px 11px 5px 9px;
  }
  .afl-top .afl-dot { width: 6px; height: 6px; border-radius: 50%; background: #58e0a8; box-shadow: 0 0 0 0 rgba(88,224,168,.6); animation: afl-pulse 2.4s ease-out infinite; }
  @keyframes afl-pulse { 0% { box-shadow: 0 0 0 0 rgba(88,224,168,.55); } 70% { box-shadow: 0 0 0 7px rgba(88,224,168,0); } 100% { box-shadow: 0 0 0 0 rgba(88,224,168,0); } }
  @media (prefers-reduced-motion: reduce) { .afl-top .afl-dot { animation: none; } }

  .afl-top .afl-headline {
    position: relative;
    margin: 12px 0 8px;
    font-size: clamp(20px, 3vw, 28px);
    line-height: 1.3;
    font-weight: 700;
    text-wrap: balance;
  }
  .afl-top .afl-headline em { font-style: normal; color: var(--afl-cyan); white-space: nowrap; }
  .afl-top .afl-sub { position: relative; margin: 0; max-width: 640px; color: #b9cade; font-size: 14.5px; }
  .afl-top .afl-ticker-wrap {
    background: linear-gradient(160deg, var(--afl-navy), var(--afl-navy-2) 85%);
    border-radius: 12px; margin-top: 12px; padding: 2px 4px 0;
    box-shadow: var(--afl-shadow); overflow: hidden;
  }
  .afl-top .tradingview-widget-copyright { padding: 2px 10px 6px; }
  .afl-top .tradingview-widget-copyright .blue-text { color: #7fa3c2; font-size: 11px; text-decoration: none; }

  /* ---------- GRID ---------- */
  .afl-top .afl-grid { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 14px; margin-top: 16px; }
  .afl-top .afl-card {
    background: var(--afl-surface); border: 1px solid var(--afl-line); border-radius: 12px;
    padding: 20px; box-shadow: var(--afl-shadow);
    transition: transform .18s ease, box-shadow .18s ease;
  }
  .afl-top .afl-card:hover { transform: translateY(-2px); }
  @media (prefers-reduced-motion: reduce) { .afl-top .afl-card { transition: none; } .afl-top .afl-card:hover { transform: none; } }
  .afl-top .afl-kpi { grid-column: span 4; min-width: 0; }
  .afl-top .afl-half { grid-column: span 6; min-width: 0; }
  .afl-top .afl-col-7 { grid-column: span 7; min-width: 0; }
  .afl-top .afl-col-5 { grid-column: span 5; min-width: 0; }
  .afl-top .afl-trade { grid-column: span 8; min-width: 0; }
  .afl-top .afl-full { grid-column: span 12; min-width: 0; }

  .afl-top .afl-label {
    display: flex; align-items: center; gap: 7px;
    font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--afl-muted); font-weight: 700;
  }
  .afl-top .afl-label svg { width: 14px; height: 14px; flex: 0 0 auto; color: var(--afl-cyan-ink); }

  /* KPI cards */
  .afl-top .afl-stars { font-size: 20px; letter-spacing: 2px; color: var(--afl-brass); margin: 10px 0 2px; }
  .afl-top .afl-stars .afl-off { color: var(--afl-line); }
  .afl-top .afl-kpi-big { font-family: ui-monospace, "SF Mono", Consolas, monospace; font-variant-numeric: tabular-nums; font-size: 34px; font-weight: 700; margin: 8px 0 2px; }
  .afl-top .afl-pill { display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; }
  .afl-top .afl-pill.afl-go { background: var(--afl-good-bg); color: var(--afl-good); }
  .afl-top .afl-pill.afl-sell { background: var(--afl-bad-bg); color: var(--afl-bad); }
  .afl-top .afl-pill.afl-caution { background: var(--afl-warn-bg); color: var(--afl-warn); }
  .afl-top .afl-pill.afl-high { background: var(--afl-bad-bg); color: var(--afl-bad); }
  .afl-top .afl-kpi-note { font-size: 12.5px; color: var(--afl-muted); margin: 8px 0 0; }
  .afl-top .afl-gauge { height: 5px; border-radius: 3px; background: var(--afl-paper-line); margin-top: 10px; overflow: hidden; }
  .afl-top .afl-gauge > i { display: block; height: 100%; background: linear-gradient(90deg, var(--afl-cyan), var(--afl-brass)); border-radius: 3px; }

  /* Judgment card（総合判定・強調表示） */
  .afl-top .afl-judgment { border: 2px solid var(--afl-brass); background: linear-gradient(140deg, var(--afl-surface), var(--afl-warn-bg)); }
  .afl-top .afl-signal-line { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-top: 8px; }
  .afl-top .afl-signal-big { padding: 8px 18px; border-radius: 40px; color: #fff; font-size: 19px; font-weight: 900; }
  .afl-top .afl-signal-big.afl-go { background: var(--afl-good); }
  .afl-top .afl-signal-big.afl-sell { background: var(--afl-bad); }
  .afl-top .afl-signal-big.afl-caution { background: var(--afl-warn); }
  .afl-top .afl-summary-strategy { margin-top: 15px; padding: 13px 15px; border-left: 4px solid var(--afl-brass); border-radius: 9px; background: var(--afl-warn-bg); font-size: 13px; }
  .afl-top .afl-summary-advice { margin-top: 14px; padding: 17px; border: 1px solid var(--afl-brass); border-radius: 11px; background: var(--afl-surface); }
  .afl-top .afl-summary-advice h3 { margin: 0 0 6px; color: var(--afl-brass); font-size: 18px; }
  .afl-top .afl-summary-advice p { margin: 0; font-size: 13.5px; }

  /* Trade ticket */
  .afl-top .afl-trade, .afl-top .afl-one { position: relative; }
  .afl-top .afl-trade { border-left: 3px solid var(--afl-brass); }
  .afl-top .afl-one {
    text-align: center; color: #eef4fb;
    background: linear-gradient(150deg, var(--afl-navy-2), var(--afl-navy));
  }
  .afl-top .afl-one .afl-label { color: #9bb4c7; justify-content: center; }
  .afl-top .afl-one .afl-h2 { color: #f3d888; }
  .afl-top .afl-one .afl-pair { font-size: 24px; font-weight: 900; margin-top: 4px; }
  .afl-top .afl-ticket-no { font-size: 11px; color: var(--afl-muted); }
  .afl-top .afl-trade h2 { font-size: 22px; margin: 6px 0 4px; }
  .afl-top .afl-trade-lead { font-size: 15px; font-weight: 700; margin: 0 0 16px; }
  .afl-top .afl-trade-row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
  .afl-top .afl-trade-box { border-radius: 10px; padding: 12px 14px; background: var(--afl-paper); border-left: 3px solid var(--afl-line); }
  .afl-top .afl-trade-box.afl-entry { border-left-color: var(--afl-cyan-ink); }
  .afl-top .afl-trade-box.afl-tp { border-left-color: var(--afl-good); }
  .afl-top .afl-trade-box.afl-sl { border-left-color: var(--afl-bad); }
  .afl-top .afl-trade-box span { display: block; font-size: 10.5px; letter-spacing: .08em; color: var(--afl-muted); text-transform: uppercase; }
  .afl-top .afl-trade-box b { display: block; font-family: ui-monospace, "SF Mono", Consolas, monospace; font-size: 21px; margin-top: 3px; font-variant-numeric: tabular-nums; color: var(--afl-ink); }
  .afl-top .afl-summary-detail-btn {
    display: flex; align-items: center; justify-content: space-between; gap: 10px;
    margin-top: 16px; padding: 13px 16px; border: 1px solid rgba(255,255,255,.28); border-radius: 10px;
    background: #f1d98b; color: #18202a; text-decoration: none; font-weight: 800; transition: .18s;
  }
  .afl-top .afl-summary-detail-btn:hover { transform: translateY(-2px); background: #ffe8a2; }
  .afl-top .afl-summary-manual-note { margin: 8px 0 0; color: #9bb4c7; font-size: 10px; text-align: center; }
  .afl-top .afl-live-chart-btn {
    display: flex; align-items: center; justify-content: space-between; gap: 10px;
    margin-top: 10px; padding: 11px 16px; border: 1px solid rgba(255,255,255,.28); border-radius: 10px;
    background: rgba(255,255,255,.06); color: #eef4fb; text-decoration: none; font-weight: 700; font-size: 13.5px;
    transition: .18s;
  }
  .afl-top .afl-live-chart-btn:hover { transform: translateY(-2px); background: rgba(255,255,255,.14); }

  .afl-top .afl-notify-btn {
    display: inline-flex; align-items: center; gap: 8px; margin-top: 10px; padding: 9px 14px;
    border: 1px solid var(--afl-line); border-radius: 10px; background: var(--afl-surface);
    color: var(--afl-ink); font-weight: 700; font-size: 12.5px; cursor: pointer; transition: .18s;
  }
  .afl-top .afl-notify-btn:hover { background: var(--afl-paper); }
  .afl-top .afl-notify-btn.afl-notify-on { border-color: var(--afl-good); color: var(--afl-good); }
  .afl-top .afl-notify-status { margin: 4px 0 0; font-size: 11px; color: var(--afl-muted); }

  /* Macro monitor（周辺市場のライブチャート） */
  .afl-top .afl-macro-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; margin-top: 14px; }
  .afl-top .afl-macro-chart { min-width: 0; min-height: 455px; padding: 13px; background: var(--afl-paper); border: 1px solid var(--afl-line); border-radius: 11px; overflow: hidden; }
  .afl-top .afl-macro-head { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; margin-bottom: 8px; }
  .afl-top .afl-macro-head strong { font-size: 15px; }
  .afl-top .afl-macro-head span { color: var(--afl-muted); font-size: 10px; letter-spacing: .05em; }
  .afl-top .afl-macro-chart iframe,
  .afl-top .afl-macro-chart .tradingview-widget-container,
  .afl-top .afl-macro-chart .tradingview-widget-container__widget {
    display: block; width: 100% !important; height: 400px !important; min-height: 400px !important;
    border: 0; border-radius: 8px; background: var(--afl-surface);
  }
  .afl-top .afl-macro-toggle { margin-top: 16px; }
  .afl-top .afl-macro-toggle > summary {
    display: flex; align-items: center; justify-content: center; gap: 10px;
    padding: 14px 18px; color: #fff; font-weight: 800; cursor: pointer; list-style: none;
    background: linear-gradient(135deg, var(--afl-navy), var(--afl-navy-2));
    border: 1px solid var(--afl-brass); border-radius: 10px; transition: filter .2s ease;
  }
  .afl-top .afl-macro-toggle > summary::-webkit-details-marker { display: none; }
  .afl-top .afl-macro-toggle > summary:hover { filter: brightness(1.12); }
  .afl-top .afl-macro-toggle > summary::before {
    content: "＋"; width: 24px; height: 24px; line-height: 22px; text-align: center;
    color: var(--afl-navy); background: var(--afl-brass); border-radius: 50%;
  }
  .afl-top .afl-macro-toggle[open] > summary::before { content: "−"; }
  .afl-top .afl-macro-toggle[open] > summary { margin-bottom: 14px; }

  /* Quick-glance grid（今日の結論カードをひとまとまりで見せる） */
  .afl-top .afl-glance-grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 8px; margin-top: 14px; }
  .afl-top .afl-glance-item { padding: 10px 8px; text-align: center; background: rgba(255,255,255,.55); border: 1px solid var(--afl-line); border-radius: 9px; min-width: 0; }
  @media (prefers-color-scheme: dark) { .afl-top .afl-glance-item { background: rgba(255,255,255,.04); } }
  .afl-top .afl-glance-label { display: block; font-size: 10px; color: var(--afl-muted); letter-spacing: .04em; margin-bottom: 4px; }
  .afl-top .afl-glance-value { display: block; font-size: 12.5px; font-weight: 800; color: var(--afl-ink); overflow-wrap: break-word; line-height: 1.35; }
  @media (max-width: 720px) { .afl-top .afl-glance-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }

  /* AIの読み（3行要約） ‒ AIアバター発言型。左のアクセント色はJSがシグナル方向で切り替える
     （--afl-avatar-accent: SELL=--afl-bad(赤) / BUY=--afl-good(緑) / WAIT=--afl-brass(中立)）。 */
  .afl-top .afl-ai-avatar-card {
    --afl-avatar-accent: var(--afl-brass);
    display: flex; gap: 14px; margin-top: 14px;
    background: linear-gradient(155deg, var(--afl-navy), var(--afl-navy-2) 88%);
    border-radius: 14px; padding: 18px 20px 18px 22px; color: #eef4fb;
    border-left: 5px solid var(--afl-avatar-accent);
    box-shadow: var(--afl-shadow), 0 0 0 1px rgba(255,255,255,.06);
    position: relative; overflow: hidden;
    transition: border-color .3s ease;
  }
  .afl-top .afl-ai-avatar-card::after {
    content: ""; position: absolute; inset: 0;
    background-image:
      radial-gradient(circle at 88% 0%, rgba(108,208,255,.16), transparent 55%),
      radial-gradient(circle at 0% 100%, color-mix(in srgb, var(--afl-avatar-accent) 22%, transparent), transparent 60%);
    pointer-events: none;
  }
  .afl-top .afl-ai-avatar {
    flex: 0 0 auto; width: 42px; height: 42px; border-radius: 50%;
    background: linear-gradient(135deg, var(--afl-cyan), var(--afl-avatar-accent));
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 12px; color: var(--afl-navy);
    box-shadow: 0 0 0 3px rgba(255,255,255,.16), 0 0 14px 1px color-mix(in srgb, var(--afl-avatar-accent) 55%, transparent);
    position: relative; z-index: 1;
    transition: background .3s ease, box-shadow .3s ease;
  }
  .afl-top .afl-ai-avatar-body { flex: 1 1 auto; min-width: 0; position: relative; z-index: 1; }
  .afl-top .afl-ai-avatar-kicker {
    display: flex; align-items: center; gap: 8px; margin-bottom: 8px; flex-wrap: wrap;
    font-size: 10.5px; letter-spacing: .12em; text-transform: uppercase; color: #8fb3d1; font-weight: 700;
  }
  .afl-top .afl-ai-avatar-pill {
    display: inline-block; padding: 2px 9px; border-radius: 999px; font-size: 10.5px; font-weight: 800;
    background: var(--afl-warn-bg); color: #7a5a1f; letter-spacing: 0; text-transform: none;
  }
  .afl-top .afl-ai-avatar-lines { margin: 0; padding: 0; list-style: none; }
  .afl-top .afl-ai-avatar-lines li {
    position: relative; padding-left: 16px; margin: 7px 0; font-size: 13.5px; line-height: 1.6; color: #e4ebf2;
  }
  .afl-top .afl-ai-avatar-lines li::before {
    content: ""; position: absolute; left: 0; top: 9px; width: 6px; height: 6px;
    border-radius: 50%; background: var(--afl-cyan);
  }
  .afl-top .afl-ai-avatar-lines li:first-child { font-weight: 700; color: #fff; }

  /* Inline daily analysis toggle（AI総合判定カード内で「今日の詳しい分析」をその場展開） */
  .afl-top .afl-analysis-toggle { margin-top: 16px; }
  .afl-top .afl-analysis-toggle > summary {
    display: flex; align-items: center; justify-content: center; gap: 10px;
    padding: 12px 16px; color: var(--afl-navy); font-weight: 800; cursor: pointer; list-style: none;
    background: var(--afl-brass); border-radius: 10px; transition: filter .2s ease;
  }
  .afl-top .afl-analysis-toggle > summary::-webkit-details-marker { display: none; }
  .afl-top .afl-analysis-toggle > summary:hover { filter: brightness(1.08); }
  .afl-top .afl-analysis-toggle > summary::before {
    content: "＋"; width: 22px; height: 22px; line-height: 21px; text-align: center; font-size: 13px;
    color: #fff; background: var(--afl-navy); border-radius: 50%;
  }
  .afl-top .afl-analysis-toggle[open] > summary::before { content: "−"; }
  .afl-top .afl-analysis-toggle[open] > summary { margin-bottom: 14px; }
  .afl-top .afl-analysis-body { font-size: 13.5px; }
  .afl-top .afl-analysis-empty { margin: 0; color: var(--afl-muted); font-size: 13px; }
  .afl-top .afl-analysis-updated { margin: 0 0 8px; color: var(--afl-muted); font-size: 11.5px; }
  .afl-top .afl-analysis-headline { margin: 0 0 10px; font-size: 17px; color: var(--afl-ink); }
  .afl-top .afl-analysis-advice p { margin: 0 0 10px; line-height: 1.7; color: var(--afl-ink); }
  .afl-top .afl-analysis-advice p:last-child { margin-bottom: 0; }
  .afl-top .afl-analysis-scenarios { display: grid; gap: 10px; margin: 14px 0; }
  .afl-top .afl-scenario { padding: 12px 14px; border-radius: 10px; border-left: 4px solid var(--afl-line); background: var(--afl-paper); }
  .afl-top .afl-scenario.afl-buy { border-left-color: var(--afl-good); }
  .afl-top .afl-scenario.afl-sell { border-left-color: var(--afl-bad); }
  .afl-top .afl-scenario.afl-neutral { border-left-color: var(--afl-warn); }
  .afl-top .afl-scenario-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 4px; }
  .afl-top .afl-scenario-label { font-weight: 800; font-size: 13.5px; }
  .afl-top .afl-scenario-prob { font-family: ui-monospace, "SF Mono", Consolas, monospace; font-weight: 700; color: var(--afl-muted); }
  .afl-top .afl-scenario-body { margin: 0; font-size: 12.5px; color: var(--afl-muted); line-height: 1.6; }
  .afl-top .afl-analysis-order { margin: 14px 0; padding: 14px; border: 1px solid var(--afl-brass); border-radius: 10px; background: var(--afl-warn-bg); }
  .afl-top .afl-analysis-order-lead { margin: 0 0 10px; font-size: 13px; font-weight: 700; color: var(--afl-ink); }
  .afl-top .afl-analysis-order-row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }
  .afl-top .afl-analysis-order-box { border-radius: 8px; padding: 8px 10px; background: var(--afl-surface); border-left: 3px solid var(--afl-line); }
  .afl-top .afl-analysis-order-box.afl-entry { border-left-color: var(--afl-cyan-ink); }
  .afl-top .afl-analysis-order-box.afl-tp { border-left-color: var(--afl-good); }
  .afl-top .afl-analysis-order-box.afl-sl { border-left-color: var(--afl-bad); }
  .afl-top .afl-analysis-order-box span { display: block; font-size: 9.5px; letter-spacing: .06em; color: var(--afl-muted); text-transform: uppercase; }
  .afl-top .afl-analysis-order-box b { display: block; font-size: 13px; margin-top: 2px; color: var(--afl-ink); }
  .afl-top .afl-analysis-order-sub { margin: 10px 0 0; font-size: 12px; color: var(--afl-muted); line-height: 1.5; }
  .afl-top .afl-analysis-risk { margin: 4px 0 0; padding: 12px 14px; border-left: 4px solid var(--afl-bad); border-radius: 9px; background: var(--afl-bad-bg); font-size: 12.5px; color: var(--afl-ink); line-height: 1.6; }
  @media (max-width: 720px) { .afl-top .afl-analysis-order-row { grid-template-columns: 1fr; } }


  /* Currency strength meter（簡易版） */
  .afl-top .afl-cs-list { margin-top: 12px; }
  .afl-top .afl-cs-row { display: flex; align-items: center; gap: 10px; padding: 7px 0; }
  .afl-top .afl-cs-code { width: 42px; flex: 0 0 auto; font-weight: 800; font-size: 13px; }
  .afl-top .afl-cs-bar-track { position: relative; flex: 1 1 auto; height: 8px; border-radius: 4px; background: var(--afl-paper-line); overflow: hidden; }
  .afl-top .afl-cs-bar { position: absolute; top: 0; bottom: 0; border-radius: 4px; }
  .afl-top .afl-cs-bar.afl-up { background: var(--afl-good); left: 50%; }
  .afl-top .afl-cs-bar.afl-down { background: var(--afl-bad); right: 50%; }
  .afl-top .afl-cs-mid-line { position: absolute; left: 50%; top: -2px; bottom: -2px; width: 1px; background: var(--afl-muted); opacity: .4; }
  .afl-top .afl-cs-value { width: 58px; flex: 0 0 auto; text-align: right; font-family: ui-monospace, "SF Mono", Consolas, monospace; font-size: 12.5px; font-weight: 700; }

  /* Global market read-out ‒ 表ではなく折り返し可能な行にして、文字数に関わらず絶対に欠けないようにする */
  .afl-top .afl-mr-list { margin-top: 12px; }
  .afl-top .afl-mr-row {
    display: flex; align-items: baseline; justify-content: space-between; flex-wrap: wrap;
    gap: 2px 12px; padding: 9px 0; border-bottom: 1px solid var(--afl-line); font-size: 13.5px;
  }
  .afl-top .afl-mr-row:last-child { border-bottom: none; }
  .afl-top .afl-mr-label { display: flex; align-items: center; gap: 8px; min-width: 0; }
  .afl-top .afl-mr-value { font-weight: 700; font-family: ui-monospace, "SF Mono", Consolas, monospace; }
  .afl-top .afl-mkt-dot { width: 7px; height: 7px; border-radius: 50%; flex: 0 0 auto; }
  .afl-top .afl-mkt-dot.afl-up { background: var(--afl-good); } .afl-top .afl-mkt-dot.afl-down { background: var(--afl-bad); } .afl-top .afl-mkt-dot.afl-flat { background: var(--afl-muted); }

  /* Technical dashboard（MACD/RSI/ボリンジャー/サポレジ） */
  .afl-top .afl-tech-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-top: 12px; }
  .afl-top .afl-mini { padding: 14px; border: 1px solid var(--afl-line); border-radius: 10px; background: var(--afl-paper); }
  .afl-top .afl-mini span { display: block; color: var(--afl-muted); font-size: 11px; letter-spacing: .04em; }
  .afl-top .afl-mini b { display: block; margin-top: 5px; font-family: ui-monospace, "SF Mono", Consolas, monospace; font-size: 17px; font-variant-numeric: tabular-nums; }
  .afl-top .afl-mini small { display: block; margin-top: 3px; font-size: 11.5px; color: var(--afl-muted); }

  /* Moving averages table */
  .afl-top .afl-ma-table { width: 100%; border-collapse: collapse; font-size: 13.5px; margin-top: 10px; }
  .afl-top .afl-ma-table th, .afl-top .afl-ma-table td { padding: 9px 6px; border-bottom: 1px solid var(--afl-line); text-align: left; }
  .afl-top .afl-ma-table th { color: var(--afl-muted); font-size: 11px; font-weight: 700; letter-spacing: .05em; }
  .afl-top .afl-ma-table td.afl-mono { font-family: ui-monospace, "SF Mono", Consolas, monospace; font-variant-numeric: tabular-nums; }

  /* Key event */
  .afl-top .afl-event { display: flex; align-items: center; gap: 22px; flex-wrap: wrap; margin-top: 12px; }
  .afl-top .afl-event-time { font-family: ui-monospace, "SF Mono", Consolas, monospace; font-size: 32px; font-weight: 700; font-variant-numeric: tabular-nums; }
  .afl-top .afl-event-body { flex: 1 1 240px; }
  .afl-top .afl-event-name { font-weight: 700; font-size: 15px; }
  .afl-top .afl-event-stars { color: var(--afl-brass); letter-spacing: 2px; margin-top: 2px; }
  .afl-top .afl-event-note { font-size: 13px; color: var(--afl-muted); margin-top: 6px; }

  /* 最新ニュース一覧 */
  .afl-top .afl-news-list { display: flex; flex-direction: column; gap: 2px; margin-top: 4px; }
  .afl-top .afl-news-row {
    display: flex; align-items: baseline; gap: 10px; padding: 9px 0;
    border-bottom: 1px solid var(--afl-line); font-size: 13.5px;
  }
  .afl-top .afl-news-row:last-child { border-bottom: none; }
  .afl-top .afl-news-source {
    flex: 0 0 auto; font-size: 10.5px; font-weight: 700; padding: 2px 8px; border-radius: 999px;
    background: var(--afl-warn-bg); color: var(--afl-warn); white-space: nowrap;
  }
  .afl-top .afl-news-title { flex: 1 1 auto; min-width: 0; color: var(--afl-ink); text-decoration: none; }
  .afl-top .afl-news-title:hover { text-decoration: underline; }
  .afl-top .afl-news-time { flex: 0 0 auto; font-size: 11px; color: var(--afl-muted); white-space: nowrap; }
  .afl-top .afl-empty { padding: 16px 0; text-align: center; color: var(--afl-muted); font-size: 13px; }
  @media (max-width: 600px) {
    .afl-top .afl-news-row { flex-wrap: wrap; }
    .afl-top .afl-news-time { flex-basis: 100%; }
  }

  /* Logbook note */
  .afl-top .afl-note {
    background: linear-gradient(160deg, var(--afl-navy), var(--afl-navy-2) 85%);
    color: #eef4fb; border-radius: 14px; padding: 30px 34px; position: relative; overflow: hidden;
  }
  .afl-top .afl-note-quote { position: absolute; top: 6px; left: 20px; font-size: 90px; color: rgba(255,255,255,.08); font-family: "Hiragino Mincho ProN", "Yu Mincho", serif; line-height: 1; }
  .afl-top .afl-note-label { display: block; font-size: 11px; letter-spacing: .14em; color: #8fb3d1; margin-bottom: 10px; }
  .afl-top .afl-note p { position: relative; font-family: "Hiragino Mincho ProN", "Yu Mincho", "Noto Serif JP", serif; font-size: clamp(17px, 2.2vw, 21px); line-height: 1.95; margin: 0; max-width: 760px; border-left: 2px solid var(--afl-brass); padding-left: 18px; }

  .afl-top h2.afl-h2 { font-size: 19px; margin: 8px 0 0; font-weight: 700; }

  /* Section divider（①結論 ②理由 ③戦略 ④注意点の見出し帯） */
  .afl-top .afl-section-divider { display: flex; align-items: center; gap: 12px; margin: 10px 4px -2px; }
  .afl-top .afl-section-num {
    width: 28px; height: 28px; border-radius: 50%; background: var(--afl-brass); color: #fff;
    display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 14px; flex: 0 0 auto;
  }
  .afl-top .afl-section-title { font-size: 15.5px; font-weight: 800; color: var(--afl-ink); letter-spacing: .02em; white-space: nowrap; }
  .afl-top .afl-section-sub { font-size: 11.5px; color: var(--afl-muted); font-weight: 500; margin-left: 2px; }
  .afl-top .afl-section-divider::after { content: ""; flex: 1 1 auto; height: 1px; background: var(--afl-line); }

  .afl-top .afl-disclaimer { font-size: 11.5px; color: var(--afl-muted); margin: 22px 4px 0; line-height: 1.8; }

  @media (max-width: 880px) {
    .afl-top .afl-shell { padding: 0 14px 30px; }
    .afl-top .afl-hero { padding: 18px 18px 14px; border-radius: 16px; }
    .afl-top .afl-kpi, .afl-top .afl-half, .afl-top .afl-col-7, .afl-top .afl-col-5, .afl-top .afl-trade, .afl-top .afl-full { grid-column: span 12; }
    .afl-top .afl-trade-row { grid-template-columns: minmax(0, 1fr); }
    .afl-top .afl-tech-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .afl-top .afl-summary-detail-btn { align-items: flex-start; }
    .afl-top .afl-summary-advice { padding: 14px; }
    .afl-top .afl-macro-grid { grid-template-columns: 1fr; }
    .afl-top .afl-macro-chart { min-height: 395px; }
    .afl-top .afl-macro-chart iframe,
    .afl-top .afl-macro-chart .tradingview-widget-container,
    .afl-top .afl-macro-chart .tradingview-widget-container__widget { height: 340px !important; min-height: 340px !important; }
  }
</style>

<div class="afl-top">
  <div class="afl-shell">

    <section class="afl-hero">
      <div class="afl-hero-grid"></div>
      <div class="afl-hero-head">
        <div class="afl-mark">
          <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M24 2 44 13.5V34.5L24 46 4 34.5V13.5Z" stroke="#6cc4ea" stroke-width="2"/>
            <line x1="15" y1="30" x2="15" y2="20" stroke="#6cc4ea" stroke-width="2"/>
            <rect x="12" y="21" width="6" height="10" fill="#6cc4ea"/>
            <line x1="24" y1="34" x2="24" y2="16" stroke="#9fdcff" stroke-width="2"/>
            <rect x="21" y="19" width="6" height="12" fill="#9fdcff"/>
            <line x1="33" y1="27" x2="33" y2="14" stroke="#eaf7ff" stroke-width="2"/>
            <rect x="30" y="16" width="6" height="8" fill="#eaf7ff"/>
            <path d="M8 33 Q22 24 40 11" stroke="#49b6e6" stroke-width="2" fill="none" stroke-linecap="round"/>
          </svg>
          <span class="afl-mark-word">AIFX研究所<small>AI FX LABO ‒ MARKET RESEARCH</small></span>
        </div>
        <span class="afl-live"><i class="afl-dot"></i>TradingView ライブ連携</span>
      </div>

      <h1 class="afl-headline"><span style="white-space:nowrap">AIが読む。</span><em>あなたが判断する。</em></h1>
      <p class="afl-sub">休むも相場。攻める日は、AIが教える。線形回帰・テクニカル・金利差・重要指標を横断して「今日はどうするか」を30秒で把握するための研究ダッシュボード。</p>
    </section>

    <div class="afl-grid">

      <div class="afl-full">
        <div class="afl-ticker-wrap">
          <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
            {
              "symbols": [
                { "proName": "FX_IDC:USDJPY", "title": "USD/JPY" },
                { "proName": "TVC:USOIL", "title": "WTI原油" },
                { "proName": "TVC:GOLD", "title": "GOLD" },
                { "proName": "FX_IDC:EURUSD", "title": "EUR/USD" },
                { "proName": "FX_IDC:GBPUSD", "title": "GBP/USD" }
              ],
              "colorTheme": "dark",
              "isTransparent": true,
              "showSymbolLogo": false,
              "displayMode": "adaptive",
              "locale": "ja"
            }
            </script>
          </div>
        </div>
      </div>

      <div class="afl-full afl-section-divider">
        <span class="afl-section-num">1</span>
        <span class="afl-section-title">今日の結論</span>
        <span class="afl-section-sub">AIの総合判断</span>
      </div>

      <section class="afl-card afl-judgment afl-full">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/></svg>TODAY'S AI SIGNAL</div>
        <h2 class="afl-h2">今日のAI総合判定</h2>
        <div class="afl-signal-line">
          <strong class="afl-signal-big afl-sell" id="afl-sig-pill">戻り売り優勢</strong>
          <span class="afl-stars" id="afl-sig-stars">★★★★<span class="afl-off">★</span></span>
        </div>
        <p class="afl-kpi-note" id="afl-sig-note">信頼度 84% ‒ 慎重にGO</p>
        <div class="afl-gauge"><i id="afl-sig-gauge" style="width:84%"></i></div>
        <p class="afl-kpi-note" id="afl-last-updated" style="opacity:.75;margin-top:6px">最終更新: ‒</p>
        <button type="button" class="afl-notify-btn" id="afl-notify-toggle">🔔 シグナル通知をオンにする</button>
        <p class="afl-notify-status" id="afl-notify-status">このページを開いている間、SELL/BUYシグナルが新しく発生した瞬間に音とブラウザ通知でお知らせします（ページを閉じている間は届きません）。</p>

        <div class="afl-glance-grid" id="afl-glance-grid">
          <div class="afl-glance-item"><span class="afl-glance-label">方向性</span><b class="afl-glance-value" id="afl-glance-bias">‒</b></div>
          <div class="afl-glance-item"><span class="afl-glance-label">信頼度</span><b class="afl-glance-value" id="afl-glance-confidence">‒</b></div>
          <div class="afl-glance-item"><span class="afl-glance-label">地合い</span><b class="afl-glance-value" id="afl-glance-mode">‒</b></div>
          <div class="afl-glance-item"><span class="afl-glance-label">戦略</span><b class="afl-glance-value" id="afl-glance-strategy">‒</b></div>
          <div class="afl-glance-item"><span class="afl-glance-label">注目点</span><b class="afl-glance-value" id="afl-glance-focus">‒</b></div>
        </div>

        <div class="afl-ai-avatar-card">
          <div class="afl-ai-avatar">AI</div>
          <div class="afl-ai-avatar-body">
            <div class="afl-ai-avatar-kicker">AIの読み<span class="afl-ai-avatar-pill" id="afl-ai-avatar-confidence">信頼度 ‒</span></div>
            <ul class="afl-ai-avatar-lines" id="afl-ai-summary-list">
              <li>データ取得中…</li>
            </ul>
          </div>
        </div>

        <details class="afl-analysis-toggle" id="afl-analysis-toggle">
          <summary><span>今日の詳しい分析を見る／閉じる</span></summary>
          <div class="afl-analysis-body">
            <p class="afl-analysis-empty" id="afl-analysis-empty" style="display:none">本日の詳しい分析はまだ準備中です。</p>
            <div id="afl-analysis-content">
              <p class="afl-analysis-updated" id="afl-analysis-updated"></p>
              <h3 class="afl-analysis-headline" id="afl-analysis-headline"></h3>
              <div class="afl-analysis-advice" id="afl-analysis-advice"></div>
              <div class="afl-analysis-scenarios" id="afl-analysis-scenarios"></div>
              <div class="afl-analysis-order" id="afl-analysis-order"></div>
              <p class="afl-analysis-risk" id="afl-analysis-risk"></p>
            </div>
          </div>
        </details>
      </section>

      <div class="afl-full afl-section-divider">
        <span class="afl-section-num">2</span>
        <span class="afl-section-title">戦略</span>
        <span class="afl-section-sub">エントリー／利確／損切り</span>
      </div>

      <section class="afl-card afl-one afl-full">
        <p class="afl-ticket-no afl-mono" id="afl-ticket-no" style="color:#9bb4c7">TICKET No. 2026-0808-01</p>
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18"/></svg>PRIORITY TRADE</div>
        <h2 class="afl-h2">今日勝負するなら、この一本</h2>
        <div class="afl-pair">USD / JPY</div>
        <p class="afl-trade-lead" id="afl-trade-lead" style="color:#eef4fb">戻り売り ‒ ただし押し目を深追いしない</p>
        <div class="afl-trade-row">
          <div class="afl-trade-box afl-entry"><span>ENTRY</span><b id="afl-trade-entry">157.xx</b></div>
          <div class="afl-trade-box afl-tp"><span>TAKE PROFIT</span><b id="afl-trade-tp">156.xx</b></div>
          <div class="afl-trade-box afl-sl"><span>STOP LOSS</span><b id="afl-trade-sl">158.xx</b></div>
        </div>
        <a class="afl-summary-detail-btn" href="/fx_daily_analysis_trial/">今日の詳しい分析を見る <span>→</span></a>
        <a class="afl-live-chart-btn" href="/live-chart/">USD/JPY ライブチャートを見る <span>→</span></a>
        <a class="afl-live-chart-btn" href="/eurusd_daily_analysis/">EUR/USD の分析を見る <span>→</span></a>
        <a class="afl-live-chart-btn" href="/track-record/">AIシグナルの実績ログを見る <span>→</span></a>
        <p class="afl-summary-manual-note">このロジックは過去データでの検証を経て設計していますが、実際の運用成績は上記の実績ログでご確認いただけます。</p>
        <p class="afl-summary-manual-note">詳細記事は手動更新｜TOPのシグナルはGitHubから自動更新</p>
      </section>

      <section class="afl-note afl-full">
        <span class="afl-note-quote" aria-hidden="true">"</span>
        <span class="afl-note-label">AI所長のひとこと</span>
        <p id="afl-note-text">強い相場ほど、飛び乗らない。<br>158円突破そのものより、突破後にその水準を維持できるかを見る。</p>
      </section>

      <div class="afl-full afl-section-divider">
        <span class="afl-section-num">3</span>
        <span class="afl-section-title">理由（材料）</span>
        <span class="afl-section-sub">なぜその判断なのか</span>
      </div>

      <section class="afl-card afl-full" id="afl-macro-monitor">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/></svg>USD/JPY MARKET DRIVERS</div>
        <h2 class="afl-h2">ドル円・市場環境モニター</h2>
        <p class="afl-kpi-note" style="margin:2px 0 10px">2つのドルストレート、安全資産、原油価格を同時監視。すべてTradingViewの1時間足です。</p>
        <details class="afl-macro-toggle">
          <summary><span>関連市場チャート4画面を開く／閉じる</span></summary>
          <div class="afl-macro-grid">
            <div class="afl-macro-chart">
              <div class="afl-macro-head"><strong>USD/JPY</strong><span>リアルタイムのローソク足（本家TradingView）</span></div>
              <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div>
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>{"autosize":true,"symbol":"FX_IDC:USDJPY","interval":"5","timezone":"Asia/Tokyo","theme":"light","style":"1","locale":"ja","hide_side_toolbar":true,"allow_symbol_change":false,"save_image":false,"calendar":false,"support_host":"https://www.tradingview.com"}</script>
              </div>
            </div>
            <div class="afl-macro-chart">
              <div class="afl-macro-head"><strong>EUR/USD</strong><span>ドル強弱</span></div>
              <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div>
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>{"autosize":true,"symbol":"FX_IDC:EURUSD","interval":"60","timezone":"Asia/Tokyo","theme":"light","style":"1","locale":"ja","hide_side_toolbar":true,"allow_symbol_change":false,"save_image":false,"calendar":false,"support_host":"https://www.tradingview.com"}</script>
              </div>
            </div>
            <div class="afl-macro-chart">
              <div class="afl-macro-head"><strong>GBP/USD</strong><span>ドル強弱の再確認</span></div>
              <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div>
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>{"autosize":true,"symbol":"FX_IDC:GBPUSD","interval":"60","timezone":"Asia/Tokyo","theme":"light","style":"1","locale":"ja","hide_side_toolbar":true,"allow_symbol_change":false,"save_image":false,"calendar":false,"support_host":"https://www.tradingview.com"}</script>
              </div>
            </div>
            <div class="afl-macro-chart">
              <div class="afl-macro-head"><strong>GOLD</strong><span>安全資産・実質金利</span></div>
              <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div>
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>{"autosize":true,"symbol":"TVC:GOLD","interval":"60","timezone":"Asia/Tokyo","theme":"light","style":"1","locale":"ja","hide_side_toolbar":true,"allow_symbol_change":false,"save_image":false,"calendar":false,"support_host":"https://www.tradingview.com"}</script>
              </div>
            </div>
            <div class="afl-macro-chart">
              <div class="afl-macro-head"><strong>WTI原油</strong><span>インフレ・資源価格</span></div>
              <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div>
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>{"autosize":true,"symbol":"TVC:USOIL","interval":"60","timezone":"Asia/Tokyo","theme":"light","style":"1","locale":"ja","hide_side_toolbar":true,"allow_symbol_change":false,"save_image":false,"calendar":false,"support_host":"https://www.tradingview.com"}</script>
              </div>
            </div>
          </div>
        </details>
      </section>

      <section class="afl-card afl-full">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19V5"/><path d="M20 19V5"/><path d="M4 12h16"/></svg>CURRENCY STRENGTH</div>
        <h2 class="afl-h2">通貨強弱（簡易版）</h2>
        <p class="afl-kpi-note" style="margin:2px 0 10px">主要7通貨ペアの直近1時間足24本（約1日）の騰落率を、±2.5%を±100とする固定スケールで-100〜+100のスコアに変換して表示しています（「その日の最大変動」を基準にする相対スケールではないため、静かな日に小さな変動が誇張されません）。USDは7ペア平均のため比較的安定した指標ですが、それ以外の通貨は1ペアのみからの簡易算出です。</p>
        <details class="afl-macro-toggle">
          <summary><span>通貨強弱バーを開く／閉じる</span></summary>
          <div class="afl-cs-list" id="afl-cs-list">
            <div class="afl-cs-row"><span class="afl-cs-code">‒</span><div class="afl-cs-bar-track"><div class="afl-cs-mid-line"></div></div><span class="afl-cs-value">読み込み中</span></div>
          </div>
        </details>
      </section>

      <section class="afl-card afl-half">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2 2 21h20L12 2Z"/><line x1="12" y1="9" x2="12" y2="14"/><circle cx="12" cy="17.5" r=".8" fill="currentColor"/></svg>INTERVENTION RISK</div>
        <div class="afl-kpi-big" id="afl-ir-big" style="font-size:28px">HIGH</div>
        <span class="afl-pill afl-high" id="afl-ir-pill">警戒レベル高</span>
        <p class="afl-kpi-note">価格だけでなく、上昇速度・要人発言・雇用統計後の値動きを重視。</p>
      </section>

      <section class="afl-card afl-half">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h4l3-8 4 16 3-8h4"/></svg>MARKET MODE</div>
        <div class="afl-kpi-big" id="afl-mm-big" style="font-size:22px">EVENT DRIVEN</div>
        <p class="afl-kpi-note" id="afl-mm-note">重要指標の結果待ちで振れやすく、方向感よりイベント後の反応を優先する局面。</p>
      </section>

      <section class="afl-card afl-full">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M7 14l3-3 3 3 5-6"/></svg>TECHNICAL DASHBOARD</div>
        <h2 class="afl-h2">MACD・RSI・ボリンジャーバンド・サポート/レジスタンス（1時間足基準）</h2>
        <p class="afl-kpi-note" style="margin:2px 0 10px">売買判定には使用していない参考指標です。線形回帰チャネルの判定を補足する目的で表示しています。</p>
        <details class="afl-macro-toggle">
          <summary><span>MACD・RSI・BB・サポレジを開く／閉じる</span></summary>
          <div class="afl-tech-grid">
            <div class="afl-mini">
              <span>MACD</span>
              <b id="afl-macd-value">‒</b>
              <small id="afl-macd-state">データ取得中</small>
            </div>
            <div class="afl-mini">
              <span>RSI（14）</span>
              <b id="afl-rsi-value">‒</b>
              <small id="afl-rsi-state">データ取得中</small>
            </div>
            <div class="afl-mini">
              <span>ボリンジャーバンド（20・±2σ）</span>
              <b id="afl-bb-value">‒</b>
              <small id="afl-bb-state">データ取得中</small>
            </div>
            <div class="afl-mini">
              <span>サポート/レジスタンス</span>
              <b id="afl-sr-value">‒</b>
              <small id="afl-sr-state">直近50本の高安値</small>
            </div>
          </div>
        </details>
      </section>

      <section class="afl-card afl-full">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19h16"/><path d="M8 15v-6M12 15V9M16 15v-3"/></svg>MOVING AVERAGES</div>
        <h2 class="afl-h2">移動平均線（MA5/25/75/200）・パーフェクトオーダー</h2>
        <details class="afl-macro-toggle">
          <summary><span>移動平均線の詳細を開く／閉じる</span></summary>
          <table class="afl-ma-table">
            <thead><tr><th>指標</th><th>値</th><th>現在値との関係</th></tr></thead>
            <tbody id="afl-ma-body">
              <tr><td>データ取得中</td><td>‒</td><td>‒</td></tr>
            </tbody>
          </table>
          <p class="afl-kpi-note" style="margin:10px 0 0" id="afl-perfect-order-note">パーフェクトオーダー判定：データ取得中</p>
        </details>
      </section>

      <section class="afl-card afl-full">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18M3 12h18"/></svg>AI'S MARKET READ</div>
        <h2 class="afl-h2">この5項目、円安と円高どちらの材料？</h2>
        <details class="afl-macro-toggle">
          <summary><span>5項目の詳細を開く／閉じる</span></summary>
          <div class="afl-mr-list">
            <div class="afl-mr-row"><span class="afl-mr-label"><i class="afl-mkt-dot afl-up" id="afl-us10y-dot"></i>米10年債利回り<b id="afl-us10y-value" class="afl-mono" style="margin-left:6px;font-weight:700"></b>が<span id="afl-us10y-dir">上昇</span>中</span><span class="afl-mr-value" id="afl-us10y-note" style="color:var(--afl-bad)">→ 円安圧力（日米金利差拡大）</span></div>
            <div class="afl-mr-row"><span class="afl-mr-label"><i class="afl-mkt-dot afl-down" id="afl-jp10y-dot"></i>日本10年債利回り<b id="afl-jp10y-value" class="afl-mono" style="margin-left:6px;font-weight:700"></b>が<span id="afl-jp10y-dir">低下</span>中</span><span class="afl-mr-value" id="afl-jp10y-note" style="color:var(--afl-bad)">→ 円安圧力（円の魅力低下）</span></div>
            <div class="afl-mr-row"><span class="afl-mr-label"><i class="afl-mkt-dot afl-up" id="afl-dxy-dot"></i>ドル指数（DXY）<b id="afl-dxy-value" class="afl-mono" style="margin-left:6px;font-weight:700"></b>が<span id="afl-dxy-dir">上昇</span>中</span><span class="afl-mr-value" id="afl-dxy-note" style="color:var(--afl-bad)">→ 円安圧力（ドルが全面的に強い）</span></div>
            <div class="afl-mr-row"><span class="afl-mr-label"><i class="afl-mkt-dot afl-up" id="afl-wti-dot"></i>WTI原油が<span id="afl-wti-dir">上昇</span>中</span><span class="afl-mr-value" id="afl-wti-note" style="color:var(--afl-bad)">→ 円安圧力（資源高で日本の貿易収支が悪化）</span></div>
            <div class="afl-mr-row"><span class="afl-mr-label"><i class="afl-mkt-dot afl-flat" id="afl-gold-dot"></i>金（GOLD）<b id="afl-gold-value" class="afl-mono" style="margin-left:6px;font-weight:700"></b>が<span id="afl-gold-dir">横ばい</span>中</span><span class="afl-mr-value" id="afl-gold-note" style="color:var(--afl-muted)">→ 中立（横ばい）</span></div>
          </div>
        </details>
        <p class="afl-kpi-note" id="afl-market-read-summary" style="margin:10px 0 0">※ 5項目中集計中です。ただし個別材料であり、AIシグナルの結論（上部カード）とは別集計です。</p>
      </section>

      <section class="afl-card afl-full">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19h16"/><path d="M4 19V9l4-4 4 6 4-8 4 5v11"/></svg>MARKET CONTEXT</div>
        <h2 class="afl-h2">今の相場環境（シグナルに連動して自動更新）</h2>
        <p class="afl-event-note" id="afl-market-context">USD/JPYは現在157.75円付近で推移（直近1時間比-0.44%）。3個の時間足が上値の重さを示しており、戻り売りが優勢な地合い。米10年債利回りは低下基調、WTI原油は上昇基調で推移している。目先は上値の重い展開が想定され、高値を追わず戻りを待つスタンスが機能しやすい局面。※このまとめは実データから自動生成された定型解説です。個別の経済指標発表やニュース速報の内容までは反映していません。</p>
      </section>

      <section class="afl-card afl-full">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>LATEST NEWS</div>
        <h2 class="afl-h2">最新ニュース（Investing.com 為替関連）</h2>
        <p class="afl-kpi-note" style="margin:2px 0 10px">Investing.comのRSSフィードから取得した直近24時間以内の見出しをそのまま並べています。重要度による絞り込みはしていないため、USD/JPYと直接関係しないニュースが混ざることがあります。</p>
        <div class="afl-news-list" id="afl-news-list">
          <div class="afl-empty">読み込み中…</div>
        </div>
      </section>

      <div class="afl-full afl-section-divider">
        <span class="afl-section-num">4</span>
        <span class="afl-section-title">注意点</span>
        <span class="afl-section-sub">今夜・直近のイベント</span>
      </div>

      <section class="afl-card afl-full">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 2v4M16 2v4M3 9h18"/><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M12 9v5M12 17h.01"/></svg>PPI RESULT</div>
        <h2 class="afl-h2">⚠️ 結果：米7月PPI、総合は鈍化もコアは予想上回る</h2>
        <div class="afl-event">
          <div class="afl-event-time" style="font-size:22px;color:var(--afl-muted)">4.7%/4.2%</div>
          <div class="afl-event-body">
            <div class="afl-event-name">米生産者物価指数（PPI）7月分・8/13 21:30発表・結果</div>
            <div class="afl-event-stars">★★★★☆</div>
            <p class="afl-event-note">総合PPIは前年比+4.7%（予想+4.9%・前回+5.5%）、前月比0.0%（予想+0.2%・前回-0.1%）といずれも予想を下回り、インフレ鈍化を示す内容。一方コアPPIは前年比+4.2%で予想+4.1%をわずかに上回り、前月比も+0.2%（予想+0.3%は下回るが前回+0.4%からは鈍化）。総合とコアで方向感が分かれる「まちまち」の結果で、CPIに続きインフレ全体の鈍化基調自体は概ね維持されたとの見方が優勢。</p>
          </div>
        </div>
        <p class="afl-kpi-note" style="margin-top:10px">※この欄はWeb検索で確認した実際の発表結果（株探）をもとに手動で記載しています。速報段階の数値のため、後日の改定に注意してください。</p>
      </section>

      <section class="afl-card afl-full">
        <div class="afl-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 2v4M16 2v4M3 9h18"/><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M9 16l2 2 4-4"/></svg>CPI RESULT</div>
        <h2 class="afl-h2">🔥 結果：米7月CPI、予想通り3.4%（コア2.5%）で伸び鈍化</h2>
        <div class="afl-event">
          <div class="afl-event-time" style="font-size:26px;color:var(--afl-muted)">+3.4%</div>
          <div class="afl-event-body">
            <div class="afl-event-name">米消費者物価指数（CPI）7月分・8/12 21:30発表・結果</div>
            <div class="afl-event-stars">★★★★★</div>
            <p class="afl-event-note">総合CPIは前年比+3.4%（予想+3.4%・前回+3.5%）、前月比+0.1%（予想+0.1%・前回-0.4%）。コアCPIも前年比+2.5%（予想+2.5%・前回+2.6%、2021年3月以来の低水準）、前月比+0.2%（予想+0.2%・前回0.0%）と、いずれも市場予想通りでサプライズなし。ガソリン等燃料価格の伸び鈍化が主因（ガソリンは前年比+24.6%高いが上昇ペースは鈍化）。発表直後のドル円は158円台後半で上値の重い反応にとどまり、サプライズがなかったことと符合する。</p>
          </div>
        </div>
        <p class="afl-kpi-note" style="margin-top:10px">※この欄はWeb検索で確認した実際の発表結果（日本経済新聞・ザイFX!・株探）をもとに手動で記載しています。</p>
      </section>

    </div>

    <p class="afl-disclaimer" id="afl-disclaimer">本サイトは投資判断の参考情報を提供する研究サイトです。将来の成果を保証するものではありません。最終的な投資判断はご自身の責任で行ってください。<br>USD/JPY・WTI・GOLD等はTradingViewのウィジェットによりリアルタイムに近い形で自動表示されます（米10年債・日本10年債・DXYはTradingViewのチャート埋め込みに対応していない銘柄のため、GitHub Actions側で取得した実データを数値として表示しています）。AIシグナル（本カード群）は5分おきに、線形回帰チャネルに基づき自動計算されます（米10年債・日本10年債・WTIは元データが日足のため1日1回のみ更新。DXYはレート制限が無いため毎回取得）。MACD・RSI・移動平均線・ボリンジャーバンド・サポート/レジスタンスは参考情報であり、売買判定ロジックには使用していません。このページを開いたまま滞在中も、5分おきに最新の計算結果を自動で取得し直します。<br>なお、本シグナルロジック（5分・15分・1時間足の方向一致＋1分足の反発検出）は、2025年1月〜2026年7月の過去19ヶ月分の実データを用いたバックテストで勝率約7割という結果が得られています。ただしこれは1分足の反発タイミングを毎分判定できた場合の理論値であり、実際の自動更新は5分〜2時間間隔のため、実運用の成績はこれと異なる可能性があります。</p>
  </div>
</div>

<script>
/* ==== AIシグナル自動反映（Phase 2） ====
   GitHub Actionsが5分おきに計算して書き出す signal.json を、GitHub本体
   （raw.githubusercontent.com。CORS対応・キー不要）から直接取得し、
   下記のカード群にそのまま反映する。取得のたびにURL末尾へタイムスタンプを
   付けて、GitHub側のCDNキャッシュ（約5分）を毎回バイパスする。
   （以前はjsDelivr経由だったが、jsDelivrはキャッシュ更新に手動パージが
   必要な上パージ自体に頻度制限があり、反映が遅れる/止まる問題があったため
   raw.githubusercontent.comへ切り替えた）
   取得に失敗した場合は、静的に書かれている現在の表示のまま何も変えない
  （サイトが壊れることはない）。

   ▼設定必須▼
   GitHubリポジトリを作成したら、下の SIGNAL_JSON_URL を
   「あなたのGitHubユーザー名」「リポジトリ名」に書き換えてください。
   例）ユーザー名が anjo-fx、リポジトリ名が aifx-signal の場合：
   "https://raw.githubusercontent.com/anjo-fx/aifx-signal/main/signal.json"

   ▼WordPress側の仕様上の注意▼
   このスクリプト内では、JavaScriptの論理AND演算子（アンパサンド2つを
   連続で書く記法）を一切使っていません。WordPressのコンテンツフィルタ
   （wptexturize等）が、生のアンパサンド2連続をHTML実体参照に自動変換し、
   構文エラーでスクリプト全体が停止する事故が過去に発生したためです
  （ネストしたif文や != null で代替しています）。
   今後この中に条件式を追加する場合も、アンパサンド2連続の使用は避けること。

   ▼チャート部分について▼
   線形回帰チャネルの4枚のミニチャートは<canvas>にJSで自前描画している。
   TradingViewの埋め込みiframe等に差し替えないこと。差し替えると、
   SELL/BUY/WAIT/GATEのラベルは自動更新されたままなのに、チャートの中身は
   無関係な汎用インジケーターになり、ラベルとチャートが矛盾する事故になる
  （実際に一度発生し、復旧した経緯がある）。 */
;(function () {
  var SIGNAL_JSON_URL = "https://raw.githubusercontent.com/norithan88-cmyk/aifx-signal/main/signal.json";

  var lastGeneratedAtMs = null; // 直近成功したsignal.jsonのgenerated_at_utc（「最終更新」表示の再取得なしの更新に使う）

  function setText(id, text) {
    var el = document.getElementById(id);
    if (el) { if (text != null) el.textContent = text; }
  }

  // 見出しの公開時刻をJSTの「MM/DD HH:MM」表記にする。
  function formatNewsTime(iso) {
    if (!iso) return "";
    var d = new Date(iso);
    if (isNaN(d.getTime())) return "";
    var utcMs = d.getTime() + d.getTimezoneOffset() * 60000;
    var jst = new Date(utcMs + 9 * 60 * 60000);
    var mm = String(jst.getMonth() + 1).padStart(2, "0");
    var dd = String(jst.getDate()).padStart(2, "0");
    var hh = String(jst.getHours()).padStart(2, "0");
    var mi = String(jst.getMinutes()).padStart(2, "0");
    return mm + "/" + dd + " " + hh + ":" + mi;
  }

  function renderNews(items) {
    var listEl = document.getElementById("afl-news-list");
    if (!listEl) return;
    if (!items || !items.length) {
      listEl.innerHTML = '<div class="afl-empty">直近24時間以内のニュースを取得できていません。時間をおいて再読み込みしてください。</div>';
      return;
    }
    listEl.innerHTML = "";
    items.forEach(function (n) {
      var row = document.createElement("div");
      row.className = "afl-news-row";

      var sourceEl = document.createElement("span");
      sourceEl.className = "afl-news-source";
      sourceEl.textContent = n.source || "";

      var titleEl = document.createElement("a");
      titleEl.className = "afl-news-title";
      titleEl.href = n.link || "#";
      titleEl.target = "_blank";
      titleEl.rel = "noopener noreferrer";
      titleEl.textContent = n.title || "";

      var timeEl = document.createElement("span");
      timeEl.className = "afl-news-time";
      timeEl.textContent = formatNewsTime(n.published_at_utc);

      row.appendChild(sourceEl);
      row.appendChild(titleEl);
      row.appendChild(timeEl);
      listEl.appendChild(row);
    });
  }

  // "たった今" / "3分前" / "2時間前" のような相対時刻表示に変換する。
  function formatRelativeTime(ms) {
    var diffSec = Math.floor((Date.now() - ms) / 1000);
    if (diffSec < 60) return "たった今";
    var diffMin = Math.floor(diffSec / 60);
    if (diffMin < 60) return diffMin + "分前";
    var diffHour = Math.floor(diffMin / 60);
    if (diffHour < 24) return diffHour + "時間前";
    var diffDay = Math.floor(diffHour / 24);
    return diffDay + "日前";
  }

  // 閲覧者のブラウザのタイムゾーンに関わらず、常にJST（日本時間）のHH:MMを返す。
  function formatJstTime(date) {
    var utcMs = date.getTime() + date.getTimezoneOffset() * 60000;
    var jst = new Date(utcMs + 9 * 60 * 60000);
    var hh = String(jst.getHours()).padStart(2, "0");
    var mm = String(jst.getMinutes()).padStart(2, "0");
    return hh + ":" + mm;
  }

  // 「最終更新」欄を、直近成功したgenerated_at_utcを基準に再描画する。
  // 再取得(fetch)なしで呼べるので、5分おきの自動再取得の合間にも
  // setIntervalで随時呼び、「〇分前」表示を鮮度良く保つ。
  function renderLastUpdated() {
    var el = document.getElementById("afl-last-updated");
    if (!el || lastGeneratedAtMs == null) return;
    el.textContent = "最終更新: " + formatRelativeTime(lastGeneratedAtMs) + "（" + formatJstTime(new Date(lastGeneratedAtMs)) + " JST）";
    el.style.color = "";
  }

  // signal.jsonの取得自体に失敗した場合の表示。直前のシグナル本体はそのまま残しつつ、
  // 「最終更新」欄だけを失敗時刻付きで明示し、サイトが止まっていないか不安にさせない。
  function renderFetchFailed() {
    var el = document.getElementById("afl-last-updated");
    if (!el) return;
    el.textContent = "取得失敗（" + formatJstTime(new Date()) + " JST）‒ 5分後に再試行します";
    el.style.color = "var(--afl-bad)";
  }

  function fmtPrice(v) {
    return (v === null || v === undefined) ? "‒" : Number(v).toFixed(2);
  }

  function applyPillClass(el, variant) {
    if (!el) return;
    el.classList.remove("afl-go", "afl-sell", "afl-caution", "afl-high");
    el.classList.add(variant);
  }

  // ==== シグナル通知（ページを開いている間だけ、音＋ブラウザ通知） ====
  // 「オン」の状態はlocalStorageに保存し、ページ再訪問時も覚えている。
  // 直前に見たbiasもlocalStorageに保存し、WAIT→SELL/BUY等の「新規発生」の瞬間だけ鳴らす
  // （同じSELL/BUYが続いている間に毎回鳴ってしまうのを防ぐため）。
  var NOTIFY_PREF_KEY = "afl_notify_enabled";
  var NOTIFY_LAST_BIAS_KEY = "afl_notify_last_bias";

  function notifyEnabled() {
    try { return localStorage.getItem(NOTIFY_PREF_KEY) === "1"; } catch (e) { return false; }
  }

  function playSignalBeep() {
    try {
      var AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      var ctx = new AudioCtx();
      [880, 1175].forEach(function (freq, i) {
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.value = freq;
        var start = ctx.currentTime + i * 0.16;
        gain.gain.setValueAtTime(0.0001, start);
        gain.gain.exponentialRampToValueAtTime(0.3, start + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.0001, start + 0.3);
        osc.connect(gain).connect(ctx.destination);
        osc.start(start);
        osc.stop(start + 0.32);
      });
    } catch (e) { /* 音が鳴らせない環境では黙って諦める */ }
  }

  function updateNotifyButton() {
    var btn = document.getElementById("afl-notify-toggle");
    var statusEl = document.getElementById("afl-notify-status");
    if (!btn) return;
    var on = false;
    if (notifyEnabled()) {
      on = (typeof Notification === "undefined" || Notification.permission === "granted");
    }
    btn.classList.toggle("afl-notify-on", on);
    btn.textContent = on ? "🔔 シグナル通知：オン" : "🔔 シグナル通知をオンにする";
    if (statusEl) {
      if (typeof Notification !== "undefined") {
        if (Notification.permission === "denied") {
          statusEl.textContent = "ブラウザの通知がブロックされています。ブラウザの設定から許可すると使えます（音だけは鳴らせます）。";
        }
      }
    }
  }

  function setupNotifyToggle() {
    var btn = document.getElementById("afl-notify-toggle");
    if (!btn) return;
    updateNotifyButton();
    btn.addEventListener("click", function () {
      if (notifyEnabled()) {
        try { localStorage.setItem(NOTIFY_PREF_KEY, "0"); } catch (e) {}
        updateNotifyButton();
        return;
      }
      var enable = function () {
        try { localStorage.setItem(NOTIFY_PREF_KEY, "1"); } catch (e) {}
        updateNotifyButton();
      };
      if (typeof Notification === "undefined") { enable(); return; }
      if (Notification.permission === "granted" || Notification.permission === "denied") { enable(); return; }
      Notification.requestPermission().then(function () { enable(); });
    });
  }

  // signal.bias の変化を見て、新規にSELL/BUYへ変わった瞬間だけ音＋通知を出す。
  function checkSignalNotification(sig) {
    var bias = sig.bias;
    if (!bias) return;
    var lastBias = null;
    try { lastBias = localStorage.getItem(NOTIFY_LAST_BIAS_KEY); } catch (e) {}
    if (bias === lastBias) return;
    try { localStorage.setItem(NOTIFY_LAST_BIAS_KEY, bias); } catch (e) {}

    var isNewSignal = false;
    if (bias === "SELL" || bias === "BUY") {
      if (lastBias !== null) { isNewSignal = true; }
    }
    if (!isNewSignal) return;
    if (!notifyEnabled()) return;

    playSignalBeep();
    if (typeof Notification !== "undefined") {
      if (Notification.permission === "granted") {
        var label = bias === "SELL" ? "戻り売り" : "押し目買い";
        try {
          new Notification("AI FX研究所：" + label + "シグナル発生", {
            body: "USD/JPY " + label + "シグナルが発生しました。詳細をサイトで確認してください。",
          });
        } catch (e) {}
      }
    }
  }

  // AI'S MARKET READの各行（米10年債・日本10年債・DXY）共通の描画処理。
  // goodTrendには、その指標がその向きに動いたとき円高（good）になる方向を渡す
  // （米10年債・DXYは"down"、日本10年債は"up"）。
  // 戻り値: そのままdirection（"good"=円高圧力 / "bad"=円安圧力 / "flat"=中立）を返す。
  // updateMarketReadSummaryで各行の判定結果を集計するために使う。
  function renderMacroRow(prefix, latest, decimals, unit, trend, goodTrend, goodLabel, badLabel) {
    var valueEl = document.getElementById("afl-" + prefix + "-value");
    if (valueEl) { if (latest != null) valueEl.textContent = latest.toFixed(decimals) + unit; }
    var dotEl = document.getElementById("afl-" + prefix + "-dot");
    var dirEl = document.getElementById("afl-" + prefix + "-dir");
    var noteEl = document.getElementById("afl-" + prefix + "-note");
    var dirLabel = { up: "上昇", down: "低下" }[trend] || "横ばい";
    if (dirEl) dirEl.textContent = dirLabel;
    if (dotEl) dotEl.className = "afl-mkt-dot afl-" + (trend === "up" || trend === "down" ? trend : "flat");
    if (trend === "up" || trend === "down") {
      if (trend === goodTrend) {
        if (noteEl) { noteEl.textContent = goodLabel; noteEl.style.color = "var(--afl-good)"; }
        return "good";
      }
      if (noteEl) { noteEl.textContent = badLabel; noteEl.style.color = "var(--afl-bad)"; }
      return "bad";
    }
    if (noteEl) { noteEl.textContent = "→ 中立（横ばい）"; noteEl.style.color = "var(--afl-muted)"; }
    return "flat";
  }

  // AI'S MARKET READ下部の「◯項目中◯項目が円安方向」を、実際の判定結果から動的に組み立てる。
  function updateMarketReadSummary(results) {
    var el = document.getElementById("afl-market-read-summary");
    if (!el) return;
    var total = results.length;
    var bad = results.filter(function (r) { return r === "bad"; }).length;
    el.textContent = "※ " + total + "項目中" + bad + "項目が円安方向。ただし個別材料であり、AIシグナルの結論（上部カード）とは別集計です。";
  }

  function renderTechnical(technical) {
    if (!technical) return;

    var STATE_TEXT_COLOR = { good: "var(--afl-good)", bad: "var(--afl-bad)", muted: "var(--afl-muted)" };
    function paintState(id, tone) {
      var el = document.getElementById(id);
      if (el) { el.style.color = STATE_TEXT_COLOR[tone] || ""; }
    }

    var macd = technical.macd;
    if (macd) {
      var macdLabel = { BULLISH: "強気（MACD＞シグナル）", BEARISH: "弱気（MACD＜シグナル）", NEUTRAL: "中立" }[macd.state] || macd.state;
      var macdTone = { BULLISH: "good", BEARISH: "bad", NEUTRAL: "muted" }[macd.state] || "muted";
      if (macd.cross === "GOLDEN_CROSS") macdLabel = "ゴールデンクロス直後";
      if (macd.cross === "DEAD_CROSS") macdLabel = "デッドクロス直後";
      setText("afl-macd-value", macd.histogram);
      setText("afl-macd-state", macdLabel);
      paintState("afl-macd-state", macdTone);
    }

    var rsi = technical.rsi;
    if (rsi) {
      var rsiLabel = { OVERBOUGHT: "買われすぎ圏", OVERSOLD: "売られすぎ圏", NEUTRAL: "中立圏" }[rsi.state] || rsi.state;
      var rsiTone = { OVERSOLD: "good", OVERBOUGHT: "bad", NEUTRAL: "muted" }[rsi.state] || "muted";
      setText("afl-rsi-value", rsi.value);
      setText("afl-rsi-state", rsiLabel);
      paintState("afl-rsi-state", rsiTone);
    }

    var bb = technical.bollinger;
    if (bb) {
      var bbLabel = { UPPER_TOUCH: "上限バンドにタッチ", LOWER_TOUCH: "下限バンドにタッチ", INSIDE: "バンド内で推移" }[bb.state] || bb.state;
      var bbTone = { LOWER_TOUCH: "good", UPPER_TOUCH: "bad", INSIDE: "muted" }[bb.state] || "muted";
      setText("afl-bb-value", bb.lower + " 〜 " + bb.upper);
      setText("afl-bb-state", bbLabel + "（中心線 " + bb.mid + "）");
      paintState("afl-bb-state", bbTone);
    }

    var sr = technical.support_resistance;
    if (sr) {
      setText("afl-sr-value", sr.support + " 〜 " + sr.resistance);
    }

    var ma = technical.moving_averages;
    var maBody = document.getElementById("afl-ma-body");
    if (ma) {
      if (maBody) {
        var rows = [5, 25, 75, 200].map(function (p) {
          var v = ma["ma" + p];
          var rel = ma.price >= v ? "価格が上" : "価格が下";
          return "<tr><td>MA " + p + "</td><td class=\"afl-mono\">" + v + "</td><td>" + rel + "</td></tr>";
        });
        maBody.innerHTML = rows.join("");
      }
      var poLabel = { BULLISH: "強気の並び（短期＞中期＞長期＞超長期）", BEARISH: "弱気の並び（短期＜中期＜長期＜超長期）" }[ma.perfect_order] || "並びが交錯（明確なトレンドなし）";
      setText("afl-perfect-order-note", "パーフェクトオーダー判定：" + poLabel);
    }
  }

  function renderCurrencyStrength(list) {
    var wrap = document.getElementById("afl-cs-list");
    if (!wrap) return;
    if (!list) return;
    if (!list.length) return;
    // strength_scoreは既に±100を上限とする固定スケール済みの値なので、
    // その日ごとの最大変動を基準にする相対スケール(旧実装)は使わない。
    var html = list.map(function (item) {
      var score = item.strength_score != null ? item.strength_score : 0;
      var widthPct = Math.min(50, (Math.abs(score) / 100) * 50);
      var barClass = score >= 0 ? "afl-up" : "afl-down";
      var barStyle = "width:" + widthPct + "%";
      var valueColor = score > 0 ? "var(--afl-good)" : (score < 0 ? "var(--afl-bad)" : "var(--afl-muted)");
      return '<div class="afl-cs-row">' +
        '<span class="afl-cs-code">' + item.code + '</span>' +
        '<div class="afl-cs-bar-track"><div class="afl-cs-mid-line"></div><div class="afl-cs-bar ' + barClass + '" style="' + barStyle + '"></div></div>' +
        '<span class="afl-cs-value" style="color:' + valueColor + '">' + (score > 0 ? "+" : "") + score.toFixed(0) + "</span>" +
        '</div>';
    }).join("");
    wrap.innerHTML = html;
  }

  function render(data) {
    var sig = data.signal || {};
    checkSignalNotification(sig);
    var starsFull = Math.max(0, Math.min(5, sig.stars || 0));
    var starsEl = document.getElementById("afl-sig-stars");
    if (starsEl) {
      var filled = "★".repeat(starsFull);
      var empty = "★".repeat(5 - starsFull);
      starsEl.innerHTML = filled + (empty ? '<span class="afl-off">' + empty + "</span>" : "");
    }
    setText("afl-sig-pill", sig.bias_label);
    applyPillClass(document.getElementById("afl-sig-pill"),
      sig.bias === "SELL" ? "afl-sell" : sig.bias === "BUY" ? "afl-go" : "afl-caution");
    setText("afl-sig-note", "信頼度 " + (sig.confidence || "‒") + "% ‒ " + (sig.confidence >= 75 ? "慎重にGO" : sig.confidence >= 60 ? "小さくGO" : "見送り推奨"));
    var gaugeEl = document.getElementById("afl-sig-gauge");
    if (gaugeEl) { if (sig.confidence) gaugeEl.style.width = sig.confidence + "%"; }

    setText("afl-ir-big", data.intervention_risk);
    var irLabel = { HIGH: "警戒レベル高", MID: "やや警戒", LOW: "平常" }[data.intervention_risk] || data.intervention_risk;
    setText("afl-ir-pill", irLabel);
    applyPillClass(document.getElementById("afl-ir-pill"),
      data.intervention_risk === "HIGH" ? "afl-high" : data.intervention_risk === "MID" ? "afl-caution" : "afl-go");

    setText("afl-mm-big", data.market_mode);
    setText("afl-mm-note", data.market_mode_note);

    var trade = data.priority_trade || {};
    setText("afl-trade-lead", trade.lead);
    setText("afl-trade-entry", fmtPrice(trade.entry));
    setText("afl-trade-tp", fmtPrice(trade.take_profit));
    setText("afl-trade-sl", fmtPrice(trade.stop_loss));

    if (data.generated_at_utc) {
      var d = new Date(data.generated_at_utc);
      if (!isNaN(d.getTime())) {
        setText("afl-ticket-no", "TICKET No. " + d.getUTCFullYear() + String(d.getUTCMonth() + 1).padStart(2, "0") + String(d.getUTCDate()).padStart(2, "0") + "-AI");
        lastGeneratedAtMs = d.getTime();
        renderLastUpdated();
      }
    }

    setText("afl-note-text", data.commentary);
    setText("afl-market-context", data.market_context);
    renderNews(data.news);

    var macro = data.macro || {};
    var marketReadResults = [
      renderMacroRow("us10y", macro.us10y_latest, 2, "%", macro.us10y_trend, "down",
        "→ 円高圧力（日米金利差縮小）", "→ 円安圧力（日米金利差拡大）"),
      renderMacroRow("jp10y", macro.jp10y_latest, 3, "%", macro.jp10y_trend, "up",
        "→ 円高圧力（円の魅力上昇）", "→ 円安圧力（円の魅力低下）"),
      renderMacroRow("dxy", macro.dxy_latest, 2, "", macro.dxy_trend, "down",
        "→ 円高圧力（ドルが全面的に弱い）", "→ 円安圧力（ドルが全面的に強い）"),
      renderMacroRow("wti", null, 2, "", macro.wti_trend, "down",
        "→ 円高圧力（資源安で日本の貿易収支が改善）", "→ 円安圧力（資源高で日本の貿易収支が悪化）"),
      renderMacroRow("gold", macro.gold_latest, 2, "", macro.gold_trend, "up",
        "→ 円高圧力（安全資産需要で円も買われやすい）", "→ 円安圧力（リスク選好で質への逃避後退）"),
    ];
    updateMarketReadSummary(marketReadResults);

    renderTechnical(data.technical);
    renderCurrencyStrength(data.currency_strength);
    renderGlance(data);
    renderDailyAnalysis(data.daily_analysis);
  }

  // 「今日の結論」カードのひとまとまり表示（5項目の一覧＋3行要約）。
  // 新たな手動入力は増やさず、既存のsignal.jsonフィールドから組み立てる。
  var BIAS_ARROW = { SELL: "↓ 戻り売り優勢", BUY: "↑ 押し目買い優勢", WAIT: "→ 方向感なし" };
  var MODE_JA = { RANGE: "レンジ", TREND: "トレンド", "EVENT DRIVEN": "イベント待ち" };

  function renderGlance(data) {
    var sig = data.signal || {};
    var trade = data.priority_trade || {};
    var da = data.daily_analysis;

    setText("afl-glance-bias", BIAS_ARROW[sig.bias] || sig.bias_label || "‒");
    setText("afl-glance-confidence", (sig.confidence != null ? sig.confidence : "‒") + "%");
    setText("afl-glance-mode", MODE_JA[data.market_mode] || data.market_mode || "‒");
    setText("afl-glance-strategy", trade.lead || "‒");
    setText("afl-glance-focus", da ? (da.headline || "‒") : "本日の詳しい分析はまだ準備中です");
    setText("afl-ai-avatar-confidence", "信頼度 " + (sig.confidence != null ? sig.confidence : "‒") + "%");

    var avatarCardEl = document.querySelector(".afl-ai-avatar-card");
    if (avatarCardEl) {
      var accentVar = { SELL: "--afl-bad", BUY: "--afl-good", WAIT: "--afl-brass" }[sig.bias] || "--afl-brass";
      avatarCardEl.style.setProperty("--afl-avatar-accent", "var(" + accentVar + ")");
    }

    var lines = [];
    lines.push(sig.bias_label || "方向感なし");
    if (data.market_mode_note) lines.push(data.market_mode_note);
    if (da) {
      if (da.headline) lines.push(da.headline);
    } else if (data.market_context) {
      var ctx = data.market_context;
      lines.push(ctx.length > 70 ? ctx.slice(0, 70) + "…" : ctx);
    }

    var listEl = document.getElementById("afl-ai-summary-list");
    if (listEl) {
      listEl.innerHTML = "";
      lines.slice(0, 3).forEach(function (t) {
        var li = document.createElement("li");
        li.textContent = t;
        listEl.appendChild(li);
      });
    }
  }

  // 「今日のAI総合判定」カード内の開閉トグルに、daily_analysis.jsonの内容をその場で展開表示する。
  // 別ページ(/fx_daily_analysis_trial/)はチャート付きの詳細版として引き続き併存させる。
  function renderDailyAnalysis(da) {
    var emptyEl = document.getElementById("afl-analysis-empty");
    var contentEl = document.getElementById("afl-analysis-content");
    if (!da) {
      if (emptyEl) emptyEl.style.display = "";
      if (contentEl) contentEl.style.display = "none";
      return;
    }
    if (emptyEl) emptyEl.style.display = "none";
    if (contentEl) contentEl.style.display = "";

    setText("afl-analysis-updated", "更新: " + (da.updated_at_jst || "‒"));
    setText("afl-analysis-headline", da.headline || "");

    var adviceEl = document.getElementById("afl-analysis-advice");
    if (adviceEl) {
      adviceEl.innerHTML = "";
      (da.advice || []).forEach(function (para) {
        var p = document.createElement("p");
        p.textContent = para;
        adviceEl.appendChild(p);
      });
    }

    var scEl = document.getElementById("afl-analysis-scenarios");
    if (scEl) {
      scEl.innerHTML = "";
      (da.scenarios || []).forEach(function (sc) {
        var card = document.createElement("div");
        var colorClass = sc.color === "buy" ? "afl-buy" : sc.color === "sell" ? "afl-sell" : "afl-neutral";
        card.className = "afl-scenario " + colorClass;
        var head = document.createElement("div");
        head.className = "afl-scenario-head";
        var label = document.createElement("span");
        label.className = "afl-scenario-label";
        label.textContent = sc.label || "";
        var prob = document.createElement("span");
        prob.className = "afl-scenario-prob";
        prob.textContent = sc.probability != null ? sc.probability + "%" : "";
        head.appendChild(label);
        head.appendChild(prob);
        var body = document.createElement("p");
        body.className = "afl-scenario-body";
        body.textContent = sc.body || "";
        card.appendChild(head);
        card.appendChild(body);
        scEl.appendChild(card);
      });
    }

    var order = da.order_plan || {};
    var orderEl = document.getElementById("afl-analysis-order");
    if (orderEl) {
      orderEl.innerHTML =
        '<p class="afl-analysis-order-lead"></p>' +
        '<div class="afl-analysis-order-row">' +
          '<div class="afl-analysis-order-box afl-entry"><span>ENTRY</span><b></b></div>' +
          '<div class="afl-analysis-order-box afl-tp"><span>TAKE PROFIT</span><b></b></div>' +
          '<div class="afl-analysis-order-box afl-sl"><span>STOP LOSS</span><b></b></div>' +
        '</div>' +
        '<p class="afl-analysis-order-sub"></p>';
      orderEl.querySelector(".afl-analysis-order-lead").textContent = order.lead || "";
      var boxes = orderEl.querySelectorAll(".afl-analysis-order-box b");
      boxes[0].textContent = order.entry != null ? order.entry : "‒";
      boxes[1].textContent = order.take_profit != null ? order.take_profit : "‒";
      boxes[2].textContent = order.stop_loss != null ? order.stop_loss : "‒";
      orderEl.querySelector(".afl-analysis-order-sub").textContent = order.sub_note || "";
    }

    setText("afl-analysis-risk", da.risk_note || "");
  }

  var AUTO_REFRESH_MS = 5 * 60 * 1000; // 5分おきに自動で再取得する

  function loadSignal() {
    var bustedUrl = SIGNAL_JSON_URL + "?t=" + Date.now();
    fetch(bustedUrl, { cache: "no-store" })
      .then(function (res) { if (!res.ok) throw new Error("signal.json fetch failed: " + res.status); return res.json(); })
      .then(render)
      .catch(function () {
        /* 取得失敗時も、シグナル本体の表示はそのまま残す（直前の内容が消えて空欄になるよりまし）。
           ただし「最終更新」欄だけは、取得に失敗したことが分かるよう時刻付きで明示する。 */
        renderFetchFailed();
      });
  }

  setupNotifyToggle();
  loadSignal();
  setInterval(loadSignal, AUTO_REFRESH_MS);
  setInterval(renderLastUpdated, 30 * 1000); // 再取得を待たずに「〇分前」表示だけ鮮度を保つ

  // タブが非表示（他のタブに切り替え等）から復帰した瞬間にも、念のため即座に再取得する
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "visible") loadSignal();
  });

})();
</script>
