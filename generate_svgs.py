#!/usr/bin/env python3
"""
Step 1: Generate Direction B SVG comic panels for Posts #11 and #16.
No external dependencies needed - pure Python SVG generation.
"""
import os

OUT_DIR = "/Users/a11/tcmway-blog/images"

# ── Direction B Color Palette ──
ZHU_RED = "#b83a2a"
APRICOT = "#e8a87c"
APRICOT_LIGHT = "#f0c8a0"
CREAM = "#fdf6ee"
GOLD = "#c9a84c"
WARM_BROWN = "#8a6e54"
DARK = "#1a1410"
IRIS_CENTER = "#d4534a"
FACE = "#fdf6ee"
FERN_GREEN = "#5a7a50"
ICE_BLUE = "#3a5a8a"

PANEL_SIZE = 512
GRID_SIZE = PANEL_SIZE * 2


def ollie_defs(panel_id=""):
    return '''  <defs>
    <radialGradient id="bodyGrad''' + panel_id + '''" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="''' + APRICOT_LIGHT + '''"/>
      <stop offset="100%" stop-color="''' + APRICOT + '''"/>
    </radialGradient>
    <radialGradient id="eyeGrad''' + panel_id + '''" cx="50%" cy="40%" r="50%">
      <stop offset="0%" stop-color="''' + IRIS_CENTER + '''"/>
      <stop offset="100%" stop-color="''' + ZHU_RED + '''"/>
    </radialGradient>
    <filter id="shadow''' + panel_id + '''" x="-20%" y="-10%" width="140%" height="140%">
      <feDropShadow dx="2" dy="4" stdDeviation="3" flood-color="#00000022"/>
    </filter>
    <filter id="softShadow''' + panel_id + '''" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#00000015"/>
    </filter>
  </defs>'''


def draw_ollie(cx, cy, scale=1.0, expression="neutral", pid=""):
    s = scale
    eye_config = {
        "neutral": (18, 20), "surprised": (16, 24), "miserable": (16, 14),
        "happy": (16, 10), "confused": (17, 18), "struggling": (16, 15), "alarmed": (17, 22)
    }
    eye_rx, eye_ry = eye_config.get(expression, (18, 20))
    eye_y = cy - 8*s

    mouth_map = {
        "neutral": f'<path d="M{cx-6*s},{cy+8*s} Q{cx},{cy+12*s} {cx+6*s},{cy+8*s}" fill="none" stroke="{DARK}" stroke-width="1.5" stroke-linecap="round"/>',
        "surprised": f'<ellipse cx="{cx}" cy="{cy+10*s}" rx="5" ry="7" fill="{DARK}"/>',
        "miserable": f'<path d="M{cx-8*s},{cy+12*s} Q{cx},{cy+6*s} {cx+8*s},{cy+12*s}" fill="none" stroke="{DARK}" stroke-width="1.5" stroke-linecap="round"/>',
        "happy": f'<path d="M{cx-7*s},{cy+8*s} Q{cx},{cy+18*s} {cx+7*s},{cy+8*s}" fill="none" stroke="{DARK}" stroke-width="1.5" stroke-linecap="round"/>',
        "confused": f'<path d="M{cx-5*s},{cy+9*s} Q{cx+2*s},{cy+13*s} {cx+5*s},{cy+9*s}" fill="none" stroke="{DARK}" stroke-width="1.5" stroke-linecap="round"/>',
        "struggling": f'<path d="M{cx-6*s},{cy+10*s} Q{cx},{cy+7*s} {cx+6*s},{cy+10*s}" fill="none" stroke="{DARK}" stroke-width="1.5" stroke-linecap="round"/>',
        "alarmed": f'<ellipse cx="{cx}" cy="{cy+10*s}" rx="6" ry="8" fill="{DARK}"/>',
    }
    mouth = mouth_map.get(expression, mouth_map["neutral"])
    
    eb_offsets = {"neutral": (0,0), "surprised": (0,-4), "happy": (0,-2), "confused": (0,-3), "alarmed": (0,-3)}
    eby = eb_offsets.get(expression, (0,0))[1]

    # Calculate iris/pupil sizes
    iris_rx = max(4, eye_rx - 5)
    iris_ry = max(4, eye_ry - 4)
    pupil_rx = max(3*s, eye_rx/3)
    pupil_ry = max(4*s, eye_ry/2.5)

    return f'''
  <ellipse cx="{cx}" cy="{cy}" rx="{55*s}" ry="{50*s}" fill="url(#bodyGrad{pid})" filter="url(#shadow{pid})"/>
  <ellipse cx="{cx-45*s}" cy="{cy-10*s}" rx="22" ry="32" fill="{APRICOT}" opacity="0.5" transform="rotate(-15 {cx-45*s} {cy-10*s})"/>
  <ellipse cx="{cx+45*s}" cy="{cy-10*s}" rx="22" ry="32" fill="{APRICOT}" opacity="0.5" transform="rotate(15 {cx+45*s} {cy-10*s})"/>
  <ellipse cx="{cx}" cy="{cy-12*s}" rx="{38*s}" ry="{35*s}" fill="{FACE}"/>
  <ellipse cx="{cx-15*s}" cy="{eye_y}" rx="{eye_rx+1}" ry="{eye_ry-1}" fill="white"/>
  <ellipse cx="{cx+15*s}" cy="{eye_y}" rx="{eye_rx+1}" ry="{eye_ry-1}" fill="white"/>
  <ellipse cx="{cx-15*s}" cy="{eye_y+3*s}" rx="{iris_rx}" ry="{iris_ry}" fill="url(#eyeGrad{pid})"/>
  <ellipse cx="{cx+15*s}" cy="{eye_y+3*s}" rx="{iris_rx}" ry="{iris_ry}" fill="url(#eyeGrad{pid})"/>
  <ellipse cx="{cx-15*s}" cy="{eye_y+5*s}" rx="{pupil_rx}" ry="{pupil_ry}" fill="{DARK}"/>
  <ellipse cx="{cx+15*s}" cy="{eye_y+5*s}" rx="{pupil_rx}" ry="{pupil_ry}" fill="{DARK}"/>
  <circle cx="{cx-18*s}" cy="{eye_y}" r="2.5" fill="white" opacity="0.9"/>
  <circle cx="{cx+12*s}" cy="{eye_y}" r="2.5" fill="white" opacity="0.9"/>
  <path d="M{cx-35*s},{eye_y-8*s+eby} Q{cx-15*s},{eye_y-16*s+eby} {cx+2*s},{eye_y-8*s+eby}" stroke="{WARM_BROWN}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M{cx-2*s},{eye_y-8*s+eby} Q{cx+15*s},{eye_y-16*s+eby} {cx+35*s},{eye_y-8*s+eby}" stroke="{WARM_BROWN}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <polygon points="{cx},{cy+2*s} {cx-8*s},{cy+10*s} {cx+8*s},{cy+10*s}" fill="{ZHU_RED}"/>
  <line x1="{cx-8*s}" y1="{cy+10*s}" x2="{cx+8*s}" y2="{cy+10*s}" stroke="{GOLD}" stroke-width="1.2"/>
  {mouth}
  <ellipse cx="{cx-25*s}" cy="{cy+4*s}" rx="8" ry="5" fill="{APRICOT}" opacity="0.35"/>
  <ellipse cx="{cx+25*s}" cy="{cy+4*s}" rx="8" ry="5" fill="{APRICOT}" opacity="0.35"/>
  <path d="M{cx-32*s},{cy-28*s} Q{cx-38*s},{cy-52*s} {cx-26*s},{cy-48*s} Q{cx-18*s},{cy-56*s} {cx-22*s},{cy-30*s}" fill="{ZHU_RED}" stroke="{WARM_BROWN}" stroke-width="1"/>
  <path d="M{cx+32*s},{cy-28*s} Q{cx+38*s},{cy-52*s} {cx+26*s},{cy-48*s} Q{cx+18*s},{cy-56*s} {cx+22*s},{cy-30*s}" fill="{ZHU_RED}" stroke="{WARM_BROWN}" stroke-width="1"/>
  <path d="M{cx},{cy-40*s} Q{cx-3*s},{cy-20*s} {cx},{cy-5*s}" stroke="{WARM_BROWN}" stroke-width="0.8" fill="none" opacity="0.4"/>
  <path d="M{cx-10*s},{cy-37*s} Q{cx-13*s},{cy-18*s} {cx-10*s},{cy-3*s}" stroke="{WARM_BROWN}" stroke-width="0.7" fill="none" opacity="0.3"/>
  <path d="M{cx+10*s},{cy-37*s} Q{cx+13*s},{cy-18*s} {cx+10*s},{cy-3*s}" stroke="{WARM_BROWN}" stroke-width="0.7" fill="none" opacity="0.3"/>
  <circle cx="{cx}" cy="{cy+25*s}" r="8" fill="{GOLD}" opacity="0.8" stroke="{ZHU_RED}" stroke-width="1.5"/>
  <circle cx="{cx}" cy="{cy+25*s}" r="3" fill="{ZHU_RED}" opacity="0.6"/>'''


def panel_svg(title, content_elements, panel_index, width=PANEL_SIZE, height=PANEL_SIZE):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
{ollie_defs(str(panel_index))}
  <rect width="{width}" height="{height}" fill="{CREAM}" rx="12"/>
  <rect x="2" y="2" width="{width-4}" height="{height-4}" fill="none" stroke="{WARM_BROWN}" stroke-width="3" rx="10"/>
  <text x="{width//2}" y="30" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="{WARM_BROWN}" font-weight="bold">{title}</text>
  <line x1="30" y1="38" x2="{width-30}" y2="38" stroke="{APRICOT}" stroke-width="1"/>
{content_elements}
  <text x="{width-20}" y="{height-12}" text-anchor="end" font-family="Georgia, serif" font-size="11" fill="{WARM_BROWN}" opacity="0.4">{panel_index}</text>
</svg>'''


# ═══ COMIC #11: Cold Progression ═══

def panel_11_01():
    pid = "1"
    content = f'''
  <rect x="430" y="80" width="12" height="160" rx="6" fill="white" stroke="{WARM_BROWN}" stroke-width="1.5"/>
  <rect x="430" y="100" width="12" height="110" rx="6" fill="{ZHU_RED}" opacity="0.6"/>
  <circle cx="436" cy="245" r="10" fill="{ZHU_RED}" stroke="{WARM_BROWN}" stroke-width="1.5"/>
  <text x="436" y="60" text-anchor="middle" font-family="Georgia, serif" font-size="20" fill="{ZHU_RED}" font-weight="bold">38&#176;C</text>
  <line x1="180" y1="400" x2="175" y2="415" stroke="{WARM_BROWN}" stroke-width="1.5" opacity="0.5"/>
  <line x1="320" y1="400" x2="325" y2="415" stroke="{WARM_BROWN}" stroke-width="1.5" opacity="0.5"/>
  <rect x="40" y="370" width="55" height="40" rx="4" fill="white" stroke="{WARM_BROWN}" stroke-width="1" opacity="0.7"/>
  <rect x="45" y="360" width="45" height="14" rx="3" fill="white" stroke="{WARM_BROWN}" stroke-width="1" opacity="0.7"/>
  <path d="M50,360 Q55,350 60,360" fill="none" stroke="{APRICOT}" stroke-width="1" opacity="0.5"/>
  {draw_ollie(256, 230, scale=1.2, expression="miserable", pid=pid)}
  <text x="256" y="460" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="{WARM_BROWN}" font-style="italic">"Just a scratchy throat..."</text>'''
    return panel_svg("Panel 1: The Onset", content, 1)

def panel_11_02():
    pid = "2"
    content = f'''
  <rect x="50" y="180" width="35" height="50" rx="5" fill="#e8ddd0" stroke="{WARM_BROWN}" stroke-width="1.5"/>
  <rect x="52" y="175" width="31" height="10" rx="3" fill="{ZHU_RED}" stroke="{WARM_BROWN}" stroke-width="1"/>
  <text x="67" y="183" text-anchor="middle" font-family="sans-serif" font-size="7" fill="white" font-weight="bold">COLD</text>
  <ellipse cx="95" cy="230" rx="5" ry="4" fill="white" stroke="{WARM_BROWN}" stroke-width="0.8"/>
  <ellipse cx="108" cy="222" rx="5" ry="4" fill="white" stroke="{WARM_BROWN}" stroke-width="0.8"/>
  {draw_ollie(280, 240, scale=1.1, expression="confused", pid=pid)}
  <ellipse cx="260" cy="280" rx="18" ry="12" fill="{APRICOT}" opacity="0.5"/>
  <ellipse cx="305" cy="280" rx="18" ry="12" fill="{APRICOT}" opacity="0.5"/>
  <ellipse cx="330" cy="190" rx="4" ry="6" fill="#99ccff" opacity="0.5"/>
  <ellipse cx="350" cy="205" rx="3" ry="5" fill="#99ccff" opacity="0.4"/>
  <line x1="380" y1="260" x2="380" y2="350" stroke="{ZHU_RED}" stroke-width="3"/>
  <polygon points="375,340 380,355 385,340" fill="{ZHU_RED}"/>
  <text x="400" y="310" font-family="Georgia, serif" font-size="11" fill="{ZHU_RED}" font-style="italic">deeper</text>
  <text x="280" y="460" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{WARM_BROWN}" font-style="italic">"Why do I feel worse?"</text>'''
    return panel_svg("Panel 2: Mis-treatment", content, 2)

def panel_11_03():
    pid = "3"
    content = f'''
  <line x1="30" y1="280" x2="482" y2="280" stroke="{WARM_BROWN}" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.4"/>
  <text x="75" y="305" font-family="sans-serif" font-size="9" fill="{WARM_BROWN}" opacity="0.5">Year 1</text>
  <text x="190" y="305" font-family="sans-serif" font-size="9" fill="{WARM_BROWN}" opacity="0.5">Year 2</text>
  <text x="305" y="305" font-family="sans-serif" font-size="9" fill="{WARM_BROWN}" opacity="0.5">Year 3</text>
  <text x="420" y="305" font-family="sans-serif" font-size="9" fill="{WARM_BROWN}" opacity="0.5">Now</text>
  {draw_ollie(75, 235, scale=0.55, expression="neutral", pid=pid)}
  <text x="75" y="195" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="{FERN_GREEN}">"Just a cold"</text>
  {draw_ollie(190, 240, scale=0.52, expression="miserable", pid=pid)}
  <text x="190" y="190" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="{APRICOT}">"Again?"</text>
  {draw_ollie(305, 245, scale=0.48, expression="struggling", pid=pid)}
  <text x="305" y="190" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="{ZHU_RED}">chronic cough</text>
  {draw_ollie(420, 255, scale=0.44, expression="miserable", pid=pid)}
  <text x="420" y="200" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="{ZHU_RED}" font-weight="bold">autoimmune?</text>
  <line x1="110" y1="270" x2="150" y2="270" stroke="{ZHU_RED}" stroke-width="1.5"/>
  <polygon points="145,265 155,270 145,275" fill="{ZHU_RED}"/>
  <line x1="225" y1="270" x2="265" y2="270" stroke="{ZHU_RED}" stroke-width="1.5"/>
  <polygon points="260,265 270,270 260,275" fill="{ZHU_RED}"/>
  <line x1="340" y1="270" x2="380" y2="270" stroke="{ZHU_RED}" stroke-width="1.5"/>
  <polygon points="375,265 385,270 375,275" fill="{ZHU_RED}"/>
  <text x="256" y="460" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{ZHU_RED}" font-style="italic">Suppressed cold = compound interest on illness</text>'''
    return panel_svg("Panel 3: Accumulation", content, 3)

def panel_11_04():
    pid = "4"
    content = f'''
  <ellipse cx="160" cy="310" rx="45" ry="20" fill="#d4c5b0" stroke="{WARM_BROWN}" stroke-width="2"/>
  <rect x="115" y="200" width="90" height="110" rx="8" fill="#d4c5b0" stroke="{WARM_BROWN}" stroke-width="2"/>
  <ellipse cx="160" cy="200" rx="45" ry="15" fill="#e8d5c0" stroke="{WARM_BROWN}" stroke-width="1.5"/>
  <ellipse cx="160" cy="200" rx="38" ry="10" fill="#d4a050" opacity="0.6"/>
  <path d="M140,185 Q135,165 140,145" fill="none" stroke="white" stroke-width="2" opacity="0.5"/>
  <path d="M160,180 Q160,155 155,135" fill="none" stroke="white" stroke-width="2" opacity="0.5"/>
  <path d="M180,185 Q185,165 180,145" fill="none" stroke="white" stroke-width="2" opacity="0.5"/>
  <ellipse cx="145" cy="195" rx="10" ry="6" fill="#e8b960" opacity="0.7" transform="rotate(-20 145 195)"/>
  <ellipse cx="170" cy="198" rx="8" ry="5" fill="#e8b960" opacity="0.6" transform="rotate(15 170 198)"/>
  {draw_ollie(360, 240, scale=1.2, expression="happy", pid=pid)}
  <ellipse cx="430" cy="170" rx="5" ry="7" fill="#99ccff" opacity="0.4"/>
  <ellipse cx="450" cy="185" rx="4" ry="5" fill="#99ccff" opacity="0.3"/>
  <text x="420" y="150" font-size="16" fill="{GOLD}" opacity="0.6">&#9829;</text>
  <text x="256" y="460" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="{FERN_GREEN}" font-weight="bold">"Hot tea. Sweat. Rest. Three days."</text>'''
    return panel_svg("Panel 4: The Right Way", content, 4)


# ═══ COMIC #16: Yin-Yang Seesaw ═══

def panel_16_01():
    pid = "1"
    content = f'''
  <polygon points="256,340 230,400 282,400" fill="{WARM_BROWN}" stroke="{DARK}" stroke-width="2"/>
  <rect x="60" y="332" width="392" height="12" rx="6" fill="#d4c5b0" stroke="{WARM_BROWN}" stroke-width="2"/>
  <text x="70" y="375" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="{DARK}" font-weight="bold">YIN</text>
  <text x="442" y="375" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="{DARK}" font-weight="bold">YANG</text>
  {draw_ollie(256, 295, scale=1.1, expression="neutral", pid=pid)}
  <text x="160" y="70" font-size="20" opacity="0.2">&#9728;</text>
  <text x="350" y="90" font-size="16" opacity="0.2">&#9790;</text>
  <text x="256" y="460" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="{FERN_GREEN}">"Everything in balance."</text>'''
    return panel_svg("Panel 1: Balance", content, 1)

def panel_16_02():
    pid = "2"
    content = f'''
  <polygon points="256,340 230,400 282,400" fill="{WARM_BROWN}" stroke="{DARK}" stroke-width="2"/>
  <line x1="80" y1="300" x2="432" y2="364" stroke="#d4c5b0" stroke-width="12" stroke-linecap="round"/>
  <line x1="80" y1="300" x2="432" y2="364" stroke="{WARM_BROWN}" stroke-width="2" stroke-linecap="round"/>
  <text x="60" y="280" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="{WARM_BROWN}" font-weight="bold" opacity="0.5">YIN</text>
  <text x="460" y="385" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="{ZHU_RED}" font-weight="bold">YANG</text>
  <text x="430" y="355" font-size="18" fill="{ZHU_RED}" opacity="0.4">&#128293;</text>
  {draw_ollie(370, 310, scale=0.9, expression="alarmed", pid=pid)}
  <text x="256" y="460" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{ZHU_RED}" font-style="italic">"Too much Yang!"</text>'''
    return panel_svg("Panel 2: Yang Excess", content, 2)

def panel_16_03():
    pid = "3"
    content = f'''
  <polygon points="256,340 230,400 282,400" fill="{WARM_BROWN}" stroke="{DARK}" stroke-width="2"/>
  <line x1="80" y1="364" x2="432" y2="300" stroke="#d4c5b0" stroke-width="12" stroke-linecap="round"/>
  <line x1="80" y1="364" x2="432" y2="300" stroke="{WARM_BROWN}" stroke-width="2" stroke-linecap="round"/>
  <text x="55" y="395" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="{ICE_BLUE}" font-weight="bold">YIN</text>
  <text x="460" y="280" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="{WARM_BROWN}" font-weight="bold" opacity="0.5">YANG</text>
  <text x="115" y="395" font-size="16" fill="#99bbdd" opacity="0.4">&#10052;</text>
  {draw_ollie(140, 320, scale=0.9, expression="struggling", pid=pid)}
  <text x="256" y="460" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{ICE_BLUE}" font-style="italic">"Too much Yin..."</text>'''
    return panel_svg("Panel 3: Yin Excess", content, 3)

def panel_16_04():
    pid = "4"
    content = f'''
  <polygon points="256,340 230,400 282,400" fill="{WARM_BROWN}" stroke="{DARK}" stroke-width="2"/>
  <line x1="90" y1="325" x2="422" y2="339" stroke="#d4c5b0" stroke-width="12" stroke-linecap="round"/>
  <line x1="90" y1="325" x2="422" y2="339" stroke="{WARM_BROWN}" stroke-width="2" stroke-linecap="round"/>
  <text x="55" y="360" text-anchor="middle" font-family="Georgia, serif" font-size="17" fill="{DARK}" font-weight="bold">YIN</text>
  <text x="457" y="375" text-anchor="middle" font-family="Georgia, serif" font-size="17" fill="{DARK}" font-weight="bold">YANG</text>
  {draw_ollie(380, 275, scale=1.0, expression="happy", pid=pid)}
  <ellipse cx="340" cy="265" rx="15" ry="10" fill="{APRICOT}" opacity="0.5" transform="rotate(-30 340 265)"/>
  <ellipse cx="200" cy="155" rx="100" ry="45" fill="white" stroke="{WARM_BROWN}" stroke-width="1.5" filter="url(#softShadow{pid})"/>
  <polygon points="280,195 295,230 300,192" fill="white" stroke="{WARM_BROWN}" stroke-width="1.5"/>
  <text x="195" y="148" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="{DARK}">"Neither side wins.</text>
  <text x="195" y="170" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="{DARK}">That's the point."</text>
  <text x="130" y="270" font-size="12" fill="{GOLD}" opacity="0.4">&#10022;</text>
  <text x="350" y="350" font-size="10" fill="{GOLD}" opacity="0.4">&#10022;</text>'''
    return panel_svg("Panel 4: Dynamic Balance", content, 4)


def generate_svgs():
    comics = {
        "comic-11-cold-progression": [panel_11_01, panel_11_02, panel_11_03, panel_11_04],
        "comic-16-yin-yang-seesaw": [panel_16_01, panel_16_02, panel_16_03, panel_16_04],
    }
    
    for name, panels in comics.items():
        tmp_dir = f"/tmp/tcmway-comics/{name}"
        os.makedirs(tmp_dir, exist_ok=True)
        print(f"\n📝 {name}:")
        for i, panel_fn in enumerate(panels):
            svg = panel_fn()
            path = f"{tmp_dir}/panel_{i+1}.svg"
            with open(path, 'w') as f:
                f.write(svg)
            print(f"  ✅ panel_{i+1}.svg")


if __name__ == "__main__":
    generate_svgs()
    print("\n🎨 SVGs generated! Ready for PNG conversion.")
