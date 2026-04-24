"""
会话管理和上下文存储
与 Web 层解耦，提供纯粹的会话管理功能
"""
from typing import List, Dict, Optional
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from core.constants import YUI_SYSTEM_PROMPT


class ConversationSession:
    """
    单个会话 session，管理对话历史
    """
    
    def __init__(self, session_id: str):
        """
        初始化会话
        
        Args:
            session_id: 会话唯一标识
        """
        self.session_id = session_id
        self.messages: List[Dict[str, str]] = [
            {'role': 'system', 'content': YUI_SYSTEM_PROMPT}
        ]
    
    def add_user_message(self, content: str):
        """
        添加用户消息
        
        Args:
            content: 用户消息内容
        """
        self.messages.append({'role': 'user', 'content': content})
    
    def add_ai_message(self, content: str):
        """
        添加 AI 回复
        
        Args:
            content: AI 回复内容
        """
        self.messages.append({'role': 'assistant', 'content': content})
    
    def get_messages(self) -> List[Dict[str, str]]:
        """
        获取所有消息历史
        
        Returns:
            消息列表
        """
        return self.messages.copy()
    
    def to_langchain_messages(self) -> List[BaseMessage]:
        """
        转换为 LangChain 消息格式
        
        Returns:
            LangChain 消息列表
        """
        messages = []
        for msg in self.messages:
            if msg['role'] == 'system':
                messages.append(SystemMessage(content=msg['content']))
            elif msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
        return messages
    
    def clear(self):
        """清除会话历史，保留系统提示"""
        self.messages = [
            {'role': 'system', 'content': YUI_SYSTEM_PROMPT}
        ]
    
    def get_message_count(self) -> int:
        """
        获取消息数量（不包括系统消息）
        
        Returns:
            消息数量
        """
        return len(self.messages) - 1  # 减去 system message
    
    async def aadd_user_message(self, content: str):
        """
        异步添加用户消息
        
        Args:
            content: 用户消息内容
        """
        # 这里可以添加异步逻辑，如保存到数据库
        self.add_user_message(content)
    
    async def aadd_ai_message(self, content: str):
        """
        异步添加 AI 回复
        
        Args:
            content: AI 回复内容
        """
        # 这里可以添加异步逻辑，如保存到数据库
        self.add_ai_message(content)


class SessionManager:
    """
    会话管理器，管理多个会话
    """
    
    def __init__(self):
        """初始化会话管理器"""
        self.sessions: Dict[str, ConversationSession] = {}
    
    def get_or_create_session(self, session_id: str) -> ConversationSession:
        """
        获取或创建会话
        
        Args:
            session_id: 会话 ID
            
        Returns:
            会话对象
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationSession(session_id)
        return self.sessions[session_id]
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """
        获取会话
        
        Args:
            session_id: 会话 ID
            
        Returns:
            会话对象，不存在则返回 None
        """
        return self.sessions.get(session_id)
    
    def delete_session(self, session_id: str):
        """
        删除会话
        
        Args:
            session_id: 会话 ID
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def clear_session(self, session_id: str):
        """
        清空会话历史
        
        Args:
            session_id: 会话 ID
        """
        session = self.get_session(session_id)
        if session:
            session.clear()
    
    def cleanup_expired_sessions(self, max_idle_time: int = 3600):
        """
        清理过期会话（可选实现）
        
        Args:
            max_idle_time: 最大空闲时间（秒）
        """
        pass


# 全局会话管理器实例
session_manager = SessionManager()
