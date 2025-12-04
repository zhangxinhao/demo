import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Next.js Demo",
  description: "A minimalist Next.js application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen bg-[var(--color-canvas)] text-[var(--color-text-primary)] antialiased">
        {children}
      </body>
    </html>
  );
}
