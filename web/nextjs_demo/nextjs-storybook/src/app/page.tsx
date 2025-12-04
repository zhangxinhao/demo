import Link from "next/link";
import { Counter } from "@/components/Counter";

export default function Home() {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        gap: "20px",
      }}
    >
      <h1 style={{ fontSize: "24px" }}>Home Page</h1>

      {/* Zustand Counter Example */}
      <Counter />

      {/* Link component for client-side navigation */}
      <Link
        href="/about"
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          backgroundColor: "#0070f3",
          color: "white",
          borderRadius: "4px",
          textDecoration: "none",
        }}
      >
        Go to About Page
      </Link>
    </div>
  );
}
