# Yui Web 应用快速启动脚本
# 使用方法: .\start_web.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Yui - AI 对话助手 Web 版" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否设置了 API Key
if (-not $env:DEEPSEEK_API_KEY) {
    Write-Host "⚠️  未检测到 DEEPSEEK_API_KEY 环境变量" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "请选择：" -ForegroundColor White
    Write-Host "1. 现在输入 API Key" -ForegroundColor White
    Write-Host "2. 稍后在运行时输入" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "请输入选项 (1/2)"
    
    if ($choice -eq "1") {
        $apiKey = Read-Host "请输入 DeepSeek API Key" -AsSecureString
        $plainApiKey = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey))
        $env:DEEPSEEK_API_KEY = $plainApiKey
        Write-Host "✓ API Key 已设置" -ForegroundColor Green
    }
} else {
    Write-Host "✓ 检测到 DEEPSEEK_API_KEY 环境变量" -ForegroundColor Green
}

Write-Host ""
Write-Host "正在启动 Web 服务器..." -ForegroundColor Cyan
Write-Host "访问地址: http://localhost:5000" -ForegroundColor Green
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host ""

# 启动应用
uv run python api/app.py
