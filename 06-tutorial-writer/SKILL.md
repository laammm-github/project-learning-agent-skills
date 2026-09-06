---
name: 06-tutorial-writer
description: 基于 project-book/01–05 的分析数据（只读），生成目标导向的 06-source-code-guide.md 与 07-extension-guide.md，不改写前序章节
---

# 06-Tutorial Writer — 教程生成

> 目标：从"代码分析者"切换为"老师"——把 01–05 的证据组织成读者可按目标导航的源码地图和可动手的扩展指南。

必读：[../references/output-contract.md](../references/output-contract.md)（章节验收）、[../references/evidence-and-safety.md](../references/evidence-and-safety.md)（增量更新规则）。

## 硬性边界

- **输入**：`project-book/01-project-overview.md` 至 `05-core-concepts.md`（**只读**）。
- **输出**：仅 `project-book/06-source-code-guide.md` 与 `project-book/07-extension-guide.md` 两个文件。
- **不得改写 01–05 的任何字节**（targeted 模式下这由 manifest `preservation` 快照强制校验）。
- 不存在 `docs/analysis/` 之类的中间目录；一切输入输出都在 `project-book/` 内。
- 若发现 01–05 有错误或过期结论：不要就地修改，记录到章节"已知问题"并交由编排器调度对应阶段（targeted 模式）修正。

## 执行流程

### Step 1：读取 01–05 并建立索引

提取：入口清单（01）、模块边界（03）、链路关键跳（04）、核心抽象与扩展点（05）。本章写作只复用这些已有证据，需要补充新证据时同样标注 `文件:行号` 并登记进本章 `chapter_sources`。

### Step 2：生成 06-source-code-guide.md（源码导航）

**教学顺序 ≠ 代码顺序**。按读者目标组织：

```markdown
# 源码导航

## 按目标导航
- 想理解启动过程 → 读哪些文件（顺序 + 每步看什么）
- 想理解核心链路 → 沿 04 章时序图的文件顺序
- 想理解数据模型 → 05 章抽象对应的源码位置

## 按模块导航
每个模块（来自 03 章边界）：职责一句话 → 关键文件与符号（`文件:行号`）→ 扩展点。

## 最短理解路径（只读 3 个文件）
1. 入口文件（项目怎么启动）
2. 核心契约文件（核心接口/抽象）
3. 主流程实现文件（数据怎么流动）

## 深入某模块的推荐阅读序
先读最简实现，再对比复杂实现；先读基类，再读具体子类。
```

### Step 3：生成 07-extension-guide.md（扩展开发指南）

**项目专属**、可照着做的步骤（与 07-example-generator 分工：本章写步骤、注册位置与测试方式；完整示例代码模板由 08-examples.md 提供）：

```markdown
# 扩展开发指南

## 扩展类型一（来自 05 章识别的真实扩展点）
### 步骤 1：创建实现（继承哪个真实基类/接口，文件放哪）
### 步骤 2：注册（真实注册表/工厂位置，`文件:行号`）
### 步骤 3：配置（涉及的配置项名）
### 步骤 4：测试（项目现有测试怎么跑，新扩展怎么验证）
### 兼容约束（版本、接口稳定性说明）

## 扩展类型二/三（同上）

## 参考现成实现
最简单实现（先读）→ 功能最全实现（对照）。
```

要求：出现的每个类名、注册函数、目录都必须真实存在并带证据；代码片段从源码摘录或做最小改写，不得虚构 API。

### Step 4：添加"下一步"引导

两章结尾给出：下一步阅读（指向其他章节）、深入文件清单、一个动手任务。

### Step 5：更新 manifest

登记两章的 `chapter_sources`（含引用到的全部源码文件）。

## 输出物

- `project-book/06-source-code-guide.md`
- `project-book/07-extension-guide.md`

## 质量检查

```
✓ 是否只写了 06/07 两个文件，01–05 字节未动？
✓ 导航是否按"读者目标"组织，且每条落到具体文件与行号？
✓ 扩展指南的基类/注册点/测试命令是否全部真实存在？
✓ 是否没有虚构 API 或占位符残留？
✓ 是否有"下一步"引导？
```

## 参考

- [../references/output-contract.md](../references/output-contract.md)
- [../references/evidence-and-safety.md](../references/evidence-and-safety.md)