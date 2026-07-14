import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Prospect Portal",
  description: "Public lead intake and internal attorney workflow",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
