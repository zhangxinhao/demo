'use client'

import { useCounterStore } from '@/store/counterStore'

export function Counter() {
  const { count, increment, decrement, reset } = useCounterStore()

  return (
    <div 
      className="flex flex-col items-center gap-[var(--space-6)] p-[var(--space-6)] rounded-[var(--radius-lg)] bg-[var(--color-surface)] border border-[var(--color-border)]"
    >
      {/* Display */}
      <div className="text-center">
        <span className="text-[var(--color-text-muted)] text-[12px] uppercase tracking-wider">
          当前计数
        </span>
        <h2 
          className="text-[36px] font-bold text-[var(--color-text-primary)] tracking-[-0.02em] mt-[var(--space-1)]"
          style={{ lineHeight: 1.2 }}
        >
          {count}
        </h2>
      </div>

      {/* Controls */}
      <div className="flex gap-[var(--space-2)]">
        {/* Decrement Button */}
        <button
          onClick={decrement}
          className="w-[40px] h-[40px] flex items-center justify-center rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-canvas)] text-[var(--color-text-primary)] font-medium text-[16px] transition-all duration-200 hover:bg-[var(--color-surface-hover)] hover:border-[var(--color-border-focus)] active:scale-95"
          aria-label="Decrement"
        >
          −
        </button>

        {/* Reset Button */}
        <button
          onClick={reset}
          className="h-[40px] px-[var(--space-4)] flex items-center justify-center rounded-[var(--radius-md)] bg-transparent text-[var(--color-text-secondary)] font-medium text-[14px] transition-all duration-200 hover:bg-[var(--color-surface-hover)] hover:text-[var(--color-text-primary)]"
        >
          重置
        </button>

        {/* Increment Button */}
        <button
          onClick={increment}
          className="w-[40px] h-[40px] flex items-center justify-center rounded-[var(--radius-md)] bg-[var(--color-accent)] text-white font-medium text-[16px] transition-all duration-200 hover:opacity-90 active:scale-95"
          aria-label="Increment"
        >
          +
        </button>
      </div>
    </div>
  )
}
