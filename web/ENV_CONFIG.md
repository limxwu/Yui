# 前端环境变量配置说明

## 概述

前端项目使用 Vite 的环境变量系统来管理 API 基础地址等配置。所有环境变量必须以 `VITE_` 前缀开头才能在客户端代码中访问。

## 配置文件

### `.env.example`（模板文件，已提交到版本控制）

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### `.env`（实际配置文件，不提交到版本控制）

复制 `.env.example` 创建 `.env` 文件：

```bash
cp .env.example .env
```

然后根据实际环境修改配置。

## 可用配置项

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `VITE_API_BASE_URL` | 后端 API 基础地址 | `http://localhost:8000/api/v1` |

## 使用示例

### 开发环境

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 测试环境

```env
VITE_API_BASE_URL=http://test-api.example.com/api/v1
```

### 生产环境

```env
VITE_API_BASE_URL=https://api.example.com/api/v1
```

## 在代码中使用

在 TypeScript/JavaScript 代码中通过 `import.meta.env` 访问：

```typescript
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
```

参考实现：[web/src/api/index.ts](../src/api/index.ts)

## 注意事项

1. **必须重启开发服务器**：修改 `.env` 文件后，需要重启 Vite 开发服务器才能生效
2. **不要提交 `.env` 文件**：`.env` 已在 `.gitignore` 中，不会被提交到版本控制
3. **提交 `.env.example`**：确保模板文件包含所有必要的配置项和示例值
4. **VITE_ 前缀**：只有以 `VITE_` 开头的变量才能在客户端代码中访问

## 相关文档

- [Vite 环境变量文档](https://cn.vitejs.dev/guide/env-and-mode.html)
- [项目 README](../../README.md)
