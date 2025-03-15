import type { Metadata } from "next";
import { Geist, Geist_Mono, Press_Start_2P } from "next/font/google";
import Link from "next/link";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const pixelFont = Press_Start_2P({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-pixel",
});

export const metadata: Metadata = {
  title: "Percy",
  description: "Amateur Radio LLM Evaluation Framework",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.className} antialiased`}>
        <nav className="fixed top-0 w-full border-b bg-background">
          <div className="flex h-16 items-center px-4 container mx-auto">
            <div className={`${pixelFont.className} text-2xl mr-8`}><Link href="/">PERCY</Link></div>
            <NavigationMenu>
              <NavigationMenuList>
                <NavigationMenuItem>
                  <NavigationMenuLink asChild>
                    <Link
                      href="/models"
                      className={navigationMenuTriggerStyle()}
                    >
                      Leaderboard
                    </Link>
                  </NavigationMenuLink>
                </NavigationMenuItem>
                <NavigationMenuItem>
                  <NavigationMenuLink asChild>
                    <Link
                      href="/handbook"
                      className={navigationMenuTriggerStyle()}
                    >
                      Handbook
                    </Link>
                  </NavigationMenuLink>
                </NavigationMenuItem>
              </NavigationMenuList>
            </NavigationMenu>
          </div>
        </nav>
        <div className="pt-20 container mx-auto">{children}</div>
        <footer className="mt-16 py-6 border-t">
          <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
            <p>This project is released in the public domain.</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
