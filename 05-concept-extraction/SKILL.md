---
name: 05-concept-extraction
description: 从源码提取真实抽象、契约、不变量与扩展点，生成 project-book/05-core-concepts.md，按需配类图与状态图
---

# 05-Concept Extraction — 概念提取

> 目标：把源码转化为读者可迁移的心智模型——项目定义了哪些核心抽象、它们承诺了什么、在哪里扩展。

必读：[../references/output-contract.md](../references/output-contract.md)、[../references/evidence-and-safety.md](../references/evidence-and-safety.md)、[../references/diagram-contract.md](../references/diagram-contract.md)（类图/状态图规则）。

## 职责

输出：
- 核心抽象（真实的类/接口/trait/schema，摘录关键签名，带 `文件:行号`）
- 设计契约（必须实现什么、数据格式约定、例外场景）
- 不变量（代码中强制维持的规则：唯一性、状态约束、边界检查）
- 扩展点（框架预留的注册/继承/插件位置）
- 类比理解（帮助记忆，但类比不能替代代码证据）
- 按需的 `domain_model` 类图与 `lifecycle` 状态图

**纪律**：只提取**真实存在**的抽象。本技能内出现的任何示例基类只是格式参考，不得写入教材；每个概念必须能在源码中搜到。

## 执行流程

### Step 1：识别核心抽象

从 03 的模块边界和 04 的链路出发，找被多处依赖的类型/接口：

```bash
rg -n "class .*(Base|Abstract|Interface|Protocol)" --type py
rg -n "interface |abstract class " --type ts
```

对每个核心抽象：摘录真实签名（关键方法 + 类型注解），标注 `文件:行号`，列出已知实现类及其位置。

### Step 2：提炼设计契约

每个核心抽象写清：
- **必须实现**：抽象方法/必填字段（证据：NotImplementedError、abstract 标记、schema required）
- **约定**：输入输出格式、命名/注册规则
- **例外**：可选行为、默认实现、特殊分支

### Step 3：提取不变量

找代码中强制维持的规则：唯一性检查、状态转移守卫、边界/参数校验、事务约束。每条不变量给出执行位置证据。

### Step 4：定位扩展点

框架留给使用者的挂点：注册表/工厂、插件发现机制、钩子/中间件接口、配置驱动的策略选择。写明"从哪个文件开始照抄哪个现成实现"。

### Step 5：类比理解（辅助，不是证据）

为每个核心概念配一句现实类比（如消息路由 ≈ 邮局分拣、插件注册 ≈ 电器插座），帮助建立直觉。类比表格必须同时给出代码位置；类比与代码行为冲突时以代码为准并说明差异。

### Step 6：按需生成类图/状态图

| 角色 | 触发条件 | Mermaid 形式 |
| --- | --- | --- |
| `domain_model` | ≥3 个核心类型之间存在真实的继承/组合/关联关系 | `classDiagram` |
| `lifecycle` | 某真实实体有 ≥3 个**有证据的**状态与转移（状态守卫/持久化/事件） | `stateDiagram-v2` |

- **枚举本身不构成状态机**；只有当代码里存在围绕状态的转移逻辑与守卫时才画 lifecycle。
- 类图只含核心接口/基类、代表性实现、中心实体、重要签名与有意义关系，不做全量类清单。
- 状态图包含转移触发条件、关键守卫、副作用/持久化、失败转移与终态。
- 不满足触发条件就不画，也不必登记 not_applicable（这两个角色是"按需"而非"必须交代"）。
- 块格式、图后五要素与 manifest 登记遵循 Diagram contract。

### Step 7：写入章节

生成 `project-book/05-core-concepts.md`，结构（占位符交付前必须全部替换）：

```markdown
# 核心概念

## 关键抽象
每个抽象：是什么（一句话）→ 真实签名摘录 → 位置 `文件:行号` → 已知实现 → 为什么这样设计（静态推断）。

## 设计契约
每个契约：必须实现/约定/例外 + 证据。

## 不变量
每条：规则 → 强制执行位置。

## 扩展点
每个：挂点位置 → 参考现成实现 → 注册方式。

## 领域模型类图（满足触发条件时）
## 生命周期状态图（满足触发条件时）

## 类比理解
| 概念 | 代码位置 | 现实类比 | 类比局限 |
```

更新 manifest：本章 `chapter_sources`、`diagrams` 条目（如有）。

## 输出物

- `project-book/05-core-concepts.md`

## 质量检查

```
✓ 每个概念是否都能在源码中搜到（真实签名 + 行号），而非示例模板？
✓ 契约是否区分了"必须实现"与"可选行为"？
✓ 类图/状态图是否只在触发条件满足时生成，且已登记 manifest？
✓ 状态图是否基于真实转移逻辑（枚举不算状态机）？
✓ 类比是否同时给出代码位置与类比局限？
✓ 是否无占位符残留？
```

## 参考

- [../references/diagram-contract.md](../references/diagram-contract.md)
- [../references/evidence-and-safety.md](../references/evidence-and-safety.md)