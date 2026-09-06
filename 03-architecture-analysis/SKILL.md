---
name: 03-architecture-analysis
description: 分析模块边界、依赖方向、运行时进程、部署拓扑、跨切面能力与架构风险，生成 project-book/03-architecture.md，并按契约交代系统结构图与运行时/部署图
---

# 03-Architecture Analysis — 架构分析

> 目标：让读者建立"系统由什么组成、运行时怎么协作、部署在哪里"的立体地图。

必读：[../references/output-contract.md](../references/output-contract.md)、[../references/evidence-and-safety.md](../references/evidence-and-safety.md)、[../references/diagram-contract.md](../references/diagram-contract.md)（本技能必须产出或显式豁免两类图表，Diagram contract 必须完整读取）。

## 职责

输出：
- 模块边界与职责（以真实接口与 import/调用为据，不是目录名猜测）
- 依赖方向（谁依赖谁、分层是否清晰、有无循环依赖）
- 运行时进程（进程/线程/worker/队列消费者及其通信方式）
- 部署拓扑（容器、服务、存储、外部依赖，仅采信声明性来源）
- 跨切面能力（日志、认证、错误处理、中间件链）
- 架构决策与风险（推断必须标注「静态推断」）

## 执行流程

### Step 1：确定模块边界

以 01 的清单为起点，对每个核心目录：读它的公开接口（`__init__.py`、`index.ts`、包导出、public API），列出关键类型/函数并标注 `文件:行号`。目录名只是线索——职责结论必须来自接口与实现代码。

### Step 2：分析依赖方向

用 import/require/use 语句构建模块间依赖（跨平台，优先 rg）：

```bash
rg -n "^(import|from) " --type py        # Python
rg -n "^import |require\(" --type ts     # TS/JS
rg -n "^import " --type go               # Go
```

整理出：哪些模块在底层被广泛依赖、依赖是否单向分层、有无循环依赖或越层调用。每条依赖边记录证据（文件:行号）。

### Step 3：识别运行时进程

寻找进程/并发证据：入口启动逻辑、`Dockerfile` CMD、`docker-compose` services、worker/队列消费者注册、线程池/asyncio 事件循环。区分"单进程多线程"与"多进程协作"，标注同步/异步边界（消息队列、回调、任务调度）。

### Step 4：部署拓扑（只采信声明性来源）

仅依据：Dockerfile、compose、k8s manifest、CI workflow、IaC（Terraform 等）、官方部署文档。仓库中没有任何部署声明时，**不要虚构拓扑**——在 manifest 中把 `runtime_deployment` 记为 `not_applicable`，理由写"仓库无部署声明文件"。

### Step 5：跨切面能力

定位日志、认证/鉴权、错误处理、配置加载、中间件/拦截器的实现位置与挂载方式（装饰器、中间件链、AOP、钩子），各给一处代表性证据。

### Step 6：架构决策与风险

- 决策：从代码事实反推设计意图（如"存储层用接口隔离，便于替换后端"），每条标注「静态推断」并给出支撑文件。
- 风险：必须指向具体位置（循环依赖、上帝对象、缺超时/重试、密钥硬编码痕迹等），并给缓解建议。

### Step 7：生成两类契约图表

按 Diagram contract 交代两个角色（full 模式两个都必须交代；实际画图或 `not_applicable` + 具体理由）：

| 角色 | 回答的学习问题 | Mermaid 形式 | 触发条件 |
| --- | --- | --- | --- |
| `system_structure` | 系统有哪些职责边界与外部参与者？ | flowchart（manifest type 为 `context` 或 `component`） | 多参与者/外部系统，或 ≥3 个职责边界 |
| `runtime_deployment` | 运行时哪些进程/容器/存储/队列在交互？ | flowchart（manifest type 为 `deployment`） | ≥2 个进程/容器/数据存储/队列 |

图表硬性规则（细节以 Diagram contract 为准）：
- 一图只回答一个学习问题；≤12 个主要节点、≤18 条边；嵌套不超过两层。
- 节点用真实源码/部署名称 + 中文职责注释；**禁止虚构通用 Controller/Service/Repository 分层**。
- 块格式：`<!-- diagram:kebab-case-id -->` 注释紧贴 Mermaid fence；图后依次给出 Purpose、阅读说明（新手向白话，鼓励配一句现实类比）、证据索引（`路径:行号`）、验证状态（未运行渲染器时最高标「静态验证」）、已知缺口。
- 每张图登记进 manifest `diagrams`（id/chapter/role/type/status/purpose/sources/node_count/edge_count），图引用的文件同时进入本章 `chapter_sources`。

### Step 8：写入章节

生成 `project-book/03-architecture.md`，结构（占位符交付前必须全部替换）：

```markdown
# 架构分析

## 架构概览
一段话总结 + system_structure 图（或 not_applicable 说明）。

## 模块边界与职责
每个模块：职责一句话、关键类型/函数、证据 `文件:行号`。

## 依赖方向
分层结论 + 关键依赖边列表（带证据）+ 循环依赖检查结论。

## 运行时视图
进程/线程/异步边界说明 + runtime_deployment 图（或 not_applicable 说明）。

## 部署拓扑
声明性来源逐条列出；无声明时明确说"仓库未声明"。

## 跨切面能力
日志/认证/错误处理/中间件：实现位置 + 挂载方式。

## 架构决策（静态推断）
每条：决策 → 支撑证据 → 推断标注。

## 架构风险与建议
每条：风险位置 → 影响 → 缓解建议。
```

更新 manifest：本章 `chapter_sources`、`diagrams` 条目。

## 输出物

- `project-book/03-architecture.md`

## 质量检查

```
✓ 每个模块职责结论是否都有 file:line 证据，而非目录名猜测？
✓ system_structure 与 runtime_deployment 两个角色是否都已交代（实图或 not_applicable+理由）？
✓ 图表节点是否与真实源码/部署名一一对应，并已登记 manifest？
✓ 图表是否 ≤12 节点/≤18 边，且图后五要素（Purpose/阅读说明/证据/验证状态/缺口）齐全？
✓ 决策与风险是否标注「静态推断」？
✓ 是否无占位符、无虚构部署拓扑？
```

## 参考

- [../references/diagram-contract.md](../references/diagram-contract.md)
- [../references/evidence-and-safety.md](../references/evidence-and-safety.md)