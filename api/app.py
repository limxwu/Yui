"""
FastAPI 后端应用主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 创建 FastAPI 应用
app = FastAPI(
    title="Yui AI Chat API",
    description="Yui AI 对话助手后端 API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入路由
from api.routes.chat import router as chat_router

# 注册路由
app.include_router(chat_router, prefix="/chat", tags=["chat"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Yui AI Chat API is running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
