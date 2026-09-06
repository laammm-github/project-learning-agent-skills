---
name: 08-learning-review
description: 生成 project-book/09-faq.md 与 10-learning-checklist.md，汇总 manifest，并强制运行 validate_book.py 作为完成门禁（PASS 才算学习完成）
---

# 08-Learning Review — 学习检查（完成门禁）

> 目标：语义查缺补漏 + 确定性校验双管齐下；教材只有在 `validate_book.py` 输出 PASS 后才算完成。

必读：[../references/output-contract.md](../references/output-contract.md)、[../references/evidence-and-safety.md](../references/evidence-and-safety.md)、[../references/diagram-contract.md](../references/diagram-contract.md)（校验图表登记时对照）。

## 执行流程

### Step 1：语义审阅全部章节

通读 `project-book/01`–`08` 与 manifest，做交叉一致性检查：
- 章节间引用是否成立（04 的链路是否用上 03 的模块名、06 的导航是否指向真实存在的文件）；
- 证据是否充足（结论有无 `文件:行号`、分级标注是否正确）；
- 图表是否与正文一致（节点/边能否在源码中找到对应）。

### Step 2：识别知识盲区

把 01 章清单中的模块/manifest 与 03–05 章已分析内容对比，列出未覆盖的机制（如配置热更新、认证、错误处理、测试策略、某子项目）。盲区靠语义对比得出，每条给出建议的补课入口文件。

### Step 3：生成 09-faq.md

问题必须来自**真实缺口**：架构疑问、安装坑、校验失败暴露的问题、盲区。禁止编造泛泛问题。

```markdown
# 常见问题

每个问题：Q（具体场景）→ A（结论 + 证据 `文件:行号`）→ 相关章节链接。
```

### Step 4：生成 10-learning-checklist.md

```markdown
# 学习检查清单

## 语义覆盖矩阵
| 学习目标 | 对应章节 | 覆盖状态 | 缺口/备注 |
（目标含：一句话定位、模块边界、核心链路、契约与扩展点、配置系统、部署形态）

## 验证结果汇总
validate_book.py 的最终输出（PASS/FAIL 历史）、manifest validation 各项状态、已运行/静态验证/未运行清单。

## 已知未知
盲区清单 + 每条的补课入口文件。

## 练习任务
3–5 个动手任务（读某文件回答某问题 / 跑某示例 / 做某小扩展），由浅入深。
```

### Step 5：汇总 manifest

补全/核对顶层字段：`schema_version: 2`、`repo_root`、`head_sha`、`generated_at`、`mode`、`targets`、`subprojects`、`project_types`、`entrypoints`、`chapter_sources`（覆盖全部十章）、`diagrams`、`validation`（paths/markdown/placeholders/secrets/diagrams/examples 六项，每项 status 合法；`failed` 不允许留在最终 manifest 中）。targeted 模式核对 `preservation` 快照存在且未在写入后刷新。

### Step 6：运行完成门禁（硬性）

```bash
python <skill_root>/scripts/validate_book.py <repo> --mode <full|fast|targeted>
# targeted 模式对每个目标章节追加 --target <chapter>
```

- 输出 **PASS** → 学习完成，把结果写入 10 章"验证结果汇总"。
- 输出 **FAIL** → 逐条阅读 ERROR：定位其所属章节与生成阶段（如证据路径失效→对应分析阶段；图表未登记→03/04/05；占位符→对应写作阶段；manifest 缺字段→本阶段），修复后**重跑校验**，循环直到 PASS。不允许带 FAIL 交付。
- WARNING（如示例未运行验证）如实记入 10 章，不得隐瞒或改写成"已验证"。

### Step 7：增量更新场景（已有教材时）

按 evidence-and-safety 的增量规则：先查 Git status 与现有 manifest；manifest HEAD 与当前不一致时用 `git diff --name-only <old>..<new>` 取变更清单（排除 `project-book/` 自身），经 `chapter_sources` 映射到受影响章节做 targeted 更新；无法区分生成文本与用户手写文本时，停下来询问，不得覆盖。

## 输出物

- `project-book/09-faq.md`
- `project-book/10-learning-checklist.md`
- 完整 manifest + `validate_book.py` PASS

## 质量检查

```
✓ 门禁是否真实运行且最终 PASS（命令与输出已记入 10 章）？
✓ FAQ 是否全部来自真实缺口（每条有证据或指向章节）？
✓ 覆盖矩阵是否对照过 01 章清单，而非凭印象打勾？
✓ manifest 六个 validation 子项是否状态合法且无 failed 残留？
✓ targeted 模式下 preservation 快照是否未被写入后刷新？
✓ WARNING 是否如实呈现？
```

## 参考

- [../references/output-contract.md](../references/output-contract.md)
- [../references/evidence-and-safety.md](../references/evidence-and-safety.md)