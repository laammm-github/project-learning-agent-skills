---
name: 02-config-and-installation
description: 分析配置系统、环境变量映射、安装步骤，生成配置与安装指南
---

# 02-Config & Installation — 安装与配置

> 目标：分析配置系统，生成安装步骤和配置指南

---

## 职责

分析项目的配置系统，输出：
- 配置加载流程
- 环境变量映射
- 安装步骤
- 配置示例

---

## 执行流程

### Step 1：识别配置系统

```bash
# 优先使用结构化清单
python scripts/inventory_repo.py <目标仓库> --config

# 或手动搜索（rg 跨平台）
# 查找配置文件
rg --files | rg "config\.json|config\.py|config-template\.json|\.env\.example"

# 查找环境变量定义
rg "os\.environ|os\.getenv|environ" --type py
```

### Step 2：分析配置加载流程

典型配置加载流程（根据项目调整）：

```python
# 示例：通用配置加载模式
# 文件位置：config.py 或 equivalent

def load_config():
    # 加载流程：
    # 1. 读取默认配置（模板文件/硬编码默认值）
    # 2. 读取用户配置（JSON/YAML/ENV 文件）
    # 3. 合并配置（用户配置覆盖默认值）
    # 4. 注入环境变量（API Key 等敏感信息）
    # 5. 返回统一配置对象
    config = merge_config(defaults, user_config, env_vars)
    return config
```

输出：`installation.md` 的"配置系统"章节

### Step 3：提取环境变量映射

典型映射模式（根据项目调整）：

```python
# 示例：环境变量映射模式
# 配置文件中的 key → 环境变量名

_CONFIG_TO_ENV = {
    "api_key": "API_KEY",           # 示例：API 密钥
    "database_url": "DATABASE_URL", # 示例：数据库连接
    "secret": "SECRET",             # 示例：应用密钥
}
```

输出：`installation.md` 的"环境变量"章节

### Step 4：生成安装步骤

结构（根据项目语言调整命令）：

```markdown
## 安装步骤

### 1. 环境要求
- [语言版本]（如 Python 3.7+、Node.js 14+ 等）

### 2. 安装依赖
```bash
# Python
pip install -r requirements.txt
# Node
npm install
# Go
go mod download
```

### 3. 配置环境
```bash
# 复制配置模板
cp config-template.json config.json  # 或 .env.example → .env

# 设置环境变量
export [ENV_VAR_NAME]="your_value"
```

### 4. 启动项目
```bash
[项目启动命令]
```
```

### Step 5：生成配置示例

```json
{
  // 示例 1：切换组件/后端/模型
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

### Step 6：生成 installation.md

结构：

```markdown
# 安装与配置指南

## 环境要求
- 语言版本
- 依赖包

## 安装步骤
1. [步骤 1]
2. [步骤 2]
...

## 配置系统

### 配置格式
- [JSON/YAML/INI]

### 配置加载流程
[流程图或步骤说明]

### 环境变量
| 配置项 | 环境变量 | 说明 |
|--------|---------|------|
| api_key | API_KEY | [说明] |
| database_url | DATABASE_URL | [说明] |

### 配置示例
[常用配置场景]

## 常见问题
- Q: 如何切换 [组件/模型/后端]？
- A: [步骤说明]
```

---

## 输出物

- `project-book/02-installation.md`

---

## 质量检查

```
✓ 安装步骤是否可执行（按步骤能跑起来）？
✓ 环境变量映射是否完整？
✓ 配置示例是否覆盖常见场景？
✓ 配置加载流程是否清晰？
```

---

## 参考

- 你的"项目学习 Skill"中的配置系统专项学习
- Supabase Agent Skills 工程组织方式