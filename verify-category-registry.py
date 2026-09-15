#!/usr/bin/env python3
"""发布门禁：确保 posts/ 下每篇文章都注册进 regenerate-archive.py 的 CATEGORIES。

背景（2026-09-15 · #55 复盘）：
    publish 提交把新文章卡片手工加进 category/*.html 后，若忘记在
    regenerate-archive.py 的 CATEGORIES 里登记 slug，CI 的
    「Regenerate archive + counts」会按注册表重建，把该文踢出分类页、
    并塞进 archive.html 页尾的「More Articles」兜底节 —— 线上回退，且静默。
    #44/45/46（09-12）与 #55（09-15）两次同因复发，故在 CI 前硬拦。

判定：注册 = CATEGORIES 中任一 slug 是文件名的子串（与 regenerate-archive.py 的
      `if slug in art["file"]` 语义一致）。

用法：
    python3 verify-category-registry.py            # 退出码 0 = 全部已注册
    python3 verify-category-registry.py --warn     # 只告警，不失败（本地可选）
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
GENERATOR = os.path.join(ROOT, "regenerate-archive.py")


def load_slugs():
    src = open(GENERATOR, encoding="utf-8").read()
    blocks = re.findall(r'"slugs": \[(.*?)\]', src, re.S)
    if not blocks:
        raise SystemExit("无法在 regenerate-archive.py 中定位 CATEGORIES 注册表")
    return re.findall(r'"([^"]+)"', "".join(blocks))


def main():
    warn_only = "--warn" in sys.argv
    slugs = load_slugs()
    posts = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "posts", "*.html")))
    unregistered = [p for p in posts if not any(s in p for s in slugs)]

    print("=== 分类注册表校验（verify-category-registry.py）===")
    print("文章数 %d｜注册表 slug %d" % (len(posts), len(slugs)))
    if not unregistered:
        print("PASS 全部文章均已注册进 CATEGORIES —— CI 重建不会产生兜底节")
        return 0

    print("")
    print("FAIL 未注册文章 %d 篇（会被 CI 踢出分类页并落入 More Articles 兜底节）：" % len(unregistered))
    for p in unregistered:
        print("   - %s" % p)
    print("")
    print("修复：在 regenerate-archive.py 的 CATEGORIES 对应分类 slugs 里补上该文 slug（可截断前缀），")
    print("      然后本地跑一次 python3 regenerate-archive.py 复核 archive/分类页/首页计数。")
    if warn_only:
        print("")
        print("--warn 模式：仅告警，不阻断。")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
