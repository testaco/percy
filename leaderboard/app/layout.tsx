import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Percy - Amateur Radio Test Bot Leaderboard",
  description: "Performance analysis of LLMs on amateur radio license exams",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={cn(
          geistSans.variable,
          geistMono.variable,
          "min-h-screen bg-background antialiased"
        )}
      >
        <div className="relative flex min-h-screen flex-col">
          <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-14 items-center">
              <div className="mr-4 flex">
                <a className="mr-6 flex items-center space-x-2" href="/">
                  <span className="font-bold">Percy</span>
                </a>
              </div>
              <nav className="flex items-center space-x-6 text-sm font-medium">
                <a className="transition-colors hover:text-foreground/80" href="/leaderboard">Leaderboard</a>
                <a className="transition-colors hover:text-foreground/80" href="/evaluations">Evaluations</a>
              </nav>
            </div>
          </header>
          <div className="flex-1">
            <div className="container">
              {children}
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}
