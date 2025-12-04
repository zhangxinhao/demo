import * as React from "react"

import { cn } from "@/lib/utils"

function Textarea({ className, ...props }: React.ComponentProps<"textarea">) {
  return (
    <textarea
      data-slot="textarea"
      className={cn(
        "flex min-h-[120px] w-full rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-canvas)] px-[var(--space-3)] py-[var(--space-3)] text-[14px] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] transition-all duration-200 focus:outline-none focus:border-[var(--color-accent)] focus:ring-[3px] focus:ring-[rgba(0,0,0,0.06)] disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
    />
  )
}

export { Textarea }
