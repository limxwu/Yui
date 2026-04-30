"""
聊天相关路由 - FastAPI 版本（接口层）
职责：处理 HTTP 请求/响应、参数验证、异常处理
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

# 导入服务层（业务逻辑）
from services.chat_service import chat_service

# 导入数据模型
from models.schemas import ChatRequest, ClearRequest, ChatResponse

# 导入自定义异常
from utils.exceptions import EmptyMessageError, LLMCallError
from utils.logger import logger

import json

# 创建路由器（接口层）
chat_router = APIRouter()

def list_sessions():
    """
    列出所有会话（接口层）
    职责：调用服务层、返回响应
    """
    return chat_service.list_sessions()

def chat_history(session_id: str):
    """
    列出会话历史（接口层）
    职责：调用服务层、返回响应
    """
    return chat_service.list_chat_history(session_id)


@chat_router.post('', response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    """
    处理聊天请求（接口层）
    职责：参数验证、调用服务层、异常处理、返回响应
    """
    try:
        logger.debug(f"收到聊天请求，session_id={chat_request.session_id}, use_rag={chat_request.use_rag}")

        # 调用服务层处理业务逻辑
        ai_response = await chat_service.send_message(
            message=chat_request.message,
            session_id=chat_request.session_id or 'default_session',
            use_rag=chat_request.use_rag
        )

        return ChatResponse(
            success=True,
            response=ai_response
        )

    except EmptyMessageError as e:
        # 业务验证异常 -> 400
        logger.warning(f"空消息错误: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except LLMCallError as e:
        # LLM 调用失败 -> 500
        logger.error(f"LLM 调用错误: {e.message}")
        raise HTTPException(status_code=500, detail=e.message)
    except HTTPException:
        # FastAPI HTTP 异常直接抛出
        raise
    except Exception as e:
        # 其他未预期异常 -> 500
        logger.error(f"未预期的错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


@chat_router.post('/stream')
async def chat_stream(chat_request: ChatRequest):
    """
    处理流式聊天请求（接口层）
    职责：参数验证、调用服务层、异常处理、返回SSE流式响应
    """
    try:
        logger.debug(f"收到流式聊天请求，session_id={chat_request.session_id}, use_rag={chat_request.use_rag}")

        # 调用服务层处理业务逻辑并返回生成器
        async def generate():
            async for chunk in chat_service.send_message_stream(
                    message=chat_request.message,
                    session_id=chat_request.session_id or 'default_session',
                    use_rag=chat_request.use_rag
            ):
                # SSE格式要求：data字段中的换行符需要特殊处理
                # 每个chunk作为单独的SSE事件发送
                if chunk:
                    # SSE协议中，data字段的值如果包含换行，需要用\n分隔多个data行
                    # 但这里我们希望保持chunk的完整性，所以直接发送
                    payload = json.dumps({"v": chunk}, ensure_ascii=False)
                    yield f"data: {payload}\n\n"


        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    except EmptyMessageError as e:
        # 业务验证异常 -> 400
        logger.warning(f"空消息错误: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except LLMCallError as e:
        # LLM 调用失败 -> 500
        logger.error(f"LLM 调用错误: {e.message}")
        raise HTTPException(status_code=500, detail=e.message)
    except HTTPException:
        # FastAPI HTTP 异常直接抛出
        raise
    except Exception as e:
        # 其他未预期异常 -> 500
        logger.error(f"未预期的错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


@chat_router.post('/clear')
async def clear_chat(clear_request: ClearRequest):
    """
    清除聊天历史（接口层）
    职责：调用服务层、返回响应
    """
    session_id = clear_request.session_id or 'default_session'
    chat_service.clear_session(session_id)
    return JSONResponse(content={'success': True})
