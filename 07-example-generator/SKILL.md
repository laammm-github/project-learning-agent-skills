---
name: 07-example-generator
description: 生成最小可运行示例和扩展模板，验证学习成果
---

# 07-Example Generator — 示例生成

> 目标：生成最小可运行示例和扩展模板

---

## 职责

输出：
- 完整扩展模板（可直接复制使用）
- 多语言示例（Python/Java/Go/TS 等）
- 配置示例（常见场景）
- FAQ 式解决方案

**与 06-tutorial-writer 的区别**：
- 06-tutorial-writer 负责：步骤说明、最小示例、注册位置
- 07-example-generator 负责：完整模板代码、多语言变体、配置示例

---

## 执行流程

### Step 1：生成 Hello World 示例

从最简单的入口开始，替换 `[项目入口]` 为实际入口点：

```python
# 通用模板（根据项目类型调整）：
# 文件：examples/hello_[项目类型].py

# Python 项目示例：
from [入口模块] import [入口类]

app = [入口类]()
app.startup()

# 发送消息/触发处理
result = app.process(
    input_data="hello",
    context={"type": "[项目类型]"}
)

print(f"结果：{result}")
```

> **通用化提示**：
> - Web 应用：启动 Flask/FastAPI 服务器 → cURL 测试
> - CLI 工具：运行命令 → 查看输出
> - 消息系统：发送消息 → 接收消息
> - 库/框架：import 模块 → 调用函数

### Step 2：生成扩展模板

参考现有扩展，生成通用模板：

```python
# 通用扩展模板（适用于大多数框架）：
# 文件：examples/custom_extension.py

from [基类模块] import [BaseClass]

class MyExtension([BaseClass]):
    """自定义扩展模板"""
    extension_type = "myextension"
    supported_features = []
    
    def startup(self):
        """初始化连接/资源"""
        print(f"[{self.extension_type}] Started")
    
    def process(self, input_data):
        """
        核心处理逻辑
        输入：input_data（类型由契约定义）
        输出：result（类型由契约定义）
        """
        # 1. 验证输入
        if not input_data:
            return self._error("Empty input")
        
        # 2. 执行业务逻辑
        result = self._do_work(input_data)
        
        # 3. 返回结果
        return result
    
    def _do_work(self, data):
        """具体的业务逻辑实现"""
        # 替换为你的实际逻辑
        return {"status": "ok", "data": data}
    
    def output(self, result):
        """输出结果"""
        print(f"[{self.extension_type}] Result: {result}")
```

```python
# 工具/功能模板（适用于 Agent 框架或类似架构）：
# 文件：examples/custom_tool.py

from [工具基类] import [BaseTool], [ResultType]

class MyTool([BaseTool]):
    """自定义工具模板"""
    name = "my_tool"
    description = "My custom tool - [请替换描述]"
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
    stage = [决策阶段]  # 如 PRE_PROCESS, RUN 等
    
    def execute(self, params: dict) -> [ResultType]:
        action = params.get("[参数名]")
        try:
            # 实现工具逻辑
            result = self._execute_action(action)
            return [ResultType].success(result)
        except Exception as e:
            return [ResultType].error(str(e))
    
    def _execute_action(self, action):
        """具体的工具逻辑"""
        return f"Action {action} performed"
```

```python
# 插件/中间件模板（适用于事件驱动架构）：
# 文件：examples/custom_plugin.py

from [注册模块] import register
from [上下文模块] import ContextType
from [回复模块] import Reply, ReplyType
from [插件基类] import Plugin, Event, EventAction

@register(
    name="MyPlugin",
    desire_priority=0,       # 优先级（数字越大越先执行）
    hidden=False,            # 是否在插件列表可见
    enabled=True,            # 默认是否启用
    desc="[插件描述]",
    version="0.1",
    author="[作者名]",
)
class MyPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
    
    def on_handle_context(self, e_context: EventContext):
        # 检查消息类型
        if e_context["context"].type != ContextType.TEXT:
            return
        
        # 处理消息
        content = e_context["context"].content
        # 替换为实际处理逻辑
        if "[触发条件]" in content.lower():
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = f"[响应内容]"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
    
    def get_help_text(self, **kwargs):
        return "[帮助文本]"
```

### Step 3：生成配置示例

```json
{
  // 示例 1：切换组件/模型/后端
  "[组件名]": "[组件标识]",
  
  // 示例 2：多组件/多通道
  "[组件类型]": "[组件 1],[组件 2]",
  
  // 示例 3：多实例/多工作区
  "[实例名]": [
    {"id": "default", "name": "Default", "workspace": "~/[项目]"},
    {"id": "custom", "name": "Custom", "workspace": "~/[项目]-custom"}
  ]
}
```

> **通用化提示**：
> - Web 应用：端口、数据库连接、认证方式
> - CLI 工具：颜色、格式、输出目录
> - 消息系统：Broker URL、Topic 名称、消费组
> - Agent 框架：Model、Tools、Channels

### Step 4：生成 examples.md

结构：

```markdown
# 示例与模板

## Hello World
[最小可运行示例]

## [扩展类型 1]
[模板代码 + 注册说明]

## [扩展类型 2]
[模板代码 + 注册说明]

## [扩展类型 3]
[模板代码 + 注册说明]

## 配置示例
[常用配置场景]

## 常见问题
[FAQ 式示例]
```

---

## 输出物

- `project-book/08-examples.md`
- `examples/` 目录（可选，存放完整示例文件）

---

## 质量检查

```
✓ Hello World 示例是否真的"最小可运行"？
✓ 模板代码是否可以直接复制使用？
✓ 注册步骤是否清晰（改哪些文件）？
✓ 配置示例是否覆盖常见场景？
✓ 模板是否通用化（不绑定特定项目类型）？
✓ 是否标注了需要替换的占位符？
```

---

## 参考

- 你的"项目学习 Skill"中的"扩展开发指南"
- Supabase Agent Skills 工程组织方式