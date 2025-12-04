"use client";

import { Counter } from "@/components/Counter";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import Link from "next/link";

export default function Home() {
  const [text, setText] = useState("");

  const handleSubmit = () => {
    console.log("Submitted text:", text);
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-[var(--space-8)] animate-fadeIn">
      {/* Header */}
      <header className="text-center mb-[var(--space-12)]">
        <h1 
          className="text-[36px] font-bold tracking-[-0.02em] text-[var(--color-text-primary)] mb-[var(--space-3)]"
          style={{ lineHeight: 1.2 }}
        >
          首页
        </h1>
        <p className="text-[14px] text-[var(--color-text-secondary)]">
          一个极简主义的 Next.js 演示应用
        </p>
      </header>

      {/* Main Card */}
      <div 
        className="w-full max-w-[480px] bg-[var(--color-canvas)] border border-[var(--color-border)] rounded-[var(--radius-lg)] p-[var(--space-6)] transition-shadow duration-200 hover:shadow-[var(--shadow-sm)]"
      >
        <Tabs defaultValue="counter" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-[var(--space-6)]">
            <TabsTrigger value="counter">计数器</TabsTrigger>
            <TabsTrigger value="editor">编辑器</TabsTrigger>
          </TabsList>

          <TabsContent value="counter">
            <div className="flex justify-center py-[var(--space-4)]">
              <Counter />
            </div>
          </TabsContent>

          <TabsContent value="editor">
            <div className="flex flex-col gap-[var(--space-4)]">
              <Textarea
                placeholder="在这里输入文本..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="min-h-[200px] resize-none"
              />
              <Button onClick={handleSubmit} className="w-full">
                提交
              </Button>
            </div>
          </TabsContent>
        </Tabs>
      </div>

      {/* Navigation */}
      <nav className="mt-[var(--space-10)]">
        <Link href="/about">
          <Button variant="ghost" className="text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]">
            了解更多 →
          </Button>
        </Link>
      </nav>
    </main>
  );
}
