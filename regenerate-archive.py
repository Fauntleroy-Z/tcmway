#!/usr/bin/env python3
"""Regenerate archive.html + category pages + homepage counts from posts directory.
Run after every new article push. No hardcoded numbers.
"""
import os, re, glob, json
from datetime import datetime

BLOG = os.environ.get("GITHUB_WORKSPACE", os.path.expanduser("~/tcmway-blog"))
POSTS_DIR = os.path.join(BLOG, "posts")
CAT_DIR = os.path.join(BLOG, "category")

# ─── Category Definitions ───
CATEGORIES = {
    "foundations": {
        "name": "Foundations",
        "subtitle": "基础概念",
        "desc": "Qi, Yin-Yang, Five Elements, diagnosis — the building blocks of classical Chinese medicine.",
        "slugs": [
            "01-why-i-share", "02-exhausted-after-sleep", "03-qi-is-not-magic",
            "04-traffic-jam", "07-six-signs-of-health", "13-medicine-character",
            "14-ten-questions", "15-your-tongue-knows", "16-yin-yang-not-good",
            "17-five-elements-not", "18-your-body-is-a-kingdom", "19-jing-qi-shen",
            "33-how-ancient-china", "34-eat-with-the-sun", "35-the-season-your-body",
            "36-surviving-the-hottest", "37-move-like-water", "38-the-one-ingredient",
            "39-what-tcm-can-learn", "40-spring-neijing-reinvention",
            "41-why-the-ancients-said", "42-the-season-of-letting-go",
            "44-li-qiu", "45-san-fu-tian", "46-why-your-acupuncturist",
            "47-moxibustion-vs", "48-what-are-meridians", "49-chu-shu",
            "50-the-yellow-emperors", "51-the-physics-of-acupuncture",
            "fn01-drink-more-hot-water",
            "fn02-chu-shu-end-of-heat"
        ]
    },
    "taiyang": {
        "name": "Cold & Defense",
        "subtitle": "太阳 · Taiyang",
        "desc": "Wind-cold, fever, the body's surface — the first line of defense.",
        "slugs": [
            "08-why-cold-hands", "09-six-layer-defense", "11-cold-is-never-just",
            "22-wind-cold-is-not"
        ]
    },
    "yangming": {
        "name": "Heat & Digestion",
        "subtitle": "阳明 · Yangming",
        "desc": "Internal Heat · Dampness · Fever",
        "slugs": [
            "06-that-heavy-feeling", "23-your-fever-might", "25-yangming-fire",
            "fn04-shang-huo-the-fire"
        ]
    },
    "shaoyang": {
        "name": "Balance & Emotions",
        "subtitle": "少阳 · Shaoyang",
        "desc": "Stuck Qi · Liver · Emotions",
        "slugs": [
            "05-body-clock", "10-stop-feeding", "12-liver-rules",
            "21-stop-fighting-start-warming", "24-when-your-body", "32-your-anxiety-is-not",
            "fn03-is-your-body-breaking-down"
        ]
    },
    "six-stages": {
        "name": "Six Stages Deep Dive",
        "subtitle": "",
        "desc": "",
        "slugs": [
            "20-what-zhang-zhongjing", "26-when-food-stops", "27-the-most-dangerous",
            "28-yang-tonics", "29-the-fire-inside", "30-when-the-body-reaches",
            "31-how-a-cold-becomes"
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
        # 2026-08-27 修复：h1 内含 <br> 时旧正则 `([^<]+)` 匹配失败，
        # 会回退取到第一个 h2（章节小标题），导致 archive 显示错误标题。
        # 改以 <title> 标签为索引标题源（archive/RSS/分类页三者一致）；
        # 无 <title> 时回退到 h1 去标签文本。
        tmatch = re.search(r'<title>(.*) — TCM Way</title>', html, re.S)
        if tmatch:
            title = tmatch.group(1).strip()
        else:
            hmatch = re.search(r'<article>.*?<h1>(.*?)</h1>', html, re.S) or re.search(r'<h2>(.*?)</h2>', html)
            title = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', hmatch.group(1))).strip() if hmatch else "Untitled"
        date = re.search(r'class="meta">([^<]+)', html)
        # 2026-08-27：分类页卡片 desc 复用文章 meta description（与手写卡片口径一致）
        mdesc = re.search(r'<meta name="description" content="(.*?)">', html, re.S)
        desc = mdesc.group(1).strip() if mdesc else ""
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
            "title": title,
            "date": date.group(1).split("&")[0].strip() if date else "",
            "wc": wc,
            "excerpt": excerpt,
            "desc": desc or excerpt,
            "is_note": is_note,
        }
        try:
            articles[num]["date_obj"] = datetime.strptime(articles[num]["date"], "%B %d, %Y")
        except (ValueError, TypeError):
            articles[num]["date_obj"] = datetime(1970, 1, 1)
        # 2026-08-26 根除：未来日期（Asia/Shanghai）文章不进入任何索引，
        # 防止未确认/未到发布日的文章被 deploy 带上线（#50/#51 事故复盘）
        try:
            from zoneinfo import ZoneInfo
            _today = datetime.now(ZoneInfo("Asia/Shanghai")).date()
        except Exception:
            _today = datetime.now().date()
        if articles[num]["date_obj"].date() > _today:
            print(f"  ⏭ 跳过未来日期文章（未到发布日）: {os.path.basename(f)} ({articles[num]['date']})")
            del articles[num]
            continue
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

# ─── Update Category Pages ───
def update_category_pages(cat_map, articles):
    """只重建分类页的卡片区（2026-08-27 修复：分类页与 archive 不同步）。

    页面骨架（title/meta/h2/intro/nav/footer）为精编内容，保持原样不动；
    卡片区由 CATEGORIES + 各文章 meta description 确定性重建。
    """
    card_pat = re.compile(r'<div class="card">.*</div>\n(?=\s*<p class="back">)', re.S)
    for cat, info in CATEGORIES.items():
        if info.get("archive_only"):
            continue
        path = os.path.join(CAT_DIR, f"{cat}.html")
        if not os.path.exists(path):
            print(f"⚠️  分类页不存在，跳过: {cat}")
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()
        m = card_pat.search(html)
        if not m:
            print(f"⚠️  未找到卡片区，跳过: {cat}")
            continue
        nums = sorted(cat_map.get(cat, []))
        cards = ""
        for i, num in enumerate(nums):
            art = articles[num]
            desc = art.get("desc") or art.get("excerpt", "")
            indent = "    " if i else ""
            cards += (f'{indent}<div class="card">\n'
                      f'      <h3><a href="/posts/{art["file"]}">{art["title"]}</a></h3>\n'
                      f'      <p class="desc">{desc}</p>\n'
                      f'    </div>\n')
        new_html = html[:m.start()] + cards + html[m.end():]
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"✅ category/{cat}.html 卡片区重建 — {len(nums)} cards")


def sync_rss(articles):
    """2026-09-01：RSS 增量补全——发布新文章后 rss.xml 长期漏条目（#50/#51 两次手动补），
    现自动对比 posts/ 与现有 guid，补缺失 item 并按日期倒序重排，更新 lastBuildDate。
    现有 item 的描述保留原样，不覆盖手写内容。"""
    rss_path = os.path.join(BLOG, "rss.xml")
    if not os.path.exists(rss_path):
        print("⚠️  rss.xml not found")
        return
    with open(rss_path, encoding="utf-8") as f:
        rss = f.read()

    head = rss
    items = []
    first = re.search(r'<item>.*?</item>', rss, re.DOTALL)
    if first:
        head = rss[:first.start()]
        items = re.findall(r'<item>.*?</item>', rss, re.DOTALL)

    def xml_escape(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    seen = set()
    out_items = []

    for art in sorted(articles.values(), key=lambda a: (a["date_obj"], a["num"]), reverse=True):
        guid = f'https://tcmway.net/posts/{art["file"]}'
        if guid in seen:
            continue
        seen.add(guid)
        existing = next((it for it in items if f'<guid>{guid}</guid>' in it), None)
        if existing:
            out_items.append(existing)
            continue
        pd = art["date_obj"].strftime("%a, %d %b %Y 00:00:00 +0800")
        desc = xml_escape(art.get("desc") or art.get("excerpt", "")).strip()
        out_items.append(
            f'  <item>\n'
            f'    <title>{xml_escape(art["title"])}</title>\n'
            f'    <link>{guid}</link>\n'
            f'    <description>{desc}</description>\n'
            f'    <pubDate>{pd}</pubDate>\n'
            f'    <guid>{guid}</guid>\n'
            f'  </item>'
        )

    # 防御性兜底：保留 posts/ 中已不存在的历史 item（不应发生）
    for it in items:
        g = re.search(r'<guid>(.*?)</guid>', it)
        if g and g.group(1) not in seen:
            seen.add(g.group(1))
            out_items.append(it)

    now = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")
    head = re.sub(
        r'<lastBuildDate>.*?</lastBuildDate>',
        f'<lastBuildDate>{now}</lastBuildDate>',
        head,
        flags=re.S,
    )
    with open(rss_path, "w", encoding="utf-8") as f:
        f.write(head + "\n".join(out_items) + "\n</channel>\n</rss>\n")
    print(f"✅ rss.xml synced — {len(out_items)} items")


# ─── Main ───
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

    # Update homepage counts + hero + recent
    total = update_homepage(cat_map, articles)
    print(f"✅ index.html updated — {total} articles")

    # Update category page cards (2026-08-27: keep category pages in sync with archive)
    update_category_pages(cat_map, articles)

    # 2026-09-01：RSS 增量补全（防发布漏条目）
    sync_rss(articles)

if __name__ == "__main__":
    main()
