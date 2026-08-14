#!/usr/bin/env python3
"""IndexNow 全量提交脚本（TCM Way）

推送全部文章 + 首页 + archive 到 IndexNow（Bing/Yandex/Seznam 收录加速）。
key 文件：801dae89441870eb2beaca24c5c304cf.txt（仓库根目录，在线可达）。

用法：
  python3 indexnow-submit.py          # 全量推送
  python3 indexnow-submit.py posts/46  # 只推送某篇（含 46 的文件名匹配）
"""

import glob
import json
import sys
import urllib.error
import urllib.request

KEY = open("801dae89441870eb2beaca24c5c304cf.txt").read().strip()
HOST = "tcmway.net"


def main():
    filter_str = sys.argv[1] if len(sys.argv) > 1 else ""
    urls = []
    for f in sorted(glob.glob("posts/*.html")):
        name = f.split("/")[-1]
        if filter_str and filter_str not in name:
            continue
        urls.append(f"https://{HOST}/posts/{name}")
    if not filter_str:
        urls += [f"https://{HOST}/", f"https://{HOST}/archive.html"]

    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": f"https://{HOST}/{KEY}.txt",
        "urlList": urls,
    }).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=payload,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        print(f"IndexNow OK: HTTP {resp.status} ({len(urls)} URLs)")
    except urllib.error.HTTPError as e:
        print(f"IndexNow HTTP Error {e.code}: {e.read().decode()[:300]}")
        sys.exit(1)
    except Exception as e:
        print(f"IndexNow ERR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
