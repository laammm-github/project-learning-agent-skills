# project-learning-agent

一个面向 Codex 的通用项目学习技能。它会从代码仓库的 manifest、入口、配置、部署文件、实现和测试中提取证据，生成可追溯、可验证、支持增量更新的项目学习手册。

它不针对某个框架或业务领域，也不会把目录名直接当成架构事实。分析结论必须能回指仓库内真实的 `文件:行号`，未执行的命令和静态推断会明确标注。

## 能做什么

- 识别单项目、Monorepo 和混合技术栈的子系统、构建清单与真实入口。
- 解释安装流程、配置变量、加载优先级和安全边界，不输出密钥值。
- 分析模块边界、运行时进程、依赖方向、部署拓扑、跨切面能力和架构风险。
- 追踪代表性代码流，覆盖输入、变换、输出、持久化和异常路径。
- 提取真实的领域类型、接口、schema、不变量和扩展点。
- 按学习问题生成有证据的 Mermaid UML 风格图，覆盖系统结构、部署、时序，并按需生成类图和状态图。
- 生成源码导航、扩展指南、示意示例、可运行示例、FAQ 和学习检查清单。
- 通过 manifest 记录 Git 源码基线、证据文件和验证状态，支持安全的定向更新。

## 使用方式

将本目录放入 Codex 的技能目录并保持目录名为 `project-learning-agent`。技能支持自动发现，也可以在请求中显式使用：

```text
使用 $project-learning-agent 学习这个仓库。
```

技能会在目标仓库的 `project-book/` 下生成或更新十章教材：

```text
project-book/
├── .learning-manifest.json
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

## 三种模式

| 模式 | 适用场景 | 输出规则 |
| --- | --- | --- |
| `full` | 第一次理解整个仓库 | 生成十章详细教材 |
| `fast` | 快速建立项目地图 | 仍生成十章，但内容精简；必须包含一条核心链路和一个已验证示例 |
| `targeted` | 只更新指定主题或章节 | 仅更新目标章节及必要依赖；无关章节的字节和时间戳必须保持不变 |

每次运行都会在 `.learning-manifest.json` 中写入 `schema_version: 2`、源码 `head_sha`、模式、目标章节、子项目、入口、章节证据、图表元数据和验证状态。

## UML 风格图规则

图表用于回答明确的学习问题，不作为装饰，也不会把整个代码库自动转成类图。默认使用可随 Markdown 审查的 Mermaid：

- 完整模式交代系统结构、运行时/部署和每条代表性核心链路；不适用时必须记录理由。
- 快速模式优先保留一张系统结构图和一张核心链路时序图。
- 定向模式只更新目标章节相关图表，保留其他图表及 manifest 记录。
- 每个节点和重要连线都必须来自真实源码、配置或部署声明，并提供 `文件:行号` 证据索引。
- 单图最多 12 个主要节点、18 条边；超过时按子系统或场景拆分。
- 类图只描述核心契约和代表性实现；状态图只有在存在至少三个真实状态及转换时才生成。
- 图表未经渲染器检查时只标记为 `静态验证`，不能声称已渲染通过。

Mermaid 的上下文、组件和部署图属于 UML 风格视图，不等同于严格 UML。仅当用户明确要求并且工具可用时使用 PlantUML。完整契约见 [references/diagram-contract.md](references/diagram-contract.md)。

## 子技能

完整流程按依赖顺序使用以下八个子技能：

1. `01-repo-discovery`：仓库发现与入口确认
2. `02-config-and-installation`：安装与配置
3. `03-architecture-analysis`：架构、进程与部署
4. `04-code-flow-analysis`：代表性代码流
5. `05-concept-extraction`：概念、契约与不变量
6. `06-tutorial-writer`：源码导航与扩展指南
7. `07-example-generator`：项目原生示例
8. `08-learning-review`：覆盖审查、FAQ、清单与确定性校验

章节依赖顺序是：发现 → 配置/架构 → 数据流/概念 → 导航/示例 → 审查。定向模式也必须遵守这个顺序，但只写入必要的目标文件。

## 命令行工具

在本技能目录执行：

```powershell
# 输出仓库清单；不输出源码内容或密钥值
python scripts/inventory_repo.py <repo>

# 校验教材、证据、manifest、Markdown 和敏感信息
python scripts/validate_book.py <repo> --mode full

# 定向更新前保存章节哈希和时间戳基线
python scripts/validate_book.py <repo> --snapshot

# 校验技能结构并运行脚本测试
python scripts/self_check.py
```

`inventory_repo.py` 会区分 manifest 确认的 `entrypoints` 和仅由文件名发现的 `entrypoint_candidates`。`validate_book.py` 会拒绝失效证据路径、越界行号、未闭合 Markdown 围栏、遗留占位符、凭据 URL、未脱敏密钥赋值，以及未登记、超复杂、来源失效或错误声称已渲染的图表。

## 安全与增量更新

- 默认只做静态分析；不会擅自安装依赖、启动容器、执行迁移或调用外部 API。
- 配置只读取模板、schema 和变量名；真实 `.env`、环境变量和密钥不会进入教材。
- 可运行示例必须使用项目实际语言，并通过原生语法、类型检查、测试或运行验证；否则只能标记为示意或未运行。
- 旧教材没有 manifest 时按 legacy 处理：先保留内容、建立基线，再逐步更新可验证部分。
- 定向模式写入前必须执行 `--snapshot`，并将快照原样写入 manifest 的 `preservation` 字段；不能在写入后重新生成快照。
- `head_sha` 表示源码分析基线。只提交 `project-book/` 不会使源码基线失效；真实源码变化则需要重新评估受影响章节。

详细规则见 [references/output-contract.md](references/output-contract.md)、[references/evidence-and-safety.md](references/evidence-and-safety.md) 和 [references/diagram-contract.md](references/diagram-contract.md)。

## 开发与验证

技能仓库自身包含跨平台 GitHub Actions，覆盖 Windows/Linux 与 Python 3.11/3.12。提交前运行：

```powershell
python scripts/self_check.py
```

当前测试覆盖 Monorepo、空格路径、Windows 路径、无 Git、缺少 `rg`、损坏 Markdown、失效证据、占位符、敏感信息、图表契约、fast 模式约束、targeted 模式保留以及 book-only Git 提交等场景。

## 设计边界

十章文件名和八个子技能名称是兼容性接口，不代表每个仓库都适合相同深度。入口识别和项目类型分类使用常见生态的启发式规则；冷门工具链或语义结论仍需要人工复核。技能不会创建 `agents/openai.yaml`，以保留现有自动发现行为。
