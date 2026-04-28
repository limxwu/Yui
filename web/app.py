"""
Streamlit 前端页面 - Yui AI 对话助手
简化版本，使用 Streamlit 官方示例风格
"""
import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(
    page_title="Yui - AI 对话助手",
    page_icon="🤖"
)

# API 基础 URL（从环境变量读取）
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

# 标题
st.title("🤖 Yui - AI 对话助手")

# 初始化 session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = []


def send_message_to_api(message: str) -> str:
    """发送消息到 FastAPI 后端"""
    try:
        res = requests.post(
            f"{API_BASE_URL}/chat",
            json={
                "message": message,
                "session_id": st.session_state.session_id
            },
            timeout=60
        )

        if res.status_code == 200:
            data = res.json()
            if data.get('success'):
                return data.get('response', '')
            else:
                return f"错误: {data.get('error', '未知错误')}"
        else:
            return f"请求失败: {res.status_code}"
    except Exception as e:
        return f"连接错误: {str(e)}"


def clear_chat():
    """清除聊天历史"""
    try:
        requests.post(
            f"{API_BASE_URL}/chat/clear",
            json={"session_id": st.session_state.session_id}
        )
    except Exception as e:
        st.error(f"清除对话失败: {str(e)}")

    # 重置本地会话
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.rerun()


# 显示聊天历史
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# 输入框
if prompt := st.chat_input("输入消息..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)

    # 添加用户消息到历史
    st.session_state.messages.append({
        'role': 'user',
        'content': prompt
    })

    # 调用 API 获取回复
    with st.chat_message("assistant"):
        with st.spinner('Yui 正在思考...'):
            response = send_message_to_api(prompt)
        st.markdown(response)

    # 添加 AI 回复到历史
    st.session_state.messages.append({
        'role': 'assistant',
        'content': response
    })

# 侧边栏 - 清除对话按钮
with st.sidebar:
    st.header("设置")
    if st.button("🗑️ 清除对话", use_container_width=True):
        clear_chat()

    st.divider()
    st.caption(f"会话 ID: {st.session_state.session_id[:8]}...")


