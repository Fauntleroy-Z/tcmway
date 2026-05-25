import os
import re

# === Direction B: 赤縁 Warm Color CSS ===
# Applied to all post pages

BLOG_CSS = """
  :root {
    --bg: #fdf6ee;
    --text: #3b2a1a;
    --accent: #b83a2a;
    --accent-warm: #e8a87c;
    --light: #fef0e2;
    --border: #e8d5c0;
    --subtle: #8a6d54;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: Georgia, 'Times New Roman', 'Noto Serif SC', serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.9;
    max-width: 720px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
  }

  header {
    text-align: center;
    padding: 2.5rem 0 2rem;
    border-bottom: 2px solid var(--border);
    margin-bottom: 2.5rem;
  }

  /* Ollie brand symbol in header */
  .brand-symbol {
    display: block;
    margin: 0 auto 1rem;
    width: 72px;
    height: 72px;
  }

  header h1 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--accent);
    position: relative;
    display: inline-block;
  }

  header h1::after {
    content: "";
    position: absolute;
    bottom: -7px;
    left: 5%;
    width: 90%;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--accent-warm), var(--accent), var(--accent-warm), transparent);
    border-radius: 2px;
  }

  header p {
    color: var(--subtle);
    font-style: italic;
    margin-top: 0.8rem;
    font-size: 1rem;
  }

  nav {
    margin-top: 1.3rem;
  }

  nav a {
    color: var(--subtle);
    text-decoration: none;
    margin: 0 0.8rem;
    font-size: 0.9rem;
    letter-spacing: 0.05em;
    font-family: Georgia, serif;
    transition: color 0.3s;
  }

  nav a:hover { color: var(--accent); }

  article h1 {
    font-size: 1.8rem;
    font-weight: normal;
    color: var(--text);
    margin-bottom: 0.6rem;
    line-height: 1.5;
    font-style: italic;
  }

  .meta {
    color: var(--subtle);
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    margin-bottom: 2.2rem;
  }

  h2 {
    font-weight: 700;
    font-size: 1.2rem;
    color: var(--accent);
    margin: 2.2rem 0 1rem;
    letter-spacing: 0.03em;
    border-left: 4px solid var(--accent-warm);
    padding-left: 1rem;
  }

  p { margin-bottom: 1.4rem; }

  blockquote {
    border-left: none;
    background: var(--light);
    margin: 2rem 0;
    padding: 1.8rem 2rem;
    color: var(--accent);
    font-style: italic;
    font-size: 1.05rem;
    line-height: 1.9;
    border-radius: 2px;
    position: relative;
  }

  blockquote::before {
    content: "✦";
    display: block;
    text-align: center;
    color: var(--accent-warm);
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
  }

  .highlight-box {
    background: linear-gradient(135deg, var(--light) 0%, #fde8d8 100%);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.8rem 2rem;
    margin: 2rem 0;
    text-align: center;
    position: relative;
    overflow: hidden;
  }

  .highlight-box::before {
    content: "";
    position: absolute;
    top: -20px;
    right: -20px;
    width: 80px;
    height: 80px;
    background: var(--accent);
    opacity: 0.06;
    border-radius: 50%;
  }

  .highlight-box p { margin-bottom: 0.5rem; font-weight: 700; color: var(--accent); }

  .checklist {
    background: var(--light);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.5rem 1.5rem 1.5rem 2rem;
    margin: 1.5rem 0;
  }

  .checklist p {
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 0.8rem;
    font-size: 0.95rem;
    letter-spacing: 0.03em;
  }

  .checklist ul { list-style: none; padding: 0; }
  .checklist li {
    padding: 0.45rem 0 0.45rem 1.8rem;
    position: relative;
    font-size: 0.92rem;
    border-bottom: 1px dashed var(--border);
    line-height: 1.7;
  }
  .checklist li:last-child { border-bottom: none; }
  .checklist li::before {
    content: "☽";
    position: absolute;
    left: 0;
    color: var(--accent-warm);
    font-size: 0.9rem;
  }

  .sign {
    display: block;
    text-align: right;
    color: var(--subtle);
    font-style: italic;
    margin: 1.5rem 0 1rem;
    font-size: 0.95rem;
  }

  .comic-break {
    display: block;
    margin: 2.5rem auto;
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(184,58,42,0.12);
  }

  footer {
    text-align: center;
    padding: 2.5rem 0 1rem;
    color: var(--subtle);
    font-size: 0.82rem;
    border-top: 2px solid var(--border);
    margin-top: 3.5rem;
    letter-spacing: 0.04em;
    line-height: 2;
  }

  footer a {
    color: var(--accent);
    text-decoration: none;
    transition: color 0.2s;
  }

  footer a:hover { color: var(--gold, #c9a84c); }

  .back { display: block; margin: 2rem 0 0; color: var(--accent); text-decoration: none; }
  .back:hover { text-decoration: underline; }
"""

POSTS_DIR = r"C:\Users\Administrator\tcmway-blog\posts"

def update_post_css(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace :root CSS variables
    content = re.sub(
        r':root\s*\{[^}]+\}',
        ':root {' + BLOG_CSS.split('{', 1)[1].split('}')[0] + '}',
        content,
        flags=re.DOTALL
    )

    # 2. Replace image references: owl-mascot-v3-mini.webp -> ollie-mini-warm.svg
    content = content.replace('images/owl-mascot-v3-mini.webp', 'images/ollie-mini-warm.svg')
    content = content.replace('images/owl-mascot-v3.png', 'images/ollie-warm.svg')
    content = content.replace('images/owl-mascot.png', 'images/ollie-warm.svg')
    content = content.replace('images/owl-mascot.webp', 'images/ollie-warm.svg')

    # 3. Update OG image
    content = content.replace('images/owl-mascot-v3.png', 'images/ollie-warm.svg')

    # 4. Add brand-symbol SVG to header (if not already present)
    brand_svg = '''  <!-- Ollie brand symbol (Direction B warm) -->
  <svg class="brand-symbol" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="36" stroke="#b83a2a" stroke-width="2" fill="none" stroke-dasharray="4 3"/>
    <circle cx="40" cy="42" r="16" fill="none" stroke="#b83a2a" stroke-width="1.8"/>
    <circle cx="33" cy="38" r="4.5" fill="none" stroke="#b83a2a" stroke-width="1.5"/>
    <circle cx="47" cy="38" r="4.5" fill="none" stroke="#b83a2a" stroke-width="1.5"/>
    <circle cx="33" cy="38" r="1.8" fill="#b83a2a"/>
    <circle cx="47" cy="38" r="1.8" fill="#b83a2a"/>
    <polygon points="40,48 37,52 43,52" fill="#b83a2a"/>
    <circle cx="40" cy="54" r="3" stroke="#c9a84c" stroke-width="1" fill="none" opacity="0.6"/>
    <polygon points="26,28 22,16 32,26" fill="none" stroke="#b83a2a" stroke-width="1.3"/>
    <polygon points="54,28 58,16 48,26" fill="none" stroke="#b83a2a" stroke-width="1.3"/>
  </svg>'''

    # Insert brand-symbol after <header> tag
    if 'class="brand-symbol"' not in content:
        content = re.sub(
            r'(<header>\s*)',
            r'\1\n' + brand_svg + '\n',
            content
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Updated: {os.path.basename(filepath)}")

# Run
if __name__ == '__main__':
    for fname in os.listdir(POSTS_DIR):
        if fname.endswith('.html'):
            update_post_css(os.path.join(POSTS_DIR, fname))

    print("\n✅ All posts updated with Direction B styling.")
