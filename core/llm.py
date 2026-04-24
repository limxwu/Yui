"""
LLM 模型初始化和配置
"""
import os
import getpass
from langchain_deepseek import ChatDeepSeek


def init_deepseek_model():
    """
    初始化 DeepSeek 模型
    
    Returns:
        ChatDeepSeek: 配置好的 DeepSeek 模型实例
    """
    # 检查 API Key
    if not os.getenv("DEEPSEEK_API_KEY"):
        os.environ["DEEPSEEK_API_KEY"] = getpass.getpass(
            prompt="Enter your DeepSeek API key: "
        )
    
    # 创建模型实例
    model = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0.7,  # 可以调整温度参数
    )
    
    return model


# 全局模型实例（懒加载）
_model_instance = None


def get_model():
    """
    获取模型实例（单例模式）
    
    Returns:
        ChatDeepSeek: DeepSeek 模型实例
    """
    global _model_instance
    if _model_instance is None:
        _model_instance = init_deepseek_model()
    return _model_instance


async def aget_model_response(model, messages):
    """
    异步获取模型响应
    
    Args:
        model: LLM 模型实例
        messages: 消息列表
        
    Returns:
        模型响应内容
    """
    # LangChain 的 invoke 方法通常是同步的，但我们可以包装为异步
    # 对于真正的异步支持，需要使用 invoke_async 或 stream 方法
    # 如果模型支持异步调用，则使用异步版本
    try:
        # 尝试使用异步调用方法
        if hasattr(model, 'ainvoke'):
            response = await model.ainvoke(messages)
        else:
            # 如果不支持异步，使用同步方法但在异步上下文中
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, model.invoke, messages)
        return response
    except Exception as e:
        # 如果异步调用失败，回退到同步调用
        return model.invoke(messages)
