"""
路由模块包 - v1 版本集中管理
"""
from fastapi import APIRouter
from api.v1.chat import chat_router
from api.v1.memory import memory_router


def get_v1_router() -> APIRouter:
    """
    获取 v1 版本的总路由器，集中管理所有 v1 路由
    
    Returns:
        APIRouter: v1 版本的总路由器实例
    """
    # 创建 v1 总路由器（不带 prefix，prefix 由 app.py 指定）
    v1_router = APIRouter()
    
    # 注册所有 v1 子路由模块到总路由器中，并设置各自的前缀和标签
    v1_router.include_router(chat_router, prefix="/chat",tags=["Chat"])
    v1_router.include_router(memory_router, prefix="/memory", tags=["Memory"])
    
    return v1_router
