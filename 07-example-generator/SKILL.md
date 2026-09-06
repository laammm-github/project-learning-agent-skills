---
name: 07-example-generator
description: 生成项目原生的示意示例与可运行示例，逐一标注验证状态，生成 project-book/08-examples.md 并写入 manifest validation.examples
---

# 07-Example Generator — 示例生成

> 目标：用最小的真实代码验证学习成果——读者复制、替换少量值、就能跑（或明确知道哪些只是示意）。

必读：[../references/output-contract.md](../references/output-contract.md)、[../references/evidence-and-safety.md](../references/evidence-and-safety.md)（"Safe execution"与示例验证规则）。

## 硬性规则

1. **项目原生**：示例必须调用目标仓库真实存在的 API/类/命令（来自 05 章扩展点与 06 章导航）。禁止套用任何外部项目的模式或想象出来的 API。
2. **语言范围**：以项目主语言为主；只有当仓库本身就提供多语言客户端/示例时才补充其他语言。
3. **验证状态逐例标注**（与 manifest 词汇一致）：
   - `已运行`：本次实际执行成功，附完整命令与输出摘要；
   - `静态验证`：通过了语法/类型级检查（附命令），或仅由源码证据支撑但未执行；
   - `示意性伪代码`：帮助理解结构，**严禁声称为可运行**。
4. **可运行示例的门槛**：不含任何未替换占位符，且至少通过语言原生语法/类型检查（如 `python -m py_compile`、`tsc --noEmit`、`go vet`）。
5. **fast 模式**：至少 1 个示例达到 `静态验证` 以上并通过语法级检查，manifest `validation.examples` 记为 `passed`（含 `command`、`exit_code: 0`、`level`）。
6. **执行边界**：运行示例若需安装依赖、启动容器或调用外部 API，须用户明确授权；否则只做语法级检查并标「未运行」+ 原因。

## 执行流程

### Step 1：Hello World 示例（最小入口）

用项目的真实入口/公开 API 写最小可运行片段：初始化 → 一次核心调用 → 打印结果。所有导入路径、类名、函数名逐一与源码核对（`文件:行号`）。

### Step 2：扩展示例（对照真实扩展点）

从 05 章扩展点中选 1–2 个，参照仓库内**现成最简实现**生成模板：

```text
模板骨架（写作参考，交付时必须实例化为项目真实 API）：
1. 继承/实现真实基类或接口（写明导入路径与基类位置证据）
2. 实现契约要求的方法（逐个对照 05 章契约清单）
3. 注册到真实注册表/工厂（写明注册位置证据）
4. 触发与验证方式（项目现有的运行/测试命令）
```

### Step 3：配置示例（脱敏）

常见配置场景各一份（切换后端、启用某功能等），只用变量名与安全的示例值；任何疑似敏感值写 `<redacted>` 或 `your-value-here`。

### Step 4：验证并记录

- 对每个"可运行"声明的示例执行语法级检查，记录命令与退出码。
- 写入 manifest：`validation.examples`（status/command/exit_code/level/reason）+ 本章 `chapter_sources`。
- 未达验证门槛的示例一律降级标注为「示意性伪代码」。

### Step 5：写入章节

生成 `project-book/08-examples.md`，结构（占位符交付前必须全部替换）：

```markdown
# 示例集

## 示例索引
| 示例 | 类型（可运行/示意） | 验证状态 | 验证命令 |
| --- | --- | --- | --- |

## Hello World
完整代码 + 运行方式 + 预期输出 + 证据（调用的 API 位置）。

## 扩展模板（每个扩展点一节）
完整代码 + 注册步骤 + 测试方式 + 对照的现成实现路径。

## 配置示例（脱敏）

## FAQ 式排错
示例跑不起来时的常见原因（来自真实报错处理代码/文档）。
```

## 输出物

- `project-book/08-examples.md`
- manifest `validation.examples` 条目

## 质量检查

```
✓ 每个示例调用的 API 是否都在源码中核实过（file:line）？
✓ 是否每个示例都有验证状态标注，且示意性示例没有被称为可运行？
✓ 可运行示例是否零占位符并附语法检查命令与结果？
✓ fast 模式下 validation.examples 是否为 passed（command + exit_code 0 + level）？
✓ 配置示例是否无任何敏感值？
```

## 参考

- [../references/evidence-and-safety.md](../references/evidence-and-safety.md)
- [../references/output-contract.md](../references/output-contract.md)