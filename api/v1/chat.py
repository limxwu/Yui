"""
聊天相关路由 - FastAPI 版本（接口层）
职责：处理 HTTP 请求/响应、参数验证、异常处理
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

# 导入服务层（业务逻辑）
from services.chat_service import chat_service

# 创建路由器（接口层）
chat_router = APIRouter()


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


@chat_router.post('', response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    """
    处理聊天请求（接口层）
    职责：参数验证、调用服务层、异常处理、返回响应
    """
    try:
        # 调用服务层处理业务逻辑
        ai_response = await chat_service.send_message(
            message=chat_request.message,
            session_id=chat_request.session_id or 'default_session'
        )
        
        return ChatResponse(
            success=True,
            response=ai_response
        )
    
    except ValueError as e:
        # 业务验证异常 -> 400
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        # FastAPI HTTP 异常直接抛出
        raise
    except Exception as e:
        # 其他异常 -> 500
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.post('/clear')
async def clear_chat(clear_request: ClearRequest):
    """
    清除聊天历史（接口层）
    职责：调用服务层、返回响应
    """
    session_id = clear_request.session_id or 'default_session'
    chat_service.clear_session(session_id)
    return JSONResponse(content={'success': True})
