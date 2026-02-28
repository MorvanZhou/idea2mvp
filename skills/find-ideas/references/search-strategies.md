# 搜索策略参考文档

## 搜索关键词模板

### Product Hunt

并行搜索以下关键词（将 `{年份}` 和 `{月份}` 替换为当前日期）：

- `"Product Hunt" best new tools {月份} {年份}`
- `"Product Hunt" trending productivity tools {年份}`
- `"Product Hunt" indie maker launch {月份} {年份}`
- `"Product Hunt" small utility app {年份}`
- `site:producthunt.com "golden kitty" OR "product of the day" tool utility {年份}`

### 中文社区

#### 小红书
- `小红书 效率工具推荐 {年份}`
- `小红书 好用的小众app {年份}`
- `小红书 独立开发者 产品推荐`
- `小红书 宝藏app 实用工具`

#### V2EX
- `site:v2ex.com 分享 小工具 推荐 {年份}`
- `site:v2ex.com 独立开发 上线 发布`
- `V2EX 效率工具 推荐 独立开发`

#### 即刻
- `即刻 独立开发者 产品 上线 {年份}`
- `即刻 效率工具 推荐`

#### 少数派
- `site:sspai.com 效率工具 推荐 {年份}`
- `少数派 App 推荐 实用工具 {年份}`
- `少数派 独立开发者 产品`

### 独立开发者社区

- `indie hackers new product launch {月份} {年份}`
- `indie maker tools daily use {年份}`
- `DecoHack 独立产品周刊`
- `独立开发者产品 工具 推荐 {年份}`
- `独立开发 盈利 小工具 {年份}`

### GitHub Trending

- `GitHub trending tool CLI utility {月份} {年份}`
- `GitHub trending productivity developer tool`
- `GitHub 热门 工具类项目 {年份}`

### 通用搜索

- `实用小工具 {年份}`
- `效率工具推荐 独立开发 {年份}`
- `好用的小众app 推荐 {年份}`
- `useful productivity tools {年份}`
- `small useful apps {年份}`
- `best indie apps {年份}`
- `best CLI tools developers {年份}`

## 筛选标准细则

### 纳入标准（全部满足）

1. **解决具体痛点**：工具有明确的使用场景和解决的问题（文件处理、时间管理、写作辅助、图片处理、开发效率等）
2. **小团队或个人作品**：优先个人开发者或 10 人以下小团队的产品
3. **C 端可用**：普通用户能直接下载/使用，不需要企业账号
4. **近期活跃**：产品在近 6 个月内有更新或发布

### 排除标准（命中任一即排除）

1. **平台型产品**：如 Notion、Figma、Slack 等已成熟的大平台
2. **框架和库**：如 React、Next.js、TailwindCSS 等开发框架
3. **基础设施**：如数据库、云服务、CI/CD 工具
4. **AI 大模型平台**：如 ChatGPT、Claude 等（但使用 AI 能力的小工具可纳入）
5. **纯 B 端 SaaS**：需要企业采购、面向团队管理的 SaaS 产品

### GitHub Trending 特别注意

- 仅筛选工具类、效率类的小项目
- 个人开发者项目优先
- 如果 Trending 中大多是平台/框架类项目，减少此来源的占比，不强行凑数
- 最多选取 3 个项目

## 搜索执行策略

### 并行搜索分组

为了效率，将搜索分为以下几组并行执行：

**第一轮（并行 5-6 个搜索）**：
1. Product Hunt 热门工具
2. 中文效率工具推荐
3. 小众 App 推荐
4. 独立开发者产品
5. GitHub 工具项目
6. 英文 indie maker 工具

**第二轮（根据第一轮结果补充，并行 2-3 个搜索）**：
- 针对第一轮发现的有趣方向，深入搜索相关工具
- 搜索特定工具的详细信息、定价、用户评价

### 去重策略

每次执行时，搜索关键词中加入当前月份以增加时效性，尽量发现新工具。如果用户提到之前已推荐过的工具，在报告中标注"上次已推荐"并优先推荐新发现的工具。
