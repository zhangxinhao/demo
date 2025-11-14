# AI Chat Interface

一个使用 Next.js 构建的 AI 聊天界面，支持流式响应（打字机效果）。

## 功能特性

- ✅ 实时流式响应（打字机效果）
- ✅ 支持 OpenAI 兼容的 API 接口
- ✅ 响应式设计，支持深色模式
- ✅ 现代化 UI，使用 Tailwind CSS
- ✅ 消息自动滚动到底部
- ✅ 支持 Enter 发送，Shift+Enter 换行

## 快速开始

### 1. 配置环境变量

复制 `env.example` 文件为 `.env.local`：

```bash
cp env.example .env.local
```

编辑 `.env.local` 文件，填入你的 API 配置：

```bash
# API endpoint
OPENAI_API_URL=https://api.openai.com/v1/chat/completions

# Your API key
OPENAI_API_KEY=your-actual-api-key-here
```

### 2. 安装依赖

```bash
pnpm install
```

### 3. 启动开发服务器

```bash
pnpm dev
```

打开浏览器访问 [http://localhost:3000](http://localhost:3000)

## 项目结构

```
app/
├── components/
│   ├── ChatMessage.tsx    # 聊天消息组件
│   └── ChatInput.tsx      # 输入框组件
├── api/
│   └── chat/
│       └── route.ts       # API 路由（处理流式请求）
├── page.tsx               # 主页面
├── layout.tsx             # 布局
└── globals.css            # 全局样式
```

## 技术栈

- **框架**: Next.js 16 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS 4
- **UI**: React 19
- **API**: OpenAI 兼容接口（支持流式响应）

## 使用说明

1. 在输入框中输入消息
2. 按 **Enter** 发送消息（按 **Shift+Enter** 换行）
3. AI 将以流式方式返回响应，展现打字机效果
4. 支持深色模式，自动跟随系统主题

## 自定义 API

如果你使用的是 OpenAI 兼容的 API（如 Azure OpenAI、本地模型等），只需在 `.env.local` 中修改 `OPENAI_API_URL` 即可。

```bash
# 例如使用 Azure OpenAI
OPENAI_API_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment/chat/completions?api-version=2024-02-15-preview
OPENAI_API_KEY=your-azure-api-key
```

如需修改模型，编辑 `app/api/chat/route.ts` 中的 `model` 参数。

## 注意事项

- 请确保 API key 安全，不要将其提交到版本控制系统
- `.env.local` 文件已在 `.gitignore` 中，不会被提交
- 首次使用前必须配置有效的 API key，否则会提示错误

