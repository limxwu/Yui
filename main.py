"""
同时启动 FastAPI 后端和 Streamlit 前端
"""
import os
import subprocess
import threading
import signal
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取端口配置
API_PORT = int(os.getenv("API_PORT", 8000))
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8501))

# 全局变量存储进程引用
backend_process = None
frontend_process = None


def start_backend():
    """启动 FastAPI 后端"""
    global backend_process
    print(f"🚀 正在启动 Yui AI Chat API 服务器...")
    print(f"📍 API 地址: http://localhost:{API_PORT}")
    print(f"📚 API 文档: http://localhost:{API_PORT}/docs")

    backend_process = subprocess.Popen([
        "uvicorn",
        "api.app:app",
        "--host", "0.0.0.0",
        "--port", str(API_PORT),
        "--reload"
    ])
    
    # 等待进程完成
    backend_process.wait()


def start_frontend():
    """启动 Streamlit 前端"""
    global frontend_process
    print(f"\n🎨 正在启动 Yui AI Chat 前端界面...")
    print(f"📍 访问地址: http://localhost:{STREAMLIT_PORT}")

    frontend_process = subprocess.Popen([
        "streamlit",
        "run",
        "web/app.py",
        "--server.port", str(STREAMLIT_PORT),
        "--server.headless", "true"
    ])
    
    # 等待进程完成
    frontend_process.wait()


def signal_handler(sig, frame):
    """处理退出信号"""
    print("\n\n🛑 正在关闭服务...")
    
    # 终止后端进程
    if backend_process and backend_process.poll() is None:
        print("⏹️  停止后端服务...")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
    
    # 终止前端进程  
    if frontend_process and frontend_process.poll() is None:
        print("⏹️  停止前端服务...")
        frontend_process.terminate()
        try:
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            frontend_process.kill()
    
    print("✅ 所有服务已关闭")
    sys.exit(0)


if __name__ == "__main__":
    print("=" * 60)
    print("  Yui AI Chat - FastAPI + Streamlit")
    print("=" * 60)
    print()

    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 在后台线程中启动后端
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()

    # 在主线程中启动前端
    start_frontend()
