#!/usr/bin/env python3
"""生成 llms.txt（LLM 友好站点索引，2026-09-05 起）。

格式参考 llmstxt.org：H1 站点名 + 简介，正文为「- [标题](URL): 一句话描述」。
数据源：posts/*.html 的 <title> 与 meta description；播客/关于页手工补充。
"""
import glob
import html
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://tcmway.net"


def clean(t):
    return html.unescape(re.sub(r"<[^>]+>", " ", t)).strip()


def title_of(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    t = clean(m.group(1)) if m else os.path.basename(path)
    # 去掉站点后缀 " — TCM Way"
    t = re.sub(r"\s*[-—]\s*TCM Way\s*$", "", t)
    return t


def desc_of(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
    if not m:
        m = re.search(r'name="description"\s+content="(.*?)"', s, re.S)
    return clean(m.group(1))[:140] if m else ""


def main():
    lines = []
    lines.append("# TCM Way")
    lines.append("")
    lines.append("> Classical Chinese medicine explained in plain English — no jargon, no")
    lines.append("> mysticism. Articles, an audio podcast, and illustrations for a Western")
    lines.append("> audience. This file lists the site's key pages for LLM access.")
    lines.append("")

    # 核心入口
    lines.append("## Start Here")
    lines.append("")
    lines.append("- [TCM Way home](https://tcmway.net/): Site home and latest articles.")
    lines.append("- [Archive](https://tcmway.net/archive.html): Full article archive.")
    lines.append("- [Podcast — East & Inner with Ollie](https://tcmway.net/podcast/): Audio podcast,")
    lines.append("  one episode per blog article, plus an RSS feed at /podcast/feed.xml.")
    lines.append("- [About](https://tcmway.net/about.html): What TCM Way is and who writes it.")
    lines.append("")

    lines.append("## Articles")
    lines.append("")
    def sort_key(path):
        """确定性排序键：数字序列降序（近似发布先后）+ 文件名升序兜底。

        兜底键不可省：fn01 与 01 的数字键同为 (1,)，7 组 fn/数字文章同键。
        只用数字键时先后由 glob.glob() 的目录枚举顺序决定，而 APFS 与 CI 的
        ext4 枚举顺序不同 → 每次部署重生成都会翻转几行 → 噪声 auto-commit
        （2026-09-22 定位，9/15 起共 5 次）。文件名唯一，故加入兜底键后
        结果与输入顺序无关。
        """
        base = os.path.basename(path)
        nums = tuple(-int(x) for x in re.findall(r"\d+", base))
        return (nums, base)

    posts = sorted(
        glob.glob(os.path.join(ROOT, "posts", "*.html")),
        key=sort_key,
    )
    for p in posts:
        slug = os.path.basename(p)
        t = title_of(p)
        d = desc_of(p)
        entry = f"- [{t}]({BASE}/posts/{slug})"
        if d:
            entry += f": {d}"
        lines.append(entry)

    out = os.path.join(ROOT, "llms.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"llms.txt 生成完成：{len(posts)} 篇文章")


if __name__ == "__main__":
    main()
