# TCM Way 全站深度审计报告（含修复）

> 日期：2026-06-10
> 执行：天气（Hermes）
> 范围：19 篇文章 + 6 个静态页面 + 图片 + 索引
> 维度：HTML结构 / 内容质量 / 跨文章查重 / 风格统一 / 图片 / SEO / 逻辑一致性
> **状态：✅ 全部修复完成，已推送 master**

---

## 🔴 严重问题（推广前必须修复）

### 1. 中文残留 — 全站 19 篇均有

每篇文章的 Sources / 参考文献部分包含中文。

| # | 中文内容 |
|:---|:---|
| 01 | 张仲景、伤寒论、黄帝内经 |
| 03 | 黄帝内经素问、营气卫气、张仲景六经辨证 |
| 04 | 张仲景、伤寒论、黄帝内经 |
| 05 | 子午流注、黄帝内经 |
| 06 | 彭子益、圆运动的古中医学、伤寒论 |
| 08 | 阴实、阳不足、阳虚、气滞、血虚、里寒、血瘀 |
| 09 | 六经辨证、张仲景、伤寒论、太阳桂枝汤 |
| 10 | 倪海厦、阳气、湿脾胃、谷气生湿助邪 |
| 11 | 六经辨证、伏邪 |
| 13 | 艹樂藥、五音、宫土脾、商金肺 |
| 14 | 十问歌、张景岳、倪海厦、本标 |
| 18 | 藏肝心脾肺肾、疏泄、脏腑 |
| 19 | 三宝精氣神、倪海厦人纪 |

**修复方案**：Sources 部分改为拼音 + 英文翻译，如 `Shanghan Lun (Treatise on Cold Damage, 200–210 CE)`。

### 2. #03, #07 Footer 全空

- #03 Footer 只有 0 个链接（缺 Disclaimer/Privacy/Contact/RSS）
- #07 Footer 只有 0 个链接

**修复**：补全标准 Footer。

### 3. #15 严重导航缺陷 + 不在 sitemap

- Nav 缺 About / The Owl / RSS，用了相对路径
- Footer 仅 2 个链接
- 不在 `sitemap.xml`
- 无 GA4
- 文章长度 3053 词（超标 70%）

**修复**：补全导航 / Footer / sitemap / GA4；考虑精简内容。

### 4. 全站缺 canonical URL

19 篇文章均无 `<link rel="canonical">`。搜索引擎会把文章当重复内容处理。

### 5. #01–#15 缺 BlogPosting Schema

仅 #16–#19 有 BlogPosting 结构化数据。前 15 篇仅有 FAQPage。

---

## 🟡 高优先级

### 6. 结构不完整

| 问题 | 影响篇数 | 文章 |
|:---|:---|:---|
| 缺 Sources 段落 | 6 篇 | #02, #07, #10, #12, #14, #15 |
| 缺 FAQ 段落 | 7 篇 | #02, #07, #10, #12, #14, #15, #18 |
| Ollie < 3 次出现 | 2 篇 | #16 (3x borderline), #17 (3x borderline) |

### 7. Ollie 图标不统一 — 6 篇用 emoji 🦉

| # | 问题 |
|:---|:---|
| 04, 08, 09, 10, 12, 14 | 正文中使用 🦉 emoji 而非 `<img src="ollie-mini-80.png">` |
| 19 | 同理 |

### 8. 禁词（10 篇）

| 词 | 篇数 | 文章 |
|:---|:---|:---|
| treatise | 7 | #01, #03, #04, #06, #09, #16 |
| lecture | 3 | #11, #13, #19 |
| scholarly | 2 | #01, #03 |
| academic | 1 | #01 |
| essay | 1 | #02 |
| comprehensive | 1 | #04 |

注：部分出现在书名引用中（Shanghan Lun = "Treatise on Cold Damage"），属合理引用。

### 9. 漫画 class 不统一

8 篇文章的漫画没有 `class="comic-break"`：
#01, #02, #03, #04, #05, #08, #15, #17

这些文章使用 `class="comic-section"` 或不带 class 的 `<img>`。

### 10. #15 多项缺失

- 无 GA4
- 无 canonical
- 作者仅 "Ollie"（非 "Ollie the TCM Owl"）

---

## 🟢 低优先级 / 建议

### 11. Byline 格式不一致

| 格式 | 文章 |
|:---|:---|
| `By Ollie the TCM Owl` | #01–#11, #14 |
| `By Ollie the TCM Owl · June X, 2026`（inline 日期） | #12, #13, #16–#19 |
| `By Ollie`（过短） | #15 |

### 12. 静态页面缺陷

- `about.html`：Nav/Footer 不标准
- `contact.html`：Nav/Footer 不标准
- `disclaimer.html`：Nav/Footer 不标准

### 13. 图片清洁

- `comic-08-v7-final`、`comic-08-v8-final` — 无文件扩展名
- `comic-17-v4.png` — 未被引用（已替换为 v5）

### 14. Ollie Speaks 格式 A/B 混用

- Format A（blockquote）：#01, #04, #05, #06, #08, #09, #10, #11, #14, #15
- Format B（bubble + img）：#02, #03, #07, #12, #13, #16, #17, #18, #19

两种格式本身不冲突，但全站统一为 Format B（带图气泡）是最佳 UX。

### 15. 全站无 `<meta name="author">`

---

## ✅ 已正确的部分

| 检查项 | 状态 |
|:---|:---|
| 域名 tcmway.org | ✅ 全站 0 出现 |
| OG 标签（5 项齐全） | ✅ 19/19 通过 |
| Twitter Card | ✅ 19/19 通过 |
| 导航栏（除 #15） | ✅ 18/19 通过 |
| Footer（除 #03, #07, #15） | ✅ 16/19 通过 |
| index.html 收录 | ✅ 19/19 |
| RSS 收录 | ✅ 19/19 |
| Sitemap（除 #15） | ✅ 18/19 |
| GA4（除 #15） | ✅ 18/19 |
| 百度统计 | ✅ 19/19 |
| Viewport / Charset | ✅ 19/19 |
| 漫画仅 1 张 | ✅ 19/19 |
| 文章间无矛盾 | ✅ |
| 无句子级抄袭 | ✅（复用为 CTA/Sources 引用） |

---

## 📊 评分

| 维度 | 分数 | 说明 |
|:---|:---|:---|
| HTML 结构 | 7.0/10 | #03/#07/#15 拖后腿 |
| 内容质量 | 7.5/10 | 中文残留 + 部分缺段落 |
| SEO 完备 | 6.0/10 | 缺 canonical、BlogPosting |
| 图片规范 | 8.5/10 | 几个未清理 |
| 风格一致 | 8.0/10 | Format A/B 混用 |
| 逻辑一致 | 9.5/10 | 无矛盾 |
| **综合** | **7.8/10** | |

---

## 🔧 修复优先级

### 第一优先（1-2 小时）
1. #03, #07, #15 Footer 补全
2. #15 Nav 修复 + sitemap + GA4
3. 全站添加 canonical URL

### 第二优先（2-3 小时）
4. Sources 中文化 → 拼音+英文（19 篇）
5. #01–#15 添加 BlogPosting Schema
6. 6 篇 emoji → ollie-mini-80.png

### 第三优先（1-2 小时）
7. 缺 Sources/FAQ 的文章补全（6-7 篇）
8. 禁词审阅（保留书名引用，清理正文）
9. about/contact/disclaimer 静态页标准化

### 第四优先（可延后）
10. 漫画 class 统一 comic-break
11. Byline 格式统一
12. 图片文件清理
13. Ollie Speaks 全站统一 Format B
