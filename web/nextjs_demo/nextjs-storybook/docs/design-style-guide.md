# 前端设计风格指南

**Version:** 1.0  
**Theme:** "Minimalist White"  
**Last Updated:** 2025-12

---

## 1. 设计哲学

界面遵循 **"隐形 UI"** 的设计理念。设计应当退居幕后，让内容成为焦点。

### 核心原则

| 原则 | 描述 |
|------|------|
| **简约至上** | 去除一切不必要的视觉噪音 |
| **内容优先** | 设计服务于内容，而非喧宾夺主 |
| **克制动效** | 动画应流畅自然，而非突兀跳跃 |
| **一致体验** | 保持跨平台、跨组件的视觉一致性 |

### 美学风格

- **视觉风格：** 纯净白色、高对比度文字、微妙边框、柔和阴影
- **动效风格：** 动态但克制，元素应滑动而非跳跃
- **材质质感：** 哑光平面，避免玻璃拟态或重度渐变

---

## 2. 色彩系统

### 2.1 核心色板

```css
:root {
  /* 背景层级 */
  --color-canvas: #FFFFFF;           /* 主画布 - 纯白 */
  --color-surface: #FAFAFA;          /* 次级表面 - 浅灰白 */
  --color-surface-hover: #F5F5F5;    /* 悬停态 */
  
  /* 文字层级 */
  --color-text-primary: #171717;     /* 主要文字 - 近黑色（柔化） */
  --color-text-secondary: #737373;   /* 次要文字 - 中性灰 */
  --color-text-muted: #A3A3A3;       /* 辅助文字 - 浅灰 */
  
  /* 功能色 */
  --color-accent: #000000;           /* 强调色 - 纯黑 */
  --color-accent-alt: #2563EB;       /* 可选强调色 - 企业蓝 */
  --color-border: #E5E7EB;           /* 边框 - 极浅灰 */
  --color-border-focus: #D1D5DB;     /* 聚焦边框 */
  
  /* 状态色 */
  --color-success: #22C55E;          /* 成功 */
  --color-warning: #F59E0B;          /* 警告 */
  --color-error: #EF4444;            /* 错误 */
  --color-info: #3B82F6;             /* 信息 */
}
```

### 2.2 色彩使用原则

| 场景 | 颜色 | 说明 |
|------|------|------|
| 页面背景 | `--color-canvas` | 主内容区域使用纯白 |
| 侧边栏/卡片 | `--color-surface` | 层级区分，微妙对比 |
| 主要按钮 | `--color-accent` | 使用纯黑或强调色 |
| 次要按钮 | `transparent` + `border` | 边框按钮，不抢焦点 |
| 禁用状态 | 50% 透明度 | 保持一致的禁用视觉 |

### 2.3 对比度要求

- 正文文字与背景对比度 ≥ **4.5:1** (WCAG AA)
- 大标题与背景对比度 ≥ **3:1**
- 交互元素与背景对比度 ≥ **3:1**

---

## 3. 字体系统

### 3.1 字体族

```css
:root {
  /* 系统字体栈 */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", 
               "Inter", "Roboto", "Helvetica Neue", sans-serif;
  
  /* 代码字体 */
  --font-mono: "JetBrains Mono", "Fira Code", "SF Mono", 
               "Consolas", monospace;
}
```

### 3.2 字号规范

| 级别 | 尺寸 | 行高 | 字重 | 使用场景 |
|------|------|------|------|----------|
| Display | 36px | 1.2 | 700 | 大标题、Hero区域 |
| H1 | 28px | 1.3 | 600 | 页面主标题 |
| H2 | 24px | 1.35 | 600 | 区块标题 |
| H3 | 20px | 1.4 | 600 | 子区块标题 |
| H4 | 16px | 1.5 | 600 | 卡片标题 |
| Body | 16px | 1.6 | 400 | 正文内容 |
| Body Small | 14px | 1.5 | 400 | 辅助说明 |
| Caption | 12px | 1.4 | 400 | 标签、元数据 |
| Code | 14px | 1.6 | 400 | 代码块 |

### 3.3 字体使用规范

```css
/* 标题样式 */
.heading {
  font-family: var(--font-sans);
  font-weight: 600;
  letter-spacing: -0.02em;  /* 标题字间距收紧 */
  color: var(--color-text-primary);
}

/* 正文样式 */
.body {
  font-family: var(--font-sans);
  font-weight: 400;
  letter-spacing: 0;
  color: var(--color-text-primary);
}

/* 代码样式 */
.code {
  font-family: var(--font-mono);
  font-size: 14px;
  background: var(--color-surface);
  padding: 2px 6px;
  border-radius: 4px;
}
```

---

## 4. 间距与圆角

### 4.1 间距系统 (8px 基数)

```css
:root {
  --space-0: 0;
  --space-1: 4px;     /* 紧凑间距 */
  --space-2: 8px;     /* 基础间距 */
  --space-3: 12px;    /* 小间距 */
  --space-4: 16px;    /* 标准间距 */
  --space-5: 20px;    /* 中等间距 */
  --space-6: 24px;    /* 常用内边距 */
  --space-8: 32px;    /* 大间距 */
  --space-10: 40px;   /* 区块间距 */
  --space-12: 48px;   /* 章节间距 */
  --space-16: 64px;   /* 页面级间距 */
}
```

### 4.2 圆角规范

```css
:root {
  --radius-sm: 4px;   /* 小元素：标签、徽章 */
  --radius-md: 8px;   /* 标准元素：按钮、输入框 */
  --radius-lg: 12px;  /* 大元素：卡片、面板 */
  --radius-xl: 16px;  /* 模态框、大卡片 */
  --radius-full: 9999px; /* 圆形：头像、药丸标签 */
}
```

### 4.3 间距使用原则

- **内边距 (Padding)：** 慷慨留白，使用 `24px` 作为常用值
- **组件间距：** 保持至少 `16px` 的呼吸空间
- **区块间距：** 使用 `32px - 48px` 区分不同功能区域
- **文字间距：** 段落间 `16px`，标题与内容间 `12px`

---

## 5. 阴影与层级

### 5.1 阴影系统

```css
:root {
  /* 无阴影 - 扁平元素 */
  --shadow-none: none;
  
  /* 微阴影 - 悬停状态、微妙提升 */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.04);
  
  /* 小阴影 - 卡片、下拉菜单 */
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.06);
  
  /* 中阴影 - 悬浮卡片、Popover */
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  
  /* 大阴影 - 模态框、抽屉 */
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
  
  /* 特大阴影 - 特殊强调 */
  --shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.16);
}
```

### 5.2 层级系统 (Z-Index)

```css
:root {
  --z-base: 0;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-fixed: 300;
  --z-modal-backdrop: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
  --z-toast: 800;
}
```

---

## 6. 组件设计规范

### 6.1 按钮 (Button)

#### 视觉规范

```css
/* 基础按钮 */
.button {
  height: 40px;
  padding: 0 16px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

/* 主要按钮 */
.button-primary {
  background: var(--color-accent);
  color: #FFFFFF;
  border: none;
}

.button-primary:hover {
  opacity: 0.9;
}

/* 次要按钮 */
.button-secondary {
  background: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.button-secondary:hover {
  background: var(--color-surface);
  border-color: var(--color-border-focus);
}

/* 幽灵按钮 */
.button-ghost {
  background: transparent;
  color: var(--color-text-secondary);
  border: none;
}

.button-ghost:hover {
  background: var(--color-surface);
  color: var(--color-text-primary);
}
```

#### 尺寸变体

| 尺寸 | 高度 | 内边距 | 字号 |
|------|------|--------|------|
| Small | 32px | 12px | 13px |
| Medium | 40px | 16px | 14px |
| Large | 48px | 20px | 16px |

### 6.2 输入框 (Input)

```css
.input {
  height: 40px;
  padding: 0 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-canvas);
  font-size: 14px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.06);
}

.input::placeholder {
  color: var(--color-text-muted);
}
```

### 6.3 卡片 (Card)

```css
.card {
  background: var(--color-canvas);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: var(--shadow-sm);
}

/* 卡片标题 */
.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}

/* 卡片内容 */
.card-content {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.6;
}
```

### 6.4 模态框 (Modal)

```css
/* 背景遮罩 */
.modal-backdrop {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
}

/* 模态框主体 */
.modal {
  background: var(--color-canvas);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  max-width: 480px;
  width: 90%;
  padding: var(--space-6);
}

/* 模态框标题 */
.modal-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: var(--space-4);
}
```

### 6.5 Toast 通知

```css
.toast {
  background: var(--color-text-primary);
  color: var(--color-canvas);
  padding: 12px 16px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  font-size: 14px;
  min-width: 200px;
}
```

---

## 7. 动效规范

### 7.1 过渡时间

```css
:root {
  --duration-instant: 0ms;
  --duration-fast: 100ms;    /* 微交互：hover、focus */
  --duration-normal: 200ms;  /* 常规过渡：颜色、透明度 */
  --duration-slow: 300ms;    /* 布局变化：展开、收起 */
  --duration-slower: 500ms;  /* 大范围动画：页面切换 */
}
```

### 7.2 缓动函数

```css
:root {
  /* 标准缓动 - 大多数场景 */
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* 进入缓动 - 元素出现 */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  
  /* 退出缓动 - 元素消失 */
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  
  /* 弹性缓动 - 强调效果 */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### 7.3 常用动效模式

#### 淡入淡出

```css
/* 元素进入 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn var(--duration-normal) var(--ease-out);
}
```

#### 侧边栏滑动

```css
/* 展开 */
.sidebar {
  width: 260px;
  transition: width var(--duration-slow) var(--ease-default);
}

/* 收起 */
.sidebar.collapsed {
  width: 64px;
}
```

#### 骨架屏微光效果

```css
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface) 25%,
    #F0F0F0 50%,
    var(--color-surface) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-md);
}
```

### 7.4 动效使用原则

| 原则 | 描述 |
|------|------|
| **有意义** | 动效应传达信息，而非装饰 |
| **快速响应** | 交互反馈应在 100ms 内 |
| **不阻塞** | 动画不应阻止用户操作 |
| **可预测** | 相同操作产生相同动效 |
| **减少干扰** | 避免同时播放多个动画 |

---

## 8. 布局结构

### 8.1 双栏可调布局

```
┌─────────────────────────────────────────────────────┐
│  [Sidebar]          │         [Main Panel]         │
│                     │                               │
│  ┌───────────────┐  │  ┌─────────────────────────┐ │
│  │ App Header    │  │  │ Tab Bar                 │ │
│  ├───────────────┤  │  ├─────────────────────────┤ │
│  │               │  │  │                         │ │
│  │ Primary       │  │  │                         │ │
│  │ Actions       │  │  │     Content Area        │ │
│  │               │  │  │                         │ │
│  ├───────────────┤  │  │                         │ │
│  │               │  │  │                         │ │
│  │ History       │  │  │                         │ │
│  │ (Scrollable)  │  │  │                         │ │
│  │               │  │  │                         │ │
│  ├───────────────┤  │  └─────────────────────────┘ │
│  │ Footer        │  │                               │
│  └───────────────┘  │                               │
└─────────────────────────────────────────────────────┘
```

### 8.2 侧边栏规范

| 状态 | 宽度 | 内容显示 |
|------|------|----------|
| 展开 | 260px | 图标 + 文字 |
| 收起 | 64px | 仅图标 |

- **背景色：** `#FAFAFA`
- **过渡动画：** `width 300ms ease`
- **分隔线：** 右侧 1px `#E5E7EB`

### 8.3 主面板规范

- **背景色：** `#FFFFFF`
- **标签栏高度：** 48px
- **内容区内边距：** 24px

---

## 9. 响应式设计

### 9.1 断点定义

```css
:root {
  --breakpoint-sm: 640px;   /* 手机横屏 */
  --breakpoint-md: 768px;   /* 平板竖屏 */
  --breakpoint-lg: 1024px;  /* 平板横屏/小笔记本 */
  --breakpoint-xl: 1280px;  /* 桌面显示器 */
  --breakpoint-2xl: 1536px; /* 大屏显示器 */
}
```

### 9.2 响应式策略

| 断点 | 侧边栏行为 | 布局调整 |
|------|------------|----------|
| < 768px | 隐藏/抽屉式 | 单栏布局 |
| 768px - 1024px | 收起状态 | 双栏布局 |
| > 1024px | 展开状态 | 双栏布局 |

---

## 10. 图标规范

### 10.1 图标风格

- **样式：** 线性图标 (Outline)
- **线宽：** 1.5px - 2px
- **圆角：** 保持一致的圆角风格
- **推荐图标库：** Lucide Icons, Heroicons

### 10.2 图标尺寸

| 场景 | 尺寸 |
|------|------|
| 按钮内图标 | 16px |
| 导航图标 | 20px |
| 功能图标 | 24px |
| 大图标/插图 | 32px+ |

### 10.3 图标颜色

- 默认状态：`--color-text-secondary`
- 悬停状态：`--color-text-primary`
- 激活状态：`--color-accent`
- 禁用状态：`--color-text-muted`

---

## 11. 可访问性 (A11y)

### 11.1 基本要求

- [ ] 所有交互元素可通过键盘访问
- [ ] 焦点状态清晰可见
- [ ] 图片和图标提供 alt 文字
- [ ] 颜色不作为唯一信息传达方式
- [ ] 表单元素关联 label

### 11.2 焦点样式

```css
/* 焦点环 */
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* 移除默认焦点（仅在提供替代方案时） */
:focus:not(:focus-visible) {
  outline: none;
}
```

### 11.3 减少动画偏好

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 12. 加载状态

### 12.1 设计原则

- **避免旋转加载器：** 使用骨架屏或微光效果
- **乐观更新：** 立即反馈用户操作
- **渐进式加载：** 内容逐步显示，避免布局跳动

### 12.2 骨架屏示例

```css
/* 文本骨架 */
.skeleton-text {
  height: 16px;
  border-radius: 4px;
}

/* 标题骨架 */
.skeleton-title {
  height: 24px;
  width: 60%;
  border-radius: 4px;
}

/* 头像骨架 */
.skeleton-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
```

---

## 13. 技术实现建议

### 13.1 推荐技术栈

| 类别 | 推荐方案 | 说明 |
|------|----------|------|
| 框架 | React / Vue 3 / Next.js | 现代化组件框架 |
| 样式 | Tailwind CSS | 实现简洁白色风格的首选 |
| 状态管理 | Zustand / Redux Toolkit | 管理全局状态 |
| 动画库 | Framer Motion / GSAP | 实现精细动效 |
| 图标 | Lucide React / Heroicons | 一致的线性图标 |

### 13.2 目录结构建议

```
/src
  /components
    /ui           # 原子组件：Button, Input, Card
    /layout       # 布局组件：Sidebar, Header, Footer
    /features     # 功能组件：按功能模块划分
  /styles
    /tokens       # 设计令牌：colors, spacing, typography
    /globals      # 全局样式
  /hooks          # 自定义 Hooks
  /utils          # 工具函数
```

### 13.3 CSS 变量组织

建议将设计令牌集中管理：

```css
/* styles/tokens/index.css */
@import './colors.css';
@import './typography.css';
@import './spacing.css';
@import './shadows.css';
@import './animations.css';
```

---

## 附录：快速参考

### 常用值速查

| 属性 | 常用值 |
|------|--------|
| 圆角 | 8px (按钮) / 12px (卡片) |
| 内边距 | 16px / 24px |
| 过渡 | 200ms ease |
| 字号 | 14px (正文) / 16px (标题) |
| 边框 | 1px solid #E5E7EB |
| 阴影 | 0 2px 4px rgba(0,0,0,0.06) |

### Tailwind 类名映射

| 设计令牌 | Tailwind 类 |
|----------|-------------|
| --color-canvas | bg-white |
| --color-surface | bg-gray-50 |
| --color-text-primary | text-neutral-900 |
| --color-text-secondary | text-neutral-500 |
| --color-border | border-gray-200 |
| --radius-md | rounded-lg |
| --shadow-sm | shadow-sm |

---

*本文档为前端设计风格指南，旨在建立统一的视觉语言和交互规范。*

