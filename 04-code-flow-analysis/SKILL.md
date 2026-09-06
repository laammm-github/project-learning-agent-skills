---
name: 04-code-flow-analysis
description: 追踪 1–3 条代表性核心链路的输入、变换、输出、持久化与异常路径，生成 project-book/04-core-flow.md，每条链路配契约时序图
---

# 04-Code Flow Analysis — 代码流分析

> 目标：跟着一次真实请求走完全程，把每一跳的数据变换和失败路径讲清楚。

必读：[../references/output-contract.md](../references/output-contract.md)、[../references/evidence-and-safety.md](../references/evidence-and-safety.md)、[../references/diagram-contract.md](../references/diagram-contract.md)（每条选定链路配一张时序图）。

## 职责

输出：
- 1–3 条代表性核心链路（full 模式按重要性选；fast 模式至少 1 条）
- 每条链路：入口 → 每一跳（文件/函数/输入/变换/输出）→ 持久化/事件 → 返回
- 至少一条失败/超时/取消路径
- 每条链路一张 `core_flow` 时序图（sequenceDiagram）

**纪律**：所有链路必须来自真实源码追踪。本技能中出现的任何"典型流程"只是思考模板，**不得作为证据写入教材**；写入教材的每一跳都要有 `文件:行号`。未运行验证的调用顺序标注「静态验证」或「静态推断」。

## 执行流程

### Step 1：选定代表性链路

从 01 确认的入口和 03 的模块边界出发，选对用户价值最高的流程（如 Web 应用的"一次 API 请求"、消息系统的"一条消息从投递到消费"、CLI 的"一条命令执行"）。选择理由写进章节。

### Step 2：逐跳追踪

从入口函数开始逐层打开源码，对每一跳记录：

| 字段 | 内容 |
| --- | --- |
| 位置 | `文件:行号`（函数/方法定义处） |
| 输入 | 接收的数据与类型 |
| 变换 | 做了什么处理（校验/转换/聚合/调用外部） |
| 输出 | 返回的数据与类型 |
| 边界 | 同步/异步、进程内/跨网络、是否持久化或发事件 |

追踪时可用（跨平台）：

```bash
rg -n "def handle|func .*Handler|app\.(get|post)|add_route" <repo>
```

### Step 3：标注数据变换链

把每一跳的输入→输出串成变换链，用真实类型/字段名（来自源码），示意：

```text
用户输入 "hello"（str）
  → 入口封装为请求上下文对象（证据：`app/api.py:42`）
  → 校验与规范化（证据：`app/service.py:88`）
  → 持久化 + 发布事件（证据：`app/repo.py:31`）
  → 响应序列化（证据：`app/api.py:57`）
```

### Step 4：识别异常路径

对每条链路至少记录一条失败路径：错误在哪捕获、如何回退/重试/超时、错误响应格式、是否写入日志或死信。均带证据。

### Step 5：每条链路生成时序图

- 角色 `core_flow`，Mermaid `sequenceDiagram`；触发条件：链路 ≥3 跳，或包含异步/回调/重试/超时/取消。
- 必须呈现：发起者与输入、同步与异步边界、重要变换、持久化/事件、返回值、至少一条适用失败路径。
- participant 用真实类/服务/队列名，禁止虚构通用分层；≤12 节点、≤18 边。
- 块格式与图后五要素（Purpose/阅读说明/证据索引/验证状态/已知缺口）遵循 Diagram contract；登记 manifest `diagrams`（role=core_flow, type=sequence）。

### Step 6：写入章节

生成 `project-book/04-core-flow.md`，结构（占位符交付前必须全部替换）：

```markdown
# 核心链路

## 链路选择说明
选了哪几条、为什么有代表性。

## 链路一：真实流程名
### 路径总览（时序图）
### 逐跳详解（每跳：位置/输入/变换/输出/边界）
### 数据变换链（真实类型与字段）
### 关键参数传递表（参数 → 在哪设置 → 在哪使用 → 证据）
### 异常路径（场景 → 处理方式 → 证据）

## 链路二/三（同上结构；fast 模式可只保留一条）
```

更新 manifest：本章 `chapter_sources`、`diagrams` 条目。

## 输出物

- `project-book/04-core-flow.md`

## 质量检查

```
✓ 每一跳是否都有 file:line 证据？是否没有把思考模板当成项目事实？
✓ 每条选定链路是否各有一张已登记的时序图？
✓ 时序图是否包含异步边界与至少一条失败/超时路径？
✓ 数据变换是否用真实类型/字段名标注了输入→输出？
✓ 调用顺序未运行时是否标注了「静态验证/静态推断」？
✓ 是否无占位符残留？
```

## 参考

- [../references/diagram-contract.md](../references/diagram-contract.md)
- [../references/evidence-and-safety.md](../references/evidence-and-safety.md)