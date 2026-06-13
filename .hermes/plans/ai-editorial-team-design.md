# TCM Way AI 编辑团队架构设计

> 设计：天气（Hermes）
> 日期：2026-06-11
> 状态：待主人审批

---

## 一、团队角色（5 人）

```
┌─────────────────────────────────────────────────┐
│              你（创始人 / 总编辑）                  │
│         只做两件事：定战略 + 最终拍板               │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│         天气 = CEO / Managing Editor             │
│  职责：选题决策、任务调度、最终审核、对外推广       │
│  工具：全部（terminal/file/web/delegate/cron）     │
│  模型：DeepSeek V4 Pro                           │
└────────────────────┬────────────────────────────┘
                     │ 调度 ↓
     ┌───────────────┼───────────────┬──────────────┐
     ▼               ▼               ▼              ▼
┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  写手    │   │  天昊     │   │  审稿     │   │  运营     │
│ Writer  │   │Illustrator│   │ Reviewer │   │ Operator │
├─────────┤   ├──────────┤   ├──────────┤   ├──────────┤
│ 执行SOP │   │ 生成漫画  │   │ 12项质检 │   │ 流量监控 │
│ 写正文  │   │ 表情/壁纸 │   │ 内容审核 │   │ 读者互动 │
│ FAQ     │   │ 统一风格  │   │ 结构检查 │   │ 推广执行 │
│ Sources │   │           │   │ 打分判定 │   │ SEO维护  │
├─────────┤   ├──────────┤   ├──────────┤   ├──────────┤
│ 模型：   │   │ 工具：    │   │ 模型：   │   │ 模型：   │
│ 百炼     │   │ bl image  │   │ DS V4    │   │ DS V4    │
│ Qwen3.7  │   │ generate  │   │ Pro      │   │ Pro      │
│ Max      │   │           │   │           │   │           │
└─────────┘   └──────────┘   └──────────┘   └──────────┘
```

### 为什么这样分

| 角色 | 为什么独立 | 跟现在的区别 |
|------|-----------|-------------|
| **CEO（天气）** | 调度+决策不能跟执行混——裁判不能兼球员 | 现在天气又写又审又发，角色冲突 |
| **Writer** | 写作是深度创意工作，需要专注，不能被打断去修 bug | 现在天气包办写作 |
| **天昊** | 已是独立角色，保持不变 | — |
| **Reviewer** | 质检必须独立——自己写的东西自己审没用 | 现在天气自写自审，漏了很多 |
| **Operator** | 发布/监控/回复/推广是重复性运维，不适合打断 CEO | 现在天气碎片化做这些 |

---

## 二、每日工作流（全自动）

```
08:00  CEO 起床
       ├── 拉取流量报告（昨天数据）
       ├── 检查选题池
       └── 执行选题决策 → 确定今日题目

08:15  CEO → Writer：派发写作任务
       Writer 执行写作 SOP：
       ├── 1. 读选题 brief
       ├── 2. 写正文（1200-1800 词）
       ├── 3. 写 FAQ（3-4 组 Q&A）
       ├── 4. 写 Sources
       ├── 5. 写 Ollie Speaks
       └── 6. 交付 HTML 草稿

09:00  CEO → 天昊：派发配图任务
       天昊生成漫画：
       ├── 读文章主题
       ├── 生成 4 格漫画（物种锁 + 颜色锁）
       └── 交付 comic-NN-v4.png

09:30  CEO → Reviewer：派发审核任务
       Reviewer 执行 12 项质检：
       ├── 内容质量（禁词/字数/Ollie 声音）
       ├── 漫画验收（物种/颜色/配文/4格完整）
       ├── 结构检查（Nav/Footer/Canonical/Schema）
       ├── 风格一致性
       └── 打分：≥9/10 = 通过，<9 = 退回

       ┌─ ≥9 分 ──→ 进入发布
       └─ <9 分 ──→ 退回 Writer/天昊修改 → 再审

10:00  天气（CEO）最终过目 → push 上线

10:15  Operator：发布后验证
       ├── curl 验证线上（非本地）
       ├── 更新 sitemap/rss
       └── 通知 CEO "上线成功"

次日   Operator：流量日报
       ├── CF + GA4 数据
       ├── 热门文章 Top 5
       └── 异常告警
```

---

## 三、选题池机制

选题不是每天拍脑袋，是一个**持续维护的知识库**：

```
~/tcmway-blog/.hermes/topic-pool/
├── README.md           ← 选题策略说明
├── pipeline.md         ← 待写选题（按优先级排序）
├── published.md        ← 已发布（防重复）
├── ideas.md            ← 灵感池（未整理的碎片想法）
└── seasonal.md         ← 节气/节日相关（时间敏感）
```

### 选题决策算法（CEO 每日执行）

1. **排除已发布**（published.md）
2. **优先时间敏感**（seasonal.md 中临近的节气/节日）
3. **系列连续性**（N/S/T 系列按顺序推进）
4. **多样性检查**（连续 3 天不写同一支柱主题）
5. **从 pipeline 中取优先级最高的**

### 选题来源

| 来源 | 频率 | 示例 |
|------|------|------|
| 系列推进 | 60% | 伤寒论 S 系列、黄帝内经 N 系列 |
| 读者问题 | 20% | "A Reader Asks: Why do I wake at 3 AM?" |
| 节气/时事 | 10% | 夏至、三伏天 |
| 灵感池挖掘 | 10% | "What Chinese medicine can learn from sourdough" |

---

## 四、技术实现方案

### Phase 1：建 Profiles（30 分钟）

```bash
# 创建 4 个 Hermes profiles
hermes profile create writer
hermes profile create reviewer  
hermes profile create operator
# 天昊已存在（WorkBuddy，通过 SharedMemory 调度）
# 天气 = default profile（CEO）
```

每个 profile 配不同的 system prompt + 工具权限：

| Profile | System Prompt 关键约束 | 可用工具 |
|---------|----------------------|----------|
| **writer** | "你是 TCM Way 的英文写手。严格按 SOP 写作。1200-1800 词。禁止使用 journey/holistic/profound 等禁词。Ollie 第一人称贯穿全文。" | file, terminal, vision |
| **reviewer** | "你是 TCM Way 的审核编辑。只做审核，不写内容。12 项检查清单逐一过。≥9/10 通过。低于 9 分必须列出具体问题。" | file, terminal, vision |
| **operator** | "你是 TCM Way 的运维。负责发布、流量监控、读者互动。不做内容决策。" | file, terminal, web, vision |

### Phase 2：建 SOP 文件（已有基础）

现有 `tcmway-blog-operations` 技能已涵盖大部分质检，需要提取为独立 SOP 给各 profile 用：

```
~/SharedMemory/sop/
├── writer-sop.md        ← 写作规范（字数/禁词/Ollie声音/FAQ/Sources格式）
├── reviewer-checklist.md ← 12 项检查清单（已有）
├── publisher-sop.md     ← 发布 6 步
└── topic-selection.md   ← 选题决策算法
```

### Phase 3：Kanban 调度（核心引擎）

天气（CEO）不亲自干活，通过 Kanban 板调度：

```python
# 每天早晨 CEO 做的事（示例）
# 1. 选题
topic = select_daily_topic(topic_pool)
# 2. 创建 Kanban 任务链
t1 = kanban_create(title=f"Write: {topic}", assignee="writer", ...)
t2 = kanban_create(title=f"Illustrate: {topic}", assignee="tianhao", ...)
t3 = kanban_create(title=f"Review: {topic}", assignee="reviewer", parents=[t1, t2])
t4 = kanban_create(title=f"Publish: {topic}", assignee="operator", parents=[t3])
```

Writer 和天昊**并行**开工（互不依赖），Reviewer 等两者都完成再启动。

---

## 五、对比：现在 vs 建成后

| 环节 | 现在 | 建成后 |
|------|------|--------|
| 选题 | 主人或天气手动想 | CEO 从选题池自动决策 |
| 写作 | 天气写，自写自审 | Writer 写，Reviewer 审，三权分立 |
| 配图 | 派天昊，天气验 | Reviewer 统一验，天气只看最终结果 |
| 质检 | 天气手动逐项查 | Reviewer 自动跑 12 项 |
| 发布 | 天气操作 | Operator 自动 push + 验证 |
| 流量 | Cron 自动报 | Operator 日报 + 异常告警 |
| 推广 | 天气碎片化做 | Operator 执行，天气定策略 |

---

## 六、费用

| 项 | 费用 |
|------|------|
| Writer（百炼 Qwen3.7-Max）| ¥0.004/1K tokens（百炼充值后）|
| Reviewer（DeepSeek V4）| 已有 |
| Operator（DeepSeek V4）| 已有 |
| 天昊（百炼 qwen-image）| 已有 |

除百炼充值外，**无新增固定成本**。

---

## 七、主人的角色变化

| 以前 | 以后 |
|------|------|
| 想题目 | 选题池自动推荐，你确认或改 |
| 看草稿 | 只看 ≥9 分的最终稿 |
| 检查漫画 | Reviewer 验过，你扫一眼 |
| 手动发布 | Operator 自动发 |
| 担心质量问题 | Reviewer 打分制，<9 分根本到不了你面前 |

**你从"主编+编辑+校对+美编+发行"变成"总编辑"——只管战略方向和最终拍板。**

---

## 八、主人决策（2026-06-11 已确认）

1. **Writer 模型** → ✅ 百炼 Qwen3.7-Max（需充值后激活）
2. **每日选题** → ✅ AI 自己定，主人回来看网站最终结果，有想法隔天指示
3. **审核分数线** → ✅ 9/10 严格
4. **现在开工** → ✅ 先建 CEO/Reviewer/Operator profiles + SOP + 选题池；Writer 等百炼充值后激活
