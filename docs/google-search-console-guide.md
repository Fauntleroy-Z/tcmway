# 🔍 Google Search Console 验证操作指南 — tcmway.org

> **状态**：待主人操作（需要访问 Google 的网络环境）
> **准备时间**：2026-05-24 14:30
> **预计耗时**：5-10 分钟

---

## ✅ 天昊已完成的准备工作

| 准备项 | 状态 | 说明 |
|--------|------|------|
| 网站在线 | ✅ | tcmway.org HTTP 200，Cloudflare CDN 正常 |
| sitemap.xml | ✅ 已更新 | 包含全部 10 个页面（首页+4栏目页+5篇文章） |
| robots.txt | ✅ | `Allow: /` + Sitemap 声明 |
| 5 篇文章全部在线 | ✅ | #01~#05 均返回 HTTP 200 |
| SEO meta 标签 | ✅ | description / OG / Twitter Card 均有 |
| HTTPS 强制跳转 | ✅ | GitHub Pages API 设置 |

---

## 🎯 主人需要做的操作（3 步，约 5 分钟）

### ⚠️ 前提：需要一个能访问 Google 的网络环境
- 公司 VPN / 手机热点(海外) / 代理工具均可
- **只需要浏览器**，不需要安装任何软件

---

### 第 1 步：添加站点到 Google Search Console（2 分钟）

1. 打开浏览器，访问：**https://search.google.com/search-console/welcome**
2. 登录你的 Google 账号（建议用 Gmail: andy.xujun@foxmail.com 对应的 Google 账号）
3. 选择验证类型：**「URL 前缀」**（推荐）— 输入 `https://tcmway.org/`
   > 💡 为什么选 URL 前缀而非域名？因为我们的网站托管在 GitHub Pages 上，无法在 DNS 添加 TXT 记录来验证「域名」级别
4. 点击「继续」

### 第 2 步：验证所有权（2 分钟）

GSC 会提供多种验证方法，按优先级选择：

#### 方法 A：HTML 文件验证（推荐 ✅ 最简单）
1. GSC 会给你一个 HTML 文件名，类似 `google1234567890abcdef.html`
2. **告诉我这个文件名**，我立刻创建并部署到 tcmway-blog 根目录 + git push
3. 回到 GSC 点击「验证」，Google 会自动检测到文件 → 通过！

#### 方法 B：HTML meta 标签验证（备选）
1. GSC 会给你一段 meta 标签：
   ```html
   <meta name="google-site-verification" content="xxxxxxxxxxx" />
   ```
2. **把这段 content 值发给我**，我加到 index.html 的 `<head>` 里 + git push
3. 回到 GSC 点击「验证」→ 通过！

#### 方法 C：Google Analytics 关联（如果你已有 GA）
1. 如果你的 Google 账号已有跟踪该网站的 GA 属性，可直接关联验证

### 第 3 步：提交 Sitemap（1 分钟）

验证通过后：
1. 在 GSC 左侧菜单找到 **「Sitemaps」**
2. 在输入框输入：`sitemap.xml`
3. 点击「提交」
4. 状态应显示为 **「成功」**

---

## 🚀 验证完成后通知天昊

一旦主人完成上述操作，告诉天昊一声"GSC 验证通过了"，我会立即：

1. ✅ 用 Indexing API 批量提交所有页面 URL 给 Google
2. ✅ 配置自动索引脚本（新文章发布后自动通知 Google）
3. ✅ 提交 Bing Webmaster Tools（同步收录）
4. ✅ 记录到自动化任务中定期监控收录状态

---

## 📊 当前 SEO 基础设施总览

```
tcmway.org/
├── index.html          (✅ 在线, 200 OK)
├── about.html          (✅ 在线)
├── about-owl.html      (✅ 在线)
├── contact.html        (✅ 在线)
├── disclaimer.html     (✅ 在线)
├── robots.txt          (✅ Allow: / + Sitemap 声明)
├── sitemap.xml         (✅ 10个URL, 已更新 #04 #05)
└── posts/
    ├── 01-*.html       (✅ 在线)
    ├── 02-*.html       (✅ 在线)
    ├── 03-*.html       (✅ 在线)
    ├── 04-*.html       (✅ 新! Traffic Jam)
    └── 05-*.html       (✅ 新! Body Clock)
```

## 🔄 备选方案（如果主人暂时无法访问 Google）

如果主人现在不方便操作 GSC，Google 其实**会自动发现和收录**新网站，只是速度较慢：

| 方式 | 预计首次收录时间 | 可控性 |
|------|-----------------|--------|
| **什么都不做**（等 Googlebot 自然发现） | 1~4 周 | ❌ 低 |
| **GSC 手动提交 sitemap**（推荐方案） | 1~7 天 | ✅ 高 |
| **Indexing API 推送**（需先过 GSC 验证） | 数小时~1 天 | ✅⭐ 最高 |
| **外链引流**（社交媒体/其他网站链接） | 3~14 天 | 🟡 中 |

即使现在不验证，只要网站有外部链接指向（比如从 Pinterest、Reddit、Twitter 分享），Google 也会加速收录。

---

## 📌 技术备忘

- **Cloudflare DNS**：域名注册商 = Cloudflare Registrar，DNS 也托管在 Cloudflare
- **GitHub Pages**：master 分支根目录自动部署，不支持服务端逻辑
- **Indexing API 日配额**：200 次/天/服务账号（对我们的小站完全够用）
- **sitemap 更新策略**：每次发布新文章后，天昊自动更新 sitemap.xml 并 push
- **建议 Google 账号**：用 Gmail（与 YouTube/Android 同账号即可）
