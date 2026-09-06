---
name: 02-config-and-installation
description: 分析安装步骤、配置加载优先级与环境变量名（不输出密钥值），生成 project-book/02-installation.md
---

# 02-Config & Installation — 安装与配置

> 目标：让读者能按文档把项目跑起来，并理解配置从哪来、谁覆盖谁。

必读：[../references/output-contract.md](../references/output-contract.md)、[../references/evidence-and-safety.md](../references/evidence-and-safety.md)（本技能涉及配置检查与安全执行，必须先读）。

## 密钥安全（硬性规则）

- 只输出**变量名、非敏感默认值、加载优先级**；严禁复制真实 `.env`、凭据存储、shell 环境或 CI secrets 中的值。
- 优先读取 `.env.example`、`.env.default`、schema 定义和设置代码，而不是真实 `.env`。
- 可疑值一律写 `<redacted>`；含凭据的连接串只保留协议与主机结构，凭据部分打码。
- 不要为了发现变量名而打印整个环境或配置文件。

## 职责

输出：
- 环境要求与官方安装步骤（标注验证状态）
- 配置加载流程与优先级（默认值 → 配置文件 → 环境变量 → 命令行）
- 环境变量映射表（变量名 → 作用 → 定义位置）
- 常见配置场景示例（脱敏）

## 执行流程

### Step 1：识别配置系统

```bash
rg -n "\.env|config|settings" --glob "*.{py,ts,js,go,rs,java}" -l
rg --files -g ".env.example" -g "*.toml" -g "*.yaml" -g "docker-compose*"
```

找到：配置文件格式（JSON/YAML/TOML/INI/.env）、配置模块位置、模板文件。

### Step 2：分析配置加载流程与优先级

打开配置模块源码，确认实际加载顺序与覆盖规则（例如 `config.py:34` 中 env 覆盖文件值），画出优先级链：

```text
硬编码默认值 → 配置模板/文件 → 环境变量 → 命令行参数（后者覆盖前者）
```

每一级标注证据 `文件:行号`；仅从代码结构推断、未运行验证的结论标注「静态推断」。

### Step 3：提取环境变量映射

从 `.env.example`、schema 或设置代码提取变量清单：

| 变量名 | 作用 | 默认值（非敏感） | 定义位置 |
| --- | --- | --- | --- |
| 示例：DATABASE_URL | 主数据库连接 | 无（必填，值 `<redacted>`） | `app/settings.py:21` |

### Step 4：整理安装步骤

命令必须来自官方文档、manifest scripts 或 Dockerfile，标注来源与验证状态：
- 本次实际执行成功 → 「已运行」+ 原始命令
- 只做语法/静态检查 → 「静态验证」
- 未执行（安装依赖、启动容器等需用户授权）→ 「未运行」+ 原因

### Step 5：写入章节与 manifest

生成 `project-book/02-installation.md`，结构（占位符交付前必须全部替换）：

```markdown
# 安装与配置指南

## 环境要求
语言版本、系统依赖（证据：manifest/CI 配置）。

## 安装步骤
1. 步骤 + 命令 + 来源与验证状态
2. ...

## 配置系统
### 配置格式与文件位置
### 配置加载流程与优先级（每级带证据）
### 环境变量映射表（只有变量名，无真实值）
### 常见配置场景（脱敏示例）

## 验证安装
如何确认服务正常启动（健康检查端点/命令），未执行的标注「未运行」。

## 常见问题
配置相关的真实坑（来自代码中的报错处理/文档警告）。
```

更新 manifest：本章 `chapter_sources`（含引用过的配置文件与源码；**不要把真实 `.env` 列入**）。

## 输出物

- `project-book/02-installation.md`

## 质量检查

```
✓ 安装命令是否都有来源，且验证状态标注正确？
✓ 配置优先级是否有代码证据，而不是想当然？
✓ 环境变量表是否只有变量名与非敏感默认值？
✓ 是否无任何真实密钥/凭据/连接串密码（可疑值已 <redacted>）？
✓ 占位符是否已全部替换？
```

## 参考

- [../references/evidence-and-safety.md](../references/evidence-and-safety.md)
- [../references/output-contract.md](../references/output-contract.md)