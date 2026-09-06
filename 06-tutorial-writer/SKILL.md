---
name: 06-tutorial-writer
description: 将原始分析数据整合转化为人类可读的教学文档和教程
---

# 06-Tutorial Writer — 教程生成

> 目标：将原始分析数据转化为人类可读的教学文档

---

## 职责

从"代码分析者"变成"老师"，输出：
- 源码导航（06-source-code-guide.md）
- 扩展开发指南（07-extension-guide.md）

**重要原则**：
- 01-05 的原始分析数据**保留不变**（存放在 project-book/）
- 06 只负责生成 06-07 章节，**不覆盖** 01-05

---

## 执行流程

### Step 1：读取原始分析数据

读取 01-05 生成的原始数据：

```
project-book/
├── 01-project-overview.md      # 原始数据
├── 02-installation.md          # 原始数据
├── 03-architecture.md          # 原始数据
├── 04-core-flow.md            # 原始数据
└── 05-core-concepts.md        # 原始数据
```

### Step 2：按教学顺序重组

**教学顺序 ≠ 代码顺序**：

```
错误顺序：从第 1 行代码开始
正确顺序：
  第 1 章：项目介绍（What）→ 01-project-overview.md（已有）
  第 2 章：快速开始（How to run）→ 02-installation.md（已有）
  第 3 章：架构概览（How it's built）→ 03-architecture.md（已有）
  第 4 章：核心流程（How it works）→ 04-core-flow.md（已有）
  第 5 章：核心概念（Key Concepts）→ 05-core-concepts.md（已有）
  第 6 章：源码导航（Where to find）→ 06-source-code-guide.md（生成）
  第 7 章：扩展开发（How to extend）→ 07-extension-guide.md（生成）
```

### Step 3：生成 06-source-code-guide.md

**职责**：按模块/文件组织源码导航

结构：

```markdown
# 源码导航

## 按模块导航

### [模块 1 目录] - [模块 1 职责]
- [文件 1:行号] - [类/函数]（[一句话说明]）
- [文件 2] - [核心方法]（[说明]）
- [文件 3] - [扩展点]（[说明]）

### [模块 2 目录] - [模块 2 职责]
...

## 按文件深度阅读

### 如果只想读 3 个文件（最快理解路径）
1. [入口文件]（理解项目怎么启动）
2. [核心契约文件]（理解核心接口）
3. [处理逻辑文件]（理解数据怎么流）

### 如果想深入某个模块
- [模块 A]：读 [最简实现] → 对比 [复杂实现]
- [模块 B]：读 [基类/抽象] → [具体实现 1] → [具体实现 2]
```

> **通用化提示**：根据项目类型调整：
> - Web 应用：路由注册 → Controller → Service → Repository
> - CLI 工具：Command Parser → Command Registry → Command Handler
> - 消息系统：Broker → Topic → Consumer
> - 数据库：Query Parser → Executor → Storage Engine

### Step 4：生成 07-extension-guide.md

**职责**：扩展开发指南（步骤说明 + 最少实现）
**与 07-example-generator 的区别**：
- 06 只负责：步骤说明、最小可运行示例、注册位置说明
- 07 负责：完整模板代码、多语言示例、配置示例

结构：

```markdown
# 扩展开发指南

## [扩展类型 1：如"添加新通道/模块"]

### 步骤 1：创建扩展类
```python
# [扩展文件路径]
from [基类/抽象] import [BaseClass]

class MyExtension([BaseClass]):
    """自定义扩展模板"""
    extension_type = "[类型标识]"
    
    def startup(self):
        """初始化连接/资源"""
        print(f"[{self.extension_type}] Started")
    
    def process(self, input_data):
        """核心处理逻辑"""
        # 1. 验证输入
        # 2. 执行业务逻辑
        # 3. 返回结果
        result = self._do_work(input_data)
        return result
    
    def output(self, result):
        """输出结果"""
        print(f"[{self.extension_type}] Sending: {result}")
```

### 步骤 2：注册到工厂/注册表
在 `[注册文件]` 添加：
```python
elif extension_type == "[类型标识]":
    from [扩展路径] import MyExtension
    ch = MyExtension()
```

### 步骤 3：测试
```bash
[项目启动命令]
```

## [扩展类型 2：如"添加新工具/功能"]

### 步骤 1：创建工具类
```python
# [工具文件路径]
from [基类] import [BaseTool]

class MyTool([BaseTool]):
    """自定义工具模板"""
    name = "my_tool"
    description = "[工具描述]"
    params = {
        "type": "object",
        "properties": {
            "[参数名]": {
                "type": "string",
                "description": "[参数说明]"
            }
        },
        "required": ["[参数名]"]
    }
    
    def execute(self, params: dict) -> [ResultType]:
        action = params.get("[参数名]")
        # 实现工具逻辑
        return [ResultType].success(f"Action {action} performed")
```

### 步骤 2：注册到 [注册文件]
在 `[注册文件]` 添加：
```python
__all__ = [
    ...
    "MyTool",
]
```

## [扩展类型 3：如"添加新插件/中间件"]

### 参考示例
- [最简单示例路径]（最简单）
- [复杂示例路径]（功能完整）

### 最小结构
```
[插件目录]/
├── __init__.py
├── [plugin].py
├── config.json.template  # 配置模板
└── README.md
```
```

### Step 5：添加"下一步"引导

每章结尾：

```markdown
---
**下一步**：进入第 X 章 [章节名] →
**深入阅读**：[相关文件路径]
**实践**：[动手任务]
```

---


### Step 6：生成交互式导航页

生成 project-book/index.html（单文件自包含，无外部依赖）：

```html
<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[项目名] 学习教材</title>
<style>
  :root { --bg: #fff; --fg: #1a1a1a; --border: #e0e0e0; --link: #2563eb; --code-bg: #f5f5f5; }
  [data-theme="dark"] { --bg: #1a1a2e; --fg: #e0e0e0; --border: #333; --link: #60a5fa; --code-bg: #2a2a3e; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--fg); display: flex; min-height: 100vh; }
  nav { width: 260px; border-right: 1px solid var(--border); padding: 1rem; position: sticky; top: 0; height: 100vh; overflow-y: auto; }
  nav a { display: block; padding: 0.4rem 0.5rem; color: var(--link); text-decoration: none; border-radius: 4px; font-size: 0.9rem; }
  nav a:hover { background: var(--code-bg); }
  main { flex: 1; padding: 2rem; max-width: 900px; }
  .theme-toggle { margin-bottom: 1rem; cursor: pointer; background: var(--code-bg); border: 1px solid var(--border); padding: 0.3rem 0.8rem; border-radius: 4px; color: var(--fg); }
  pre { background: var(--code-bg); padding: 1rem; border-radius: 6px; overflow-x: auto; margin: 1rem 0; }
  h2 { margin-top: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
  h3 { margin-top: 1.5rem; }
  p, li { line-height: 1.7; }
  /* Mermaid 暗色适配 */
  [data-theme="dark"] .mermaid { filter: invert(0.85) hue-rotate(180deg); }
</style>
</head>
<body>
<nav>
  <button class="theme-toggle" onclick="toggleTheme()">切换亮暗主题</button>
  <a href="#ch1">第 1 章：项目概览</a>
  <a href="#ch2">第 2 章：安装与配置</a>
  <a href="#ch3">第 3 章：架构分析</a>
  <a href="#ch4">第 4 章：核心链路</a>
  <a href="#ch5">第 5 章：核心概念</a>
  <a href="#ch6">第 6 章：源码导航</a>
  <a href="#ch7">第 7 章：扩展开发</a>
  <a href="#ch8">第 8 章：示例</a>
  <a href="#ch9">第 9 章：FAQ</a>
  <a href="#ch10">第 10 章：检查清单</a>
</nav>
<main>
  <!-- 从 project-book/ 各章节提取标题、Mermaid 图、关键段落填充此处 -->
  <div id="ch1"><!-- 01-project-overview.md 内容 --></div>
  <div id="ch2"><!-- 02-installation.md 内容 --></div>
  <div id="ch3"><!-- 03-architecture.md 内容 --></div>
  <div id="ch4"><!-- 04-core-flow.md 内容 --></div>
  <div id="ch5"><!-- 05-core-concepts.md 内容 --></div>
  <div id="ch6"><!-- 06-source-code-guide.md 内容 --></div>
  <div id="ch7"><!-- 07-extension-guide.md 内容 --></div>
  <div id="ch8"><!-- 08-examples.md 内容 --></div>
  <div id="ch9"><!-- 09-faq.md 内容 --></div>
  <div id="ch10"><!-- 10-learning-checklist.md 内容 --></div>
</main>
<script>
  function toggleTheme() {
    const html = document.documentElement;
    html.dataset.theme = html.dataset.theme === 'dark' ? 'light' : 'dark';
  }
</script>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'default' });
</script>
</body>
</html>
```

**要求**：
- 嵌入所有 Mermaid 图到对应章节
- 亮暗双主题切换（纯 CSS，system font stack）
- 确认 index.html 可离线打开且图正常渲染


## 输出物

- `project-book/06-source-code-guide.md`
- `project-book/07-extension-guide.md`

**注意**：不生成 01-05，仅整合 01-05 的原始数据

---

## 数据流说明

```
原始数据（01-05）          教学转换（06）           最终产物（project-book）
project-book/      →     06-tutorial-writer     →    project-book/
├── 01-project-overview.md     （只读）              ├── 01-project-overview.md
├── 02-installation.md         （只读）              ├── 02-installation.md
├── 03-architecture.md         （只读）              ├── 03-architecture.md
├── 04-core-flow.md            （只读）              ├── 04-core-flow.md
└── 05-core-concepts.md        （只读）              ├── 05-core-concepts.md
                                                         ├── 06-source-code-guide.md ← 生成
                                                         └── 07-extension-guide.md ← 生成
```

---

## 质量检查

```
✓ 是否只生成 06-07，不覆盖 01-05？
✓ 06 是否按模块组织源码导航？
✓ 07 是否提供可复制的扩展模板？
✓ 是否有"下一步"引导？
✓ index.html 是否可离线打开且图正常渲染？
✓ 模板是否通用化（不绑定特定项目类型）？
```

---

## 参考

- Claude Technical Writing Skill 模式
- 你的"项目学习 Skill"中的教程生成章节
- 技术文档最佳实践（Diátaxis 框架）