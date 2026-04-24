print("=" * 60)
print("Yui - AI 对话助手")
print("=" * 60)
print("\n正在启动 Web 服务器...")
print("访问地址: http://localhost")
print("按 Ctrl+C 停止服务器\n")

from api.app import app
app.run(debug=True, host='0.0.0.0', port=80)
