"""
Pydantic 数据模型（请求/响应 Schema）
集中管理所有 API 的数据验证模型
"""
from pydantic import BaseModel, Field
from typing import Optional


# ==================== 聊天相关模型 ====================

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str = Field(..., min_length=1, description="用户消息内容")
    session_id: Optional[str] = Field("default_session", description="会话 ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "你好，请介绍一下自己",
                "session_id": "user_123"
            }
        }


class ClearRequest(BaseModel):
    """清除会话请求模型"""
    session_id: Optional[str] = Field("default_session", description="会话 ID")


class ChatResponse(BaseModel):
    """聊天响应模型"""
    success: bool = Field(..., description="请求是否成功")
    response: Optional[str] = Field(None, description="AI 回复内容")
    error: Optional[str] = Field(None, description="错误信息（如果失败）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "response": "你好！我是 Yui AI 助手...",
                "error": None
            }
        }


# ==================== 会话相关模型（未来扩展）====================

class SessionInfo(BaseModel):
    """会话信息模型"""
    session_id: str
    message_count: int
    created_at: str
    last_updated: str


class SessionListResponse(BaseModel):
    """会话列表响应模型"""
    success: bool
    sessions: list[SessionInfo]


# ==================== 文档相关模型（未来扩展）====================

class DocumentUploadRequest(BaseModel):
    """文档上传请求模型"""
    filename: str
    content: bytes
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "example.pdf",
                "content": "<base64_encoded_content>"
            }
        }
