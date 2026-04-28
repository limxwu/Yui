"""
聊天相关路由 - FastAPI 版本
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import asyncio

# 导入业务逻辑
from core.llm import get_model, aget_model_response
from memory.session_manager import session_manager

# 创建路由器
router = APIRouter()

# 初始化 DeepSeek 模型（懒加载，首次调用时初始化）
_model = None


def get_model_instance():
    """获取模型实例（懒加载）"""
    global _model
    if _model is None:
        _model = get_model()
    return _model


# 请求模型
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default_session"


class ClearRequest(BaseModel):
    session_id: Optional[str] = "default_session"


class ChatResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None


@router.post("/api/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    """处理聊天请求（异步版本）"""
    try:
        user_message = chat_request.message.strip()
        
        if not user_message:
            raise HTTPException(status_code=400, detail="消息不能为空")
        
        # 使用会话 ID
        session_id = chat_request.session_id or 'default_session'
        
        # 获取或创建会话（使用 memory 层的会话管理器）
        conversation = session_manager.get_or_create_session(session_id)
        
        # 添加用户消息
        conversation.add_user_message(user_message)
        
        # 转换为 LangChain 格式
        messages = conversation.to_langchain_messages()
        
        # 调用 LLM（异步）
        model_instance = get_model_instance()
        
        # 直接异步调用（FastAPI 原生支持异步）
        response = await aget_model_response(model_instance, messages)
        
        ai_response = response.content if hasattr(response, 'content') else str(response)
        
        # 添加 AI 回复到会话
        conversation.add_ai_message(ai_response)
        
        return ChatResponse(
            success=True,
            response=ai_response
        )
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/clear")
async def clear_chat(clear_request: ClearRequest):
    """清除聊天历史"""
    session_id = clear_request.session_id or 'default_session'
    session_manager.clear_session(session_id)
    return JSONResponse(content={'success': True})
