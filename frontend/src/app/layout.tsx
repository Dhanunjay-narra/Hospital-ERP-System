import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ApexCare — Enterprise Hospital ERP & CRM Platform",
  description: "Unified Enterprise Hospital ERP and Patient CRM Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased bg-slate-50 text-slate-900">
        {children}
      </body>
    </html>
  );
}
