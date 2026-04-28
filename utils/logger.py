"""
统一日志配置模块
提供标准化的日志记录器，支持控制台和文件输出
"""
import logging
import sys
from pathlib import Path
from core.config import settings


def setup_logger(name: str = "yui") -> logging.Logger:
    """
    创建统一的日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 配置好的日志记录器实例
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加 handler
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 创建格式化器
    formatter = logging.Formatter(
        fmt=settings.LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 控制台 Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件 Handler（如果配置了 LOG_FILE）
    if settings.LOG_FILE:
        log_path = Path(settings.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(settings.LOG_FILE, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# 创建默认日志记录器实例
logger = setup_logger("yui")
