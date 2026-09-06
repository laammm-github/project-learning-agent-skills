---
name: project-learning-agent
description: A methodology for learning open-source projects, supporting full/fast/targeted modes, auto-generating project learning materials
---

# Project Tutor Skill Suite

> Agent 学习开源项目 → 生成人类可读教材的完整技能套件
> 基于"项目学习 Skill"方法论，采用模块化 Skill 架构

---

## 一、套件架构

```
Project Tutor Skill Suite
├── SKILL.md                          # Orchestrator：协调子 Skill
├── 01-repo-discovery/               # 阶段 1：项目发现
├── 02-config-and-installation/      # 阶段 2：安装与配置（新增）
├── 03-architecture-analysis/        # 阶段 3：架构分析
├── 04-code-flow-analysis/           # 阶段 4：代码流分析
├── 05-concept-extraction/           # 阶段 5：概念提取
├── 06-tutorial-writer/              # 阶段 6：教程生成
├── 07-example-generator/            # 阶段 7：示例生成
└── 08-learning-review/              # 阶段 8：学习检查
```

### 使用方式

```bash
# 方式 1：让 Agent 自动调度（推荐）
"请帮我学习这个项目，使用 project-learning-agent 套件"

# 方式 2：指定子 Skill
"使用 01-repo-discovery 扫描项目结构"
"使用 06-tutorial-writer 生成教程文档"
```

---

## 二、核心原则

### 学习顺序：由外向内、由粗到细

```
Phase 1: 项目发现（What）           → 项目是什么？技术栈？入口？
Phase 2: 安装配置（How to install）  → 怎么跑起来？配置系统？
Phase 3: 架构分析（How it's built）  → 模块划分、依赖关系、设计模式
Phase 4: 代码流分析（How it works）  → 数据从哪来、到哪去、经历什么变换
Phase 5: 概念提取（Key Concepts）    → 核心设计模式、抽象、契约
Phase 6: 教程生成（Teaching）        → 把分析结果转化为人类可读教材
Phase 7: 示例生成（Examples）        → 最小可运行示例、扩展模板
Phase 8: 学习检查（Review）          → 验证学习完整性，生成检查清单
```

### 输出物优先

每个 Phase 必须有可交付产物，而非只输入不输出。

### 数据流分层

```
原始分析数据层（01-05）：
  01-repo-discovery      → 01-project-overview.md（原始数据）
  02-config-and-installation → 02-installation.md（原始数据）
  03-architecture-analysis  → 03-architecture.md（原始数据）
  04-code-flow-analysis     → 04-core-flow.md（原始数据）
  05-concept-extraction     → 05-core-concepts.md（原始数据）
  ↓ 保留在 docs/analysis/ 供深挖

教学格式转换层（06）：
  06-tutorial-writer      → 整合原始数据为教学格式（01-06 章节）
  ↓ 生成最终产物

示例与检查层（07-08）：
  07-example-generator    → 08-examples.md
  08-learning-review      → 09-faq.md + 10-learning-checklist.md
```

---

## 三、项目类型识别

**不同项目，学习策略不同。先判断类型，再决定子 Skill 组合。**

| 类型 | 特征目录 | 学习重点 | 核心子 Skill |
|------|---------|---------|-------------|
| **消息中间件** | channel/、broker/ | 消息入口、路由、消费者 | 01→02→03→04→05 |
| **Web 应用** | router/、controller/ | 路由、请求处理、数据库 | 01→02→03→04→05 |
| **CLI 工具** | cmd/、commands/ | 命令注册、参数解析 | 01→02→03→05 |
| **库/框架** | src/、lib/ | API 设计、设计模式 | 01→02→03→05→06 |
| **Agent 框架** | agent/、tools/ | Agent 循环、工具系统 | 01→02→03→04→05→06 |
| **数据库/存储** | engine/、storage/ | 查询解析、存储引擎 | 01→02→03→04→05 |

---

## 四、最终产物：project-book/

学习完成后，生成完整教材：

```
project-book/
├── 01-project-overview.md       # 项目简介、技术栈、快速开始
├── 02-installation.md           # 安装与配置指南
├── 03-architecture.md           # 系统架构、模块职责、数据流
├── 04-core-flow.md              # 核心链路（用户请求完整路径）
├── 05-core-concepts.md          # 关键设计模式、抽象、契约
├── 06-source-code-guide.md      # 源码导航（按模块、按文件）
├── 07-extension-guide.md        # 扩展开发指南（模块、工具、插件等）
├── 08-examples.md               # 最小可运行示例
├── 09-faq.md                    # 常见问题与疑难解答
└── 10-learning-checklist.md     # 学习检查清单
```

---

## 五、子 Skill 索引

每个子 Skill 是独立的，可单独调用，也可由 Orchestrator 协调。

| 序号 | 子 Skill | 输入 | 输出文件 | 产物编号 | 参考 |
|------|---------|------|---------|---------|------|
| 1 | [01-repo-discovery](01-repo-discovery/SKILL.md) | 项目仓库 | `01-project-overview.md` | 01 | CLAUDE.md Generator |
| 2 | [02-config-and-installation](02-config-and-installation/SKILL.md) | 配置系统 | `02-installation.md` | 02 | 配置系统专项学习 |
| 3 | [03-architecture-analysis](03-architecture-analysis/SKILL.md) | 源码 | `03-architecture.md` | 03 | Agent Toolkit |
| 4 | [04-code-flow-analysis](04-code-flow-analysis/SKILL.md) | 核心链路代码 | `04-core-flow.md` | 04 | 消息流追踪最佳实践 |
| 5 | [05-concept-extraction](05-concept-extraction/SKILL.md) | 核心类/函数 | `05-core-concepts.md` | 05 | 类比学习理论 |
| 6 | [06-tutorial-writer](06-tutorial-writer/SKILL.md) | 01-05 原始数据 | `06-07` 章节整合 | 06-07 | Technical Writing |
| 7 | [07-example-generator](07-example-generator/SKILL.md) | 扩展点代码 | `08-examples.md` | 08 | Supabase Agent Skills |
| 8 | [08-learning-review](08-learning-review/SKILL.md) | 全部产物 | `09-10` 章节 | 09-10 | 元认知理论 |

### 编号逻辑说明

**原则：子 Skill 编号 = 产物编号**

- 01-05：原始分析数据层，一一对应
- 06：教学格式转换层，整合 01-05 生成 06-07
- 07-08：示例与检查层，分别生成 08 和 09-10

---

## 六、设计参考

本套件参考以下开源项目和方法论：

- **Agent Skills 官方规范**：https://github.com/agentskills/agentskills
- **Supabase Agent Skills**：https://github.com/supabase/agent-skills
- **Claude Technical Writing Skill**：Anthropic 内部文档
- **Project Documentation Skills**：https://www.reddit.com/r/ClaudeCode/comments/1ufee3y/
- **Agent Toolkit**：https://github.com/softaworks/agent-toolkit

---

## 七、使用示例

### 完整学习流程

```
用户："请帮我学习这个项目"

Agent 调度：
1. 01-repo-discovery → 01-project-overview.md
2. 02-config-and-installation → 02-installation.md
3. 03-architecture-analysis → 03-architecture.md
4. 04-code-flow-analysis → 04-core-flow.md
5. 05-concept-extraction → 05-core-concepts.md
6. 06-tutorial-writer → 整合生成 06-07 章节
7. 07-example-generator → 08-examples.md
8. 08-learning-review → 检查清单 + FAQ
```

### 快速学习流程（只学核心）

```
用户："快速了解这个项目，我需要知道核心架构和怎么扩展"

Agent 调度：
1. 01-repo-discovery → 01-project-overview.md
2. 02-config-and-installation → 02-installation.md
3. 03-architecture-analysis → 03-architecture.md
4. 07-example-generator → 08-examples.md（扩展模板）
```

### 针对性学习

```
用户："我想理解核心数据流的完整路径"

Agent 调度：
1. 04-code-flow-analysis → 04-core-flow.md（专注数据流）
2. 05-concept-extraction → 提取核心抽象
```

---

## 八、质量检查

每个子 Skill 输出前，检查：

```
✓ 产物是否让新人能看懂？
✓ 是否有代码示例（而非纯文字）？
✓ 是否标注了"数据变换"（输入→输出）？
✓ 是否有关联文件路径（方便深挖）？
```

---

## 九、完整使用示例

### 场景 1：完整学习一个新项目

```
用户提示词：
"请帮我学习这个开源项目，使用 project-learning-agent 套件生成完整教材"

Agent 调度流程：
1. 01-repo-discovery → 扫描项目结构，生成 01-project-overview.md
2. 02-config-and-installation → 分析配置系统，生成 02-installation.md
3. 03-architecture-analysis → 分析架构，生成 03-architecture.md
4. 04-code-flow-analysis → 跟踪核心链路，生成 04-core-flow.md
5. 05-concept-extraction → 提取核心概念，生成 05-core-concepts.md
6. 06-tutorial-writer → 整合为教学文档，生成 06-source-code-guide.md + 07-extension-guide.md
7. 07-example-generator → 生成 08-examples.md
8. 08-learning-review → 生成 09-faq.md + 10-learning-checklist.md

最终产物：
project-book/
├── 01-project-overview.md
├── 02-installation.md
├── 03-architecture.md
├── 04-core-flow.md
├── 05-core-concepts.md
├── 06-source-code-guide.md
├── 07-extension-guide.md
├── 08-examples.md
├── 09-faq.md
└── 10-learning-checklist.md
```

### 场景 2：快速了解项目核心

```
用户提示词：
"快速了解这个项目，我需要知道核心架构和怎么扩展"

Agent 调度流程：
1. 01-repo-discovery → 01-project-overview.md
2. 02-config-and-installation → 02-installation.md
3. 03-architecture-analysis → 03-architecture.md
4. 07-example-generator → 08-examples.md（扩展模板）

节省时间：跳过 04-06，直接获取核心架构 + 扩展方法
```

### 场景 3：针对性学习核心数据流

```
用户提示词：
"我想理解核心数据流的完整路径"

Agent 调度流程：
1. 04-code-flow-analysis → 04-core-flow.md（专注数据流）
2. 05-concept-extraction → 提取核心抽象

适用于：已有基础，只想深入理解特定流程
```

### 场景 4：学习如何贡献代码

```
用户提示词：
"我想学习这个项目，准备贡献代码"

Agent 调度流程：
1. 01-repo-discovery → 01-project-overview.md
2. 02-config-and-installation → 02-installation.md
3. 03-architecture-analysis → 03-architecture.md
4. 04-code-flow-analysis → 04-core-flow.md
5. 05-concept-extraction → 05-core-concepts.md
6. 06-tutorial-writer → 06-source-code-guide.md + 07-extension-guide.md
7. 07-example-generator → 08-examples.md（扩展模板）
8. 08-learning-review → 10-learning-checklist.md（检查贡献者准备度）

重点：07-extension-guide.md 提供扩展开发方法
```