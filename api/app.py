from flask import Flask, render_template, request, jsonify, session
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os
import getpass
from dotenv import load_dotenv
from pathlib import Path

# 加载 .env 文件
load_dotenv()

from core.constants import YUI_SYSTEM_PROMPT

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 初始化 Flask 应用，指定模板和静态文件路径
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / 'templates'),
    static_folder=str(BASE_DIR / 'static')
)
app.secret_key = 'yui-secret-key-change-in-production'

# 初始化 DeepSeek 模型
if not os.getenv("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass(prompt="Enter your DeepSeek API key: ")

model = ChatDeepSeek(model="deepseek-chat")


@app.route('/')
def index():
    """渲染聊天页面"""
    return render_template('chat.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """处理聊天请求"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400
        
        # 从 session 中获取对话历史
        if 'messages' not in session:
            session['messages'] = [
                {'role': 'system', 'content': YUI_SYSTEM_PROMPT}
            ]
        
        # 添加用户消息到历史
        session['messages'].append({'role': 'user', 'content': user_message})
        
        # 转换为 LangChain 消息格式
        messages = []
        for msg in session['messages']:
            if msg['role'] == 'system':
                messages.append(SystemMessage(content=msg['content']))
            elif msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
        
        # 调用 DeepSeek 模型
        response = model.invoke(messages)
        ai_response = response.content
        
        # 添加 AI 回复到历史
        session['messages'].append({'role': 'assistant', 'content': ai_response})
        
        # 保持 session 更新
        session.modified = True
        
        return jsonify({
            'success': True,
            'response': ai_response
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """清除聊天历史"""
    session.pop('messages', None)
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
