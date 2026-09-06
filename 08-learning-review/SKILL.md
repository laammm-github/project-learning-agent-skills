---
name: 08-learning-review
description: 验证学习完整性，生成学习检查清单和 FAQ，查漏补缺
---

# 08-Learning Review — 学习检查

> 目标：验证学习完整性，生成检查清单，查漏补缺

---

## 职责

- 检查是否完成核心学习目标
- 生成学习检查清单
- 识别知识盲区
- 提供下一步学习建议

---

## 执行流程

### Step 1：核对核心目标

根据项目类型，检查是否掌握：

**逻辑伪代码（供 Agent 参考执行）**：

```
if project_type == "消息中间件":
    checks = [
        "能说清消息从哪来、到哪去",
        "能画出消息流图",
        "知道通道如何注册",
        "知道路由逻辑在哪",
        "知道消费者如何消费",
    ]
elif project_type == "Web 应用":
    checks = [
        "能说清 HTTP 请求完整路径",
        "知道路由注册在哪",
        "知道控制器逻辑",
        "知道数据库操作",
        "知道中间件链",
    ]
elif project_type == "CLI 工具":
    checks = [
        "知道命令注册机制",
        "知道参数解析流程",
        "知道命令执行链路",
        "知道帮助文档如何生成",
    ]
elif project_type == "Agent 框架":
    checks = [
        "能描述 Agent 规划循环",
        "知道工具如何调用",
        "知道记忆系统",
        "知道扩展点",
    ]
elif project_type == "库/框架":
    checks = [
        "知道 API 文档位置",
        "知道核心类关系",
        "知道如何集成到现有项目",
        "知道常见使用模式",
    ]
elif project_type == "数据库/存储":
    checks = [
        "知道查询解析流程",
        "知道存储引擎",
        "知道事务机制",
        "知道索引原理",
    ]

# 通用检查（所有项目类型）
checks.extend([
    "能用一句话说明项目是什么",
    "知道核心目录职责",
    "知道怎么启动项目",
    "知道怎么扩展（根据项目类型确定扩展方式）",
])
```

### Step 2：检查产出物完整性

**逻辑伪代码（供 Agent 参考执行）**：

```
expected_outputs = [
    "01-project-overview.md",
    "02-installation.md",
    "03-architecture.md",
    "04-core-flow.md",
    "05-core-concepts.md",
    "06-source-code-guide.md",
    "07-extension-guide.md",
    "08-examples.md",
]

# Agent 需要检查：
for output in expected_outputs:
    if 文件不存在:
        标记为缺失
```

### Step 3：识别知识盲区

检查是否有未覆盖的模块：

**逻辑伪代码（供 Agent 参考执行）**：

```
blind_spots = []

# 检查分析文档中是否覆盖以下内容：
if "config" not in 已分析的模块:
    blind_spots.append("配置系统工作原理")

if "plugin" not in 已分析的模块:
    blind_spots.append("插件/中间件机制")

if "error_handling" not in 已分析的模块:
    blind_spots.append("异常处理路径")

if "testing" not in 已分析的模块:
    blind_spots.append("测试覆盖范围")

# 根据项目类型补充特定盲区
if project_type == "Web 应用":
    if "middleware" not in 已分析的模块:
        blind_spots.append("中间件链")
    if "auth" not in 已分析的模块:
        blind_spots.append("认证授权机制")

if project_type == "Agent 框架":
    if "tool" not in 已分析的模块:
        blind_spots.append("工具调用机制")
    if "memory" not in 已分析的模块:
        blind_spots.append("记忆系统")
```

**Agent 需要执行的实际操作**：

```bash
# 检查配置系统分析
grep -ri "config\|配置" project-book/03-architecture.md project-book/01-project-overview.md

# 检查插件/中间件分析
grep -ri "plugin\|中间件\|middleware" project-book/03-architecture.md

# 检查异常处理分析
grep -ri "error\|exception\|异常\|错误" project-book/04-core-flow.md

# 检查测试覆盖分析
grep -ri "test\|测试" project-book/01-project-overview.md project-book/03-architecture.md
```

### Step 4：生成学习检查清单

结构：

```markdown
# 学习检查清单

## 核心目标完成度

### 项目理解
- [ ] 能用一句话说明项目是什么
- [ ] 知道项目类型：[类型]
- [ ] 知道核心技术栈

### 架构理解
- [ ] 能画出数据流图
- [ ] 知道核心模块职责
- [ ] 知道模块间依赖关系

### 核心链路
- [ ] 能描述"输入 → 处理 → 输出"完整路径
- [ ] 知道路由/分发逻辑
- [ ] 知道核心算法/循环流程

### 扩展开发
- [ ] 知道怎么添加[扩展类型 1]
- [ ] 知道怎么添加[扩展类型 2]
- [ ] 知道怎么写[扩展类型 3]

### 配置系统
- [ ] 知道配置加载流程
- [ ] 知道如何修改配置

## 产出物检查

- [ ] 01-project-overview.md ✓
- [ ] 02-installation.md ✓
- [ ] 03-architecture.md ✓
- [ ] 04-core-flow.md ✓
- [ ] 05-core-concepts.md ✓
- [ ] 06-source-code-guide.md ✓
- [ ] 07-extension-guide.md ✓
- [ ] 08-examples.md ✓

## 知识盲区

| 盲区 | 建议 | 相关文件 |
|------|------|---------|
| 配置系统 | 深入阅读 config.py/config.json | [路径] |
| 插件系统 | 读 [最简单插件] 源码 | [路径] |
| 异常处理 | 检查 try-except 链 | [路径] |

## 下一步学习建议

1. [深入某个模块]
2. [尝试修改一个小功能]
3. [读测试代码了解正确行为]
4. [贡献 PR 或写自己的扩展]
```

### Step 5：生成 FAQ

基于知识盲区，生成常见问题：

```markdown
# 常见问题

## Q: 这个项目的配置系统怎么工作？
A: [简要说明]

## Q: 怎么添加[扩展类型]？
A: [步骤说明]

## Q: 核心数据流是怎样的？
A: [简要说明]
```

---


### Step 6：设计挑战练习

基于 05 章提取的扩展点，设定一个"增加新功能"的场景，要求读者完成 6 维评估：

1. **暴露给调用者的知识量**：新接口需要调用者知道多少内部细节？
2. **依赖方向**：新代码是否依赖了不稳定的模块？是否引入了反向依赖？
3. **变更局部性**：如果未来需求变化，改动范围是否集中？
4. **可观测性**：新功能出问题时，排查难度如何？
5. **迁移成本**：现有调用方需要改多少代码？
6. **变化是否真实存在**：这个需求是真实业务需求还是假设？

至少生成 1 个设计挑战任务，任务格式：

`markdown
### 设计挑战：[简短标题]

**场景**：[具体的新功能需求描述]

**要求**：
- 设计接口/类/模块边界
- 回答上述 6 维评估，每维 1-3 句话

**参考**：05 章 [扩展点名称]（文件:行号）
`

「静态推断」——所有设计挑战基于 AI 对代码的理解，不保证 100% 准确。

## 输出物

- `project-book/09-faq.md`
- `project-book/10-learning-checklist.md`

---

## 质量检查

```
✓ 检查清单是否覆盖核心学习目标？
✓ 是否识别了知识盲区？
✓ 是否有具体的下一步建议？
✓ FAQ 是否针对实际盲区？
✓ 检查清单是否适配了项目类型？
```

---

## 参考

- 你的"项目学习 Skill"中的检查清单章节
- 认知科学中的"元认知"（对学习的思考）