"""
同时启动 FastAPI 后端和 Streamlit 前端
"""
import os
import subprocess
import threading
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取端口配置
API_PORT = int(os.getenv("API_PORT", 8000))
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8501))


def start_backend():
    """启动 FastAPI 后端"""
    print(f"🚀 正在启动 Yui AI Chat API 服务器...")
    print(f"📍 API 地址: http://localhost:{API_PORT}")
    print(f"📚 API 文档: http://localhost:{API_PORT}/docs")

    subprocess.run([
        "uvicorn",
        "api.app:app",
        "--host", "0.0.0.0",
        "--port", str(API_PORT),
        "--reload"
    ])


def start_frontend():
    """启动 Streamlit 前端"""
    print(f"\n🎨 正在启动 Yui AI Chat 前端界面...")
    print(f"📍 访问地址: http://localhost:{STREAMLIT_PORT}")

    subprocess.run([
        "streamlit",
        "run",
        "web/app.py",
        "--server.port", str(STREAMLIT_PORT),
        "--server.headless", "true"
    ])


if __name__ == "__main__":
    print("=" * 60)
    print("  Yui AI Chat - FastAPI + Streamlit")
    print("=" * 60)
    print()

    # # 在后台线程中启动后端
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()

    # 在主线程中启动前端
    start_frontend()
