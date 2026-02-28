---
name: find-ideas
description: This skill should be used when users want to discover trending tools, small projects, and indie products to spark new product ideas. It searches GitHub Trending, Product Hunt, indie maker communities, and Chinese platforms like XiaoHongShu to find recently popular small tools and products, then analyzes them to generate actionable product ideas and expansion directions. Triggers include requests like "find ideas", "explore trending tools", "what small tools are popular recently", "help me find product inspiration", "search for indie products", or any task involving product idea discovery and trend exploration.
---

# Find Ideas — 实用工具探索与产品灵感发现

## Overview

本 skill 通过搜索多个平台（GitHub Trending、Product Hunt、独立开发者社区、小红书等）发现近期流行的实用小工具和独立产品，分析其解决的痛点和商业模式，并基于这些发现生成可拓展的产品 Ideas 和创业方向。全程使用中文输出。

## 核心原则

1. **聚焦小工具和小产品**：只关注解决日常具体需求的工具或产品，排除平台型产品、大型框架、基础设施类项目和 AI 大模型平台
2. **真实性优先**：所有推荐的工具必须是真实存在的产品，不得虚构工具名称或功能
3. **C 端视角**：优先关注个人开发者或小团队的产品，以及 C 端用户能自发发现、下载、使用的工具
4. **重在启发而非列举**：工具推荐是手段，核心目的是通过分析这些工具来激发新的产品灵感和发现未被满足的市场需求
5. **扩展思维**：在列出工具后，必须进行深度的延伸思考，帮助用户从已有产品中发现新的机会

## 执行流程

### 第一步：多平台搜索发现工具

读取 `references/search-strategies.md` 获取各平台的搜索关键词模板和筛选标准，然后**并行**使用 `web_search` 工具或者 `agent-browser` skill 搜索多个来源。

**搜索来源优先级**：
1. **Product Hunt**：搜索近期热门的小工具和独立产品
2. **中文社区**（小红书、V2EX、即刻、少数派）：搜索中文用户关注的效率工具和小众 App
3. **独立开发者社区**（Indie Hackers、DecoHack 独立产品周刊等）：搜索独立开发者的新产品
4. **GitHub Trending**：有限度参考，仅筛选工具类小项目（非平台、非框架）
5. **通用搜索**：搜索近期效率工具推荐、小众 App 推荐等内容

**筛选标准**：

| 纳入 | 排除 |
|------|------|
| 解决具体日常痛点的工具 | 平台型产品 |
| 个人开发者或小团队的产品 | 大型框架、基础设施类 |
| CLI 工具、桌面小工具、浏览器插件、移动端 App、Web 小工具 | AI 大模型平台 |
| 买断制或免费工具 | 纯 B 端 SaaS |

搜索完成后，从所有来源中筛选出 **5-8 个最有启发性的工具**。

### 第二步：有限度参考 GitHub Trending

使用 `web_search` 搜索 GitHub Trending 上的项目，仅筛选明确是**工具类、效率类**的小项目。如果 Trending 中大多是平台/框架类项目，减少或跳过此来源，不强行凑数。从中选出 **最多 3 个**工具类小项目。

### 第三步：深度分析与 Idea 扩展

这是本 skill 的核心价值所在。读取 `references/idea-expansion-guide.md`，基于搜索到的工具进行深度分析：

1. **痛点提炼**：从每个工具中提炼出它解决的核心痛点
2. **模式识别**：识别多个工具之间的共同模式或趋势（如"AI + 日常小工具"、"自动化替代手动操作"等）
3. **空白发现**：基于痛点和模式，思考有哪些相邻需求尚未被满足
4. **Idea 生成**：生成 5 个可拓展的产品 Ideas，每个都要有具体的使用场景和差异化切入点
5. **趋势洞察**：总结 2-3 条产品趋势或市场规律

### 第四步：输出报告

按照 `assets/report-template.md` 的格式输出完整报告，包含四个部分：
1. 实用 App & 小工具推荐
2. GitHub 工具类小项目
3. 产品 Ideas & 拓展方向
4. 今日洞察

## Bundled Resources

本 skill 包含以下资源文件：

### references/

- **`references/search-strategies.md`** — 搜索策略参考文档。包含各平台（Product Hunt、小红书、GitHub、V2EX、即刻、少数派、Indie Hackers 等）的搜索关键词模板、筛选标准细则、以及 GitHub Trending 的使用注意事项。在第一步和第二步开始前读取此文件。
- **`references/idea-expansion-guide.md`** — Idea 扩展指南。包含从工具发现到 Idea 生成的思维框架：痛点提炼方法、模式识别维度、空白发现策略、Idea 评估标准。在第三步分析时读取此文件。

### assets/

- **`assets/report-template.md`** — 报告输出模板。定义了完整报告的四个部分及每个部分的详细格式要求。在第四步输出报告时参照此模板。

## 工具使用指南

### web_search 使用场景

在第一步和第二步中，先读取 `references/search-strategies.md` 获取关键词模板，然后并行使用 `web_search` 进行搜索。典型搜索包括：

- Product Hunt 搜索：`"Product Hunt" trending tools {当前月份} {当前年份}`
- 中文工具推荐：`好用的小众app 推荐 {当前年份}`、`效率工具推荐 独立开发`
- 独立开发者：`indie maker tools {当前年份}`、`DecoHack 独立产品周刊`
- GitHub 工具：`GitHub trending tool CLI utility {当前月份}`

更多关键词模板参见 `references/search-strategies.md`。

### agent-browser 使用场景

当需要深入了解某个工具的详情时，使用 `agent-browser` skill：

- 访问 Product Hunt 产品页面查看功能介绍和用户评价
- 访问 GitHub 项目页面查看 README 和 Star 数
- 浏览工具官网了解定价和功能细节

## 交互规范

1. **开场**：当用户触发本 skill 时，简要说明将要搜索的范围，然后立即开始搜索
2. **搜索过程**：并行搜索多个平台，不需要逐步汇报进度
3. **报告输出**：搜索完成后，一次性输出完整报告
4. **语言**：全程使用中文
