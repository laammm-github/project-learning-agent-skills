---
name: project-learning-agent
description: 当用户要求学习/理解一个陌生代码仓库、生成或增量更新项目教材（project-book）时使用；支持 full/fast/targeted 三种模式；不用于一次性代码问答。
---

# Project Learning Agent（编排器）

把陌生代码仓库转化为可追溯、可验证的十章项目教材（`project-book/`）。本技能是编排器：负责选定模式、按序调度 8 个子技能、执行统一契约与完成门禁。全文约定：`<skill_root>` 指本技能安装目录（本 SKILL.md 所在目录），`<repo>` 指被学习的目标仓库根目录；脚本命令一律带 `<skill_root>` 前缀，因为运行时工作目录通常是目标仓库。核心纪律：**每个结论回指仓库内真实的 `文件:行号`；未执行的命令与静态推断必须显式标注。**

## 一、必读契约

以下参考文件是本技能的一部分，在对应时机必须实际读取，不得凭记忆执行：

| 契约 | 读取时机 |
| --- | --- |
| [references/output-contract.md](references/output-contract.md) | 每次运行开始前：输出目录、manifest schema、章节验收标准 |
| [references/evidence-and-safety.md](references/evidence-and-safety.md) | 配置检查、命令执行、增量更新前：证据分级、密钥安全、规模控制 |
| [references/diagram-contract.md](references/diagram-contract.md) | 创建或更新任何图表前：图表角色、块格式、证据与登记规则 |

## 二、三种模式

| 模式 | 适用场景 | 输出规则 |
| --- | --- | --- |
| `full` | 第一次完整学习仓库 | 十章 + manifest；必须交代 `system_structure`、`runtime_deployment`、`core_flow` 三个图表角色（不适用时在 manifest 记 `not_applicable` 并给出具体理由） |
| `fast` | 快速建立项目地图 | 仍生成十章，但每章只保留主要子系统所需证据；必须交代 `system_structure` 与 `core_flow`；实际图表通常不超过 2 张；至少 1 条核心链路和 1 个通过语法级验证的示例（manifest `validation.examples.status = passed`） |
| `targeted` | 只更新指定章节/主题 | 仅写目标章节；**任何写入前**必须运行 `python <skill_root>/scripts/validate_book.py <repo> --snapshot` 并把结果存入 manifest `preservation` 字段；无关章节的字节与时间戳保持不变；不创建空占位章节 |

模式判定：用户未指定时，仓库尚无 `project-book/` 用 `full`；已有教材且用户只关心特定主题用 `targeted`；用户要求"快速了解"用 `fast`。

## 三、流水线与技能→章节映射

唯一产物目录是目标仓库下的 `project-book/`（含 `.learning-manifest.json`）。**不要创建 `docs/analysis/` 等其他产物目录。**

子技能编号与章节编号不是一一对应，以下表为准：

| 顺序 | 子技能 | 写入章节 | manifest 职责 |
| --- | --- | --- | --- |
| 1 | [01-repo-discovery](01-repo-discovery/SKILL.md) | `01-project-overview.md` | `subprojects`、`project_types`、`entrypoints`、`chapter_sources`、`head_sha` |
| 2 | [02-config-and-installation](02-config-and-installation/SKILL.md) | `02-installation.md` | 本章 `chapter_sources` |
| 3 | [03-architecture-analysis](03-architecture-analysis/SKILL.md) | `03-architecture.md` | 本章 `chapter_sources` + `diagrams`（system_structure、runtime_deployment） |
| 4 | [04-code-flow-analysis](04-code-flow-analysis/SKILL.md) | `04-core-flow.md` | 本章 `chapter_sources` + `diagrams`（core_flow） |
| 5 | [05-concept-extraction](05-concept-extraction/SKILL.md) | `05-core-concepts.md` | 本章 `chapter_sources` + `diagrams`（domain_model、lifecycle，按需） |
| 6 | [06-tutorial-writer](06-tutorial-writer/SKILL.md) | `06-source-code-guide.md`、`07-extension-guide.md`（对 01–05 只读） | 两章 `chapter_sources` |
| 7 | [07-example-generator](07-example-generator/SKILL.md) | `08-examples.md` | 本章 `chapter_sources` + `validation.examples` |
| 8 | [08-learning-review](08-learning-review/SKILL.md) | `09-faq.md`、`10-learning-checklist.md` | 汇总顶层字段与 `validation`，执行完成门禁 |

子技能可单独调用（如用户只要数据流分析时只跑 04），但写入的章节仍必须满足 output-contract；单独调用后若产出完整教材，仍应运行完成门禁。

## 四、项目类型识别（线索，不是结论）

先运行跨平台清单脚本，再结合目录特征判断类型、决定学习重点：

```bash
python <skill_root>/scripts/inventory_repo.py <repo>
```

**目录名只是线索**：类型结论必须由 manifest、入口或实现代码佐证并标注 `文件:行号`，不得把目录名直接当成架构事实。

| 类型 | 常见线索 | 学习重点 |
| --- | --- | --- |
| 消息中间件 | channel/、broker/ | 消息入口、路由、消费者 |
| Web 应用 | router/、controller/ | 路由、请求处理、持久化 |
| CLI 工具 | cmd/、commands/ | 命令注册、参数解析 |
| 库/框架 | src/、lib/ | API 设计、契约、扩展点 |
| Agent 框架 | agent/、tools/ | Agent 循环、工具系统 |
| 数据库/存储 | engine/、storage/ | 查询解析、存储引擎 |

所有类型都按第三节的完整流水线执行；类型只影响各阶段的深挖重点与示例选择。

## 五、调度示例

- **完整学习**（"帮我学习这个项目，生成完整教材"）→ `full`：按 1→8 全量执行。
- **快速了解**（"快速掌握核心架构和扩展方式"）→ `fast`：仍按 1→8 执行，但每章精简到主子系统证据；至少 1 条核心链路时序图 + 1 个语法级验证示例。
- **针对性深挖**（"只想理解核心数据流"）→ `targeted --target 04-core-flow.md`：先 snapshot，只更新目标章节及其图表/manifest 条目。
- **准备贡献代码** → `full`，重点精读 06/07 章（源码导航 + 扩展指南）与 10 章实践任务。

## 六、全局硬性规则（对所有子技能生效）

1. **证据**：关键结论必须回指 `文件:行号`（仓库相对 POSIX 路径）；每章至少一条内联证据引用，且被引文件必须登记进该章 `chapter_sources`。
2. **分级**：命令与结论标注 已运行 / 静态验证 / 静态推断 / 未运行；README 表述只是线索，需对照 manifest、入口、测试或实现确认。
3. **安全**：默认只做静态分析；安装依赖、启动容器、迁移、外部 API 调用需用户明确授权；只输出配置变量名与非敏感默认值，严禁输出真实密钥值。
4. **占位符**：交付章节中不得残留任何 `[占位符]` 样式文本（校验器会直接拒绝）。
5. **图表**：只使用 diagram-contract 定义的 Mermaid 块格式并登记 manifest；每图回答一个学习问题，≤12 节点、≤18 边；节点用真实源码名，禁止虚构通用分层。
6. **门禁**：结束前必须运行 `python <skill_root>/scripts/validate_book.py <repo> --mode <mode>`（targeted 追加 `--target`），输出 PASS 才算完成；FAIL 时回到对应阶段修复后重跑。

## 七、最终产物

```text
project-book/
├── .learning-manifest.json      # 源码基线、证据、图表与验证状态（schema_version 2）
├── 01-project-overview.md       # 项目形状、技术栈、入口、阅读路线
├── 02-installation.md           # 安装、配置优先级、变量名（不含密钥值）
├── 03-architecture.md           # 模块边界、依赖方向、运行时/部署 + 结构图
├── 04-core-flow.md              # 1–3 条代表性链路 + 时序图
├── 05-core-concepts.md          # 真实抽象、契约、不变量、扩展点 + 按需类图/状态图
├── 06-source-code-guide.md      # 目标导向源码导航
├── 07-extension-guide.md        # 项目专属扩展步骤与注册位置
├── 08-examples.md               # 项目原生示例（标注验证状态）
├── 09-faq.md                    # 来自真实缺口的 FAQ
└── 10-learning-checklist.md     # 覆盖矩阵、验证结果、练习任务
```