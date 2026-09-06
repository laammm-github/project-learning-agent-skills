---
name: 04-code-flow-analysis
description: 跟踪核心数据流，分析数据从输入到输出的完整路径和变换，标注数据变换
---

# 04-Code Flow Analysis — 代码流分析

> 目标：跟踪一条请求从输入到输出的完整路径，标注数据变换

---

## 职责

深入核心链路，输出：
- 完整请求路径图（时序图）
- 每个环节的数据变换说明
- 关键参数传递说明
- 异常处理路径

---

## 执行流程

### Step 1：识别核心入口点

根据项目类型：
- 消息中间件：看 `channel/` 或 `broker/`
- Web 应用：看路由注册（router/、controller/）
- CLI 工具：看命令注册（cmd/、commands/）
- Agent 框架：看 `bridge/` 或 `agent/`

### Step 2：跟完整路径

从入口开始，逐层跟踪（根据项目类型调整）：

```python
# 通用请求处理流示例（根据项目类型替换）：
# Web 应用示例：
Controller.handle_request(req)       # 1. 接收请求
  → Controller.validate()            # 2. 参数验证
    → Service.process(data)          # 3. 业务逻辑
      → Repository.query()           # 4. 数据访问
        → Database.execute()         # 5. 执行查询

# 消息系统示例：
Broker.receive(message)              # 1. 接收消息
  → Broker.validate()                # 2. 消息验证
    → Router.route(message)          # 3. 路由分发
      → Consumer.process(msg)        # 4. 消费者处理
        → Processor.execute()        # 5. 处理逻辑
```

### Step 3：标注数据变换

每个环节标注：
- **输入**：接收什么数据
- **变换**：做了什么处理
- **输出**：返回什么数据

```
用户输入 "hello"
  │ 输入：字符串
  ▼
Controller.handle_request(msg)
  │ 变换：封装为 Context 对象
  ▼
Context(content="hello", type=TEXT)
  │ 输入：Context 对象
  ▼
Service.process(data)
  │ 变换：执行业务逻辑，添加元数据
  ▼
Result(content="Hello!", status=OK)
```

### Step 4：识别异常路径

检查：
- 失败回退（try-except-fallback）
- 超时处理
- 错误响应格式

### Step 5：生成 core-flow.md

结构：

```markdown
# 核心链路：[核心流程名称]

## 路径总览
[Mermaid 时序图]

## 详细步骤

### 步骤 1：[模块 A]
- 文件：[路径]
- 函数：[函数名]
- 输入：[参数说明]
- 变换：[做了什么处理]
- 输出：[返回值]
- 异常：[可能的错误]

### 步骤 2：[模块 B]
...

## 数据流图
```
输入 → [A] → [B] → [C] → 输出
       ↑      ↓
      日志   缓存
```

## 关键参数传递
| 参数 | 在哪设置 | 在哪使用 | 说明 |
|------|---------|---------|------|
| session_id | [入口] | [处理] | [说明] |
| channel_type | [Context] | [Router] | [说明] |

## 异常处理
1. [异常场景] → [处理方式]
2. ...
```

---

## 输出物

- `project-book/04-core-flow.md`

---

## 质量检查

```
✓ 是否标注了每个环节的数据变换？
✓ 时序图是否清晰（箭头方向正确）？
✓ 关键参数是否有传递说明？
✓ 异常路径是否覆盖？
```

---

## 参考

- 你的"项目学习 Skill"中的核心链路分析
- 消息流追踪最佳实践