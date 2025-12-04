"use client";
import { useRouter } from "next/navigation";

export default function About() {
  const router = useRouter();

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
      <h1 style={{ fontSize: "24px" }}>About Page</h1>
      <p>This is the about page, demonstrating Next.js routing.</p>
      <button
        onClick={() => router.push("/")}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer",
          backgroundColor: "#0070f3",
          color: "white",
          border: "none",
          borderRadius: "4px",
        }}
      >
        Go Back Home
      </button>
    </div>
  );
}

