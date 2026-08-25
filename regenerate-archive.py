#!/usr/bin/env python3
"""Regenerate archive.html + category pages + homepage counts from posts directory.
Run after every new article push. No hardcoded numbers.
"""
import os, re, glob, json
from datetime import datetime

BLOG = os.environ.get("GITHUB_WORKSPACE", os.path.expanduser("~/tcmway-blog"))
POSTS_DIR = os.path.join(BLOG, "posts")
CAT_DIR = os.path.join(BLOG, "category")

# ─── Category Definitions（2026-08-25 Foundations 计划：六经齐全 + Foundations 纯化）───
CATEGORIES = {
    # 三大根基 · 基础概念中心：只留真·基础概念
    "foundations": {
        "name": "Foundations",
        "subtitle": "基础概念",
        "desc": "Qi, Yin-Yang, Five Elements, diagnosis, meridians — the building blocks of classical Chinese medicine.",
        "slugs": [
            "01-why-i-share", "03-qi-is-not-magic", "07-six-signs-of-health",
            "13-medicine-character", "14-ten-questions", "15-your-tongue-knows",
            "16-yin-yang-not-good", "17-five-elements-not", "18-your-body-is-a-kingdom",
            "19-jing-qi-shen", "48-what-are-meridians",
            "50-the-yellow-emperors-inner-classic", "51-the-physics-of-acupuncture"
        ]
    },
    # 六经：总览 + 传变 + 张仲景
    "six-stages": {
        "name": "Six Stages · Overview & Transmission",
        "subtitle": "六经总览 · 传变",
        "desc": "The master framework: the Shanghan Lun's six-layer defense, how illness moves between layers, and Zhang Zhongjing.",
        "slugs": [
            "09-six-layer-defense", "11-cold-is-never-just",
            "20-what-zhang-zhongjing", "31-how-a-cold-becomes"
        ]
    },
    "taiyang": {
        "name": "Taiyang · Cold & Defense",
        "subtitle": "太阳 · 表证",
        "desc": "Wind-cold, the body's surface — the first line of defense.",
        "slugs": [
            "08-why-cold-hands", "22-wind-cold-is-not"
        ]
    },
    "yangming": {
        "name": "Yangming · Heat & Digestion",
        "subtitle": "阳明 · 里热",
        "desc": "Internal heat, dampness, digestion.",
        "slugs": [
            "02-exhausted-after-sleep", "06-that-heavy-feeling", "25-yangming-fire"
        ]
    },
    "shaoyang": {
        "name": "Shaoyang · Balance & Emotions",
        "subtitle": "少阳 · 枢机",
        "desc": "Stuck Qi, the Liver, emotions — the half-inside, half-outside space.",
        "slugs": [
            "04-traffic-jam", "05-body-clock", "10-stop-feeding", "12-liver-rules",
            "21-stop-fighting-start-warming", "23-your-fever-might", "32-your-anxiety-is-not"
        ]
    },
    "taiyin": {
        "name": "Taiyin · Digestion Collapses",
        "subtitle": "太阴 · 里虚寒",
        "desc": "When food stops being food — the digestion-focused stage.",
        "slugs": [
            "26-when-food-stops"
        ]
    },
    "shaoyin": {
        "name": "Shaoyin · The Quiet Decline",
        "subtitle": "少阴 · 心肾",
        "desc": "The deepest quiet: exhaustion, cold, and warming the fire.",
        "slugs": [
            "27-the-most-dangerous", "28-yang-tonics", "29-the-fire-inside"
        ]
    },
    "jueyin": {
        "name": "Jueyin · The Last Line",
        "subtitle": "厥阴 · 寒热错杂",
        "desc": "Mixed heat and cold — the body's final line of defense.",
        "slugs": [
            "24-when-your-body", "30-when-the-body-reaches"
        ]
    },
    # 四季 · 节气
    "seasons": {
        "name": "Seasons & Solar Terms",
        "subtitle": "四季 · 节气",
        "desc": "Seasonal living: spring, summer, autumn, and the solar terms.",
        "slugs": [
            "33-how-ancient-china", "35-the-season-your-body", "36-surviving-the-hottest",
            "40-spring-neijing", "41-why-the-ancients-said", "42-the-season-of-letting-go",
            "44-li-qiu", "49-chu-shu"
        ]
    },
    # 食疗 · 生活
    "food-lifestyle": {
        "name": "Food & Daily Life",
        "subtitle": "食疗 · 生活",
        "desc": "Eating, moving, and living with the body's own clock.",
        "slugs": [
            "34-eat-with-the-sun", "37-move-like-water", "38-the-one-ingredient",
            "39-what-tcm-can-learn"
        ]
    },
    # 艾灸
    "moxibustion": {
        "name": "Moxibustion",
        "subtitle": "艾灸",
        "desc": "The warmer half of acupuncture: moxa and the slow kind of heat.",
        "slugs": [
            "45-san-fu-tian", "46-why-your-acupuncturist", "47-moxibustion-vs"
        ]
    },
    # 短文 Field Notes
    "field-notes": {
        "name": "Field Notes",
        "subtitle": "短文",
        "desc": "Short field notes on culture, season, and the body.",
        "slugs": [
            "fn01-drink-more-hot-water", "fn02-chu-shu-end-of-heat",
            "fn03-is-your-body-breaking-down"
        ],
        "archive_only": True
    }
}

# ─── Scan All Articles ───
def scan_articles():
    articles = {}
    fn_counter = 200  # FN 短文伪编号起始（不占长文编号，archive 显示 FN01/FN02...）
    for f in sorted(glob.glob(os.path.join(POSTS_DIR, "*-*.html"))):
        prefix = os.path.basename(f).split("-")[0]
        if prefix.lower().startswith("fn"):
            fn_counter += 1
            num = fn_counter
            display = f"FN{int(prefix[2:]):02d}"
            is_note = True
        else:
            num = int(prefix)
            display = str(num)
            is_note = False
        with open(f) as fh:
            html = fh.read()
        # 2026-08-21：文章标题已从 h2 升为唯一 h1（5b65d71 起），优先取 article 内 h1
        title = re.search(r'<article>.*?<h1>([^<]+)</h1>', html, re.S) or re.search(r'<h2>([^<]+)</h2>', html)
        date = re.search(r'class="meta">([^<]+)', html)
        # 2026-08-19：正文词数（reading time 用，220 wpm）
        mbody = re.search(r'<article>(.*?)</article>', html, re.S)
        plain = re.sub(r'<[^>]+>', ' ', mbody.group(1) if mbody else html)
        wc = len(plain.split())
        # 2026-08-21：首页 excerpt 取文章正文开头文本（剔除 meta/last-updated，
        # 兼容历史文章正文无 <p> 包裹的情况；截 150 字符）
        excerpt = ""
        if mbody:
            body_txt = re.sub(
                r'<div class="meta">.*?</div>|<div class="last-updated".*?</div>',
                " ",
                mbody.group(1),
                flags=re.S,
            )
            body_txt = re.sub(r'<h1>.*?</h1>|<h2>.*?</h2>', " ", body_txt, flags=re.S)
            body_txt = re.sub(r'<span class="note-badge">.*?</span>|<div class="ollie-take-badge">.*?</div>', " ", body_txt, flags=re.S)
            body_txt = re.sub(r'<[^>]+>', " ", body_txt)
            excerpt = re.sub(r'\s+', " ", body_txt).strip()[:150]
        articles[num] = {
            "num": num,
            "display": display,
            "file": os.path.basename(f),
            "title": title.group(1) if title else "Untitled",
            "date": date.group(1).split("&")[0].strip() if date else "",
            "wc": wc,
            "excerpt": excerpt,
            "is_note": is_note,
        }
        try:
            articles[num]["date_obj"] = datetime.strptime(articles[num]["date"], "%B %d, %Y")
        except (ValueError, TypeError):
            articles[num]["date_obj"] = datetime(1970, 1, 1)
    return articles


def reading_time(wc: int) -> int:
    """220 wpm 四舍五入取整，最低 1 分钟。"""
    return max(1, round(wc / 220))

# ─── Assign Categories ───
def assign_categories(articles):
    cat_map = {cat: [] for cat in CATEGORIES}
    uncategorized = {}

    for num, art in articles.items():
        matched = False
        for cat, info in CATEGORIES.items():
            for slug in info["slugs"]:
                if slug in art["file"]:
                    cat_map[cat].append(num)
                    matched = True
                    break
            if matched:
                break
        if not matched:
            uncategorized[num] = art

    return cat_map, uncategorized

# ─── Generate Archive ───
def generate_archive(articles, cat_map, uncategorized=None):
    uncategorized = uncategorized or {}
    header = '''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9S528TPWH"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-G9S528TPWH');</script>

<meta charset="UTF-8">
<link rel="icon" type="image/png" sizes="32x32" href="/images/brand/favicon.png">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>All Articles — TCM Way</title>
<meta name="description" content="Browse all articles from TCM Way — articles on classical Chinese medicine, organized by category.">
<meta property="og:title" content="All Articles — TCM Way">
<meta property="og:description" content="Browse all articles from TCM Way, organized by category.">
<meta property="og:image" content="https://tcmway.net/images/brand/og-card.png">
<meta property="og:url" content="https://tcmway.net/archive.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TCM Way">
<meta name="twitter:card" content="summary">
<link rel="canonical" href="https://tcmway.net/archive.html">
<style>
  :root{--bg:#fdf6ee;--text:#3b2a1a;--accent:#b83a2a;--accent-warm:#e8a87c;--light:#fef0e2;--border:#e8d5c0;--subtle:#8a6d54}
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:Georgia,'Times New Roman',serif;background:var(--bg);color:var(--text);line-height:2;max-width:720px;margin:0 auto;padding:0 1.5rem 3rem}
  header{text-align:center;padding:3rem 0 2rem;border-bottom:2px solid var(--border);margin-bottom:2.5rem}
  header h1{font-size:2rem;font-weight:500;letter-spacing:.08em;color:var(--accent);display:inline-block}
  header h1::after{content:"";display:block;width:90%;height:3px;margin:6px auto 0;background:linear-gradient(90deg,transparent,var(--accent-warm),var(--accent),var(--accent-warm),transparent);border-radius:2px}
  nav{margin-top:1.5rem}
  nav a{color:var(--subtle);text-decoration:none;margin:0 .8rem;font-size:.9rem;letter-spacing:.06em}
  nav a:hover{color:var(--accent)}
  h2{color:var(--accent);font-size:1.25rem;margin:2.2rem 0 .8rem;border-left:4px solid var(--accent-warm);padding-left:.8rem}
  .article-list{list-style:none;padding:0}
  .article-list li{margin:.5rem 0;padding:.6rem 1rem;background:#fff;border-radius:6px;border:1px solid var(--border);display:flex;align-items:flex-start;gap:.8rem;transition:box-shadow .2s}
  .article-list li:hover{box-shadow:0 2px 6px rgba(0,0,0,.06)}
  .art-num{background:var(--accent);color:#fff;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:700;flex-shrink:0;margin-top:3px}
  .art-info{flex:1}
  .art-info a{color:var(--text);text-decoration:none;font-weight:700;font-size:.95rem}
  .art-info a:hover{color:var(--accent)}
  .art-date{font-size:.75rem;color:var(--subtle);text-transform:uppercase;letter-spacing:.05em}
  footer{text-align:center;padding:3rem 0 1rem;color:var(--subtle);font-size:.82rem;border-top:2px solid var(--border);margin-top:3rem;letter-spacing:.04em;line-height:2}
  footer a{color:var(--accent);text-decoration:none}
  .brand-symbol{display:block;margin:0 auto 1.2rem;width:110px;height:auto}
  @media(max-width:600px){body{padding:0 1rem 2rem}header{padding:2rem 0 1.5rem}header h1{font-size:1.8rem}}
</style>
<script type="application/ld+json">
{"@context":"https://schema.org","@graph":[{"@type":"WebSite","name":"TCM Way","url":"https://tcmway.net/","description":"Ancient wisdom, modern life — classical Chinese medicine translated for the modern mind."},{"@type":"Organization","name":"TCM Way","url":"https://tcmway.net/","logo":"https://tcmway.net/images/brand/logo-tcmway-header.png"}]}
</script>
</head>
<body>

<header>
  <img src="/images/brand/logo-tcmway-header.png" width="300" height="300" class="brand-symbol" alt="TCM Way">
  <h1>TCM Way</h1>
  <nav>
    <a href="/">Home</a>
    <a href="/start-here.html">Start Here</a>
    <a href="/archive.html">Archive</a>
    <a href="/podcast/">Podcast</a>
    <a href="/ollies-corner.html">Ollie's Corner</a>
    <a href="/about.html">About</a>
  </nav>
</header>

<p style="text-align:center;color:var(--subtle);margin-bottom:1.5rem">''' + str(len(articles)) + ''' articles · Browse by category or scroll through all</p>
'''

    body = ""
    for cat, info in CATEGORIES.items():
        nums = sorted(cat_map.get(cat, []))
        if not nums:
            continue
        body += f'<h2>{info["name"]}</h2>\n'
        if info.get("subtitle"):
            body += f'<p style="color:var(--subtle);font-size:.88rem;margin-bottom:1rem">{info["subtitle"]}</p>\n'
        body += '<ul class="article-list">\n'
        for num in nums:
            art = articles[num]
            note_badge = ' <span class="note-badge">Field Note</span>' if art.get("is_note") else ''
            body += f'  <li><span class="art-num">{art.get("display", num)}</span><span class="art-info"><a href="/posts/{art["file"]}">{art["title"]}</a>{note_badge}<br><span class="art-date">{art["date"]} &middot; {reading_time(art["wc"])} min read</span></span></li>\n'
        body += '</ul>\n'

    # Fallback: render any uncategorized articles so new posts never silently vanish
    if uncategorized:
        body += '<h2>More Articles</h2>\n'
        body += '<ul class="article-list">\n'
        for num in sorted(uncategorized):
            art = articles[num]
            note_badge = ' <span class="note-badge">Field Note</span>' if art.get("is_note") else ''
            body += f'  <li><span class="art-num">{art.get("display", num)}</span><span class="art-info"><a href="/posts/{art["file"]}">{art["title"]}</a>{note_badge}<br><span class="art-date">{art["date"]} &middot; {reading_time(art["wc"])} min read</span></span></li>\n'
        body += '</ul>\n'

    footer = '''
<footer>
  <div style="text-align:center;padding-top:12px;border-top:1px solid #e8dcc8;">
    <img src="/images/brand/logo-tcmway-header.png" width="300" height="300" alt="TCM Way" style="max-width:140px;width:100%;height:auto;vertical-align:middle;margin-right:6px;">
    <span style="color:#997a5c;font-size:0.85rem;">TCM Way &mdash; Ancient wisdom, modern life.</span>
  </div>
</footer>
</body>
</html>'''

    return header + body + footer

# ─── Update Homepage Counts ───
def update_homepage(cat_map, articles):
    with open(os.path.join(BLOG, "index.html")) as f:
        html = f.read()

    # --- Category counts ---
    for cat, nums in cat_map.items():
        count = len(nums)
        if cat in CATEGORIES:
            pattern = rf'(<a href="/category/{cat}.html">.*?<div class="card-count">)\d+ articles'
            repl = rf'\g<1>{count} articles'
            html = re.sub(pattern, repl, html, count=1, flags=re.DOTALL)

    total = len(articles)

    # --- Hero card: update to latest article ---
    # 2026-08-20 修复：FN 短文伪编号(200+) > 长文编号，按 max(key) 排序会把短文排在长文前面。
    # 改为按发布日期排序（同日期按伪编号降序兜底）。
    latest_art = max(articles.values(), key=lambda a: (a["date_obj"], a["num"]))
    art = latest_art
    # 2026-08-13 修复：旧逻辑只替换编号前缀（45→46），slug 保留旧文章的，
    # 生成 46-san-fu-tian-... 幽灵链接（#45 实战#46 首页 Latest 404）。
    # 改为整体替换为最新文章的完整文件名。
    hero_pattern = r'(<a href=")posts/[^"]*(" class="hero-card">)'
    html = re.sub(hero_pattern, rf'\g<1>posts/{art["file"]}\2', html)
    hero_title = r'(<div class="hero-title">)[^<]*(</div>)'
    html = re.sub(hero_title, rf'\g<1>{art["title"]}\2', html)
    hero_meta = r'(<div class="hero-meta">)[^<]*(</div>)'
    html = re.sub(hero_meta, rf'\g<1>{art["date"]} &middot; By Ollie &middot; {reading_time(art["wc"])} min read · Read →\2', html)
    if re.search(r'<div class="hero-excerpt">', html):
        hero_excerpt = r'(<div class="hero-excerpt">)[^<]*(</div>)'
        html = re.sub(hero_excerpt, rf'\g<1>{art["excerpt"]}\2', html, count=1)
    else:
        hero_excerpt = r'(<div class="hero-title">[^<]*</div>)(\s*)'
        html = re.sub(hero_excerpt, rf'\g<1>\n    <div class="hero-excerpt">{art["excerpt"]}</div>\2', html, count=1)

    # --- Recent posts: rebuild 5 most recent ---
    recent_nums = [
        a["num"] for a in sorted(
            articles.values(),
            key=lambda a: (a["date_obj"], a["num"]),
            reverse=True,
        )[:5]
    ]
    recent_pattern = r'(<!-- ═══ RECENT POSTS ═══ -->\n<h2[^>]*>Recent Articles</h2>\n\n).*?(<div class="view-all">)'
    recent_html = '\n'.join([
        (f'<div class="post">\n  <h2><a href="posts/{articles[n]["file"]}"><img src="images/ollie-mini-80.png" width="80" height="80" class="mini-owl" alt="">{articles[n]["title"]}</a></h2>\n'
         + ('  <span class="note-badge">Field Note</span>\n' if articles[n].get("is_note") else '')
         + f'  <div class="date">{articles[n]["date"]} &middot; By Ollie &middot; {reading_time(articles[n]["wc"])} min read</div>\n  <div class="excerpt"><p>{articles[n].get("excerpt", "")}</p></div>\n</div>')
        for n in recent_nums
    ])
    html = re.sub(recent_pattern, rf'\g<1>\n{recent_html}\n\n\2', html, count=1, flags=re.DOTALL)

    # --- View all count ---
    html = re.sub(r'View all \d+ articles', f'View all {total} articles', html)

    with open(os.path.join(BLOG, "index.html"), "w") as f:
        f.write(html)
    return total

# ─── Main ───
def generate_category_pages(articles, cat_map):
    """Render one page per visible category (archive_only 不生成独立页)。2026-08-25 新增。"""
    nav = ('<nav>\n'
           '    <a href="/">Home</a>\n'
           '    <a href="/start-here.html">Start Here</a>\n'
           '    <a href="/archive.html">Archive</a>\n'
           '    <a href="/podcast/">Podcast</a>\n'
           '    <a href="/ollies-corner.html">Ollie\'s Corner</a>\n'
           '    <a href="/about.html">About</a>\n'
           '  </nav>')
    css = '''  :root {
    --bg: #fdf6ee;
    --text: #3b2a1a;
    --accent: #b83a2a;
    --accent-warm: #e8a87c;
    --light: #fef0e2;
    --border: #e8d5c0;
    --subtle: #8a6d54;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  .brand-symbol{display:block;margin:0 auto 1.2rem;width:110px;height:auto}
  body { font-family: Georgia, 'Times New Roman', serif; background: var(--bg); color: var(--text); line-height: 1.9; max-width: 720px; margin: 0 auto; padding: 2rem 1.5rem; }
  header { text-align: center; padding: 2rem 0 2rem; border-bottom: 1px solid var(--border); margin-bottom: 2.5rem; }
  header h1 { font-size: 2rem; font-weight: normal; letter-spacing: 0.04em; color: var(--accent); }
  nav { margin-top: 1rem; }
  nav a { color: var(--subtle); text-decoration: none; margin: 0 0.6rem; font-size: 0.92rem; }
  nav a:hover, nav a.active { color: var(--accent); }
  nav a.active { font-weight: bold; }
  h2 { font-weight: normal; color: var(--accent); margin: 2rem 0 1rem; font-size: 1.4rem; border-left: 4px solid var(--accent-warm); padding-left: 0.8rem; }
  h3 { font-weight: normal; color: var(--accent); margin: 0 0 0.3rem; font-size: 1.15rem; }
  p { margin-bottom: 1.2rem; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .card { background: white; border: 1px solid var(--border); border-radius: 8px; padding: 1.2rem 1.5rem; margin: 1rem 0; }
  .card .desc { color: var(--subtle); font-size: 0.92rem; margin: 0; }
  .back { margin-top: 2rem; font-size: 0.95rem; }
  footer { text-align: center; padding: 2rem 0; color: var(--subtle); font-size: 0.85rem; border-top: 1px solid var(--border); margin-top: 3rem; }
  footer a { color: var(--accent); text-decoration: none; }
  @media(max-width:600px){.brand-symbol{width:120px}}
  @media(max-width:400px){.brand-symbol{width:100px}}'''
    footer = ('<footer>\n'
              '  <p>&copy; 2026 TCM Way. All illustrations and written content are copyrighted.</p>\n'
              '  <p><a href="/disclaimer.html">Medical Disclaimer</a> &middot; <a href="/privacy.html">Privacy</a> &middot; <a href="/contact.html">Contact</a> &middot; <a href="/rss.xml">RSS</a></p>\n'
              '  <div style="text-align:center;padding-top:12px;border-top:1px solid #e8dcc8;">\n'
              '    <img width="300" height="300" src="/images/brand/logo-tcmway-header.png" alt="TCM Way" style="max-width:140px;width:100%;height:auto;vertical-align:middle;margin-right:6px;">\n'
              '    <span style="color:#997a5c;font-size:0.85rem;">TCM Way &mdash; Ancient wisdom, modern life.</span>\n'
              '  </div>\n'
              '</footer>\n')
    generated = 0
    for cat, info in CATEGORIES.items():
        if info.get("archive_only"):
            continue
        nums = sorted(cat_map.get(cat, []))
        cards = ""
        for num in nums:
            art = articles[num]
            cards += (f'    <div class="card">\n'
                      f'      <h3><a href="/posts/{art["file"]}">{art["title"]}</a></h3>\n'
                      f'      <p class="desc">{art.get("excerpt", "")} &middot; {art["date"]}</p>\n'
                      f'    </div>\n')
        if not cards:
            cards = '    <p>Articles are on the way.</p>\n'
        subtitle = info.get("subtitle", "")
        subtitle_html = (f' <span style="font-size:0.7em;color:var(--subtle);font-weight:normal;">{subtitle}</span>'
                         if subtitle else "")
        html = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
                '<!-- Google tag (gtag.js) -->\n'
                '<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9S528TPWH"></script>\n'
                '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-G9S528TPWH\');</script>\n'
                '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                f'<title>{info["name"]} — TCM Way</title>\n'
                f'<link rel="canonical" href="https://tcmway.net/category/{cat}.html">\n'
                '<link rel="icon" type="image/png" sizes="32x32" href="/images/brand/favicon.png">\n'
                f'<meta name="description" content="{info["desc"]}">\n'
                f'<meta property="og:title" content="{info["name"]} — TCM Way">\n'
                f'<meta property="og:description" content="{info["desc"]}">\n'
                '<meta property="og:image" content="https://tcmway.net/images/brand/og-card.png">\n'
                f'<meta property="og:url" content="https://tcmway.net/category/{cat}.html">\n'
                '<meta property="og:type" content="website">\n<meta property="og:site_name" content="TCM Way">\n'
                '<meta name="twitter:card" content="summary">\n'
                f'<style>\n{css}\n</style>\n'
                '<script type="application/ld+json">\n'
                '{"@context":"https://schema.org","@graph":[{"@type":"WebSite","name":"TCM Way","url":"https://tcmway.net/","description":"Ancient wisdom, modern life — classical Chinese medicine translated for the modern mind."},{"@type":"Organization","name":"TCM Way","url":"https://tcmway.net/","logo":"https://tcmway.net/images/brand/logo-tcmway-header.png"}]}\n'
                '</script>\n</head>\n<body>\n'
                '<header>\n  <img width="300" height="300" src="/images/brand/logo-tcmway-header.png" alt="TCM Way — yin-yang pendant" class="brand-symbol">\n'
                '  <h1>TCM Way</h1>\n  ' + nav + '\n</header>\n'
                f'<h2>{info["name"]}{subtitle_html}</h2>\n'
                f'<p>{info["desc"]}</p>\n'
                + cards +
                '<p class="back">&larr; <a href="/start-here.html">Start Here</a> &middot; <a href="/archive.html">All articles</a></p>\n'
                + footer +
                '</body>\n</html>\n')
        path = os.path.join(CAT_DIR, f"{cat}.html")
        with open(path, "w") as f:
            f.write(html)
        generated += 1
    print(f"✅ category pages regenerated: {generated}")


def main():
    articles = scan_articles()
    cat_map, uncategorized = assign_categories(articles)

    print(f"Articles: {len(articles)}")
    print(f"Categories:")
    for cat, nums in cat_map.items():
        print(f"  {cat}: {len(nums)} articles")

    if uncategorized:
        print(f"\n⚠️  Uncategorized ({len(uncategorized)}):")
        for num, art in sorted(uncategorized.items()):
            print(f"  #{num}: {art['title'][:60]}")

    # Generate archive
    archive_html = generate_archive(articles, cat_map, uncategorized)
    with open(os.path.join(BLOG, "archive.html"), "w") as f:
        f.write(archive_html)
    print(f"\n✅ archive.html regenerated")

    # Generate category pages (2026-08-25 Foundations 计划新增)
    generate_category_pages(articles, cat_map)

    # Update homepage counts + hero + recent
    total = update_homepage(cat_map, articles)
    print(f"✅ index.html updated — {total} articles")

if __name__ == "__main__":
    main()
