"""
聊天服务层 - 封装聊天相关的业务逻辑
"""
from typing import AsyncGenerator
from core.llm import get_model, aget_model_response, aget_model_stream
from memory.session_manager import session_manager
from utils.exceptions import EmptyMessageError, LLMCallError
from utils.logger import logger


class ChatService:
    """聊天服务类，封装所有聊天相关的业务逻辑"""
    
    def __init__(self):
        self._model = None
    
    def _get_model_instance(self):
        """获取模型实例（懒加载）"""
        if self._model is None:
            self._model = get_model()
        return self._model
    
    async def send_message(self, message: str, session_id: str = "default_session") -> str:
        """
        发送消息并获取 AI 回复
        
        Args:
            message: 用户消息
            session_id: 会话 ID
            
        Returns:
            str: AI 的回复内容
            
        Raises:
            EmptyMessageError: 当消息为空时
            LLMCallError: LLM 调用失败时
        """
        # 验证输入
        user_message = message.strip()
        if not user_message:
            logger.warning(f"收到空消息，session_id={session_id}")
            raise EmptyMessageError()
        
        logger.info(f"处理聊天请求，session_id={session_id}, message_length={len(user_message)}")
        
        try:
            # 获取或创建会话
            conversation = session_manager.get_or_create_session(session_id)
            
            # 添加用户消息到会话
            conversation.add_user_message(user_message)
            
            # 转换为 LangChain 格式
            messages = conversation.to_langchain_messages()
            
            # 调用 LLM 获取回复
            model_instance = self._get_model_instance()
            response = await aget_model_response(model_instance, messages)
            
            # 提取 AI 回复内容
            ai_response = response.content if hasattr(response, 'content') else str(response)
            
            # 添加 AI 回复到会话
            conversation.add_ai_message(ai_response)
            
            logger.info(f"聊天请求处理成功，session_id={session_id}, response_length={len(ai_response)}")
            
            return ai_response
            
        except EmptyMessageError:
            raise
        except Exception as e:
            logger.error(f"LLM 调用失败，session_id={session_id}, error={str(e)}", exc_info=True)
            raise LLMCallError(f"AI 回复生成失败: {str(e)}")
    
    async def send_message_stream(
        self, 
        message: str, 
        session_id: str = "default_session"
    ) -> AsyncGenerator[str, None]:
        """
        发送消息并获取流式 AI 回复
        
        Args:
            message: 用户消息
            session_id: 会话 ID
            
        Yields:
            str: SSE 格式的 AI 回复片段
            
        Raises:
            EmptyMessageError: 当消息为空时
            LLMCallError: LLM 调用失败时
        """
        # 验证输入
        user_message = message.strip()
        if not user_message:
            logger.warning(f"收到空消息，session_id={session_id}")
            raise EmptyMessageError()
        
        logger.info(f"处理流式聊天请求，session_id={session_id}, message_length={len(user_message)}")
        
        try:
            # 获取或创建会话
            conversation = session_manager.get_or_create_session(session_id)
            
            # 添加用户消息到会话
            conversation.add_user_message(user_message)
            
            # 转换为 LangChain 格式
            messages = conversation.to_langchain_messages()
            
            # 调用 LLM 获取流式回复
            model_instance = self._get_model_instance()
            full_response = ""
            
            async for chunk in aget_model_stream(model_instance, messages):
                full_response += chunk
                # 按照 SSE 协议格式返回数据
                yield chunk
            
            # 添加完整的 AI 回复到会话
            conversation.add_ai_message(full_response)
            
            logger.info(f"流式聊天请求处理成功，session_id={session_id}, response_length={len(full_response)}")
            
        except EmptyMessageError:
            raise
        except Exception as e:
            logger.error(f"LLM 流式调用失败，session_id={session_id}, error={str(e)}", exc_info=True)
            raise LLMCallError(f"AI 流式回复生成失败: {str(e)}")
    
    def clear_session(self, session_id: str = "default_session") -> None:
        """
        清除指定会话的历史记录
        
        Args:
            session_id: 会话 ID
        """
        logger.info(f"清除会话，session_id={session_id}")
        session_manager.clear_session(session_id)


# 创建全局服务实例（单例模式）
chat_service = ChatService()
