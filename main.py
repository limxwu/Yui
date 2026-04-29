"""
启动 FastAPI 后端
"""
import os
import subprocess
import signal
import sys
from dotenv import load_dotenv

load_dotenv()
API_PORT = int(os.getenv("API_PORT", 8000))
backend_process = None


def start_backend():
    global backend_process
    print(f"正在启动 Yui AI Chat API 服务器...")
    print(f"API 地址: http://localhost:{API_PORT}")
    print(f"API 文档: http://localhost:{API_PORT}/docs")
    backend_process = subprocess.Popen([
        "uvicorn", "api.app:app", "--host", "0.0.0.0",
        "--port", str(API_PORT), "--reload"
    ])
    backend_process.wait()


def signal_handler(sig, frame):
    print("\n正在关闭服务...")
    if backend_process and backend_process.poll() is None:
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    start_backend()
