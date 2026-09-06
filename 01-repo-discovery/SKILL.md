---
name: 01-repo-discovery
description: 扫描项目结构，识别项目类型，生成项目概览文档（一句话定位、技术栈、入口文件）
---

# 01-Repo Discovery — 项目发现

> 目标：扫描项目结构，识别项目类型，生成项目概览文档

---

## 职责

快速扫描项目，输出：
- 项目是什么（一句话定位）
- 技术栈
- 目录结构
- 入口文件
- 项目类型判断

---

## 执行流程

### Step 1：扫描顶层结构

```bash
# 优先使用结构化清单
python scripts/inventory_repo.py <目标仓库>
# 或手动查看
ls -la
find . -maxdepth 1 -type d | sort
```

输出：`project-overview.md` 的"目录结构"章节

### Step 2：识别项目类型

根据目录特征判断（见主 Skill.md 的"项目类型识别"表）

输出：`project-overview.md` 的"项目类型"章节

### Step 3：读取 README

提取：
- 项目定位
- 核心特性
- 快速开始命令
- 架构图（如果有）

输出：`project-overview.md` 的"项目简介"章节

### Step 4：找入口文件

```bash
# 优先使用结构化清单
python scripts/inventory_repo.py <目标仓库> --entrypoints

# 或手动搜索（rg 跨平台）
# Python
rg --files | rg "main\.py$|app\.py$|__main__\.py$"

# Node
rg --files | rg "index\.ts$|server\.js$"

# Go
rg --files | rg "main\.go$"
```

输出：`project-overview.md` 的"入口文件"章节

### Step 5：分析依赖

```bash
# 优先使用结构化清单
python scripts/inventory_repo.py <目标仓库> --deps

# 或直接读取依赖文件
cat requirements.txt    # Python
cat package.json        # Node
cat go.mod             # Go
```

输出：`project-overview.md` 的"技术栈"章节

### Step 6：生成 project-overview.md

结构：

```markdown
# 项目概览：[项目名]

## 基本信息
- 语言：
- 协议：
- 入口：

## 一句话定位
[项目是做什么的？]

## 核心特性
1. ...
2. ...
3. ...

## 目录结构
[树状图]

## 入口文件
- Python: [路径]
- Node: [路径]

## 技术栈
- 框架：
- 数据库：
- 消息队列：
- 其他依赖：

## 快速开始
[安装 + 运行命令]
```

---

## 输出物

- `project-book/01-project-overview.md`

---

## 质量检查

```
✓ 一句话定位是否清晰？
✓ 目录结构是否标注了核心模块？
✓ 入口文件是否准确？
✓ 技术栈是否完整？
```

---

## 参考

- CLAUDE.md Generator 类 Skill（社区案例）
- Agent Skills 官方规范：https://github.com/agentskills/agentskills