from flask import Flask, render_template, request, jsonify
from flask_session import Session
import os
import asyncio
from dotenv import load_dotenv
from pathlib import Path

# 加载 .env 文件
load_dotenv()

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 初始化 Flask 应用，指定模板和静态文件路径
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / 'templates'),
    static_folder=str(BASE_DIR / 'static')
)

# 配置服务器端 Session（使用文件系统存储）
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = BASE_DIR / 'flask_session'
app.config['SESSION_PERMANENT'] = False
app.config['SECRET_KEY'] = 'yui-secret-key-change-in-production'

# 创建 session 存储目录
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

# 初始化 Session
Session(app)

# 导入业务逻辑
from core.llm import get_model, aget_model_response
from memory.session_manager import session_manager

# 初始化 DeepSeek 模型（懒加载，首次调用时初始化）
model = None


def get_model_instance():
    """获取模型实例（懒加载）"""
    global model
    if model is None:
        model = get_model()
    return model


@app.route('/')
def index():
    """渲染聊天页面"""
    return render_template('chat.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """处理聊天请求（异步版本）"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400
        
        # 从 Flask session 中获取会话 ID
        session_id = request.cookies.get('session') or 'default_session'
        
        # 获取或创建会话（使用 memory 层的会话管理器）
        conversation = session_manager.get_or_create_session(session_id)
        
        # 添加用户消息
        conversation.add_user_message(user_message)
        
        # 转换为 LangChain 格式
        messages = conversation.to_langchain_messages()
        
        # 调用 LLM（异步）
        model_instance = get_model_instance()
        
        # 在异步上下文中运行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(aget_model_response(model_instance, messages))
        finally:
            loop.close()
        
        ai_response = response.content if hasattr(response, 'content') else str(response)
        
        # 添加 AI 回复到会话
        conversation.add_ai_message(ai_response)
        
        return jsonify({
            'success': True,
            'response': ai_response
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """清除聊天历史"""
    session_id = request.cookies.get('session') or 'default_session'
    session_manager.clear_session(session_id)
    return jsonify({'success': True})
