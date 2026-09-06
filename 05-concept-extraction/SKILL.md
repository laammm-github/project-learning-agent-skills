---
name: 05-concept-extraction
description: 从代码中提取核心设计概念、抽象和契约，而非解释代码细节
---

# 05-Concept Extraction — 概念提取

> 目标：从代码中提取设计概念，而非解释代码细节

---

## 职责

将源码转化为人类可理解的设计概念：
- 核心抽象提炼
- 设计契约说明
- 概念关系图
- 类比理解（用现实世界类比）

---

## 执行流程

### Step 1：识别核心抽象

找出项目中最重要的抽象，使用**真实代码**而非伪代码，替换 `[语言]` 为项目实际语言：

```python
# 示例（Python 项目）：常见抽象基类模式
# 文件位置：请替换为实际路径，如 base.py:12、interface.rs:45

class BaseClass(object):
    # 类属性（必须由子类覆盖）
    class_type = ""           # 类型标识（如 "web", "file", "api"）
    supported_features = []   # 支持的功能列表
    
    def startup(self):        # 初始化（必须实现）
        raise NotImplementedError
    
    def stop(self):           # 清理（可选）
        pass
    
    def process(self, input_data):  # 核心处理（必须实现）
        raise NotImplementedError
    
    def output(self, result):   # 输出结果（必须实现）
        raise NotImplementedError
```

**提取的概念**：

```
BaseClass = "[抽象名称] 的契约定义"
作用：定义所有实现类必须遵循的接口
类比：[项目相关的现实类比]
位置：[文件路径:行号]
```

> **通用化提示**：根据项目类型调整类名和方法名：
> - Web 框架：Controller（处理请求）
> - 消息系统：Broker（路由消息）
> - CLI 工具：Command（执行命令）
> - Agent 框架：Tool（调用外部能力）

### Step 2：提炼设计契约

每个核心类/接口，说明：
- **契约**：必须实现什么
- **约定**：数据格式规范
- **例外**：特殊处理场景

```python
# 示例（Python 项目）：通用扩展点模式
# 文件位置：请替换为实际路径

class BaseExtension:
    # 必须定义的属性
    name: str = "base_extension"        # 扩展名称
    version: str = "1.0"                # 版本号
    description: str = "Base extension" # 描述
    
    # 核心方法
    def execute(self, params: dict) -> dict:
        raise NotImplementedError
```

**契约说明**：

```
BaseExtension 契约：
- 必须实现：execute(params) → dict
- 必须定义：name, version, description
- 约束：name 唯一、description 清晰（用于注册/发现）
```

### Step 3：构建概念关系

根据项目类型调整关系图：

```
# 通用关系模板（根据项目类型调整）：

[核心入口] ──→ [处理层] ──→ [输出层]
    │             │             │
    │             │             └──→ [辅助组件]
    │             │
    │             └──→ [可替换实现]
    │
    └──→ [多种实现方式]

# 常见项目类型的关系图示例：

# Web 应用：
Router ──→ Controller ──→ Service ──→ Database
  │           │            │
  │           └──→ Middleware ──→ 日志/认证/缓存
  └──→ API 端点定义

# 消息系统：
Producer ──→ Broker ──→ Consumer
  │            │            │
  └──→ 消息发送   └──→ 路由/过滤  └──→ 消息处理

# CLI 工具：
CLI Parser ──→ Command Registry ──→ Command Handler
      │                   │                    │
      └──→ 参数解析        └──→ 命令注册          └──→ 执行逻辑
```

### Step 4：用类比帮助理解

将项目抽象映射到现实类比：

```python
# 示例（Agent 框架）：
def run(self, query, context):
    # 1. 解析请求
    resolved = self.resolve_agent(context)
    # 2. 构建上下文
    ctx = self.build_context(query, context)
    # 3. 执行主逻辑
    result = self.execute_loop(resolved, ctx)
    return result
```

**类比：餐厅点餐系统**

```
1. 顾客点餐（系统接收查询）
2. 厨师看菜谱（Agent 加载配置）
3. 需要切菜？→ 调用切菜工具（Tool Call）
4. 菜切好了？→ 继续做下一道（Loop）
5. 菜做好了？→ 上菜（Return）
6. 做了 30 道菜还没好？→ 放弃重试（max_steps）
```

> **通用化提示**：
> - Web 应用：餐厅点餐（请求→处理→响应）
> - 消息队列：邮局分拣（消息路由）
> - 编译器：翻译官（代码→中间表示→机器码）
> - 数据库：档案管理员（查询→检索→返回）

### Step 5：生成 core-concepts.md

结构：

```markdown
# 核心概念

## 关键抽象

### [抽象名称]
- 是什么：[一句话描述]
- 类比：[现实类比]
- 位置：[文件路径:行号]
- 契约：
  - 必须实现：[方法名列表]
  - 数据格式：[输入/输出类型]
- 为什么这样设计：[设计意图]

### [第二个抽象]
...

## 设计契约

### [契约名称]
- 输入：[参数说明]
- 输出：[返回值]
- 约束：[注意事项]
- 扩展点：[如何覆盖/扩展]
- 位置：[文件路径]

## 概念关系图
[Mermaid 关系图，根据实际项目类型生成]

## 类比理解
| 概念 | 代码位置 | 现实类比 |
|------|---------|---------|
| [概念 1] | [路径] | [类比] |
| [概念 2] | [路径] | [类比] |
```

---

## 输出物

- `project-book/05-core-concepts.md`

---

## 质量检查

```
✓ 概念是否用"是什么 + 类比"解释？
✓ 契约是否标注了"必须做"和"可选做"？
✓ 概念关系图是否清晰？
✓ 类比是否帮助理解而非混淆？
✓ 是否标注了代码位置（方便深挖）？
✓ 是否适配了项目类型（Web/CLI/Agent/...）？
```

---

## 参考

- 认知科学中的"类比学习"理论
- 你的"项目学习 Skill"中的"概念提取"缺失环节