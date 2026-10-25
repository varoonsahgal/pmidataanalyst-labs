"""Hero art for the four session pages, drawn in code so it stays crisp, themable and tiny.

Each function returns an inline <svg> string. The builder inlines it into the page (so it
uses the page fonts) and, for cards, re-prefixes the ids so two copies can share a page.
"""
import math
import random
import re

MONO = "DM Mono, ui-monospace, monospace"
SANS = "Space Grotesk, system-ui, sans-serif"


# --------------------------------------------------------------------------- Session 1
def art_s1():
    """An LLM sold in a box. The sticker says what isn't in it."""
    # front face 130..430 x 160..500, depth offset (+86, -56)
    bar = []
    x = 150
    rnd = random.Random(4)
    while x < 232:
        w = rnd.choice([1, 1, 2, 3])
        bar.append(f'<rect x="{x}" y="448" width="{w}" height="30" fill="#DCE6F5" opacity=".75"/>')
        x += w + rnd.choice([1, 2, 2, 3])
    bar = "".join(bar)

    def burst(cx, cy, ro, ri, n):
        pts = []
        for i in range(n * 2):
            r = ro if i % 2 == 0 else ri
            a = math.pi * i / n - math.pi / 2
            pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
        return " ".join(pts)

    def bubble(x, y, w, text, cls, dots):
        d = "".join(f'<circle cx="{dx}" cy="{dy}" r="{r}" fill="rgba(255,138,76,.55)"/>' for dx, dy, r in dots)
        return (f'<g class="s1-float {cls}">{d}<rect x="{x}" y="{y}" width="{w}" height="34" rx="17" '
                f'fill="rgba(8,26,53,.82)" stroke="#FF8A4C" stroke-opacity=".7" stroke-dasharray="4 4"/>'
                f'<text x="{x + w / 2}" y="{y + 22}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#FFD0B8">{text}</text></g>')

    return f'''<svg class="art art-s1" viewBox="0 0 640 560" role="img" aria-labelledby="s1-art-t">
<title id="s1-art-t">A large language model sold in a box. A sticker on it reads "Mind-reader not included". The side of the box says "What you don't say, it makes up", a tag says "Assumptions sold separately", and question bubbles float around it: timeframe? adoption = ? consent rule? which table?</title>
<style>
.art-s1 .s1-float {{ animation: s1f 6s ease-in-out infinite; }}
.art-s1 .s1-float.b2 {{ animation-delay: -1.5s; animation-duration: 7s; }}
.art-s1 .s1-float.b3 {{ animation-delay: -3s; animation-duration: 6.5s; }}
.art-s1 .s1-float.b4 {{ animation-delay: -4.2s; animation-duration: 7.5s; }}
@keyframes s1f {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
.art-s1 .s1-sticker {{ transform-box: fill-box; transform-origin: center; animation: s1w 4.5s ease-in-out infinite; }}
@keyframes s1w {{ 0%,100% {{ transform: rotate(-14deg) scale(1); }} 50% {{ transform: rotate(-9deg) scale(1.04); }} }}
.art-s1 .s1-cur {{ animation: s1b 1s steps(1) infinite; }}
@keyframes s1b {{ 50% {{ opacity: 0; }} }}
.art-s1 .s1-tag {{ transform-box: view-box; transform-origin: 131px 200px; animation: s1t 5s ease-in-out infinite; }}
@keyframes s1t {{ 0%,100% {{ transform: rotate(0deg); }} 50% {{ transform: rotate(4deg); }} }}
.art-s1 .s1-skel {{ animation: s1s 2.4s ease-in-out infinite; }}
@keyframes s1s {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: .8; }} }}
</style>
<defs>
  <linearGradient id="s1-front" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A4278"/><stop offset="1" stop-color="#0E2A52"/></linearGradient>
  <linearGradient id="s1-top" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#2B5A9A"/><stop offset="1" stop-color="#3A6DB0"/></linearGradient>
  <linearGradient id="s1-side" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0D2648"/><stop offset="1" stop-color="#071A33"/></linearGradient>
  <linearGradient id="s1-win" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#061226"/><stop offset="1" stop-color="#11284C"/></linearGradient>
  <linearGradient id="s1-band" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF4A00"/><stop offset="1" stop-color="#FF7A2A"/></linearGradient>
  <radialGradient id="s1-glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FF4A00" stop-opacity=".42"/><stop offset=".6" stop-color="#FF4A00" stop-opacity=".1"/><stop offset="1" stop-color="#FF4A00" stop-opacity="0"/></radialGradient>
  <radialGradient id="s1-stk" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#FF8A4C"/><stop offset="1" stop-color="#E03C00"/></radialGradient>
  <linearGradient id="s1-shine" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <filter id="s1-blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="s1-shadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#000" flood-opacity=".45"/></filter>
</defs>
<ellipse cx="330" cy="300" rx="300" ry="250" fill="url(#s1-glow)"/>
<ellipse cx="330" cy="512" rx="240" ry="20" fill="#000" opacity=".5" filter="url(#s1-blur)"/>

<g class="s1-tag">
  <path d="M131,200 C98,214 52,248 22,292" fill="none" stroke="#C5CEDC" stroke-width="1.5"/>
  <g transform="translate(2,262) rotate(-8)">
    <path d="M0,10 L14,0 L118,0 Q124,0 124,6 L124,58 Q124,64 118,64 L14,64 L0,54 Z" fill="#F4F6FA"/>
    <circle cx="14" cy="32" r="4" fill="#0C2040"/>
    <text x="26" y="26" font-family="{MONO}" font-size="10" letter-spacing="1" fill="#5A6B80">PRICE TAG</text>
    <text x="26" y="42" font-family="{SANS}" font-size="12.5" font-weight="700" fill="#0C2040">Assumptions</text>
    <text x="26" y="56" font-family="{SANS}" font-size="12.5" font-weight="700" fill="#FF4A00">sold separately</text>
  </g>
</g>

<g filter="url(#s1-shadow)">
  <polygon points="130,160 430,160 516,104 216,104" fill="url(#s1-top)"/>
  <polygon points="430,160 516,104 516,444 430,500" fill="url(#s1-side)"/>
  <rect x="130" y="160" width="300" height="340" fill="url(#s1-front)"/>
</g>
<path d="M130,160 L216,104 L516,104 L516,444 M430,160 L516,104" stroke="#fff" stroke-opacity=".22" fill="none"/>
<rect x="130.5" y="160.5" width="299" height="339" fill="none" stroke="#fff" stroke-opacity=".16"/>
<polygon points="216,104 516,104 430,160 130,160" fill="url(#s1-shine)"/>
<g transform="matrix(1,-0.651,0,1,430,160)">
  <text transform="translate(50,70) rotate(90)" font-family="{MONO}" font-size="11.5" letter-spacing="2" fill="#8FA6C8">WHAT YOU DON'T SAY, IT MAKES UP</text>
</g>

<rect x="130" y="160" width="300" height="34" fill="url(#s1-band)"/>
<text x="148" y="182" font-family="{MONO}" font-size="11.5" letter-spacing="2.6" fill="#fff">LARGE LANGUAGE MODEL</text>
<text x="146" y="250" font-family="{SANS}" font-size="58" font-weight="700" letter-spacing="-2" fill="#fff">LLM</text>
<text x="268" y="226" font-family="{SANS}" font-size="13" font-weight="600" fill="#DCE6F5">Writes SQL in seconds.</text>
<text x="268" y="244" font-family="{SANS}" font-size="13" font-weight="600" fill="#DCE6F5">Sounds sure of everything.</text>

<rect x="148" y="266" width="264" height="132" rx="12" fill="url(#s1-win)" stroke="#fff" stroke-opacity=".18"/>
<rect x="210" y="280" width="190" height="44" rx="12" fill="#FF4A00"/>
<text x="222" y="298" font-family="{SANS}" font-size="12" fill="#fff">What's our early VEEV</text>
<text x="222" y="314" font-family="{SANS}" font-size="12" fill="#fff">adoption looking like?</text>
<rect x="160" y="334" width="196" height="52" rx="12" fill="#fff" fill-opacity=".09"/>
<g class="s1-skel">
  <rect x="172" y="346" width="150" height="7" rx="3.5" fill="#DCE6F5" opacity=".7"/>
  <rect x="172" y="359" width="118" height="7" rx="3.5" fill="#DCE6F5" opacity=".55"/>
  <rect x="172" y="372" width="86" height="7" rx="3.5" fill="#DCE6F5" opacity=".4"/>
</g>
<rect x="262" y="370" width="7" height="11" fill="#FF8A4C" class="s1-cur"/>
<circle cx="340" cy="360" r="9" fill="#00C9A7"/>
<path d="M335.5,360 l3,3 l5.5,-6" fill="none" stroke="#052" stroke-width="2"/>

<text x="148" y="422" font-family="{MONO}" font-size="10" letter-spacing="1.6" fill="#8FA6C8">CONTENTS</text>
<text x="148" y="437" font-family="{SANS}" font-size="12" fill="#DCE6F5">1 × next-token predictor · fluency · confidence</text>
{bar}
<text x="246" y="456" font-family="{MONO}" font-size="9.5" letter-spacing="1.2" fill="#FF8A4C">DOES NOT INCLUDE</text>
<text x="246" y="470" font-family="{SANS}" font-size="11" fill="#9BAAC2">your timeframe · your definitions</text>
<text x="246" y="484" font-family="{SANS}" font-size="11" fill="#9BAAC2">your consent rules · your tables</text>

<g class="s1-sticker">
  <polygon points="{burst(474, 112, 78, 64, 18)}" fill="url(#s1-stk)" stroke="#fff" stroke-width="3"/>
  <text x="474" y="95" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="700" fill="#fff" letter-spacing=".5">MIND-READER</text>
  <text x="474" y="123" text-anchor="middle" font-family="{SANS}" font-size="27" font-weight="700" fill="#fff" letter-spacing="1">NOT</text>
  <text x="474" y="145" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="700" fill="#fff" letter-spacing="1">INCLUDED</text>
</g>

{bubble(36, 70, 128, "timeframe?", "b1", [(150, 118, 4), (160, 132, 3)])}
{bubble(250, 22, 132, "adoption = ?", "b2", [(318, 70, 4), (326, 84, 3)])}
{bubble(528, 286, 108, "consent?", "b3", [(526, 330, 4), (520, 342, 3)])}
{bubble(10, 400, 122, "which table?", "b4", [(126, 444, 4), (134, 456, 3)])}
</svg>'''


# --------------------------------------------------------------------------- Session 2 (two profiles)
PROFILE = ("M150,52 C214,50 260,92 266,160 C270,188 268,204 272,224 C274,236 268,244 270,252 "
           "C276,276 292,300 300,322 C303,331 298,338 290,340 C282,342 280,350 284,356 "
           "C290,366 288,374 280,378 C286,384 286,394 278,398 C272,402 268,410 272,420 "
           "C278,436 276,456 262,466 C246,476 222,478 210,486 C204,500 204,530 206,560 "
           "L60,560 C64,520 70,490 66,460 C40,430 24,380 26,320 C28,210 62,54 150,52 Z")
FACE_W, FACE_H, FACE_OX, FACE_OY, FACE_STEP = 680, 600, 24, 14, 8.5


def _path_points(d, n=24):
    """Sample an M/C/L/Z path into polygon points."""
    toks = re.findall(r"[MCLZ]|-?\d+(?:\.\d+)?", d)
    pts, i, cur, cmd = [], 0, (0.0, 0.0), None
    while i < len(toks):
        t = toks[i]
        if t in "MCLZ":
            cmd = t
            i += 1
            if t == "Z":
                break
            continue
        if cmd == "M" or cmd == "L":
            cur = (float(toks[i]), float(toks[i + 1]))
            pts.append(cur)
            i += 2
        elif cmd == "C":
            c1 = (float(toks[i]), float(toks[i + 1]))
            c2 = (float(toks[i + 2]), float(toks[i + 3]))
            p = (float(toks[i + 4]), float(toks[i + 5]))
            for k in range(1, n + 1):
                s = k / n
                a = (1 - s) ** 3
                b = 3 * (1 - s) ** 2 * s
                c = 3 * (1 - s) * s * s
                e = s ** 3
                pts.append((a * cur[0] + b * c1[0] + c * c2[0] + e * p[0],
                            a * cur[1] + b * c1[1] + c * c2[1] + e * p[1]))
            cur = p
            i += 6
    return pts


def _hair_x(ly):
    pts = [(110, 245), (190, 200), (260, 165), (330, 112), (450, 74), (600, 60)]
    if ly <= pts[0][0]:
        return 1e9
    for (y0, x0), (y1, x1) in zip(pts, pts[1:]):
        if y0 <= ly <= y1:
            return x0 + (x1 - x0) * (ly - y0) / (y1 - y0)
    return 60


def face_dots():
    """Halftone dots for one profile (facing right) in the 680x600 design space: [x, y, r]."""
    from PIL import Image, ImageDraw, ImageFilter
    sc = 2
    mask = Image.new("L", (FACE_W * sc, FACE_H * sc), 0)
    poly = [((x + FACE_OX) * sc, (y + FACE_OY) * sc) for x, y in _path_points(PROFILE)]
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    inner = mask.filter(ImageFilter.MinFilter(19))
    dots = []
    step = FACE_STEP
    y = step / 2
    while y < FACE_H:
        x = step / 2
        while x < FACE_W / 2:
            px, py = int(x * sc), int(y * sc)
            if mask.getpixel((px, py)) > 128:
                lx, ly = x - FACE_OX, y - FACE_OY
                rim = inner.getpixel((px, py)) < 128
                if ly < 110 or lx < _hair_x(ly):
                    L = 0.13 + 0.13 * max(0.0, math.sin(lx * 0.23 + ly * 0.09)) + (0.1 if rim and ly < 200 else 0)
                else:
                    L = 0.36 + 0.5 * min(1, max(0, (lx - 60) / 240))
                    L -= 0.12 * ((ly - 290) / 270) ** 2
                    if ((lx - 240) / 13) ** 2 + ((ly - 262) / 6) ** 2 < 1:
                        L = 0.06
                    elif ((lx - 236) / 22) ** 2 + ((ly - 245) / 4.5) ** 2 < 1:
                        L = 0.14
                    if ((lx - 286) / 6) ** 2 + ((ly - 346) / 3.5) ** 2 < 1:
                        L = 0.16
                    if 258 < lx < 286 and abs(ly - 379) < 3:
                        L = 0.14
                    dd = math.hypot(lx - 156, (ly - 304) * 0.72)
                    if 13 < dd < 21:
                        L = 0.22
                    if ((lx - 238) / 42) ** 2 + ((ly - 318) / 34) ** 2 < 1:
                        L += 0.1
                    if lx > 110 and ly > 446 + (lx - 150) * 0.22:
                        L -= 0.22
                    if rim and lx > 190:
                        L += 0.2
                L = max(0.0, min(1.0, L))
                if L > 0.04:
                    dots.append([round(x, 1), round(y, 1), round(step * 0.52 * math.sqrt(L), 2)])
            x += step
        y += step
    return dots


def art_s2_static(dots=None, labels=True):
    """Both profiles as a static SVG: real (teal dots) facing synthetic (orange squares)."""
    dots = dots or face_dots()
    rnd = random.Random(11)
    out = []
    for x, y, r in dots:
        a = min(1, 0.4 + r / FACE_STEP)
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#00C9A7" fill-opacity="{a:.2f}"/>')
        s = 2 * r * 0.92 * (1 + (rnd.random() - 0.5) * 0.25)
        g = 90 + round(70 * min(1, r / (FACE_STEP * 0.52)))
        out.append(f'<rect x="{FACE_W - x - s / 2:.1f}" y="{y - s / 2:.1f}" width="{s:.1f}" height="{s:.1f}" fill="rgb(255,{g},20)" fill-opacity="{a:.2f}"/>')
    lab = ""
    if labels:
        lab = (f'<text x="110" y="592" text-anchor="middle" font-family="{MONO}" font-size="16" letter-spacing="3" fill="#00C9A7">REAL</text>'
               f'<text x="570" y="592" text-anchor="middle" font-family="{MONO}" font-size="16" letter-spacing="3" fill="#FF8A4C">SYNTHETIC</text>')
    return (f'<svg class="art art-s2" viewBox="0 0 {FACE_W} {FACE_H + 10}" role="img" aria-label="Two faces in profile, nose to nose. The left one is drawn in teal dots and labelled real; the right one is its mirror image in orange pixels, labelled synthetic.">'
            + "".join(out) + lab + '</svg>')


# --------------------------------------------------------------------------- Session 3
def art_s3():
    """A balance scale. One pan holds the claim. The other pan is empty."""
    def weight(cx, label):
        return (f'<g><path d="M{cx - 34},{506} L{cx + 34},{506} L{cx + 27},{470} L{cx - 27},{470} Z" fill="url(#s3-iron)" stroke="#FFD27A" stroke-opacity=".5"/>'
                f'<path d="M{cx - 12},{470} C{cx - 12},{452} {cx + 12},{452} {cx + 12},{470}" fill="none" stroke="#FFD27A" stroke-opacity=".55" stroke-width="4"/>'
                f'<text x="{cx}" y="{494}" text-anchor="middle" font-family="{MONO}" font-size="8.6" letter-spacing=".2" fill="#FFE2A8">{label}</text></g>')

    return f'''<svg class="art art-s3" viewBox="0 0 640 560" role="img" aria-labelledby="s3-art-t">
<title id="s3-art-t">A brass balance scale. The left pan holds a glowing block that reads +20% ahead of plan. The right pan is empty except for a question mark. On the floor beside it sit three weights nobody put on the scale: baseline, window, population.</title>
<style>
.art-s3 .s3-q {{ transform-box: fill-box; transform-origin: center; animation: s3q 2.8s ease-in-out infinite; }}
@keyframes s3q {{ 0%,100% {{ opacity: .65; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.08); }} }}
.art-s3 .s3-glow {{ animation: s3g 3.2s ease-in-out infinite; }}
@keyframes s3g {{ 0%,100% {{ opacity: .55; }} 50% {{ opacity: .95; }} }}
</style>
<defs>
  <radialGradient id="s3-bg" cx="50%" cy="45%" r="48%"><stop offset="0" stop-color="#E8A320" stop-opacity=".32"/><stop offset="1" stop-color="#E8A320" stop-opacity="0"/></radialGradient>
  <linearGradient id="s3-brass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9A6400"/><stop offset=".45" stop-color="#FFD27A"/><stop offset=".6" stop-color="#E8A320"/><stop offset="1" stop-color="#8A5A00"/></linearGradient>
  <linearGradient id="s3-brass-v" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE2A8"/><stop offset="1" stop-color="#B07A10"/></linearGradient>
  <linearGradient id="s3-iron" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#27466F"/><stop offset="1" stop-color="#132A4B"/></linearGradient>
  <linearGradient id="s3-claim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF8A4C"/><stop offset="1" stop-color="#FF4A00"/></linearGradient>
  <filter id="s3-blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="s3-sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#000" flood-opacity=".45"/></filter>
</defs>
<ellipse cx="320" cy="280" rx="320" ry="250" fill="url(#s3-bg)"/>
<ellipse cx="330" cy="512" rx="250" ry="16" fill="#000" opacity=".5" filter="url(#s3-blur)"/>

<g filter="url(#s3-sh)">
  <path d="M242,506 L398,506 L380,478 L260,478 Z" fill="url(#s3-brass)"/>
  <rect x="300" y="470" width="40" height="10" rx="3" fill="url(#s3-brass)"/>
  <rect x="312" y="186" width="16" height="288" fill="url(#s3-brass)"/>
  <rect x="306" y="300" width="28" height="8" rx="3" fill="url(#s3-brass)"/>
  <rect x="306" y="420" width="28" height="8" rx="3" fill="url(#s3-brass)"/>
  <path d="M320,136 L332,162 L308,162 Z" fill="url(#s3-brass-v)"/>
</g>

<g>
  <animateTransform attributeName="transform" type="rotate" values="-8 320 176;-5.5 320 176;-8 320 176" keyTimes="0;.5;1" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="5.5s" repeatCount="indefinite"/>
  <rect x="104" y="171" width="432" height="10" rx="5" fill="url(#s3-brass-v)"/>
  <circle cx="112" cy="176" r="8" fill="url(#s3-brass-v)"/>
  <circle cx="528" cy="176" r="8" fill="url(#s3-brass-v)"/>

  <g>
    <animateTransform attributeName="transform" type="rotate" values="8 112 176;5.5 112 176;8 112 176" keyTimes="0;.5;1" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="5.5s" repeatCount="indefinite"/>
    <path d="M112,176 L50,338 M112,176 L174,338" stroke="#FFD27A" stroke-opacity=".7" stroke-width="1.5"/>
    <ellipse class="s3-glow" cx="112" cy="300" rx="70" ry="44" fill="#FF4A00" opacity=".6" filter="url(#s3-blur)"/>
    <rect x="68" y="262" width="88" height="68" rx="10" fill="url(#s3-claim)" stroke="#FFD0B8" stroke-opacity=".7"/>
    <text x="112" y="304" text-anchor="middle" font-family="{SANS}" font-size="29" font-weight="700" fill="#fff">+20%</text>
    <text x="112" y="322" text-anchor="middle" font-family="{MONO}" font-size="9" letter-spacing=".8" fill="#FFE8DC">AHEAD OF PLAN</text>
    <path d="M38,338 L186,338 Q112,384 38,338 Z" fill="url(#s3-brass-v)"/>
    <text x="112" y="250" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="1.6" fill="#FFD0B8">THE CLAIM</text>
  </g>

  <g>
    <animateTransform attributeName="transform" type="rotate" values="8 528 176;5.5 528 176;8 528 176" keyTimes="0;.5;1" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="5.5s" repeatCount="indefinite"/>
    <path d="M528,176 L466,338 M528,176 L590,338" stroke="#FFD27A" stroke-opacity=".7" stroke-width="1.5"/>
    <rect x="484" y="262" width="88" height="68" rx="10" fill="#00C9A7" fill-opacity=".07" stroke="#00C9A7" stroke-width="2" stroke-dasharray="6 5"/>
    <text class="s3-q" x="528" y="312" text-anchor="middle" font-family="{SANS}" font-size="46" font-weight="700" fill="#00C9A7">?</text>
    <path d="M454,338 L602,338 Q528,384 454,338 Z" fill="url(#s3-brass-v)"/>
    <text x="528" y="250" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="1.6" fill="#7EE7D2">COMPARED TO…</text>
  </g>
</g>

{weight(428, "BASELINE")}
{weight(505, "WINDOW")}
{weight(582, "POPULATION")}
<text x="510" y="530" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="#C9B48A">never put on the scale</text>
<path d="M436,446 C 470,420 505,400 528,392" fill="none" stroke="#FFD27A" stroke-opacity=".45" stroke-dasharray="3 5"/>
<path d="M524,388 l6,3 l-6,5" fill="none" stroke="#FFD27A" stroke-opacity=".6"/>
</svg>'''


# --------------------------------------------------------------------------- Session 4
DOG = ("M44,214 C30,214 14,216 8,208 C4,202 10,198 18,202 C26,206 36,206 44,200 "
       "C36,184 34,156 46,132 C56,112 72,96 86,80 C92,72 96,62 98,50 "
       "L100,16 C101,10 106,10 108,14 L120,36 "
       "C126,34 134,36 140,40 C150,44 162,46 172,50 C178,52 180,58 176,62 "
       "C172,66 162,68 152,70 C146,72 142,76 140,82 "
       "C144,98 146,118 142,140 L144,206 C150,207 154,211 150,214 L126,214 "
       "C128,198 128,176 124,160 C118,174 110,184 98,190 "
       "C102,198 106,206 112,214 Z")


def art_s4():
    """Silver Blaze, at night. A sitting dog, a stable, a moon, and a sky chart with a gap."""
    rnd = random.Random(1892)
    stars = []
    for i in range(70):
        x, y = rnd.uniform(6, 634), rnd.uniform(6, 330)
        if (x - 468) ** 2 + (y - 128) ** 2 < 95 ** 2:
            continue
        r = rnd.choice([0.7, 0.9, 1.1, 1.4, 1.8])
        d = rnd.uniform(0, 4)
        stars.append(f'<circle class="s4-tw" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#E6EEFF" style="animation-delay:-{d:.1f}s"/>')
    stars = "".join(stars)

    def constel(x, top, base=246):
        pts = []
        y = base
        n = 0
        while y >= top - 0.1:
            pts.append((x + (6 if n % 2 else -6), y))
            y -= (base - top) / max(1, round((base - top) / 26))
            n += 1
        line = " ".join(f"{a:.0f},{b:.0f}" for a, b in pts)
        dots = "".join(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="{2.6 if i == len(pts) - 1 else 2}" fill="#fff"/>' for i, (a, b) in enumerate(pts))
        return f'<polyline points="{line}" fill="none" stroke="#B4C8FF" stroke-opacity=".55" stroke-width="1"/>{dots}'

    return f'''<svg class="art art-s4" viewBox="0 0 640 560" role="img" aria-labelledby="s4-art-t">
<title id="s4-art-t">A moonlit night. A dog sits silently in front of a stable with one lit window; the speech bubble above it is empty. In the stars, a constellation chart shows two bars, IQOS and VEEV, and a third outlined bar with nothing in it, under a magnifying glass.</title>
<style>
.art-s4 .s4-tw {{ animation: s4t 3.6s ease-in-out infinite; }}
@keyframes s4t {{ 0%,100% {{ opacity: .25; }} 50% {{ opacity: 1; }} }}
.art-s4 .s4-dot {{ animation: s4d 2.4s ease-in-out infinite; }}
.art-s4 .s4-dot.d2 {{ animation-delay: .3s; }} .art-s4 .s4-dot.d3 {{ animation-delay: .6s; }}
@keyframes s4d {{ 0%,100% {{ opacity: .15; }} 40% {{ opacity: .7; }} }}
.art-s4 .s4-lens {{ animation: s4l 9s ease-in-out infinite; }}
@keyframes s4l {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(-8px,6px); }} }}
.art-s4 .s4-win {{ animation: s4w 4s ease-in-out infinite; }}
@keyframes s4w {{ 0%,100% {{ opacity: .85; }} 50% {{ opacity: 1; }} 70% {{ opacity: .7; }} }}
</style>
<defs>
  <radialGradient id="s4-moon" cx="40%" cy="38%" r="65%"><stop offset="0" stop-color="#FFFDF4"/><stop offset=".7" stop-color="#E4E8F2"/><stop offset="1" stop-color="#B9C4DC"/></radialGradient>
  <radialGradient id="s4-halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#C9D6FF" stop-opacity=".38"/><stop offset="1" stop-color="#C9D6FF" stop-opacity="0"/></radialGradient>
  <radialGradient id="s4-lamp" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFB347" stop-opacity=".75"/><stop offset="1" stop-color="#FFB347" stop-opacity="0"/></radialGradient>
  <linearGradient id="s4-hill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#132B52"/><stop offset="1" stop-color="#0A1A33"/></linearGradient>
  <linearGradient id="s4-ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#081A35"/><stop offset="1" stop-color="#040D1C"/></linearGradient>
  <linearGradient id="s4-rim" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B4C8FF" stop-opacity=".7"/><stop offset=".5" stop-color="#B4C8FF" stop-opacity="0"/></linearGradient>
</defs>
{stars}
<circle cx="468" cy="128" r="150" fill="url(#s4-halo)"/>
<circle cx="468" cy="128" r="62" fill="url(#s4-moon)"/>
<circle cx="448" cy="112" r="9" fill="#C7CFE0" opacity=".6"/>
<circle cx="484" cy="146" r="13" fill="#C7CFE0" opacity=".45"/>
<circle cx="492" cy="104" r="6" fill="#C7CFE0" opacity=".5"/>

<g>
  <text x="56" y="44" font-family="{MONO}" font-size="10.5" letter-spacing="1.6" fill="#8FA6C8">DEVICE SESSIONS · JAPAN</text>
  <line x1="56" y1="252" x2="300" y2="252" stroke="#B4C8FF" stroke-opacity=".35"/>
  {constel(96, 72)}
  {constel(176, 150)}
  <rect x="236" y="110" width="40" height="142" fill="none" stroke="#B4C8FF" stroke-opacity=".55" stroke-dasharray="4 5"/>
  <text x="96" y="272" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#B4C8FF">IQOS</text>
  <text x="176" y="272" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#B4C8FF">VEEV</text>
  <text x="256" y="272" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="500" fill="#fff">?</text>
  <g class="s4-lens">
    <circle cx="256" cy="170" r="44" fill="#B4C8FF" fill-opacity=".06" stroke="#DCE6FF" stroke-width="3"/>
    <circle cx="256" cy="170" r="44" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="1" stroke-dasharray="40 240" transform="rotate(-140 256 170)"/>
    <path d="M287,201 L314,228" stroke="#DCE6FF" stroke-width="9" stroke-linecap="round"/>
    <path d="M287,201 L314,228" stroke="#0C2040" stroke-width="3" stroke-linecap="round" opacity=".5"/>
  </g>
</g>

<path d="M0,392 C90,360 170,352 260,366 C350,380 420,350 500,338 C560,330 610,336 640,344 L640,560 L0,560 Z" fill="url(#s4-hill)"/>
<g>
  <circle class="s4-win" cx="500" cy="318" r="40" fill="url(#s4-lamp)"/>
  <path d="M430,350 L430,296 L478,262 L526,262 L574,296 L574,350 Z" fill="#061226"/>
  <path d="M478,262 L526,262 L526,250 L478,250 Z" fill="#061226"/>
  <path d="M502,250 L502,226" stroke="#061226" stroke-width="2.5"/>
  <path d="M494,232 L512,232 M502,226 l7,4 l-7,3" stroke="#061226" stroke-width="2" fill="none"/>
  <rect class="s4-win" x="491" y="306" width="22" height="18" rx="1" fill="#FFB347"/>
  <path d="M502,306 L502,324 M491,315 L513,315" stroke="#061226" stroke-width="1.5"/>
  <path d="M452,350 L452,322 L470,322 L470,350" fill="#0C1C36"/>
</g>
<g stroke="#061226" stroke-width="4">
  <path d="M318,378 L318,352 M352,374 L352,348 M386,368 L386,342 M420,362 L420,336"/>
  <path d="M312,362 L426,346 M312,372 L426,356" stroke-width="2.5"/>
</g>
<path d="M0,470 C120,450 260,446 380,458 C470,466 560,462 640,452 L640,560 L0,560 Z" fill="url(#s4-ground)"/>

<g transform="translate(104,256)">
  <path d="{DOG}" fill="#02081A"/>
  <path d="{DOG}" fill="none" stroke="url(#s4-rim)" stroke-width="2"/>
  <circle cx="146" cy="47" r="2" fill="#B4C8FF" opacity=".8"/>
</g>
<g transform="translate(318,236)">
  <path d="M0,16 Q0,0 16,0 L84,0 Q100,0 100,16 L100,46 Q100,62 84,62 L40,62 L16,84 L22,62 L16,62 Q0,62 0,46 Z" fill="rgba(8,26,53,.55)" stroke="#B4C8FF" stroke-opacity=".7" stroke-width="1.5" stroke-dasharray="5 5"/>
  <circle class="s4-dot" cx="30" cy="31" r="5" fill="#DCE6FF"/>
  <circle class="s4-dot d2" cx="50" cy="31" r="5" fill="#DCE6FF"/>
  <circle class="s4-dot d3" cx="70" cy="31" r="5" fill="#DCE6FF"/>
</g>
</svg>'''


def prefix_ids(svg, p):
    """Make every id in an inline SVG unique so the same art can appear twice on a page."""
    import re
    ids = set(re.findall(r'id="([^"]+)"', svg))
    for i in sorted(ids, key=len, reverse=True):
        svg = svg.replace(f'id="{i}"', f'id="{p}{i}"')
        svg = svg.replace(f'url(#{i})', f'url(#{p}{i})')
        svg = svg.replace(f'aria-labelledby="{i}"', f'aria-labelledby="{p}{i}"')
        svg = svg.replace(f'href="#{i}"', f'href="#{p}{i}"')
    return svg
