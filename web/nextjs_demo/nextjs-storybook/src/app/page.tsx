import Link from "next/link";
import { Counter } from "@/components/Counter";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-8 p-8">
      <h1 className="text-3xl font-bold">Home Page</h1>

      {/* Zustand Counter Example */}
      <Counter />

      {/* shadcn-ui Button Variants Example */}
      <section className="flex flex-col gap-4 items-center">
        <h2 className="text-xl font-semibold">Button Variants</h2>
        <div className="flex flex-wrap gap-3 justify-center">
          <Button variant="default">Default</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="destructive">Destructive</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="link">Link</Button>
        </div>
      </section>

      {/* Button Sizes Example */}
      <section className="flex flex-col gap-4 items-center">
        <h2 className="text-xl font-semibold">Button Sizes</h2>
        <div className="flex flex-wrap gap-3 items-center justify-center">
          <Button size="sm">Small</Button>
          <Button size="default">Default</Button>
          <Button size="lg">Large</Button>
        </div>
      </section>

      {/* Button States Example */}
      <section className="flex flex-col gap-4 items-center">
        <h2 className="text-xl font-semibold">Button States</h2>
        <div className="flex flex-wrap gap-3 justify-center">
          <Button>Normal</Button>
          <Button disabled>Disabled</Button>
        </div>
      </section>

      {/* Link with Button styling */}
      <section className="flex flex-col gap-4 items-center">
        <h2 className="text-xl font-semibold">Navigation</h2>
        <Button asChild>
          <Link href="/about">Go to About Page</Link>
        </Button>
      </section>
    </div>
  );
}
