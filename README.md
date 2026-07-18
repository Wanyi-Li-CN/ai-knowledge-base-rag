# 🧠 AI多Agent私有知识库智能问答系统

> 毕业设计：基于LangChain多智能体协同 + PostgreSQL/pgvector 向量检索的私有知识库智能问答平台

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-orange.svg)](https://python.langchain.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16+-black.svg)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 项目简介

本项目针对传统轻量化单RAG文档问答系统功能单一、检索性能弱、无任务协同能力等短板，设计并实现一套**基于LangChain多智能体协同 + PostgreSQL/pgvector向量检索**的私有知识库智能问答平台。

系统支持多格式文档解析、向量知识库构建、多轮上下文问答、批量文档智能加工、任务异步调度、检索性能可视化监控等完整能力。

---
## 📸 运行截图

### 前端界面

| 功能 | 截图 |
|------|------|
| 对话问答 | ![对话界面](screenshots/frontend-chat.png) |
| 文档上传 | ![上传功能](screenshots/frontend-upload.png) |
| 文档问答 | ![文档对话](screenshots/frontend-resume-chat.png) |

### 后端 API

| 功能 | 截图 |
|------|------|
| Swagger 文档 | ![Swagger](screenshots/swagger-api.png) |
| 问答 API 返回 | ![问答响应](screenshots/api-chat-response.png) |

---

## 📊 当前进度

| 模块 | 状态 | 说明 |
|------|------|------|
| 文档上传与解析（TXT） | ✅ 已完成 | 支持TXT文件上传和文本提取 |
| 文档上传与解析（PDF/DOCX） | ✅ 已完成 | 解析引擎扩展中 |
| 分层自适应文本切片 | ✅ 已完成 | LangChain RecursiveCharacterTextSplitter |
| pgvector向量存储 | ✅ 已完成 | PostgreSQL + pgvector 向量检索 |
| RAG智能问答 | ✅ 已完成 | DeepSeek大模型 + 阿里云百炼Embedding |
| 前端交互界面 | ✅ 已完成 | Next.js + TypeScript + Ant Design |
| 多Agent协同调度 | 🔄 开发中 | 5类Agent拆分与调度中心 |
| 三级幻觉抑制 | 🔄 开发中 | 检索过滤 + Prompt约束 + 答案校验 |
| 系统监控与可视化 | 📋 计划中 | ECharts性能监控面板 |
| 文档智能加工 | 📋 计划中 | 摘要生成、观点提取 |

---

## 🏗️ 系统架构

### 六层分层架构

| 层级 | 技术 | 核心职责 |
|:---:|:---|:---|
| **1** | Next.js + Ant Design | 用户界面、对话问答、文档上传、监控面板 |
| **2** | FastAPI | 路由分发、参数校验、跨域处理、异步任务 |
| **3** | LangChain | 调度中心、任务分发、Agent执行监控、异常重试 |
| **4** | 自研解析引擎 | PDF/DOCX/TXT解析、文本清洗、自适应切片 |
| **5** | LangChain + pgvector | Embedding、向量检索、结果重排、Prompt组装、LLM推理 |
| **6** | PostgreSQL + pgvector | 业务数据存储、向量存储、HNSW索引优化 |

### 核心运行流程

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户上传文档                              │
└─────────────────────────┬───────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│             ① 文档解析Agent → 文本提取 → 切片                    │
└─────────────────────────┬───────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│             ② 检索Agent → 向量化 → 存入pgvector                  │
└─────────────────────────────────────────────────────────────────┘
                          ⬇️
┌─────────────────────────────────────────────────────────────────┐
│                        用户提问                                  │
└─────────────────────────┬───────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│             ③ 调度Agent → 分发任务                              │
└─────────────────────────┬───────────────────────────────────────┘
                          ▼
          ┌───────────────┴───────────────┐
          ▼                               ▼
┌──────────────────┐          ┌──────────────────┐
│ ④ 检索Agent      │          │ ⑤ 对话Agent      │
│ 向量检索+重排    │          │ 上下文管理       │
└────────┬─────────┘          └────────┬─────────┘
         └───────────────┬───────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│             ⑥ 拼接防幻觉Prompt → DeepSeek推理                   │
└─────────────────────────┬───────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│             ⑦ 问答Agent → 幻觉校验 → 返回答案                   │
└─────────────────────────────────────────────────────────────────┘
```

### 多Agent协同（核心创新）

系统拆分 **5 类独立智能体**，由调度中心统一管控：

| Agent | 职责 |
|:---|:---|
| **文档解析Agent** | 文档解析、文本清洗、分层切片、文档分类 |
| **检索Agent** | 向量编码、多路召回、片段重排、相似度过滤 |
| **对话问答Agent** | 多轮上下文维护、Prompt组装、幻觉抑制 |
| **文档加工Agent** | 自动摘要、核心观点提取、段落精简 |
| **任务调度Agent** | 任务分发、异步队列、状态监控、失败重试 |

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本 |
|------|------|
| Python | 3.12+ |
| Node.js | 18+ |
| PostgreSQL | 16+ (with pgvector) |
| Docker | 可选 |

### 1. 克隆项目

```bash
git clone https://github.com/Wanyi-Li-CN/ai-knowledge-base-rag.git
cd ai-knowledge-base-rag
```

### 2. 后端配置

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 3. 环境变量配置

复制 `.env.example` 为 `.env`：

```env
# 数据库
DATABASE_URL=postgresql://postgres:password@localhost:5432/knowledge_base

# 大模型（DeepSeek）
OPENAI_API_KEY=your_deepseek_api_key
OPENAI_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat

# Embedding（阿里云百炼）
EMBEDDING_PROVIDER=aliyun
EMBEDDING_API_KEY=your_bailian_api_key
EMBEDDING_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
EMBEDDING_MODEL=text-embedding-v3
```

### 4. 启动后端

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

访问 `http://localhost:8001/docs` 查看 API 文档。

### 5. 前端配置

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:3000` 使用系统。

### 6. Docker 一键部署（可选）

```bash
docker-compose up -d
```

---

## 🛠️ 技术栈

| 分类 | 技术 | 说明 |
|------|------|------|
| **后端框架** | FastAPI | 异步高性能 Web 框架 |
| **AI 框架** | LangChain | Agent 编排、检索链、Prompt 管理 |
| **大模型** | DeepSeek | 兼容 OpenAI 格式，中文能力强 |
| **Embedding** | 阿里云百炼 | text-embedding-v3 |
| **向量数据库** | PostgreSQL + pgvector | 关系型 + 向量混合存储 |
| **前端框架** | Next.js + TypeScript | React 全栈框架 |
| **UI 组件库** | Ant Design | 工业级后台组件库 |
| **可视化** | ECharts | 监控图表展示 |
| **部署** | Docker + docker-compose | 容器化一键部署 |

---

## ✨ 核心功能

### 已完成

- [x] 文档上传（TXT 格式）
- [x] 文档解析与文本提取
- [x] 分层自适应文本切片
- [x] pgvector 向量存储与检索
- [x] RAG 智能问答（DeepSeek）
- [x] 前端对话界面
- [x] 多文件批量上传

### 开发中

- [ ] 多 Agent 协同调度（5 类 Agent）
- [ ] 三级幻觉抑制机制
- [ ] PDF/DOCX 文档解析
- [ ] 多路召回 + 结果重排

### 计划中

- [ ] 系统监控与可视化面板（ECharts）
- [ ] 对话历史存储
- [ ] 文档智能加工（摘要/观点提取）
- [ ] 用户权限与知识库分组
- [ ] Redis 缓存优化

---

## 📁 项目结构

```
ai-knowledge-base-rag/
├── backend/
│   ├── app/
│   │   ├── api/              # API 路由层
│   │   │   └── v1/           # API v1 版本
│   │   ├── core/             # 核心配置
│   │   ├── models/           # 数据模型
│   │   ├── services/         # 业务逻辑层
│   │   │   ├── parser/       # 文档解析
│   │   │   ├── rag/          # RAG 核心
│   │   │   └── agents/       # Agent 实现
│   │   └── main.py           # FastAPI 入口
│   ├── uploads/              # 上传文件存储
│   ├── .env                  # 环境变量
│   └── requirements.txt      # Python 依赖
├── frontend/
│   ├── app/                  # Next.js 应用
│   ├── lib/                  # 工具库
│   ├── package.json          # Node 依赖
│   └── tsconfig.json         # TypeScript 配置
├── docker-compose.yml        # Docker 编排
└── README.md
```

---

## 📝 关键技术创新点

1. **基于 LangChain 的多智能体协同调度架构**
2. **PostgreSQL + pgvector 混合存储向量方案**
3. **分层自适应切片 + 多路召回融合检索策略**
4. **三级联动多级幻觉抑制机制**
5. **动态对话窗口缓存优化**
6. **多 Agent 任务可视化监控体系**

---

## 📄 License

MIT License

---

## 👨‍💻 作者

**Wanyi-Li-CN**

- GitHub: [Wanyi-Li-CN](https://github.com/Wanyi-Li-CN)
- 邮箱:3066129214@qq.com

---

## ⭐ Star 支持

如果这个项目对你有帮助，欢迎 Star 支持！
```
