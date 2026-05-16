import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Keiba Prediction",
  description: "LightGBM & Gemini Hybrid Prediction",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
