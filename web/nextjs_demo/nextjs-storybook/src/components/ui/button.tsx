import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-[var(--radius-md)] text-[14px] font-medium transition-all duration-200 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-accent)]",
  {
    variants: {
      variant: {
        default:
          "bg-[var(--color-accent)] text-white hover:opacity-90 active:scale-[0.98]",
        destructive:
          "bg-[var(--color-error)] text-white hover:opacity-90 active:scale-[0.98]",
        outline:
          "border border-[var(--color-border)] bg-transparent text-[var(--color-text-primary)] hover:bg-[var(--color-surface)] hover:border-[var(--color-border-focus)]",
        secondary:
          "bg-[var(--color-surface)] text-[var(--color-text-primary)] hover:bg-[var(--color-surface-hover)]",
        ghost:
          "bg-transparent text-[var(--color-text-secondary)] hover:bg-[var(--color-surface)] hover:text-[var(--color-text-primary)]",
        link: 
          "text-[var(--color-text-primary)] underline-offset-4 hover:underline bg-transparent",
      },
      size: {
        default: "h-[40px] px-[var(--space-4)]",
        sm: "h-[32px] px-[var(--space-3)] text-[13px]",
        lg: "h-[48px] px-[var(--space-5)] text-[16px]",
        icon: "size-[40px]",
        "icon-sm": "size-[32px]",
        "icon-lg": "size-[48px]",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

function Button({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean
  }) {
  const Comp = asChild ? Slot : "button"

  return (
    <Comp
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
