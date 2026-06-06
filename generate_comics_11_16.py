#!/usr/bin/env python3
"""
Generate TCM Way comic strips for Posts #11 and #16.
Direction B standard: warm hand-drawn feel, radial gradients, drop shadows, organic curves.
Uses cairosvg to render SVG → PNG.
"""
import subprocess
import os
import sys
from PIL import Image

VENV_PYTHON = "/Users/a11/.workbuddy/binaries/python/envs/default/bin/python3"
OUT_DIR = "/Users/a11/tcmway-blog/images"

# ── Direction B Color Palette ──
ZHU_RED = "#b83a2a"       # 朱红
APRICOT = "#e8a87c"        # 杏色
APRICOT_LIGHT = "#f0c8a0"  # 浅杏
CREAM = "#fdf6ee"          # 暖米
GOLD = "#c9a84c"           # 金色
WARM_BROWN = "#8a6e54"     # 暖棕
DARK = "#1a1410"           # 深黑
IRIS_CENTER = "#d4534a"    # 虹膜中心
FACE = "#fdf6ee"           # 面部
FERN_GREEN = "#5a7a50"     # 蕨绿（眼睛高光底色）

# Panel dimensions
PANEL_SIZE = 512  # Each panel 512x512
GRID_SIZE = PANEL_SIZE * 2  # 2x2 = 1024x1024


def ollie_defs(scale=1.0):
    """Generate Direction B standard SVG <defs> for Ollie at given scale."""
    return f'''
  <defs>
    <radialGradient id="bodyGrad" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="{APRICOT_LIGHT}"/>
      <stop offset="100%" stop-color="{APRICOT}"/>
    </radialGradient>
    <radialGradient id="eyeGrad" cx="50%" cy="40%" r="50%">
      <stop offset="0%" stop-color="{IRIS_CENTER}"/>
      <stop offset="100%" stop-color="{ZHU_RED}"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-10%" width="140%" height="140%">
      <feDropShadow dx="2" dy="4" stdDeviation="3" flood-color="#00000022"/>
    </filter>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#00000015"/>
    </filter>
  </defs>'''


def draw_ollie(cx, cy, scale=1.0, expression="neutral", facing="front"):
    """Draw Ollie mascot - Direction B compliant.
    
    expression: "neutral", "surprised", "miserable", "happy", "confused", "struggling", "alarmed"
    facing: "front", "left", "right"
    """
    s = scale
    body_rx, body_ry = 55*s, 50*s
    face_rx, face_ry = 38*s, 35*s
    
    # Eye parameters by expression
    eye_open = {
        "neutral": (18, 20), "surprised": (16, 24), "miserable": (16, 14),
        "happy": (16, 10), "confused": (17, 18), "struggling": (16, 15), "alarmed": (17, 22)
    }.get(expression, (18, 20))
    eye_rx, eye_ry = eye_open
    
    # Eye position adjustment for facing
    eye_offset_x = {"left": -4, "right": 4, "front": 0}.get(facing, 0)
    eye_y = cy - 8*s
    
    # Mouth by expression
    mouths = {
        "neutral": f'<path d="M{cx-6*s},{cy+8*s} Q{cx},{cy+12*s} {cx+6*s},{cy+8*s}" fill="none" stroke="{DARK}" stroke-width="1.5" stroke-linecap="round"/>',
        "surprised": f'<ellipse cx="{cx}" cy="{cy+10*s}" rx="5" ry="7" fill="{DARK}"/>',
        "miserable": f'<path d="M{cx-8*s},{cy+12*s} Q{cx},{cy+6*s} {cx+8*s},{cy+12*s}" fill="none" stroke="{DARK}" stroke-width="1.5" stroke-linecap="round"/>',
        "happy": f'<path d="M{cx-7*s},{cy+8*s} Q{cx},{cy+18*s} {cx+7*s},{cy+8*s}" fill="none" stroke="{DARK}" stroke-width="1.5" stroke-linecap="round"/>',
        "confused": f'<path d="M{cx-5*s},{cy+9*s} Q{cx+2*s},{cy+13*s} {cx+5*s},{cy+9*s}" fill="none" stroke="{DARK}" stroke-width="1.5" stroke-linecap="round"/>',
        "struggling": f'<path d="M{cx-6*s},{cy+10*s} Q{cx},{cy+7*s} {cx+6*s},{cy+10*s}" fill="none" stroke="{DARK}" stroke-width="1.5" stroke-linecap="round"/>',
        "alarmed": f'<ellipse cx="{cx}" cy="{cy+10*s}" rx="6" ry="8" fill="{DARK}"/>',
    }
    mouth = mouths.get(expression, mouths["neutral"])
    
    eyebrow_offsets = {
        "neutral": (0, 0), "surprised": (0, -4), "miserable": (0, 0), "happy": (0, -2),
        "confused": (0, -3), "struggling": (0, 0), "alarmed": (0, -3)
    }
    eb_off = eyebrow_offsets.get(expression, (0, 0))
    
    return f'''
  <!-- Ollie Body -->
  <ellipse cx="{cx}" cy="{cy}" rx="{body_rx}" ry="{body_ry}" fill="url(#bodyGrad)" filter="url(#shadow)"/>
  
  <!-- Wing hints -->
  <ellipse cx="{cx-45*s}" cy="{cy-10*s}" rx="22" ry="32" fill="{APRICOT}" opacity="0.5" transform="rotate(-15 {cx-45*s} {cy-10*s})"/>
  <ellipse cx="{cx+45*s}" cy="{cy-10*s}" rx="22" ry="32" fill="{APRICOT}" opacity="0.5" transform="rotate(15 {cx+45*s} {cy-10*s})"/>
  
  <!-- Face disc -->
  <ellipse cx="{cx}" cy="{cy-12*s}" rx="{face_rx}" ry="{face_ry}" fill="{FACE}"/>
  
  <!-- Eye whites -->
  <ellipse cx="{cx-15*s+eye_offset_x}" cy="{eye_y}" rx="{eye_rx+1}" ry="{eye_ry-1}" fill="white"/>
  <ellipse cx="{cx+15*s+eye_offset_x}" cy="{eye_y}" rx="{eye_rx+1}" ry="{eye_ry-1}" fill="white"/>
  
  <!-- Irises -->
  <ellipse cx="{cx-15*s+eye_offset_x}" cy="{eye_y+3*s}" rx="{eye_rx-5}" ry="{eye_ry-4}" fill="url(#eyeGrad)"/>
  <ellipse cx="{cx+15*s+eye_offset_x}" cy="{eye_y+3*s}" rx="{eye_rx-5}" ry="{eye_ry-4}" fill="url(#eyeGrad)"/>
  
  <!-- Pupils -->
  <ellipse cx="{cx-15*s+eye_offset_x}" cy="{eye_y+5*s}" rx="{max(4*s, eye_rx/3)}" ry="{max(5*s, eye_ry/2.5)}" fill="{DARK}"/>
  <ellipse cx="{cx+15*s+eye_offset_x}" cy="{eye_y+5*s}" rx="{max(4*s, eye_rx/3)}" ry="{max(5*s, eye_ry/2.5)}" fill="{DARK}"/>
  
  <!-- Eye highlights -->
  <circle cx="{cx-18*s+eye_offset_x}" cy="{eye_y}" r="2.5" fill="white" opacity="0.9"/>
  <circle cx="{cx+12*s+eye_offset_x}" cy="{eye_y}" r="2.5" fill="white" opacity="0.9"/>
  
  <!-- Eyelids -->
  <path d="M{cx-35*s+eye_offset_x},{eye_y-8*s+eb_off[0]} Q{cx-15*s+eye_offset_x},{eye_y-16*s+eb_off[1]} {cx+2*s+eye_offset_x},{eye_y-8*s+eb_off[0]}" stroke="{WARM_BROWN}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M{cx-2*s+eye_offset_x},{eye_y-8*s+eb_off[0]} Q{cx+15*s+eye_offset_x},{eye_y-16*s+eb_off[1]} {cx+35*s+eye_offset_x},{eye_y-8*s+eb_off[0]}" stroke="{WARM_BROWN}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  
  <!-- Beak -->
  <polygon points="{cx},{cy+2*s} {cx-8*s},{cy+10*s} {cx+8*s},{cy+10*s}" fill="{ZHU_RED}"/>
  <line x1="{cx-8*s}" y1="{cy+10*s}" x2="{cx+8*s}" y2="{cy+10*s}" stroke="{GOLD}" stroke-width="1.2"/>
  
  <!-- Mouth -->
  {mouth}
  
  <!-- Blush -->
  <ellipse cx="{cx-25*s}" cy="{cy+4*s}" rx="8" ry="5" fill="{APRICOT}" opacity="0.35"/>
  <ellipse cx="{cx+25*s}" cy="{cy+4*s}" rx="8" ry="5" fill="{APRICOT}" opacity="0.35"/>
  
  <!-- Ear tufts (Q-path organic curves) -->
  <path d="M{cx-32*s},{cy-28*s} Q{cx-38*s},{cy-52*s} {cx-26*s},{cy-48*s} Q{cx-18*s},{cy-56*s} {cx-22*s},{cy-30*s}" fill="{ZHU_RED}" stroke="{WARM_BROWN}" stroke-width="1"/>
  <path d="M{cx+32*s},{cy-28*s} Q{cx+38*s},{cy-52*s} {cx+26*s},{cy-48*s} Q{cx+18*s},{cy-56*s} {cx+22*s},{cy-30*s}" fill="{ZHU_RED}" stroke="{WARM_BROWN}" stroke-width="1"/>
  
  <!-- Feather texture lines -->
  <path d="M{cx},{cy-40*s} Q{cx-3*s},{cy-20*s} {cx},{cy-5*s}" stroke="{WARM_BROWN}" stroke-width="0.8" fill="none" opacity="0.4"/>
  <path d="M{cx-10*s},{cy-37*s} Q{cx-13*s},{cy-18*s} {cx-10*s},{cy-3*s}" stroke="{WARM_BROWN}" stroke-width="0.7" fill="none" opacity="0.3"/>
  <path d="M{cx+10*s},{cy-37*s} Q{cx+13*s},{cy-18*s} {cx+10*s},{cy-3*s}" stroke="{WARM_BROWN}" stroke-width="0.7" fill="none" opacity="0.3"/>
  
  <!-- Pendant -->
  <circle cx="{cx}" cy="{cy+25*s}" r="8" fill="{GOLD}" opacity="0.8" stroke="{ZHU_RED}" stroke-width="1.5"/>
  <path d="M{cx-3*s},{cy+17*s} L{cx},{cy+22*s} L{cx+3*s},{cy+17*s}" fill="none" stroke="{GOLD}" stroke-width="1"/>
  <!-- Yin-yang inner -->
  <circle cx="{cx}" cy="{cy+25*s}" r="3" fill="{ZHU_RED}" opacity="0.6"/>
'''


def create_panel_svg(title, content_elements, panel_index, width=PANEL_SIZE, height=PANEL_SIZE):
    """Create a complete panel SVG with cream background, border, and content."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
{ollie_defs()}
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="{CREAM}" rx="12"/>
  <rect x="2" y="2" width="{width-4}" height="{height-4}" fill="none" stroke="{WARM_BROWN}" stroke-width="3" rx="10"/>
  
  <!-- Title bar -->
  <text x="{width//2}" y="30" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="{WARM_BROWN}" font-weight="bold">{title}</text>
  <line x1="30" y1="38" x2="{width-30}" y2="38" stroke="{APRICOT}" stroke-width="1"/>
  
{content_elements}
  
  <!-- Panel number -->
  <text x="{width-20}" y="{height-12}" text-anchor="end" font-family="Georgia, serif" font-size="11" fill="{WARM_BROWN}" opacity="0.4">{panel_index}</text>
</svg>'''


# ═══════════════════════════════════════════════════════════════
# COMIC #11 — Cold Progression (感冒六经传变)
# ═══════════════════════════════════════════════════════════════

def panel_11_01():
    """Panel 1: Initial Stage - Ollie sore throat, shivering."""
    content = f'''
  <!-- Thermometer -->
  <rect x="430" y="80" width="12" height="180" rx="6" fill="white" stroke="{WARM_BROWN}" stroke-width="1.5"/>
  <rect x="430" y="100" width="12" height="130" rx="6" fill="{ZHU_RED}" opacity="0.6"/>
  <circle cx="436" cy="265" r="10" fill="{ZHU_RED}" stroke="{WARM_BROWN}" stroke-width="1.5"/>
  <text x="436" y="45" text-anchor="middle" font-family="Georgia, serif" font-size="20" fill="{ZHU_RED}" font-weight="bold">38°C</text>
  
  <!-- Shiver lines around Ollie -->
  <line x1="180" y1="380" x2="175" y2="400" stroke="{WARM_BROWN}" stroke-width="1.5" opacity="0.5"/>
  <line x1="200" y1="385" x2="205" y2="405" stroke="{WARM_BROWN}" stroke-width="1.5" opacity="0.5"/>
  <line x1="320" y1="380" x2="325" y2="400" stroke="{WARM_BROWN}" stroke-width="1.5" opacity="0.5"/>
  <line x1="340" y1="385" x2="335" y2="405" stroke="{WARM_BROWN}" stroke-width="1.5" opacity="0.5"/>
  
  <!-- Tissue box on desk -->
  <rect x="40" y="350" width="60" height="45" rx="4" fill="white" stroke="{WARM_BROWN}" stroke-width="1" opacity="0.7"/>
  <rect x="45" y="340" width="50" height="15" rx="3" fill="white" stroke="{WARM_BROWN}" stroke-width="1" opacity="0.7"/>
  <path d="M50,340 Q55,330 60,340" fill="none" stroke="{APRICOT}" stroke-width="1" opacity="0.5"/>
  
  <!-- Sick Ollie - center, large -->
  {draw_ollie(270, 220, scale=1.2, expression="miserable", facing="front")}
  
  <!-- Left wing touching throat -->
  <ellipse cx="230" cy="200" rx="18" ry="14" fill="{APRICOT}" opacity="0.6" transform="rotate(-20 230 200)"/>
  
  <!-- Symptom text -->
  <text x="270" y="430" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="{WARM_BROWN}" font-style="italic">"Just a scratchy throat..."</text>'''
    
    return create_panel_svg("Panel 1: The Onset", content, 1)


def panel_11_02():
    """Panel 2: Mis-treatment - takes medicine, gets worse."""
    content = f'''
  <!-- Medicine bottle -->
  <rect x="60" y="180" width="35" height="50" rx="5" fill="#e8ddd0" stroke="{WARM_BROWN}" stroke-width="1.5"/>
  <rect x="62" y="175" width="31" height="10" rx="3" fill="{ZHU_RED}" stroke="{WARM_BROWN}" stroke-width="1"/>
  <text x="77" y="183" text-anchor="middle" font-family="sans-serif" font-size="7" fill="white" font-weight="bold">COLD</text>
  <text x="77" y="210" text-anchor="middle" font-family="sans-serif" font-size="5" fill="{WARM_BROWN}">pills</text>
  
  <!-- Spilled pills -->
  <ellipse cx="105" cy="230" rx="6" ry="4" fill="white" stroke="{WARM_BROWN}" stroke-width="0.8"/>
  <ellipse cx="115" cy="220" rx="6" ry="4" fill="white" stroke="{WARM_BROWN}" stroke-width="0.8"/>
  
  <!-- Ollie confused, worse -->
  {draw_ollie(290, 230, scale=1.1, expression="confused", facing="front")}
  
  <!-- Stomach pain - hands on stomach -->
  <ellipse cx="270" cy="270" rx="18" ry="12" fill="{APRICOT}" opacity="0.5" transform="rotate(10 270 270)"/>
  <ellipse cx="310" cy="270" rx="18" ry="12" fill="{APRICOT}" opacity="0.5" transform="rotate(-10 310 270)"/>
  
  <!-- Sweat drops -->
  <ellipse cx="340" cy="180" rx="4" ry="6" fill="#99ccff" opacity="0.5"/>
  <ellipse cx="360" cy="195" rx="3" ry="5" fill="#99ccff" opacity="0.4"/>
  
  <!-- Descending arrow (pathogen going deeper) -->
  <line x1="380" y1="250" x2="380" y2="350" stroke="{ZHU_RED}" stroke-width="3" marker-end="url(#arrowDown)"/>
  <text x="395" y="310" font-family="Georgia, serif" font-size="11" fill="{ZHU_RED}" font-style="italic">deeper</text>
  
  <defs>
    <marker id="arrowDown" markerWidth="10" markerHeight="10" refX="5" refY="10" orient="auto">
      <path d="M0,0 L5,10 L10,0" fill="{ZHU_RED}"/>
    </marker>
  </defs>
  
  <text x="290" y="420" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{WARM_BROWN}" font-style="italic">"Why do I feel worse?"</text>'''
    
    return create_panel_svg("Panel 2: Mis-treatment", content, 2)


def panel_11_03():
    """Panel 3: Accumulation - repeated colds accumulate."""
    content = f'''
  <!-- Background timeline -->
  <line x1="30" y1="260" x2="482" y2="260" stroke="{WARM_BROWN}" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.4"/>
  
  <!-- Year labels -->
  <text x="80" y="285" font-family="sans-serif" font-size="9" fill="{WARM_BROWN}" opacity="0.5">Year 1</text>
  <text x="200" y="285" font-family="sans-serif" font-size="9" fill="{WARM_BROWN}" opacity="0.5">Year 2</text>
  <text x="320" y="285" font-family="sans-serif" font-size="9" fill="{WARM_BROWN}" opacity="0.5">Year 3</text>
  <text x="440" y="285" font-family="sans-serif" font-size="9" fill="{WARM_BROWN}" opacity="0.5">Now</text>
  
  <!-- Series of Ollies getting progressively worse -->
  <!-- Year 1: Normal Ollie -->
  {draw_ollie(75, 220, scale=0.55, expression="neutral")}
  <text x="75" y="180" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="{FERN_GREEN}">"Just a cold"</text>
  
  <!-- Year 2: Tired Ollie -->
  {draw_ollie(190, 225, scale=0.52, expression="miserable")}
  <text x="190" y="175" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="{APRICOT}">"Again?"</text>
  
  <!-- Year 3: Exhausted Ollie -->
  {draw_ollie(305, 230, scale=0.48, expression="struggling")}
  <text x="305" y="175" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="{ZHU_RED}">chronic cough</text>
  
  <!-- Now: Collapsed Ollie -->
  {draw_ollie(420, 240, scale=0.44, expression="miserable")}
  <text x="420" y="180" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="{ZHU_RED}" font-weight="bold">autoimmune?</text>
  
  <!-- Arrows between stages -->
  <line x1="115" y1="250" x2="150" y2="250" stroke="{ZHU_RED}" stroke-width="1.5" marker-end="url(#arrowRight)"/>
  <line x1="230" y1="250" x2="265" y2="250" stroke="{ZHU_RED}" stroke-width="1.5" marker-end="url(#arrowRight)"/>
  <line x1="345" y1="250" x2="380" y2="250" stroke="{ZHU_RED}" stroke-width="1.5" marker-end="url(#arrowRight)"/>
  
  <defs>
    <marker id="arrowRight" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8" fill="{ZHU_RED}"/>
    </marker>
  </defs>
  
  <!-- Warning text -->
  <text x="260" y="430" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{ZHU_RED}" font-style="italic">"Every suppressed cold = compound interest on illness"</text>'''
    
    return create_panel_svg("Panel 3: Accumulation", content, 3)


def panel_11_04():
    """Panel 4: Correct solution - ginger tea, sweat, rest."""
    content = f'''
  <!-- Large steam mug -->
  <ellipse cx="160" cy="310" rx="45" ry="20" fill="#d4c5b0" stroke="{WARM_BROWN}" stroke-width="2"/>
  <rect x="115" y="200" width="90" height="110" rx="8" fill="#d4c5b0" stroke="{WARM_BROWN}" stroke-width="2"/>
  <ellipse cx="160" cy="200" rx="45" ry="15" fill="#e8d5c0" stroke="{WARM_BROWN}" stroke-width="1.5"/>
  <!-- Ginger tea color -->
  <ellipse cx="160" cy="200" rx="38" ry="10" fill="#d4a050" opacity="0.6"/>
  
  <!-- Steam lines -->
  <path d="M140,185 Q135,165 140,145" fill="none" stroke="{CREAM}" stroke-width="2" opacity="0.5"/>
  <path d="M160,180 Q160,155 155,135" fill="none" stroke="{CREAM}" stroke-width="2" opacity="0.5"/>
  <path d="M180,185 Q185,165 180,145" fill="none" stroke="{CREAM}" stroke-width="2" opacity="0.5"/>
  
  <!-- Ginger slices -->
  <ellipse cx="145" cy="195" rx="10" ry="6" fill="#e8b960" opacity="0.7" transform="rotate(-20 145 195)"/>
  <ellipse cx="170" cy="198" rx="8" ry="5" fill="#e8b960" opacity="0.6" transform="rotate(15 170 198)"/>
  
  <!-- Happy Ollie - larger, prominent -->
  {draw_ollie(370, 240, scale=1.2, expression="happy", facing="left")}
  
  <!-- Sweat drops (good sweat) -->
  <ellipse cx="440" cy="170" rx="5" ry="7" fill="#99ccff" opacity="0.4"/>
  <ellipse cx="460" cy="185" rx="4" ry="5" fill="#99ccff" opacity="0.3"/>
  
  <!-- Heart/stars -->
  <text x="430" y="150" font-size="16" fill="{GOLD}" opacity="0.6">&#9829;</text>
  
  <!-- Bottom text -->
  <text x="260" y="430" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="{FERN_GREEN}" font-weight="bold">"Hot tea. Sweat. Rest. Three days."</text>'''
    
    return create_panel_svg("Panel 4: The Right Way", content, 4)


# ═══════════════════════════════════════════════════════════════
# COMIC #16 — Yin-Yang Seesaw (阴阳跷跷板)
# ═══════════════════════════════════════════════════════════════

def panel_16_01():
    """Panel 1: Balance - seesaw level, Ollie calm."""
    content = f'''
  <!-- Seesaw base -->
  <polygon points="256,340 230,400 282,400" fill="{WARM_BROWN}" stroke="{DARK}" stroke-width="2"/>
  
  <!-- Seesaw board (balanced horizontal) -->
  <rect x="60" y="332" width="392" height="12" rx="6" fill="#d4c5b0" stroke="{WARM_BROWN}" stroke-width="2"/>
  
  <!-- Labels -->
  <text x="70" y="370" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="{DARK}" font-weight="bold">YIN</text>
  <text x="442" y="370" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="{DARK}" font-weight="bold">YANG</text>
  
  <!-- Ollie sitting centered on seesaw -->
  {draw_ollie(256, 290, scale=1.1, expression="neutral")}
  
  <!-- Peaceful symbols -->
  <text x="160" y="80" font-size="20" opacity="0.3">&#9728;</text>
  <text x="350" y="100" font-size="16" opacity="0.3">&#9790;</text>
  
  <text x="256" y="430" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="{FERN_GREEN}">"Everything in balance."</text>'''
    
    return create_panel_svg("Panel 1: Balance", content, 1)


def panel_16_02():
    """Panel 2: Yang Excess - seesaw tilted right."""
    content = f'''
  <!-- Seesaw base -->
  <polygon points="256,340 230,400 282,400" fill="{WARM_BROWN}" stroke="{DARK}" stroke-width="2"/>
  
  <!-- Seesaw board (tilted right - yang side down) -->
  <line x1="80" y1="300" x2="432" y2="364" stroke="#d4c5b0" stroke-width="12" stroke-linecap="round"/>
  <line x1="80" y1="300" x2="432" y2="364" stroke="{WARM_BROWN}" stroke-width="2" stroke-linecap="round"/>
  
  <!-- Labels -->
  <text x="70" y="285" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="{WARM_BROWN}" font-weight="bold" opacity="0.5">YIN</text>
  <text x="460" y="380" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="{ZHU_RED}" font-weight="bold">YANG</text>
  
  <!-- Fire/heat symbols on Yang side -->
  <text x="420" y="340" font-size="18" fill="{ZHU_RED}" opacity="0.5">&#128293;</text>
  
  <!-- Ollie on the yang (right) side - surprised/alarmed -->
  {draw_ollie(380, 310, scale=0.9, expression="alarmed", facing="left")}
  
  <text x="256" y="430" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{ZHU_RED}" font-style="italic">"Too much Yang!"</text>'''
    
    return create_panel_svg("Panel 2: Yang Excess", content, 2)


def panel_16_03():
    """Panel 3: Yin Excess - seesaw tilted left."""
    content = f'''
  <!-- Seesaw base -->
  <polygon points="256,340 230,400 282,400" fill="{WARM_BROWN}" stroke="{DARK}" stroke-width="2"/>
  
  <!-- Seesaw board (tilted left - yin side down) -->
  <line x1="80" y1="364" x2="432" y2="300" stroke="#d4c5b0" stroke-width="12" stroke-linecap="round"/>
  <line x1="80" y1="364" x2="432" y2="300" stroke="{WARM_BROWN}" stroke-width="2" stroke-linecap="round"/>
  
  <!-- Labels -->
  <text x="70" y="390" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="#3a5a8a" font-weight="bold">YIN</text>
  <text x="460" y="280" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="{WARM_BROWN}" font-weight="bold" opacity="0.5">YANG</text>
  
  <!-- Cold/ice symbols on Yin side -->
  <text x="120" y="370" font-size="18" fill="#99bbdd" opacity="0.5">&#10052;</text>
  
  <!-- Ollie on the yin (left) side - struggling -->
  {draw_ollie(130, 315, scale=0.9, expression="struggling", facing="right")}
  
  <text x="256" y="430" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="#3a5a8a" font-style="italic">"Too much Yin..."</text>'''
    
    return create_panel_svg("Panel 3: Yin Excess", content, 3)


def panel_16_04():
    """Panel 4: Dynamic Balance - slight rock, Ollie beside, smiling."""
    content = f'''
  <!-- Seesaw base -->
  <polygon points="256,340 230,400 282,400" fill="{WARM_BROWN}" stroke="{DARK}" stroke-width="2"/>
  
  <!-- Seesaw board (slightly tilted, dynamic) -->
  <line x1="90" y1="325" x2="422" y2="339" stroke="#d4c5b0" stroke-width="12" stroke-linecap="round"/>
  <line x1="90" y1="325" x2="422" y2="339" stroke="{WARM_BROWN}" stroke-width="2" stroke-linecap="round"/>
  
  <!-- Labels both highlighted equally -->
  <text x="60" y="360" text-anchor="middle" font-family="Georgia, serif" font-size="17" fill="{DARK}" font-weight="bold">YIN</text>
  <text x="452" y="370" text-anchor="middle" font-family="Georgia, serif" font-size="17" fill="{DARK}" font-weight="bold">YANG</text>
  
  <!-- Ollie standing beside the seesaw, pointing -->
  {draw_ollie(380, 270, scale=1.0, expression="happy", facing="left")}
  
  <!-- Pointing wing -->
  <ellipse cx="340" cy="260" rx="15" ry="10" fill="{APRICOT}" opacity="0.5" transform="rotate(-30 340 260)"/>
  
  <!-- Speech bubble -->
  <ellipse cx="200" cy="155" rx="100" ry="45" fill="white" stroke="{WARM_BROWN}" stroke-width="1.5" filter="url(#softShadow)"/>
  <polygon points="280,195 295,230 300,192" fill="white" stroke="{WARM_BROWN}" stroke-width="1.5"/>
  <text x="200" y="150" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="{DARK}">"Neither side wins.</text>
  <text x="200" y="172" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="{DARK}">That's the point."</text>
  
  <!-- Small sparkle effects -->
  <text x="130" y="270" font-size="12" fill="{GOLD}" opacity="0.6">&#10022;</text>
  <text x="350" y="350" font-size="10" fill="{GOLD}" opacity="0.6">&#10022;</text>
  ''' 
    
    return create_panel_svg("Panel 4: Dynamic Balance", content, 4)


def svg_to_png(svg_content, output_path):
    """Convert SVG to PNG using cairosvg."""
    import cairosvg
    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=output_path)


def compose_grid(png_paths, output_path):
    """Compose 4 PNG panel images into a 2×2 grid."""
    panel_size = PANEL_SIZE
    grid = Image.new("RGB", (GRID_SIZE, GRID_SIZE), CREAM.replace('#', ''))
    
    positions = [
        (0, 0),           # Top-left
        (panel_size, 0),  # Top-right
        (0, panel_size),  # Bottom-left
        (panel_size, panel_size),  # Bottom-right
    ]
    
    for i, (png_path, (x, y)) in enumerate(zip(png_paths, positions)):
        img = Image.open(png_path)
        grid.paste(img, (x, y))
    
    grid.save(output_path, "PNG")
    print(f"  ✅ Composed: {output_path}")


def generate_comic(comic_name, panels, output_name):
    """Generate a complete 4-panel comic: SVGs → PNGs → grid."""
    print(f"\n{'='*60}")
    print(f"Generating {comic_name}...")
    print(f"{'='*60}")
    
    tmp_dir = f"/tmp/tcmway-comics/{comic_name}"
    os.makedirs(tmp_dir, exist_ok=True)
    
    png_paths = []
    
    for i, panel_fn in enumerate(panels):
        svg_content = panel_fn()
        panel_svg_path = f"{tmp_dir}/panel_{i+1}.svg"
        panel_png_path = f"{tmp_dir}/panel_{i+1}.png"
        
        with open(panel_svg_path, 'w') as f:
            f.write(svg_content)
        print(f"  📝 SVG: {panel_svg_path}")
        
        svg_to_png(svg_content, panel_png_path)
        print(f"  🖼️  PNG: {panel_png_path}")
        png_paths.append(panel_png_path)
    
    output_png = os.path.join(OUT_DIR, f"{output_name}.png")
    output_svg = os.path.join(OUT_DIR, f"{output_name}.svg")
    
    compose_grid(png_paths, output_png)
    
    # Also save combined SVG for reference
    print(f"  💾 Final: {output_png}")
    return output_png


if __name__ == "__main__":
    print("🎨 TCM Way Comic Generator — Direction B Standard")
    print(f"   Palette: {ZHU_RED} / {APRICOT} / {GOLD} / {WARM_BROWN}")
    
    # Comic #11: Cold Progression
    generate_comic("comic-11", [panel_11_01, panel_11_02, panel_11_03, panel_11_04], 
                   "comic-11-cold-progression-new")
    
    # Comic #16: Yin-Yang Seesaw
    generate_comic("comic-16", [panel_16_01, panel_16_02, panel_16_03, panel_16_04],
                   "comic-16-yin-yang-seesaw")
    
    print("\n✅ All comics generated!")
