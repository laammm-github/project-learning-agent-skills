---
name: 01-repo-discovery
description: 扫描仓库结构，识别子项目、技术栈与真实入口，生成带 file:line 证据的 project-book/01-project-overview.md
---

# 01-Repo Discovery — 项目发现

> 目标：弄清"项目是什么、由什么组成、从哪里开始读"，产出有证据的项目概览。

必读：[../references/output-contract.md](../references/output-contract.md)（章节验收与 manifest）、[../references/evidence-and-safety.md](../references/evidence-and-safety.md)（规模控制与证据分级）。

## 职责

输出：
- 项目形状（单项目 / Monorepo / 混合栈）与仓库目录结构
- 项目类型判断（线索 + 证据，不是目录名猜测）
- 技术栈（回指 manifest 文件）
- 已确认的入口文件（打开看过，带行号）
- 新人阅读路线

## 执行流程

### Step 1：获取结构化清单（跨平台）

优先使用本技能自带脚本，保证 Windows/Linux/macOS 行为一致：

```bash
python <skill_root>/scripts/inventory_repo.py <repo>
```

输出 JSON 包含：manifest 清单、已确认 `entrypoints`、`entrypoint_candidates`、顶层目录（已排除依赖/构建/VCS 目录）。需要补充搜索时用 `rg --files` 或 `rg <pattern> -n`（无 rg 时回退跨平台文件遍历）。**不要使用 `find`、`ls -la`、`grep -r` 等 bash-only 命令。**

### Step 2：识别项目类型（线索，不是结论）

结合清单与主 SKILL.md 的"项目类型识别"表做初步判断；结论必须由 manifest、入口或实现代码佐证并标注 `文件:行号`。Monorepo 按子项目分别记录类型与 manifest。

### Step 3：读取 README 与 manifest

README 表述只是线索：技术栈、运行方式等关键断言必须对照 `pyproject.toml` / `package.json` / `go.mod` / `Cargo.toml` 等 manifest 确认。提取：项目定位、核心特性、快速开始命令。

### Step 4：确认入口文件

对清单给出的 `entrypoints` 与采用的 `entrypoint_candidates` 逐一打开确认（例如 `src/app.py:12` 定义了 `create_app()`），未打开确认的候选不得写成结论。

### Step 5：规划阅读路线

给出"从哪开始读"的最短路径：入口 → 核心契约/抽象 → 主要流程实现，落到具体文件。

### Step 6：写入章节与 manifest

生成 `project-book/01-project-overview.md`，结构（方括号内容交付前必须替换为真实值，产物中不得残留占位符）：

```markdown
# 项目概览：项目真实名称

## 基本信息
- 语言/运行时（证据：`pyproject.toml:12`）
- 协议（证据：`LICENSE:1`）
- 项目类型：结论 + 证据

## 一句话定位
项目是做什么的，一段话说清。

## 核心特性
每条特性附实现位置证据。

## 仓库形状与目录结构
树状图 + 核心模块一句话职责标注；说明排除过的依赖/构建目录。

## 子项目（Monorepo 时；单项目省略本节）
每个子项目：路径、manifest、类型。

## 入口文件
已确认入口，逐个带 `文件:行号`。

## 技术栈
框架/存储/消息队列/外部依赖，逐项回指 manifest 位置。

## 快速开始
命令来自官方文档或 manifest scripts；本次未实际执行的命令标注「未运行」。

## 阅读路线
入口 → 契约 → 实现的具体文件顺序。
```

同时写入 manifest 字段：`head_sha`（`git rev-parse HEAD`，非 Git 仓库为 null）、`generated_at`、`mode`、`subprojects`、`project_types`、`entrypoints`、`chapter_sources` 中本章条目（= 本章引用过的全部文件）。

## 输出物

- `project-book/01-project-overview.md`
- `project-book/.learning-manifest.json`（初始字段）

## 质量检查

```
✓ 一句话定位是否有 manifest/README/代码证据支撑？
✓ 入口是否全部打开确认过（带行号），而不是照抄候选清单？
✓ 本章内联证据路径是否都已登记进 chapter_sources？
✓ 阅读路线是否落到具体文件路径？
✓ 是否无占位符残留、无密钥值？
```

## 参考

- [../references/output-contract.md](../references/output-contract.md)
- [../references/evidence-and-safety.md](../references/evidence-and-safety.md)