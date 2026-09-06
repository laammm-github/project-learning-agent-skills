# project-book 模板

> 学习完成后，目标仓库内最终产物的目录结构与验收规则。契约细节以 references/output-contract.md 为准。

---

## 目录结构

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
├── 08-examples.md               # 项目原生示例（逐例标注验证状态）
├── 09-faq.md                    # 来自真实缺口的 FAQ
└── 10-learning-checklist.md     # 覆盖矩阵、验证结果、已知未知、练习任务
```

- full/fast 模式：十章 + manifest 全部必须存在。
- targeted 模式：manifest + 目标章节必须存在；无关章节字节与时间戳保持不变（写入前用 `validate_book.py <repo> --snapshot` 采集快照存入 manifest `preservation`）。

---

## 生成规则（技能 → 章节映射）

| 子技能 | 写入章节 |
| --- | --- |
| 01-repo-discovery | 01-project-overview.md（+ manifest 初始字段） |
| 02-config-and-installation | 02-installation.md |
| 03-architecture-analysis | 03-architecture.md（+ system_structure / runtime_deployment 图表条目） |
| 04-code-flow-analysis | 04-core-flow.md（+ core_flow 图表条目） |
| 05-concept-extraction | 05-core-concepts.md（+ 按需 domain_model / lifecycle 图表条目） |
| 06-tutorial-writer | 06-source-code-guide.md + 07-extension-guide.md（对 01–05 只读） |
| 07-example-generator | 08-examples.md（+ validation.examples） |
| 08-learning-review | 09-faq.md + 10-learning-checklist.md（+ manifest 汇总与完成门禁） |

注意：子技能编号与章节编号不是一一对应（06 号技能写 06+07 两章，07 号技能写 08 章，08 号技能写 09+10 章）。

---

## 图表规则（详见 references/diagram-contract.md）

- 一律使用 Mermaid；块前紧贴 `<!-- diagram:kebab-case-id -->` 注释，并登记进 manifest `diagrams`。
- 每图回答一个学习问题；≤12 节点、≤18 边；节点用真实源码/部署名。
- 图后五要素齐全：Purpose、阅读说明（新手向白话，鼓励一句类比）、证据索引（路径:行号）、验证状态、已知缺口。
- full 模式必须交代 system_structure / runtime_deployment / core_flow 三个角色；fast 模式交代 system_structure / core_flow；不适用记 not_applicable + 具体理由。

---

## 验收清单（交付前逐项确认）

```
✓ 十章 + .learning-manifest.json 是否齐全且非空？
✓ python scripts/validate_book.py <repo> --mode <mode> 是否输出 PASS（硬门禁）？
✓ 每章是否至少一条内联证据（路径:行号），且引用文件已登记 chapter_sources？
✓ 图表是否全部按契约登记（无未注册 Mermaid 块、无失效登记）？
✓ 是否无占位符残留（形如 [项目名]、[路径] 的文本）？
✓ 是否无任何真实密钥/凭据值（可疑值已 <redacted>）？
✓ 示例是否逐例标注验证状态，示意性示例未被称为可运行？
✓ 章节间是否有交叉引用（"详见第 X 章"）且指向成立？
```