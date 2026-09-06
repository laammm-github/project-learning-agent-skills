# project-book 模板

> 学习完成后，生成的最终产物目录结构

---

## 目录结构

```
project-book/
├── 01-project-overview.md       # 项目简介、技术栈、快速开始
├── 02-installation.md           # 安装与配置指南
├── 03-architecture.md           # 系统架构、模块职责、数据流
├── 04-core-flow.md              # 核心链路（用户请求完整路径）
├── 05-core-concepts.md          # 关键设计模式、抽象、契约
├── 06-source-code-guide.md      # 源码导航（按模块、按文件）
├── 07-extension-guide.md        # 扩展开发指南（通道、工具、插件）
├── 08-examples.md               # 最小可运行示例
├── 09-faq.md                    # 常见问题与疑难解答
└── 10-learning-checklist.md     # 学习检查清单
```

---

## 生成规则

### 由 Orchestrator 协调生成

```
子 Skill → 输出文件
01-repo-discovery → 01-project-overview.md
02-config-and-installation → 02-installation.md
03-architecture-analysis → 03-architecture.md
04-code-flow-analysis → 04-core-flow.md
05-concept-extraction → 05-core-concepts.md
06-tutorial-writer → 06-source-code-guide.md + 07-extension-guide.md
07-example-generator → 08-examples.md
08-learning-review → 09-faq.md + 10-learning-checklist.md
| （管道） | .pipeline/ 下 8 个 JSON 中间产物（每阶段自动写入） |
```

### 特殊文件

- `02-installation.md`：由 02-config-and-installation 生成（分析配置系统）
- `06-source-code-guide.md`：由 06-tutorial-writer 整合（基于 01-05 原始数据）
- `07-extension-guide.md`：由 06-tutorial-writer 整合 + 07-example-generator 提供模板

---

## 使用方式

```bash
# 学习完成后，目录应包含：
ls project-book/
01-project-overview.md
02-installation.md
...
10-learning-checklist.md

# 新人可以按顺序阅读 01-10
# 或按需跳转（如只看 03-04 了解架构和核心流程）
```

---

## 质量检查

```
✓ 10 个文件是否都存在？
✓ 每个文件是否有实质性内容（非空）？
✓ 是否有交叉引用（如"详见第 X 章"）？
✓ 代码示例是否可运行？
✓ 图表是否清晰（Mermaid 格式正确）？
```