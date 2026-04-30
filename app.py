"""
FastAPI 后端应用主入口
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import (JSONResponse,FileResponse)
from fastapi.requests import Request
from api.v1 import get_v1_router


# 创建 FastAPI 应用
app = FastAPI(
    title="Yui AI Chat API",
    description="Yui AI 对话助手后端 API",
    version="1.0.0"
)



# 注册 v1 版本的所有路由（集中管理）
app.include_router(get_v1_router(), prefix="/api/v1")
# 挂载静态文件目录
# app.mount("/static",StaticFiles(directory="static"), name="static")
# 挂载前端打包文件
import os
if os.path.exists("dist"):
    app.mount("/assets",StaticFiles(directory="dist/assets"), name="assets")


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.get("/")
async def root(request: Request):
    """提供 Vue 3 SPA 的主页面"""
    if os.path.exists("dist/index.html"):
        return FileResponse("dist/index.html")
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "前端构建产物不存在，请先运行 cd web-ui && npm run build"}
        )


# Catch-all 路由 - 处理所有前端路由（必须放在最后）
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """
    Catch-all 路由，将所有非 API 请求重定向到 index.html
    这样可以支持 Vue Router 的 HTML5 History 模式
    """
    # 如果请求的是静态资源（如 favicon.ico），返回 404
    if full_path.endswith(('.ico', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.css', '.js', '.json')):
        return JSONResponse(status_code=404, content={"error": "资源未找到"})

    # 其他所有路径都返回 index.html，让前端路由处理
    if os.path.exists("dist/index.html"):
        return FileResponse("dist/index.html")
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "前端构建产物不存在，请先运行 cd web && npm run build"}
        )

if __name__ == "__main__":
    import uvicorn
    from core.config import settings
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)