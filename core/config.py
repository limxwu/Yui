"""
统一配置管理模块
从环境变量加载配置，提供全局配置实例
"""
import os
from dotenv import load_dotenv
from typing import Optional
from pathlib import Path

# 加载 .env 文件
load_dotenv()


class Settings:
    """应用配置类 - 集中管理所有配置项"""
    
    # ==================== 应用基础配置 ====================
    APP_NAME: str = "Yui AI Chat"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # ==================== API 服务器配置 ====================
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    API_PREFIX: str = "/api/v1"
    
    # ==================== LLM 配置 ====================
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    
    # Ollama 配置（可选）
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # ==================== Streamlit 前端配置 ====================
    STREAMLIT_HOST: str = os.getenv("STREAMLIT_HOST", "localhost")
    STREAMLIT_PORT: int = int(os.getenv("STREAMLIT_PORT", 8501))
    
    # ==================== 会话管理配置 ====================
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", 3600))  # 秒
    DEFAULT_SESSION_ID: str = "default_session"
    
    # ==================== 日志配置 ====================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE", None)  # 如果设置则输出到文件
    
    # ==================== 向量数据库配置 ====================
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
    
    # ==================== 文档处理配置 ====================
    MAX_DOCUMENT_SIZE: int = int(os.getenv("MAX_DOCUMENT_SIZE", 10 * 1024 * 1024))  # 10MB
    
    def validate(self) -> None:
        """验证配置的有效性"""
        if not self.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY 环境变量未设置")
    
    def __repr__(self) -> str:
        return f"Settings(DEBUG={self.DEBUG}, API_PORT={self.API_PORT}, MODEL={self.DEEPSEEK_MODEL})"


# 创建全局配置实例（单例模式）
settings = Settings()
