# 🚀 Yui - AI 智能对话系统

**Yui** 是一个基于 **Python** 构建的高性能、可扩展的 AI 集成项目，采用标准化的分层架构设计，旨在探索 LLM 在工程化实践中的最佳方案。

> "Information is not just data, it's the core of existence."

---

## 📖 项目简介

**Yui** 的命名灵感来源于《刀剑神域》（Sword Art Online）中的系统级 AI 程序 —— MHCP（Mental Health Counseling Program）。

本项目采用**清晰的分层架构**（接口层、业务层、基础设施层），利用 Python 灵活的异步生态（**FastAPI** + **LangChain**），构建一套标准化的 AI 代理（Agent）逻辑。通过对大语言模型的深度封装，实现复杂的任务编排、长短期记忆管理以及多工具调用（Function Calling），打造一个真正的智能后端内核。

### 🏗️ 架构特点

- ✅ **分层清晰**: 接口层、业务层、基础设施层职责明确
- ✅ **配置统一**: 所有配置集中管理，支持环境变量
- ✅ **日志完善**: 统一的日志系统，支持控制台和文件输出
- ✅ **异常规范**: 完善的异常体系，便于精确错误处理
- ✅ **易于扩展**: 模块化设计，新增功能只需在对应层添加

---

## 🛠️ 技术栈

### 核心框架
* **Python:** 3.14+
* **Web 框架:** [FastAPI](https://fastapi.tiangolo.com/) - 高性能异步 Web 框架
* **前端界面:** Vue 3 + Vite + TypeScript + Tailwind CSS
* **AI 框架:** [LangChain](https://github.com/langchain-ai/langchain) - LLM 应用开发框架

### AI 模型支持
* **DeepSeek:** 通过 DeepSeek API 调用
* **Ollama:** 支持本地模型（Llama 3.2 等）

### 数据存储
* **ChromaDB:** 向量数据库（用于 RAG）
* **内存存储:** 会话状态管理

### 开发工具
* **包管理:** [uv](https://github.com/astral-sh/uv) - 极速 Python 包管理器
* **环境管理:** Python venv
* **异步处理:** asyncio

### 基础设施
* **配置管理:** 基于环境变量的统一配置
* **日志系统:** Python logging 标准化配置
* **异常处理:** 自定义异常体系

---

## ✨ 核心特性

### 🎯 架构设计
- **分层架构**: 接口层、业务层、基础设施层清晰分离
- **单向依赖**: 上层调用下层，避免循环依赖
- **职责明确**: 每层只关注自己的职责，易于维护和测试

### 🤖 AI 能力
- **异步推理架构**: 基于 `asyncio` 实现非阻塞的 AI 响应，支持高并发对话处理
- **动态记忆中枢**: 实现基于内存的长短期记忆管理，模拟系统的"持久化经验"
- **精细化 Tool 绑定**: 利用 Python 的装饰器特性，将本地函数快速转化为 AI 可调用的 Tools
- **结构化数据解析**: 利用 Pydantic 进行严格的 Schema 验证，确保 AI 输出与业务逻辑的完美对齐

### 🔧 工程化实践
- **统一配置管理**: 所有配置集中在 `core/config.py`，支持环境变量覆盖
- **标准化日志系统**: 统一的日志格式和级别控制，支持控制台和文件输出
- **完善的异常体系**: 分层异常类设计，包含 HTTP 状态码，便于精确处理
- **可观测性集成**: 完整的日志记录，实时追踪请求处理链路

---

## 🚀 快速开始

### 前置要求

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) 包管理器（推荐）或 pip

### 1. 克隆仓库

```bash
git clone https://github.com/limxwu/yui.git
cd Yui
```

### 2. 环境配置

复制环境变量模板并编辑：

```bash
# Windows PowerShell
cp .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件，填入你的配置：

```env
# DeepSeek API Key（必填）
DEEPSEEK_API_KEY=sk-your_api_key_here

# API 服务器配置
API_HOST=0.0.0.0
API_PORT=8000

# 日志配置
LOG_LEVEL=INFO
# LOG_FILE=./logs/yui.log  # 可选：输出到文件
```

### 3. 安装依赖

```bash
# 使用 uv（推荐，速度更快）
uv sync

# 或使用 pip
pip install -r requirements.txt
```

### 4. 启动服务

#### 方式一：启动后端服务

```bash
python main.py
```

或者：

```bash
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

这将启动 FastAPI 后端: http://localhost:8000

#### 方式二：启动前端服务（新终端）

```bash
cd web
npm run dev
```

这将启动 Vue 3 前端: http://localhost:5173

### 5. 访问应用

- 📖 **API 文档**: http://localhost:8000/docs （Swagger UI）
- 🎨 **前端界面**: http://localhost:5173 （Vue 3 SPA）
- 💚 **健康检查**: http://localhost:8000/health

### 6. 前端环境配置

如果需要修改前端调用后端 API 的地址，可以在 `web/` 目录下创建 `.env` 文件：

```bash
cd web
cp .env.example .env
```

然后编辑 `.env` 文件，修改 `VITE_API_BASE_URL` 变量：

```env
VITE_API_BASE_URL=http://your-api-server:8000/api/v1
```

重启前端服务使配置生效。

---

## 🏗️ 项目结构

```
Yui/
├── api/                    # 【接口层】API 路由和请求处理
│   ├── v1/                 # API v1 版本
│   │   ├── __init__.py     # v1 路由集中管理
│   │   └── chat.py         # 聊天相关路由
│   └── app.py              # FastAPI 应用入口
│
├── services/               # 【业务逻辑层】核心业务逻辑
│   ├── __init__.py
│   └── chat_service.py     # 聊天服务
│
├── models/                 # 【数据模型层】Pydantic Schemas
│   ├── __init__.py
│   └── schemas.py          # 请求/响应数据模型
│
├── core/                   # 【基础设施层】底层工具和配置
│   ├── __init__.py
│   ├── config.py           # 统一配置管理
│   ├── llm.py              # LLM 客户端封装
│   ├── constants.py        # 常量定义
│   └── docling_transformer.py  # 文档转换工具
│
├── memory/                 # 【数据访问层】会话和数据持久化
│   ├── __init__.py
│   └── session_manager.py  # 会话管理器
│
├── utils/                  # 【工具层】通用工具函数
│   ├── __init__.py
│   ├── logger.py           # 日志配置
│   └── exceptions.py       # 自定义异常类
│
├── web/                    # 【前端层】Vue 3 SPA
│   ├── src/                # 源代码
│   │   ├── api/            # API 调用封装
│   │   ├── components/     # Vue 组件
│   │   ├── composables/    # Composition API
│   │   ├── types/          # TypeScript 类型定义
│   │   └── App.vue         # 根组件
│   ├── .env                # 环境变量（不提交）
│   ├── .env.example        # 环境变量模板
│   ├── package.json        # Node.js 依赖
│   └── vite.config.ts      # Vite 配置
│
├── tests/                  # 【测试层】单元测试和集成测试
├── docs/                   # 【文档层】项目文档
│   ├── ARCHITECTURE.md     # 架构说明
│   └── REFACTORING_SUMMARY.md  # 重构总结
└── scripts/                # 【脚本层】运维和部署脚本
```

### 分层说明

| 层级 | 目录 | 职责 |
|------|------|------|
| **接口层** | `api/` | 处理 HTTP 请求/响应、参数验证、异常转换 |
| **业务层** | `services/` | 封装核心业务逻辑，不依赖具体协议 |
| **数据模型层** | `models/` | Pydantic 数据模型，类型安全和验证 |
| **基础设施层** | `core/` | LLM 客户端、配置管理、工具类 |
| **数据访问层** | `memory/` | 会话管理、数据持久化 |
| **工具层** | `utils/` | 日志、异常等通用工具 |
| **前端层** | `web/` | Vue 3 SPA 用户界面 |

---

## 📝 API 使用示例

### 发送聊天请求

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好，请介绍一下自己",
    "session_id": "user_123"
  }'
```

### 清除会话历史

```bash
curl -X POST "http://localhost:8000/api/v1/chat/clear" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user_123"
  }'
```

### Python 调用示例

```python
import requests

# 发送消息
response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={
        "message": "你好",
        "session_id": "test_session"
    }
)

print(response.json())
# {'success': True, 'response': '你好！我是 Yui AI 助手...', 'error': None}
```

---

## 📚 开发指南

### 添加新接口

1. 在 `models/schemas.py` 中定义请求/响应模型
2. 在 `services/` 中创建或更新服务类
3. 在 `api/v1/` 中创建路由文件
4. 在 `api/v1/__init__.py` 中注册路由

### 异常处理原则

- **业务层**: 抛出自定义异常（`EmptyMessageError`, `LLMCallError` 等）
- **接口层**: 捕获自定义异常，转换为 `HTTPException`
- **日志**: 业务层记录业务日志，接口层记录请求日志

### 日志级别使用

- **DEBUG**: 详细的调试信息
- **INFO**: 一般信息（请求处理、业务操作）
- **WARNING**: 警告信息（空消息、超时等）
- **ERROR**: 错误信息（LLM 调用失败、数据库错误）
- **CRITICAL**: 严重错误（系统崩溃）

更多开发规范请参考 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 📅 开发计划 (Roadmap)

### 短期优化
- [ ] **单元测试**: 为服务层编写完整的测试用例
- [ ] **中间件**: 添加认证、限流、请求日志中间件
- [ ] **全局异常处理**: FastAPI 全局异常处理器
- [ ] **健康检查增强**: 更详细的 `/health` 端点

### 中期优化
- [ ] **RAG 增强**: 接入 ChromaDB，实现企业级知识检索
- [ ] **数据库集成**: 使用 SQLAlchemy 或 Tortoise ORM
- [ ] **缓存层**: Redis 缓存常用数据
- [ ] **消息队列**: Celery 处理异步任务

### 长期优化
- [ ] **多模态扩展**: 增加对视觉模型（GPT-4o/Claude 3.5）的适配
- [ ] **微服务拆分**: 将聊天、文档、用户拆分为独立服务
- [ ] **容器化部署**: Docker + Docker Compose
- [ ] **CI/CD 流程**: GitHub Actions 自动化测试和部署
- [ ] **监控告警**: Prometheus + Grafana

---

## 🤝 参与贡献

这是一个致力于探索 Python AI 工程化最佳实践的项目。欢迎通过提交 **Pull Request** 或 **Issue** 来帮助 Yui 进化。

### 贡献指南

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

### 开发环境设置

```bash
# 安装开发依赖
uv sync

# 运行测试（待实现）
pytest tests/

# 代码格式化（待实现）
black .
flake8
```

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - LLM 应用开发框架
- [FastAPI](https://fastapi.tiangolo.com/) - 高性能 Web 框架
- [DeepSeek](https://deepseek.com/) - 强大的语言模型
- [Vue 3](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Vite](https://vitejs.dev/) - 下一代前端构建工具
- [Tailwind CSS](https://tailwindcss.com/) - 实用优先的 CSS 框架

---

**Project Yui** —— 赋予代码以智慧，构建响应式智能内核。

<div align="center">

Made with ❤️ by Yui Team

[⭐ Star this repo](https://github.com/limxwu/yui) | [🐛 Report Bug](https://github.com/limxwu/yui/issues) | [💡 Request Feature](https://github.com/limxwu/yui/issues)

</div>
