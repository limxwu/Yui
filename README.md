# 🚀 Yui

**Yui** 是一个基于 **Python** 构建的高性能、可扩展的实验性 AI 集成项目，旨在探索 LLM 在动态语言环境下的工程化实践。

> "Information is not just data, it's the core of existence."

---

## 📖 项目简介

**Yui** 的命名灵感来源于《刀剑神域》（Sword Art Online）中的系统级 AI 程序 —— MHCP（Mental Health Counseling Program）。

本项目弃用了传统的重量级框架，转而利用 Python 灵活的异步生态（如 **LangChain** 或 **FastAPI**），构建一套标准化的 AI 代理（Agent）逻辑。通过对大语言模型的深度封装，实现复杂的任务编排、长短期记忆管理以及多工具调用（Function Calling），打造一个真正的智能后端内核。

## 🛠️ 技术栈

* **核心语言:** Python 3.14
* **AI 框架:** [LangChain](https://github.com/langchain-ai/langchain) / [Semantic Kernel](https://github.com/microsoft/semantic-kernel)
* **Web 服务:** FastAPI / Flask
* **异步处理:** asyncio
* **支持模型:** OpenAI / Anthropic / Local LLMs (via Ollama)
* **环境管理:** Poetry / venv

## ✨ 核心特性

- **异步推理架构:** 基于 `asyncio` 实现非阻塞的 AI 响应，支持高并发对话处理。
- **动态记忆中枢:** 实现基于 Redis 或向量数据库的长短期记忆（Buffer/Summary Memory），模拟系统的“持久化经验”。
- **精细化 Tool 绑定:** 利用 Python 的装饰器特性，将本地函数快速转化为 AI 可调用的 Tools。
- **结构化数据解析:** 利用 Pydantic 进行严格的 Schema 验证，确保 AI 输出与业务逻辑的完美对齐。
- **可观测性集成:** 内置对 LangSmith 或自定义日志系统的支持，实时追踪 Chain 的执行链路。

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone [https://github.com/your-username/project-yui.git](https://github.com/your-username/project-yui.git)
cd project-yui
```

### 2. 环境配置
创建 `.env` 文件并配置您的环境变量：

```env
OPENAI_API_KEY=your_api_key_here
# 若使用本地模型
# OLLAMA_BASE_URL=http://localhost:11434
# LOG_LEVEL=DEBUG
```

### 3. 安装依赖并运行
```bash
pip install -r requirements.txt
python main.py
```

## 🏗️ 项目结构

- `yui/core/`: 存放 LLM 初始化、提示词模板及 Chain 的定义。
- `yui/agents/`: 存放具体的 Agent 决策逻辑与工具集。
- `yui/memory/`: 基于内存或数据库的会话状态管理。
- `yui/api/`: 基于 FastAPI 构建的外部通信接口。

## 📅 开发计划 (Roadmap)

- [ ] **RAG 增强:** 接入 ChromaDB 或 Pinecone，实现企业级知识检索。
- [ ] **多模态扩展:** 增加对视觉模型（GPT-4o/Claude 3.5）的适配。
- [ ] **分布式部署:** 支持使用 Docker 容器化部署及负载均衡。
- [ ] **UI 交互层:** 提供基于 Streamlit 的快速测试交互界面。

---

## 🤝 参与贡献

这是一个致力于探索 Python AI 工程化最佳实践的项目。欢迎通过提交 **Pull Request** 或 **Issue** 来帮助 Yui 进化。

---

**Project Yui** —— 赋予代码以智慧，构建响应式智能内核。