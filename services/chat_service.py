"""
聊天服务层 - 封装聊天相关的业务逻辑
使用 LangChain LCEL 构建 RAG 链
"""
from typing import AsyncGenerator

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from core.llm import get_model
from memory.persistent_memory import persistent_memory
from memory.session_manager import session_manager
from utils.exceptions import EmptyMessageError, LLMCallError
from utils.logger import logger


class ChatService:
    """聊天服务类，封装所有聊天相关的业务逻辑"""
    
    def __init__(self):
        self._model = None
        self._rag_chain = None
        self._stream_rag_chain = None
    
    def _get_model_instance(self):
        """获取模型实例（懒加载）"""
        if self._model is None:
            self._model = get_model()
        return self._model
    
    def _build_rag_prompt(self) -> ChatPromptTemplate:
        """
        构建 RAG 提示模板
        
        Returns:
            ChatPromptTemplate: RAG 提示模板
        """
        from core.constants import YUI_SYSTEM_PROMPT
        
        messages = [
            ("system", YUI_SYSTEM_PROMPT),
            ("system", "以下是参考上下文：\n{context}"),
            ("placeholder", "{history}"),
            ("human", "{question}"),
        ]
        
        return ChatPromptTemplate.from_messages(messages)
    
    def _build_normal_prompt(self) -> ChatPromptTemplate:
        """
        构建普通对话提示模板（无 RAG）
        
        Returns:
            ChatPromptTemplate: 普通对话提示模板
        """
        from core.constants import YUI_SYSTEM_PROMPT
        
        messages = [
            ("system", YUI_SYSTEM_PROMPT),
            ("placeholder", "{history}"),
            ("human", "{question}"),
        ]
        
        return ChatPromptTemplate.from_messages(messages)
    
    def _create_rag_chain(self, use_stream: bool = False):
        """
        创建 RAG 链（使用 LCEL）
        
        Args:
            use_stream: 是否创建流式链
            
        Returns:
            可运行的链对象
        """
        model = self._get_model_instance()
        prompt = self._build_rag_prompt()
        
        # 定义检索函数
        def retrieve_documents(query: dict) -> dict:
            """检索相关文档"""
            question = query.get("question", "")
            if not question:
                return {"context": "", **query}
            
            try:
                # 从向量数据库检索相关文档
                docs_with_scores = persistent_memory.similarity_search_with_score(question)
                
                # 提取文档内容并拼接
                if docs_with_scores:
                    # 只取前 3 个最相关的文档
                    context_docs = [doc.page_content for doc, score in docs_with_scores[:3]]
                    context = "\n\n".join(context_docs)
                else:
                    context = "未找到相关文档"
                    
                logger.debug(f"检索到 {len(docs_with_scores)} 个相关文档")
            except Exception as e:
                logger.warning(f"文档检索失败: {str(e)}")
                context = "文档检索失败"
            
            return {"context": context, **query}
        
        # 使用 LCEL 构建链
        chain = (
            {
                "context": retrieve_documents,
                "history": lambda x: x.get("history", []),
                "question": lambda x: x.get("question", "")
            }
            | prompt
            | model
            | StrOutputParser()
        )
        
        return chain
    
    def _create_normal_chain(self, use_stream: bool = False):
        """
        创建普通对话链（无 RAG，使用 LCEL）
        
        Args:
            use_stream: 是否创建流式链
            
        Returns:
            可运行的链对象
        """
        model = self._get_model_instance()
        prompt = self._build_normal_prompt()
        
        # 使用 LCEL 构建链
        chain = (
            {
                "history": lambda x: x.get("history", []),
                "question": lambda x: x.get("question", "")
            }
            | prompt
            | model
            | StrOutputParser()
        )
        
        return chain
    
    def _format_history(self, messages: list) -> str:
        """
        格式化历史对话为字符串
        
        Args:
            messages: 消息列表
            
        Returns:
            格式化后的历史对话字符串
        """
        formatted = []
        for msg in messages:
            role = msg.get('role', '')
            content = msg.get('content', '')
            if role == 'user':
                formatted.append(f"用户: {content}")
            elif role == 'assistant':
                formatted.append(f"AI: {content}")
        return "\n".join(formatted)
    
    async def send_message(
        self, 
        message: str, 
        session_id: str = "default_session",
        use_rag: bool = True
    ) -> str:
        """
        发送消息并获取 AI 回复
        
        Args:
            message: 用户消息
            session_id: 会话 ID
            use_rag: 是否使用 RAG（检索增强生成）
            
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
        
        logger.info(f"处理聊天请求，session_id={session_id}, use_rag={use_rag}, message_length={len(user_message)}")
        
        try:
            # 获取或创建会话
            conversation = session_manager.get_or_create_session(session_id)
            
            # 添加用户消息到会话
            conversation.add_user_message(user_message)
            
            # 转换为 LangChain 消息格式
            lc_messages = conversation.to_langchain_messages()
            
            # 选择链类型
            if use_rag:
                chain = self._create_rag_chain()
                input_data = {
                    "question": user_message,
                    "history": lc_messages
                }
            else:
                chain = self._create_normal_chain()
                input_data = {
                    "question": user_message,
                    "history": lc_messages
                }
            
            # 调用链获取回复
            response = await chain.ainvoke(input_data)
            
            # 添加 AI 回复到会话
            conversation.add_ai_message(response)
            
            logger.info(f"聊天请求处理成功，session_id={session_id}, response_length={len(response)}")
            
            return response
            
        except EmptyMessageError:
            raise
        except Exception as e:
            logger.error(f"LLM 调用失败，session_id={session_id}, error={str(e)}", exc_info=True)
            raise LLMCallError(f"AI 回复生成失败: {str(e)}")
    
    async def send_message_stream(
        self, 
        message: str, 
        session_id: str = "default_session",
        use_rag: bool = True
    ) -> AsyncGenerator[str, None]:
        """
        发送消息并获取流式 AI 回复
        
        Args:
            message: 用户消息
            session_id: 会话 ID
            use_rag: 是否使用 RAG（检索增强生成）
            
        Yields:
            str: AI 回复片段
            
        Raises:
            EmptyMessageError: 当消息为空时
            LLMCallError: LLM 调用失败时
        """
        # 验证输入
        user_message = message.strip()
        if not user_message:
            logger.warning(f"收到空消息，session_id={session_id}")
            raise EmptyMessageError()
        
        logger.info(f"处理流式聊天请求，session_id={session_id}, use_rag={use_rag}, message_length={len(user_message)}")
        
        full_response = ""
        try:
            # 获取或创建会话
            conversation = session_manager.get_or_create_session(session_id)
            
            # 添加用户消息到会话
            conversation.add_user_message(user_message)
            
            # 转换为 LangChain 消息格式
            lc_messages = conversation.to_langchain_messages()
            
            # 选择链类型
            if use_rag:
                chain = self._create_rag_chain()
                input_data = {
                    "question": user_message,
                    "history": lc_messages
                }
            else:
                chain = self._create_normal_chain()
                input_data = {
                    "question": user_message,
                    "history": lc_messages
                }
            
            # 流式调用链
            async for chunk in chain.astream(input_data):
                full_response += chunk
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
