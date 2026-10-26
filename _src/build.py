#!/usr/bin/env python3
"""Build the Project HORIZON Data Analyst lab guides into ../ (static, GitHub Pages ready).

    python3 _src/build.py          # writes index.html, session1-4.html, glossary.html

Pages live in _src/pages/*.html as three blocks: <!--HERO-->, <!--BRIEF--> (optional) and
<!--MAIN-->. Inside them, a few short tags expand into the full components:

    <prompt model="sonnet" note="…">raw text</prompt>      Claude Desktop prompt, copy button
    <sql note="…">raw SQL</sql>                             SQLTools block, highlighted, copy button
    <out label="…">raw text</out>                           an output / error block
    <predict id="s1-x" [opts="yes|no"] [ph="…"]>question</predict>
    <reveal id="s1-x" title="…" [nogut]>html</reveal>
    <chat [hints="a|b"]>text</chat>      <unmute>text</unmute>
    <stephead step="step1" n="1" eyebrow="…" mins="5 min" model="sonnet">Title|dek</stephead>
    {{CHART:name}}  {{ART:name}}  {{ART:name:prefix}}  {{ICON:name}}  {{DOTS}}

The table of contents is generated from elements carrying data-toc (plus data-toc-grp and
data-toc-sub).
"""
import json
import os
import re
import sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import art      # noqa: E402
import charts   # noqa: E402

SITE = "https://varoonsahgal.github.io/pmidataanalyst-labs/"

PAGES = [
    dict(key="s0", file="index.html", hue="s0", fx="embers", scene=True, nav="Start here",
         title="Start here", short="Start here",
         desc="Lab guides for the PMI Data Analyst Future Skills class: four sessions, one fictional warehouse (Project HORIZON), one rule. AI answers. Data decides. You sign."),
    dict(key="s1", file="session1.html", hue="s1", fx="tokens", nav="1", long="Mind-reader",
         title="Session 1 · Mind-reader not included", short="Mind-reader not included",
         desc="Session 1 · Prompt Engineering for Analytics (WA3899). What you don't say, it makes up. Ground the prompt, find the silent zero, build a reusable template."),
    dict(key="s2", file="session2.html", hue="s2", fx="rows", nav="2", long="Deepfake data",
         title="Session 2 · Deepfake data", short="Deepfake data",
         desc="Session 2 · Generative Analytics Engineering (WA3900). Realistic is not real. Plan on the premium model, prove it in the warehouse, produce on the thrifty model, then count."),
    dict(key="s3", file="session3.html", hue="s3", fx="percent", nav="3", long="Compared to what?",
         title="Session 3 · Compared to what?", short="Compared to what?",
         desc="Session 3 · Evidence-Based Reasoning (WA3901). No baseline, no claim. Turn a confident dashboard sentence into a hypothesis, test it, and rate the evidence."),
    dict(key="s4", file="session4.html", hue="s4", fx="stars", nav="4", long="The dog that didn't bark",
         title="Session 4 · The dog that didn't bark", short="The dog that didn't bark",
         desc="Session 4 · AI Judgment & Bias Awareness (WA3902). Read for what's missing. Confirm each suspicion in the warehouse, then validate, caveat or escalate."),
    dict(key="gl", file="glossary.html", hue="gl", fx="rows", nav="Glossary", title="Glossary", short="Glossary", short_mast=True,
         desc="Every term and acronym from the four PMI Data Analyst sessions, in plain English."),
]
NAV_DOT = {"s1": "#FF4A00", "s2": "#00C9A7", "s3": "#E8A320", "s4": "#5B86F0"}

# Instructor guides: one hub plus one guide per session. Built with guide_html(): noindex, their own
# nav, assets/guide.css on top of site.css, and never linked from the student pages.
GUIDES = [
    dict(key="i0", file="instructor.html", hue="s0", fx="embers", nav="Hub", short="Instructor hub",
         title="Instructor hub", student="index.html",
         pin="AI answers. Data decides. You sign. Every guide on this site serves that one sentence.",
         desc="Instructor guides for the PMI Data Analyst Future Skills class: the basics from zero, then one guide per session."),
    dict(key="i1", file="instructor-s1.html", hue="s1", fx="tokens", nav="S1", dot="s1", short="Session 1 guide",
         title="Session 1 instructor guide · Mind-reader not included", student="session1.html",
         pin="What you don't say, the model makes up. Your job is to say it, then check the number.",
         desc="Instructor guide for Session 1 (WA3899): the lab taught from zero, every number explained, a timed script and the fixes."),
    dict(key="i2", file="instructor-s2.html", hue="s2", fx="rows", nav="S2", dot="s2", short="Session 2 guide",
         title="Session 2 instructor guide · Deepfake data", student="session2.html",
         pin="Realistic is not real. Plan on the expensive model, prove the plan in the warehouse, let the cheap model type, then count.",
         desc="Instructor guide for Session 2 (WA3900): the lab taught from zero, every number explained, a timed script and the fixes."),
    dict(key="i3", file="instructor-s3.html", hue="s3", fx="percent", nav="S3", dot="s3", short="Session 3 guide",
         title="Session 3 instructor guide · Compared to what?", student="session3.html",
         pin="No baseline, no claim. If you can't say what a number is compared to, it isn't a finding yet.",
         desc="Instructor guide for Session 3 (WA3901): the lab taught from zero, every number explained, a timed script and the fixes."),
    dict(key="i4", file="instructor-s4.html", hue="s4", fx="stars", nav="S4", dot="s4", short="Session 4 guide",
         title="Session 4 instructor guide · The dog that didn't bark", student="session4.html",
         pin="Read for what's missing. AI output never warns you about its own gaps, so you find them and confirm each one in the warehouse.",
         desc="Instructor guide for Session 4 (WA3902): the lab taught from zero, every number explained, a timed script and the fixes."),
]

LANES = {"do": "Students do", "see": "They see", "mean": "It means", "say": "You say",
         "you": "You do", "watch": "Watch for"}

ICONS = {
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/><path d="M12 1v4M12 19v4M1 12h4M19 12h4"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5" stroke-linecap="round"/></svg>',
    "mic": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M8.5 21h7"/></svg>',
    "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "copy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/></svg>',
    "claude": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l1.6 6.2L19 4.6l-3.6 5.4L22 12l-6.6 1.9 3.6 5.5-5.4-3.6L12 22l-1.6-6.2L5 19.4l3.6-5.5L2 12l6.6-1.9L5 4.6l5.4 3.6z"/></svg>',
    "db": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/><path d="M4.5 5.5v13c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-13M4.5 12c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8"/></svg>',
    "out": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h10M4 18h7"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "down": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M6 13l6 6 6-6"/></svg>',
    "ext": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M9 7h8v8"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
    "theme": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 3a9 9 0 1 0 9 9 7 7 0 0 1-9-9z"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>',
    "paste": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="6" y="4" width="12" height="17" rx="2"/><path d="M9 4V3h6v1M9 10h6M9 14h4" stroke-linecap="round"/></svg>',
    "run": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15l12.5-7.5z"/></svg>',
    "read": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/></svg>',
}

MODELS = {
    "sonnet": ("sonnet", "Claude Desktop · Sonnet"),
    "opus": ("opus", "Claude Desktop · Opus (premium)"),
    "haiku": ("haiku", "Claude Desktop · Haiku (thrifty)"),
    "none": ("none", "SQLTools only · no model"),
    "any": ("sonnet", "Claude Desktop"),
}

# --------------------------------------------------------------------------- SQL highlighting
SQL_KW = set("""SELECT FROM WHERE AND OR NOT JOIN LEFT ON USING GROUP BY ORDER AS IN IS NULL DISTINCT
FILTER WITH CASE WHEN THEN ELSE END ROLLUP LIMIT DESC ASC DATE TRUE FALSE DROP TABLE IF EXISTS CREATE
INSERT INTO VALUES NUMERIC TEXT BOOLEAN""".split())
SQL_FN = set("count sum avg round date_trunc coalesce nullif bool_or min max".split())
TOKEN = re.compile(r"(--[^\n]*)|('(?:[^']|'')*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][A-Za-z_0-9]*)|(\s+)|(.)", re.S)


def hl_sql(src):
    out = []
    for m in TOKEN.finditer(src):
        com, st, num, word, ws, other = m.groups()
        if com:
            out.append(f'<span class="c">{escape(com)}</span>')
        elif st:
            out.append(f'<span class="s">{escape(st)}</span>')
        elif num:
            out.append(f'<span class="n">{num}</span>')
        elif word:
            if word.upper() in SQL_KW and (word.isupper() or word.lower() in ("true", "false")):
                out.append(f'<span class="k">{word}</span>')
            elif word.lower() in SQL_FN:
                out.append(f'<span class="f">{word}</span>')
            else:
                out.append(escape(word))
        else:
            out.append(escape(ws or other))
    return "".join(out)


def hl_prompt(src):
    s = escape(src)
    s = re.sub(r"\{\{([A-Z_]+)\}\}", r'<span class="ph">&#123;&#123;\1&#125;&#125;</span>', s)
    return s


def dedent(text):
    text = text.strip("\n")
    lines = text.split("\n")
    ind = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
    return "\n".join(l[ind:] for l in lines).rstrip()


def attrs(s):
    return dict(re.findall(r'([a-z-]+)="([^"]*)"', s)) | {k: "" for k in re.findall(r'\s([a-z-]+)(?=\s|$)', " " + re.sub(r'([a-z-]+)="[^"]*"', "", s))}


def code_block(kind, a, body):
    body = dedent(body)
    if kind == "prompt":
        cls, ic, where = "prompt", ICONS["claude"], MODELS.get(a.get("model", "any"), MODELS["any"])[1]
        html = hl_prompt(body)
        hint = a.get("note", "Paste into the chat")
    elif kind == "sql":
        cls, ic, where = "sql", ICONS["db"], "SQLTools · HORIZON"
        parts = re.split(r"[«»]", body)
        html = "".join(f'<span class="hl">{hl_sql(p)}</span>' if i % 2 else hl_sql(p) for i, p in enumerate(parts))
        hint = a.get("note", "Ctrl+E Ctrl+E to run")
    else:
        cls, ic, where = "out" + (" err" if "err" in a else ""), ICONS["out"], a.get("label", "Output")
        html = escape(body)
        hint = a.get("note", "")
    copy = "" if kind == "out" else f'<button type="button" class="copy" aria-label="Copy this block">{ICONS["copy"]}<span>Copy</span></button>'
    wrapcls = " nowrap" if "nowrap" in a else ""
    return (f'<div class="code {cls}{wrapcls}"><div class="code-h"><span class="where">{ic}{escape(where)}</span>'
            f'<span class="sp"></span><span class="hint">{escape(hint)}</span>{copy}</div><pre>{html}</pre></div>')


def expand(src):
    """Expand the short tags. Code bodies are lifted out first so nothing else touches them."""
    stash = []

    def keep(html):
        stash.append(html)
        return f"\x00{len(stash) - 1}\x00"

    src = re.sub(r"<(prompt|sql|out)((?:\s[^>]*)?)>(.*?)</\1>",
                 lambda m: keep(code_block(m.group(1), attrs(m.group(2) or ""), m.group(3))), src, flags=re.S)

    def predict(m):
        a = attrs(m.group(1))
        pid = a["id"]
        q = m.group(2).strip()
        if "opts" in a:
            btns = "".join(f'<button type="button" data-v="{escape(o)}" aria-pressed="false">{escape(o)}</button>' for o in a["opts"].split("|"))
            guess = f'<div class="guess"><div class="opts" role="group" aria-label="Your prediction">{btns}</div><span class="locked"><span></span></span></div>'
        else:
            ph = a.get("ph", "Your guess")
            guess = (f'<div class="guess"><label class="vh" for="g-{pid}">Your prediction</label>'
                     f'<input id="g-{pid}" type="text" inputmode="text" autocomplete="off" placeholder="{escape(ph)}">'
                     f'<button type="button">Lock it in</button><span class="locked"><span></span></span></div>')
        lbl = a.get("label", "Predict first · Gut vs Ground Truth")
        return (f'<div class="predict rise" data-p="{pid}"><span class="ico" aria-hidden="true">{ICONS["target"]}</span>'
                f'<span class="box-lbl">{escape(lbl)}</span><p class="q">{q}</p>{guess}'
                f'<p class="alsochat">Type it in the class chat too. Then run it.</p></div>')

    src = re.sub(r"<predict((?:\s[^>]*)?)>(.*?)</predict>", predict, src, flags=re.S)

    def reveal(m):
        a = attrs(m.group(1))
        p = f' data-p="{a["id"]}"' if a.get("id") else ""
        ng = " data-nogut" if "nogut" in a or not a.get("id") else ""
        title = a.get("title", "Reveal")
        return (f'<details class="reveal"{p}{ng}><summary><span class="eye" aria-hidden="true">{ICONS["eye"]}</span>'
                f'<span>{title}</span><span class="yourguess"></span></summary><div class="reveal-b">{m.group(2)}</div></details>')

    # reveals can nest charts but never other reveals
    src = re.sub(r"<reveal((?:\s[^>]*)?)>(.*?)</reveal>", reveal, src, flags=re.S)

    def chat(m):
        a = attrs(m.group(1) or "")
        hints = ""
        if a.get("hints"):
            hints = '<div class="hints">' + "".join(f"<span>{escape(h)}</span>" for h in a["hints"].split("|")) + "</div>"
        lbl = a.get("label", "Post in the chat")
        return (f'<div class="chatbox rise"><span class="ico" aria-hidden="true">{ICONS["chat"]}</span>'
                f'<span class="box-lbl">{escape(lbl)}</span><p>{m.group(2).strip()}</p>{hints}</div>')

    src = re.sub(r"<chat((?:\s[^>]*)?)>(.*?)</chat>", chat, src, flags=re.S)
    src = re.sub(r"<unmute>(.*?)</unmute>",
                 lambda m: (f'<div class="unmute rise"><span class="ico" aria-hidden="true">{ICONS["mic"]}</span>'
                            f'<span class="box-lbl">Unmute moment</span><p>{m.group(1).strip()}</p></div>'), src, flags=re.S)

    def stephead(m):
        a = attrs(m.group(1))
        title, _, dek = m.group(2).partition("|")
        model = a.get("model")
        mc = ""
        if model:
            k, label = MODELS[model]
            mc = f'<span class="model-chip {k}">{escape(label.split(" · ", 1)[-1] if model != "none" else "No model · SQLTools")}</span>'
        return (f'<header class="step"><div class="step-n" data-n="{a["n"]}" aria-hidden="true">{a["n"]}</div>'
                f'<div class="step-t"><span class="eyebrow">{a.get("eyebrow", "")}</span><h2>{title.strip()}</h2>'
                + (f"<p>{dek.strip()}</p>" if dek.strip() else "") +
                f'</div><div class="step-side"><span class="mins">{ICONS["clock"]}{escape(a.get("mins", ""))}</span>{mc}'
                f'<button type="button" class="donebtn" data-step="{a["step"]}" aria-pressed="false"><span class="box">{ICONS["check"]}</span><span class="t">Mark done</span></button></div></header>')

    src = re.sub(r"<stephead((?:\s[^>]*)?)>(.*?)</stephead>", stephead, src, flags=re.S)

    # instructor guides: walked-step lanes and the recurring "Back to the point" box
    def lane(m):
        k = m.group(1)
        label = attrs(m.group(2) or "").get("label", LANES[k])
        return f'<div class="lane {k}"><span class="k">{escape(label)}</span><div>{m.group(3).strip()}</div></div>'

    src = re.sub(r'<lane ([a-z]+)((?:\s[^>]*)?)>(.*?)</lane>', lane, src, flags=re.S)
    src = re.sub(r"<point>(.*?)</point>",
                 lambda m: f'<div class="point rise"><span class="k">Back to the point</span><p>{m.group(1).strip()}</p></div>',
                 src, flags=re.S)

    def tok(m):
        kind, name = m.group(1), m.group(2)
        if kind == "CHART":
            return charts.CHARTS[name]()
        if kind == "ICON":
            return ICONS[name]
        if kind == "ART":
            name, _, prefix = name.partition(":")
            svg = ART[name]()
            return art.prefix_ids(svg, prefix) if prefix else svg
        raise KeyError(m.group(0))

    src = re.sub(r"\{\{(CHART|ICON|ART):([a-z0-9:-]+)\}\}", tok, src)
    src = src.replace("{{DOTS}}", escape(json.dumps(FACE_DOTS, separators=(",", ":"))))
    src = re.sub("\x00(\\d+)\x00", lambda m: stash[int(m.group(1))], src)
    return src


FACE_DOTS = art.face_dots()
FACES_ALT = ("Two faces in profile, nose to nose: the left one drawn in teal dots (real), "
             "the right one its mirror image in orange pixels (synthetic).")
ART = {
    "s1": art.art_s1,
    "s2": lambda: f'<img src="images/faces-labelled.svg" alt="{FACES_ALT}" width="680" height="620">',
    "s2-nolabel": lambda: f'<img src="images/faces.svg" alt="{FACES_ALT}" width="680" height="620" loading="lazy">',
    "s3": art.art_s3,
    "s4": art.art_s4,
}


def build_toc(main):
    items = []
    for m in re.finditer(r'<(?:section|div|h3|header|article|aside)\b([^>]*\bdata-toc="[^"]*"[^>]*)>', main):
        a = attrs(m.group(1))
        if a.get("data-toc-grp"):
            items.append(f'<li class="grp">{escape(a["data-toc-grp"])}</li>')
        sub = "data-toc-sub" in a
        li = '<li class="sub">' if sub else "<li>"
        items.append(f'{li}<a href="#{a["id"]}"><span>{escape(a["data-toc"])}</span><span class="ok" aria-hidden="true">✓</span></a></li>')
    return "\n".join(items)


def page_html(p, blocks, prev, nxt):
    hero = expand(blocks.get("HERO", ""))
    brief = expand(blocks.get("BRIEF", ""))
    main = expand(blocks.get("MAIN", ""))
    toc = build_toc(main)
    steps = len(re.findall(r'class="donebtn"', main))
    nav = []
    for q in PAGES:
        cur = ' aria-current="page"' if q["key"] == p["key"] else ""
        if q["key"] in NAV_DOT:
            nav.append(f'<a href="{q["file"]}"{cur} data-collect="{q["key"]}" title="{escape(q["short"])}" style="--d:{NAV_DOT[q["key"]]}"><span class="dot"></span>Session {q["nav"]}'
                       f'<span class="lbl-long"> · {escape(q["long"])}</span><span class="done-mark" hidden>★</span></a>')
        else:
            nav.append(f'<a href="{q["file"]}"{cur}>{escape(q["nav"])}</a>')
    nav = "\n      ".join(nav)
    og = f'{SITE}images/og-{p["key"]}.jpg'
    url = SITE + ("" if p["file"] == "index.html" else p["file"])
    title = f'{p["title"]} · HORIZON analyst labs'
    tocblock = ""
    if toc:
        prog = (f'<div class="toc-prog"><div class="bar"><i></i></div><div class="txt"><span class="c">0 of {steps} steps</span><span>progress saved here</span></div></div>' if steps else "")
        tocblock = f'''<details class="toc" id="toc" open>
    <summary>On this page</summary>
    {prog}
    <ol>
{toc}
    </ol>
  </details>'''
    pager = []
    if prev:
        pager.append(f'<a class="pv" href="{prev["file"]}"><span class="k">← Previous</span><b>{escape(prev["short"])}</b></a>')
    else:
        pager.append("<span></span>")
    if nxt:
        pager.append(f'<a class="nx" href="{nxt["file"]}"><span class="k">Next →</span><b>{escape(nxt["short"])}</b></a>')
    pager = f'<nav class="pager" aria-label="Previous and next guide">{"".join(pager)}</nav>'
    mast_cls = "mast scene" if p.get("scene") else ("mast short" if p.get("short_mast") else "mast")
    if blocks.get("BRIEF", "").strip():
        mast_cls += " has-brief"
    fx = f'<canvas class="mast-fx" data-fx="{p["fx"]}" aria-hidden="true"></canvas>' if p.get("fx") else ""
    briefblock = f'<section class="brief" aria-label="Mission brief"><div class="brief-in">{brief}</div></section>' if brief.strip() else ""
    frame_cls = "frame" if toc else "frame notoc"
    return f'''<!doctype html>
<html lang="en" class="no-js hue-{p["hue"]}" data-page="{p["key"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(p["desc"])}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#0C2040">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Project HORIZON · Data Analyst lab guides">
<meta property="og:title" content="{escape(p["title"])}">
<meta property="og:description" content="{escape(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og}">
<script>try{{var t=localStorage.getItem('pmi-da-theme');if(/[?&]dark/.test(location.search))t='dark';if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Mono:ital,wght@0,400;0,500;1,400&display=swap">
<link rel="stylesheet" href="assets/site.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230C2040'/%3E%3Ccircle cx='16' cy='19' r='8' fill='%23FF4A00'/%3E%3Crect x='4' y='19' width='24' height='9' fill='%230C2040'/%3E%3Crect x='6' y='20' width='20' height='2' rx='1' fill='%2300C9A7'/%3E%3C/svg%3E">
</head>
<body>
<a class="skip" href="#main">Skip to the guide</a>
<div id="readbar" aria-hidden="true"></div>
<header class="topbar">
  <div class="topbar-in">
    <a class="brand" href="index.html"><svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#FF4A00" fill-opacity=".14"/><circle cx="16" cy="19" r="8" fill="#FF4A00"/><rect x="4" y="19" width="24" height="9" fill="#0C2040"/><rect x="6" y="20" width="20" height="2" rx="1" fill="#00C9A7"/></svg>Project HORIZON <span>· analyst labs</span></a>
    <nav class="nav" aria-label="Lab guides">
      {nav}
    </nav>
    <div class="tools">
      <span class="gut-chip" title="Your own Gut vs Ground Truth score across all four sessions. Saved only in this browser."><span class="lbl">Gut vs Truth</span><span class="g">Gut <b>0</b></span><span class="t">Truth <b>0</b></span></span>
      <button class="iconbtn" id="theme" type="button" aria-label="Switch theme">{ICONS["theme"]}</button>
      <button class="iconbtn menu-btn" type="button" aria-label="Menu" aria-expanded="false">{ICONS["menu"]}</button>
    </div>
  </div>
</header>

<section class="{mast_cls}">
  {fx}
  <div class="mast-in">
{hero}
  </div>
  <a class="scroll-cue" href="#main">Scroll</a>
</section>
{briefblock}

<div class="{frame_cls}">
  {tocblock}
  <main id="main" tabindex="-1">
{main}
{pager}
  </main>
</div>

<footer class="foot">
  <div class="foot-in">
    <div>
      <p class="rule-big"><span>AI answers.</span> <span>Data decides.</span> <span>You sign.</span></p>
      <p>Lab guides for the PMI DI&amp;A Future Skills Data Analyst class: WA3899 · WA3900 · WA3901 · WA3902. Project HORIZON is a fictional, training-only data estate; no real consumer data appears anywhere in these guides.</p>
      <small>Your guesses, score, progress and cards are saved only in this browser. <button type="button" class="linkbtn" data-reset>Reset them</button></small>
    </div>
    <nav aria-label="All guides">
      {"".join(f'<a href="{q["file"]}">{escape(q["title"])}</a>' for q in PAGES)}
    </nav>
  </div>
</footer>
<div id="tip" role="tooltip" aria-hidden="true"></div>
<script src="assets/site.js" defer></script>
</body>
</html>
'''


def guide_html(p, blocks, prev, nxt):
    """An instructor guide: same shell as a lab page, with its own nav, the point pinned on the TOC, noindex."""
    hero = expand(blocks.get("HERO", ""))
    main = expand(blocks.get("MAIN", ""))
    toc = build_toc(main)
    nav = []
    for q in GUIDES:
        cur = ' aria-current="page"' if q["key"] == p["key"] else ""
        if q.get("dot"):
            nav.append(f'<a href="{q["file"]}"{cur} style="--d:{NAV_DOT[q["dot"]]}"><span class="dot"></span>{escape(q["nav"])}'
                       f'<span class="lbl-long"> guide</span></a>')
        else:
            nav.append(f'<a href="{q["file"]}"{cur}>{escape(q["short"])}</a>')
    nav.append(f'<a href="{p["student"]}" class="stu">Student page ↗</a>')
    nav = "\n      ".join(nav)
    title = f'{p["title"]} · HORIZON analyst labs'
    og = f'{SITE}images/og-{p["hue"]}.jpg'
    pager = []
    if prev:
        pager.append(f'<a class="pv" href="{prev["file"]}"><span class="k">← Previous</span><b>{escape(prev["short"])}</b></a>')
    else:
        pager.append("<span></span>")
    if nxt:
        pager.append(f'<a class="nx" href="{nxt["file"]}"><span class="k">Next →</span><b>{escape(nxt["short"])}</b></a>')
    pager = f'<nav class="pager" aria-label="Previous and next guide">{"".join(pager)}</nav>'
    switch = "".join(
        f'<a href="{q["file"]}"' + (' aria-current="page"' if q["key"] == p["key"] else "") + f'>{escape(q["short"])}</a>'
        for q in GUIDES)
    hero = hero.replace("{{GUIDES}}", f'<nav class="guides" aria-label="Instructor guides">{switch}'
                                      f'<a href="{p["student"]}" class="stu">Student page ↗</a></nav>')
    return f'''<!doctype html>
<html lang="en" class="no-js hue-{p["hue"]} guide" data-page="{p["key"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(p["desc"])}">
<meta name="robots" content="noindex">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#0C2040">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Project HORIZON · Data Analyst instructor guides">
<meta property="og:title" content="{escape(p["title"])}">
<meta property="og:description" content="{escape(p["desc"])}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<script>try{{var t=localStorage.getItem('pmi-da-theme');if(/[?&]dark/.test(location.search))t='dark';if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Mono:ital,wght@0,400;0,500;1,400&display=swap">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/guide.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230C2040'/%3E%3Ccircle cx='16' cy='19' r='8' fill='%23FF4A00'/%3E%3Crect x='4' y='19' width='24' height='9' fill='%230C2040'/%3E%3Crect x='6' y='20' width='20' height='2' rx='1' fill='%2300C9A7'/%3E%3C/svg%3E">
</head>
<body>
<a class="skip" href="#main">Skip to the guide</a>
<div id="readbar" aria-hidden="true"></div>
<header class="topbar">
  <div class="topbar-in">
    <a class="brand" href="instructor.html"><svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#FF4A00" fill-opacity=".14"/><circle cx="16" cy="19" r="8" fill="#FF4A00"/><rect x="4" y="19" width="24" height="9" fill="#0C2040"/><rect x="6" y="20" width="20" height="2" rx="1" fill="#00C9A7"/></svg>Project HORIZON <span>· instructor</span></a>
    <nav class="nav" aria-label="Instructor guides">
      {nav}
    </nav>
    <div class="tools">
      <button class="iconbtn" id="theme" type="button" aria-label="Switch theme">{ICONS["theme"]}</button>
      <button class="iconbtn menu-btn" type="button" aria-label="Menu" aria-expanded="false">{ICONS["menu"]}</button>
    </div>
  </div>
</header>

<section class="mast">
  <canvas class="mast-fx" data-fx="{p["fx"]}" aria-hidden="true"></canvas>
  <div class="mast-in">
{hero}
  </div>
  <a class="scroll-cue" href="#main">Scroll</a>
</section>

<div class="frame">
  <details class="toc" id="toc" open>
    <summary>On this page</summary>
    <div class="pin"><b>The point</b>{escape(p["pin"])}</div>
    <ol>
{toc}
    </ol>
  </details>
  <main id="main" tabindex="-1">
{main}
{pager}
  </main>
</div>

<footer class="foot">
  <div class="foot-in">
    <div>
      <p class="rule-big"><span>AI answers.</span> <span>Data decides.</span> <span>You sign.</span></p>
      <p>Instructor guides for the PMI DI&amp;A Future Skills Data Analyst class: WA3899 · WA3900 · WA3901 · WA3902. Not linked from the student pages and hidden from search engines, but public to anyone who has the link. Project HORIZON is a fictional, training-only data estate.</p>
    </div>
    <nav aria-label="All instructor guides">
      {"".join(f'<a href="{q["file"]}">{escape(q["title"])}</a>' for q in GUIDES)}
      <a href="index.html">Student site</a>
    </nav>
  </div>
</footer>
<div id="tip" role="tooltip" aria-hidden="true"></div>
<script src="assets/site.js" defer></script>
</body>
</html>
'''


def split_blocks(text):
    blocks = {}
    for m in re.finditer(r"<!--(HERO|BRIEF|MAIN)-->(.*?)(?=<!--(?:HERO|BRIEF|MAIN)-->|\Z)", text, re.S):
        blocks[m.group(1)] = m.group(2)
    return blocks


def write_images():
    """The static halftone faces, shared by the cards, the start page and the no-JS fallback."""
    for name, labels in (("faces.svg", False), ("faces-labelled.svg", True)):
        svg = art.art_s2_static(FACE_DOTS, labels=labels).replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        with open(os.path.join(OUT, "images", name), "w", encoding="utf-8") as f:
            f.write(svg)


def main():
    write_images()
    order = [p for p in PAGES if p["key"] != "gl"]
    for i, p in enumerate(PAGES):
        src = os.path.join(HERE, "pages", p["key"] + ".html")
        if not os.path.exists(src):
            print("skip (no source yet):", p["key"])
            continue
        blocks = split_blocks(open(src, encoding="utf-8").read())
        if p["key"] == "gl":
            prev, nxt = PAGES[4], None
        else:
            j = order.index(p)
            prev = order[j - 1] if j > 0 else None
            nxt = order[j + 1] if j + 1 < len(order) else PAGES[5]
        html = page_html(p, blocks, prev, nxt)
        with open(os.path.join(OUT, p["file"]), "w", encoding="utf-8") as f:
            f.write(html)
        left = re.findall(r"<(?:prompt|sql|predict|reveal|chat|unmute|stephead)\b|\{\{[A-Z]+:", html)
        print(f"{p['file']:16} {len(html) // 1024:4} KB" + (f"   UNEXPANDED: {left}" if left else ""))
    for i, p in enumerate(GUIDES):
        src = os.path.join(HERE, "pages", p["key"] + ".html")
        if not os.path.exists(src):
            print("skip (no source yet):", p["key"])
            continue
        blocks = split_blocks(open(src, encoding="utf-8").read())
        prev = GUIDES[i - 1] if i > 0 else None
        nxt = GUIDES[i + 1] if i + 1 < len(GUIDES) else None
        html = guide_html(p, blocks, prev, nxt)
        with open(os.path.join(OUT, p["file"]), "w", encoding="utf-8") as f:
            f.write(html)
        left = re.findall(r"<(?:prompt|sql|predict|reveal|chat|unmute|stephead|lane|point)\b|\{\{[A-Z]+[:}]", html)
        print(f"{p['file']:20} {len(html) // 1024:4} KB" + (f"   UNEXPANDED: {left}" if left else ""))


if __name__ == "__main__":
    main()
