"""Inline SVG charts for the lab guides. Every number here was run against HORIZON.

Style follows the class charts: thin marks (<= 24px), 4px rounded data-ends square at the
baseline, hairline recessive grid, values in text tokens (never the series colour), one axis,
a hover/focus tooltip on every mark (data-tip="value|label"), and the table view alongside.
Colours come from CSS classes so light and dark themes each get their own validated steps.
"""
from html import escape


def _fmt(v, unit=""):
    if isinstance(v, float) and not v.is_integer():
        s = f"{v:,.1f}"
    else:
        s = f"{int(v):,}"
    return f"{s}{unit}"


def _ticks(vmax, n=4):
    raw = vmax / n
    mag = 10 ** (len(str(int(raw))) - 1) if raw >= 1 else 1
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if step >= raw:
            break
    top = step * n
    while top < vmax:
        top += step
    t = []
    v = 0
    while v <= top + 1e-9:
        t.append(v)
        v += step
    return t, top


def _bar_v(x, y0, w, h, r=4):
    """Column with rounded top, square at the baseline (y0 = baseline)."""
    if h <= 0:
        return ""
    r = min(r, h, w / 2)
    y = y0 - h
    return (f"M{x:.1f},{y0:.1f} L{x:.1f},{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} "
            f"L{x + w - r:.1f},{y:.1f} Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f} L{x + w:.1f},{y0:.1f} Z")


def _bar_h(x0, y, w, h, r=4):
    """Bar with rounded right end, square at the baseline (x0 = baseline)."""
    if w <= 0:
        return ""
    r = min(r, w, h / 2)
    x = x0 + w
    return (f"M{x0:.1f},{y:.1f} L{x - r:.1f},{y:.1f} Q{x:.1f},{y:.1f} {x:.1f},{y + r:.1f} "
            f"L{x:.1f},{y + h - r:.1f} Q{x:.1f},{y + h:.1f} {x - r:.1f},{y + h:.1f} L{x0:.1f},{y + h:.1f} Z")


def cols(data, title, unit="", w=680, h=300, hot=(), ghost=(), shade=None, ymax=None,
         notes=(), label_fmt=None, sub_labels=None, ytick_unit=None, label_only=None):
    """Vertical columns. data = [(label, value)]. shade = (x_from, x_to) in slot units."""
    L, R, T, B = 48, 12, 30, 46
    pw, ph = w - L - R, h - T - B
    vmax = ymax or max(v for _, v in data) * 1.08
    ticks, top = _ticks(vmax)
    n = len(data)
    slot = pw / n
    bw = min(26, slot * 0.46)
    out = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">']
    if shade:
        a, b, lab = shade
        out.append(f'<rect class="shade" x="{L + a * slot:.1f}" y="{T}" width="{(b - a) * slot:.1f}" height="{ph}" rx="4"/>')
        out.append(f'<text class="note" x="{L + (a + b) / 2 * slot:.1f}" y="{T - 10}" text-anchor="middle">{escape(lab)}</text>')
    for t in ticks:
        y = T + ph - ph * t / top
        out.append(f'<line class="grid" x1="{L}" x2="{w - R}" y1="{y:.1f}" y2="{y:.1f}"/>')
        tl = _fmt(t) if t < 1000 or t % 1000 else f"{int(t / 1000)}K"
        out.append(f'<text class="tick" x="{L - 8}" y="{y + 4:.1f}" text-anchor="end">{tl}{ytick_unit or ""}</text>')
    out.append(f'<line class="axis" x1="{L}" x2="{w - R}" y1="{T + ph}" y2="{T + ph}"/>')
    for i, (lab, v) in enumerate(data):
        cx = L + slot * (i + 0.5)
        x = cx - bw / 2
        bh = ph * v / top
        tip = f"{_fmt(v, unit)}|{lab}"
        if i in ghost:
            out.append(f'<rect class="b-ghost" x="{x:.1f}" y="{T + ph - ph * 0.12:.1f}" width="{bw:.1f}" height="{ph * 0.12:.1f}" rx="4" data-tip="{escape(tip)}" tabindex="0"/>')
        else:
            cls = "b-hot" if i in hot else "b-main"
            out.append(f'<path class="{cls} grow" style="--i:{i}" d="{_bar_v(x, T + ph, bw, bh)}" data-tip="{escape(tip)}" tabindex="0"/>')
        vlab = label_fmt(v) if label_fmt else _fmt(v, unit)
        vy = T + ph - (ph * 0.12 if i in ghost else bh) - 8
        if label_only is None or i in label_only:
            out.append(f'<text class="val{" hot" if i in hot else ""}" x="{cx:.1f}" y="{vy:.1f}" text-anchor="middle">{escape(vlab)}</text>')
        out.append(f'<text class="tick" x="{cx:.1f}" y="{T + ph + 18}" text-anchor="middle">{escape(lab)}</text>')
        if sub_labels and sub_labels[i]:
            out.append(f'<text class="note" x="{cx:.1f}" y="{T + ph + 34}" text-anchor="middle">{escape(sub_labels[i])}</text>')
    for (xslot, text, anchor) in notes:
        out.append(f'<text class="note" x="{L + xslot * slot:.1f}" y="{T + ph + 38}" text-anchor="{anchor}">{escape(text)}</text>')
    out.append("</svg>")
    return "".join(out)


def hbars(data, title, unit="", w=680, row=34, hot=(), ghost=(), xmax=None, label_w=150,
          value_fmt=None, ref=None, cls_main="b-main", good=()):
    """Horizontal bars. data = [(label, value, optional_note)]."""
    L, R, T, B = label_w, 150, 8, 26
    h = T + B + row * len(data)
    pw = w - L - R
    vmax = xmax or max(d[1] for d in data)
    out = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">']
    out.append(f'<line class="axis" x1="{L}" x2="{L}" y1="{T - 2}" y2="{T + row * len(data) + 2}"/>')
    bh = min(22, row * 0.58)
    for i, d in enumerate(data):
        lab, v = d[0], d[1]
        note = d[2] if len(d) > 2 else ""
        y = T + row * i + (row - bh) / 2
        bw = pw * v / vmax if vmax else 0
        tip = f"{value_fmt(v) if value_fmt else _fmt(v, unit)}|{lab}"
        out.append(f'<text class="lab" x="{L - 12}" y="{y + bh / 2 + 4.5:.1f}" text-anchor="end">{escape(lab)}</text>')
        if i in ghost or v == 0:
            out.append(f'<rect class="b-ghost" x="{L + 1}" y="{y:.1f}" width="{pw * 0.06:.1f}" height="{bh:.1f}" rx="4" data-tip="{escape(tip)}" tabindex="0"/>')
            tx = L + pw * 0.06 + 10
        else:
            c = "b-hot" if i in hot else ("b-good" if i in good else cls_main)
            out.append(f'<path class="{c} growx" style="--i:{i}" d="{_bar_h(L, y, bw, bh)}" data-tip="{escape(tip)}" tabindex="0"/>')
            tx = L + bw + 10
        vtxt = value_fmt(v) if value_fmt else _fmt(v, unit)
        out.append(f'<text class="val{" hot" if i in hot else ""}" x="{tx:.1f}" y="{y + bh / 2 + 4.5:.1f}">{escape(vtxt)}'
                   + (f'<tspan class="note" dx="8">{escape(note)}</tspan>' if note else "") + '</text>')
    if ref:
        rv, rl = ref
        rx = L + pw * rv / vmax
        out.append(f'<line class="ref-line" x1="{rx:.1f}" x2="{rx:.1f}" y1="{T - 4}" y2="{T + row * len(data) + 4}"/>')
        out.append(f'<text class="note" x="{rx:.1f}" y="{T + row * len(data) + 18}" text-anchor="middle">{escape(rl)}</text>')
    out.append("</svg>")
    return "".join(out)


def grouped_hbars(data, title, series, w=680, row=52, label_w=90, xmax=None):
    """Two series per category. data = [(label, v1, v2)]; series = [(name, cls), (name, cls)]."""
    L, R, T, B = label_w, 150, 6, 10
    h = T + B + row * len(data)
    pw = w - L - R
    vmax = xmax or max(max(d[1], d[2]) for d in data)
    bh = 16
    out = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">']
    out.append(f'<line class="axis" x1="{L}" x2="{L}" y1="{T}" y2="{T + row * len(data)}"/>')
    for i, (lab, a, b) in enumerate(data):
        y = T + row * i + (row - (bh * 2 + 2)) / 2
        out.append(f'<text class="lab" x="{L - 12}" y="{y + bh + 5:.1f}" text-anchor="end">{escape(lab)}</text>')
        for j, (v, (nm, cls)) in enumerate(((a, series[0]), (b, series[1]))):
            yy = y + j * (bh + 2)
            tip = f"{v:,}|{lab} · {nm}"
            if v == 0:
                out.append(f'<rect class="b-ghost" x="{L + 1}" y="{yy:.1f}" width="{pw * 0.05:.1f}" height="{bh}" rx="4" data-tip="{escape(tip)}" tabindex="0"/>')
                out.append(f'<text class="val hot" x="{L + pw * 0.05 + 10:.1f}" y="{yy + bh - 3.5:.1f}">0 {escape(nm.lower())}</text>')
            else:
                bw = pw * v / vmax
                out.append(f'<path class="{cls} growx" style="--i:{i * 2 + j}" d="{_bar_h(L, yy, bw, bh)}" data-tip="{escape(tip)}" tabindex="0"/>')
                out.append(f'<text class="val" x="{L + bw + 8:.1f}" y="{yy + bh - 3.5:.1f}">{v:,}</text>')
    out.append("</svg>")
    return "".join(out)


def stack1(parts, title, w=680, h=74):
    """One stacked bar. parts = [(label, value, cls)]. 2px surface gap between segments."""
    L, R = 0, 0
    total = sum(p[1] for p in parts)
    pw = w - L - R
    out = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">']
    x = L
    for i, (lab, v, cls) in enumerate(parts):
        sw = pw * v / total - (2 if i < len(parts) - 1 else 0)
        pct = 100 * v / total
        tip = f"{v:,} · {pct:.1f}%|{lab}"
        r = 4 if i == len(parts) - 1 else 0
        if r:
            d = _bar_h(x, 8, sw, 30)
            out.append(f'<path class="{cls}" d="{d}" data-tip="{escape(tip)}" tabindex="0"/>')
        else:
            out.append(f'<rect class="{cls}" x="{x:.1f}" y="8" width="{sw:.1f}" height="30" data-tip="{escape(tip)}" tabindex="0"/>')
        anchor = "start" if i == 0 else "end"
        tx = x + 4 if i == 0 else x + sw
        out.append(f'<text class="lab" x="{tx:.1f}" y="60" text-anchor="{anchor}">{escape(lab)} · {pct:.1f}%</text>')
        x += sw + 2
    out.append("</svg>")
    return "".join(out)


def lost_middle(w=680, h=230):
    """Illustrative U-curve: accuracy by where the key fact sits in a long prompt."""
    L, R, T, B = 48, 16, 20, 44
    pw, ph = w - L - R, h - T - B
    pts = [(0, .76), (.1, .68), (.25, .57), (.4, .52), (.5, .51), (.6, .53), (.75, .58), (.9, .67), (1, .74)]
    def xy(px, py):
        return L + pw * px, T + ph - ph * (py - .4) / .45
    d = "M" + " L".join(f"{xy(a, b)[0]:.1f},{xy(a, b)[1]:.1f}" for a, b in pts)
    out = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="Illustrative curve: models answer best when the key fact is at the start or the end of a long prompt, worst when it is in the middle.">']
    for t in (.4, .55, .7, .85):
        y = xy(0, t)[1]
        out.append(f'<line class="grid" x1="{L}" x2="{w - R}" y1="{y:.1f}" y2="{y:.1f}"/>')
    out.append(f'<line class="axis" x1="{L}" x2="{w - R}" y1="{T + ph}" y2="{T + ph}"/>')
    area = d + f" L{xy(1, .4)[0]:.1f},{xy(1, .4)[1]:.1f} L{xy(0, .4)[0]:.1f},{xy(0, .4)[1]:.1f} Z"
    out.append(f'<path d="{area}" fill="var(--c-main)" opacity=".1"/>')
    out.append(f'<path class="ln" d="{d}"/>')
    for (a, b), lab in (((0, .76), "start: rules"), ((.5, .51), "middle: gets lost"), ((1, .74), "end: question")):
        x, y = xy(a, b)
        out.append(f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="5" data-tip="{escape(lab)}|where the key fact sits" tabindex="0"/>')
        anchor = "start" if a == 0 else ("end" if a == 1 else "middle")
        out.append(f'<text class="lab" x="{x + (8 if a == 0 else -8 if a == 1 else 0):.1f}" y="{y - 12:.1f}" text-anchor="{anchor}">{escape(lab)}</text>')
    out.append(f'<text class="tick" x="{L}" y="{T + ph + 20}">start of prompt</text>')
    out.append(f'<text class="tick" x="{w - R}" y="{T + ph + 20}" text-anchor="end">end of prompt</text>')
    out.append(f'<text class="tick" x="{L - 8}" y="{T + 10}" text-anchor="end">↑</text>')
    out.append(f'<text class="note" x="{L + pw / 2:.1f}" y="{T + ph + 38}" text-anchor="middle">illustrative shape, after Liu et al., Lost in the Middle (TACL 2024)</text>')
    out.append("</svg>")
    return "".join(out)


Q8 = ["2024 Q1", "Q2", "Q3", "Q4", "2025 Q1", "Q2", "Q3", "Q4"]
Q8S = ["Q1 ’24", "Q2", "Q3", "Q4", "Q1 ’25", "Q2", "Q3", "Q4"]

CHARTS = {
    "s1-lost-middle": lambda: lost_middle(),
    "s2-prices": lambda: hbars(
        [("Opus 5.5", 20.0), ("Sonnet 5.5", 10.0), ("Haiku 5.5", 0.5, "40× cheaper than Opus")],
        "Price per million output tokens: Opus 5.5 $20, Sonnet 5.5 $10, Haiku 5.5 $0.50.",
        value_fmt=lambda v: f"${v:,.2f}" if v < 1 else f"${v:,.0f}", label_w=110, hot=(2,), row=40),
    "s2-consent-jp": lambda: hbars(
        [("18-24", 73.1), ("25-34", 69.5), ("35-44", 71.1), ("45-54", 70.2), ("55+", 69.7)],
        "Share of Japan consent records that allow marketing, by age band: about 70 percent in every band, 73.1 percent for 18-24.",
        unit="%", xmax=100, label_w=80, hot=(0,), value_fmt=lambda v: f"{v:.1f}%"),
    "s2-funnel": lambda: hbars(
        [("ZYN consumers", 609, "100%"), ("adopted", 507, "83.3%"), ("converted", 276, "45.3%"), ("retained 90d", 179, "64.9% of converters")],
        "Japan ZYN funnel: 609 consumers, 507 adopted, 276 converted, 179 retained.",
        label_w=130, good=(1, 2, 3)),
    "telemetry-jp": lambda: hbars(
        [("IQOS", 13052), ("VEEV", 7411), ("ZYN", 0, "no device, no telemetry")],
        "Japan device telemetry rows by product: IQOS 13,052, VEEV 7,411, ZYN none.",
        label_w=80, hot=()),
    "s3-campaigns": lambda: hbars(
        [("1 · IT IQOS Autumn Conversion Push", 74), ("2 · IT ZYN 2024", 0, "never tagged"), ("3 · ID IQOS 2024", 0, "never tagged"),
         ("4 · ID VEEV 2024", 0, "never tagged"), ("5 · ID ZYN 2024", 0, "never tagged")],
        "Attributed lifecycle events per campaign: campaign 1 in Italy has 74; campaigns 2 to 5 have none.",
        label_w=250, w=720),
    "s3-quarters": lambda: cols(
        list(zip(Q8, [3, 29, 19, 16, 10, 14, 17, 8])),
        "Indonesia VEEV conversions by quarter: 3, 29, 19, 16, 10, 14, 17, 8. The campaign window from 24 March to 23 May 2024 overlaps the jump from Q1 to Q2 2024; the data starts on 1 January 2024.",
        hot=(1,), shade=(0.92, 1.58, "campaign 4 window · 24 Mar – 23 May 2024"),
        notes=((0, "↑ data starts 1 Jan 2024", "start"),)),
    "s3-italy": lambda: cols(
        [("unattributed baseline", 13.5), ("post-campaign Jul–Dec 2025", 21.4), ("Q4 2025", 31.5)],
        "Italy IQOS conversion rate: unattributed baseline 13.5 percent; after the campaign, July to December 2025, 21.4 percent; Q4 2025 about 31.5 percent.",
        unit="%", ymax=35, hot=(1,), w=620, h=280, ytick_unit="%"),
    "s4-italy-bands": lambda: grouped_hbars(
        [("18-24", 249, 0), ("25-34", 594, 514), ("35-44", 570, 484), ("45-54", 353, 303), ("55+", 234, 194)],
        "Italy consumers and marketable consumers by age band: 18-24 has 249 consumers and 0 marketable.",
        [("Consumers", "b-dim"), ("Marketable", "b-good")]),
    "s4-under25": lambda: hbars(
        [("Indonesia", 0.0), ("Italy", 0.0), ("Japan", 73.05)],
        "Share of under-25 consent records that allow marketing: Indonesia 0, Italy 0, Japan 73.05 percent.",
        xmax=100, label_w=100, value_fmt=lambda v: f"{v:.2f}%", good=(2,)),
    "s4-sessions": lambda: cols(
        list(zip(Q8S, [27534, 69444, 101825, 123936, 137200, 139252, 137824, 112164])),
        "Japan device sessions by quarter, 2024 Q1 to 2025 Q4: rising to 139,252 in 2025 Q2, then 112,164 in 2025 Q4.",
        hot=(7,), label_fmt=lambda v: f"{v / 1000:.0f}K", w=420, h=260, label_only=(5, 7)),
    "s4-devices": lambda: cols(
        list(zip(Q8S, [348, 698, 956, 1171, 1292, 1329, 1315, 966])),
        "Japan devices reporting by quarter: peaking at 1,329 in 2025 Q2, then 966 in 2025 Q4.",
        hot=(7,), w=420, h=260, label_only=(5, 7)),
    "s4-coverage": lambda: stack1(
        [("tied to a consumer", 16320, "b-main"), ("anonymised", 4143, "b-hot")],
        "Japan telemetry rows: 16,320 tied to a consumer (79.8 percent), 4,143 anonymised (20.2 percent)."),
}
