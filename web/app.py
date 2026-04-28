"""
Streamlit 前端页面 - Yui AI 对话助手
简化版本，使用 Streamlit 官方示例风格
"""
import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv
import json

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
if 'use_rag' not in st.session_state:
    st.session_state.use_rag = True  # 默认启用 RAG


def send_message_to_api(message: str) -> str:
    """发送消息到 FastAPI 后端（非流式）"""
    try:
        res = requests.post(
            f"{API_BASE_URL}/chat",
            json={
                "message": message,
                "session_id": st.session_state.session_id,
                "use_rag": st.session_state.use_rag
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


def send_message_stream_to_api_sync(message: str):
    """发送消息到 FastAPI 后端并接收流式响应（同步版本）"""
    try:
        import httpx
        from httpx_sse import connect_sse
        
        with httpx.Client() as client:
            with connect_sse(
                client,
                "POST",
                f"{API_BASE_URL}/chat/stream",
                json={
                    "message": message,
                    "session_id": st.session_state.session_id,
                    "use_rag": st.session_state.use_rag
                }
            ) as event_source:
                for sse in event_source.iter_sse():
                    chunk = json.loads(sse.data)['v']
                    yield chunk
    except httpx.ReadTimeout:
        yield "连接错误: 读取超时，请检查网络连接或稍后重试"
    except httpx.ConnectTimeout:
        yield "连接错误: 连接超时，请确保后端服务正在运行"
    except Exception as e:
        yield f"连接错误: {str(e)}"


def upload_document_to_api(file) -> dict:
    """上传文档到 FastAPI 后端"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        res = requests.post(
            f"{API_BASE_URL}/memory/document",
            files=files,
            timeout=120  # 文档处理可能需要更长时间
        )
        
        if res.status_code == 200:
            return res.json()
        else:
            return {
                "success": False,
                "message": f"请求失败: {res.status_code} - {res.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"连接错误: {str(e)}"
        }


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

    # 调用 API 获取回复（使用流式响应）
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 使用同步流式请求
        for chunk in send_message_stream_to_api_sync(prompt):
            full_response += chunk
            # Streamlit markdown渲染：保持原始内容不变
            # Markdown规范中，段落间的空行（双换行）会自动识别
            # 单个换行需要两个空格才能生效，但我们不修改原始数据
            message_placeholder.markdown(full_response + "▌")
        
        # 最终显示完整响应，移除光标
        message_placeholder.markdown(full_response)
        response = full_response

    # 添加 AI 回复到历史
    st.session_state.messages.append({
        'role': 'assistant',
        'content': response
    })

# 侧边栏 - 清除对话按钮和文档上传
with st.sidebar:
    st.header("设置")
    
    # RAG 开关
    st.subheader("🧠 RAG 设置")
    use_rag = st.checkbox(
        "启用知识库检索",
        value=st.session_state.use_rag,
        help="启用后，AI 会从已上传的文档中检索相关信息来回答问题"
    )
    if use_rag != st.session_state.use_rag:
        st.session_state.use_rag = use_rag
        st.rerun()
    
    st.divider()
    
    # 文档上传区域
    st.subheader("📄 文档上传")
    uploaded_file = st.file_uploader(
        "上传文档到知识库",
        type=['pdf', 'docx', 'doc', 'txt'],
        help="支持 PDF、DOCX、DOC、TXT 格式"
    )
    
    if uploaded_file is not None:
        if st.button("⬆️ 上传文档", use_container_width=True):
            with st.spinner("正在处理文档..."):
                result = upload_document_to_api(uploaded_file)
                
                if result.get('success'):
                    st.success(result.get('message', '上传成功'))
                else:
                    st.error(result.get('message', '上传失败'))
    
    st.divider()
    
    # 清除对话按钮
    if st.button("🗑️ 清除对话", use_container_width=True):
        clear_chat()

    st.divider()
    st.caption(f"会话 ID: {st.session_state.session_id[:8]}...")


