"use client";

import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function About() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-[var(--space-8)] animate-fadeIn">
      {/* Content Card */}
      <div className="w-full max-w-[480px] bg-[var(--color-canvas)] border border-[var(--color-border)] rounded-[var(--radius-lg)] p-[var(--space-8)] text-center transition-shadow duration-200 hover:shadow-[var(--shadow-sm)]">
        {/* Header */}
        <h1 
          className="text-[28px] font-semibold tracking-[-0.02em] text-[var(--color-text-primary)] mb-[var(--space-4)]"
          style={{ lineHeight: 1.3 }}
        >
          关于
        </h1>
        
        {/* Description */}
        <p className="text-[16px] text-[var(--color-text-secondary)] leading-relaxed mb-[var(--space-8)]">
          这是一个关于页面，展示了 Next.js 的路由功能。
          <br />
          整体设计遵循极简主义风格指南。
        </p>

        {/* Features */}
        <div className="flex flex-col gap-[var(--space-3)] mb-[var(--space-8)]">
          <div className="flex items-center gap-[var(--space-3)] p-[var(--space-3)] rounded-[var(--radius-md)] bg-[var(--color-surface)]">
            <span className="w-2 h-2 rounded-full bg-[var(--color-success)]" />
            <span className="text-[14px] text-[var(--color-text-primary)]">简约设计</span>
          </div>
          <div className="flex items-center gap-[var(--space-3)] p-[var(--space-3)] rounded-[var(--radius-md)] bg-[var(--color-surface)]">
            <span className="w-2 h-2 rounded-full bg-[var(--color-success)]" />
            <span className="text-[14px] text-[var(--color-text-primary)]">响应式布局</span>
          </div>
          <div className="flex items-center gap-[var(--space-3)] p-[var(--space-3)] rounded-[var(--radius-md)] bg-[var(--color-surface)]">
            <span className="w-2 h-2 rounded-full bg-[var(--color-success)]" />
            <span className="text-[14px] text-[var(--color-text-primary)]">流畅动效</span>
          </div>
        </div>

        {/* Back Button */}
        <Link href="/">
          <Button variant="outline" className="w-full">
            ← 返回首页
          </Button>
        </Link>
      </div>

      {/* Footer */}
      <footer className="mt-[var(--space-10)] text-center">
        <p className="text-[12px] text-[var(--color-text-muted)]">
          基于 Next.js 构建 · 遵循极简设计风格指南
        </p>
      </footer>
    </main>
  );
}
