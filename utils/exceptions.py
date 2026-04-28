"""
自定义异常类模块
定义业务层的异常类型，便于分层处理
"""


class AppError(Exception):
    """应用基础异常类"""
    def __init__(self, message: str = "应用错误", code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)


# ==================== 聊天服务异常 ====================

class ChatServiceError(AppError):
    """聊天服务基础异常"""
    def __init__(self, message: str = "聊天服务错误"):
        super().__init__(message=message, code=500)


class EmptyMessageError(ChatServiceError):
    """空消息异常"""
    def __init__(self, message: str = "消息不能为空"):
        super().__init__(message=message, code=400)


class LLMCallError(ChatServiceError):
    """LLM 调用失败异常"""
    def __init__(self, message: str = "LLM 调用失败"):
        super().__init__(message=message, code=500)


# ==================== 会话管理异常 ====================

class SessionError(AppError):
    """会话管理基础异常"""
    def __init__(self, message: str = "会话错误"):
        super().__init__(message=message, code=500)


class SessionNotFoundError(SessionError):
    """会话未找到异常"""
    def __init__(self, session_id: str):
        super().__init__(message=f"会话不存在: {session_id}", code=404)


class SessionTimeoutError(SessionError):
    """会话超时异常"""
    def __init__(self, session_id: str):
        super().__init__(message=f"会话已超时: {session_id}", code=408)


# ==================== 文档处理异常 ====================

class DocumentError(AppError):
    """文档处理基础异常"""
    def __init__(self, message: str = "文档处理错误"):
        super().__init__(message=message, code=500)


class DocumentSizeExceededError(DocumentError):
    """文档大小超限异常"""
    def __init__(self, max_size: int):
        super().__init__(
            message=f"文档大小超过限制 ({max_size / 1024 / 1024:.2f} MB)",
            code=413
        )


class DocumentParseError(DocumentError):
    """文档解析失败异常"""
    def __init__(self, filename: str):
        super().__init__(message=f"文档解析失败: {filename}", code=400)


# ==================== 配置异常 ====================

class ConfigurationError(AppError):
    """配置错误异常"""
    def __init__(self, message: str = "配置错误"):
        super().__init__(message=message, code=500)
