import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title:"KEIBA LAB — 客観データ競馬予測", description:"オッズと人気を使わず、競走能力と条件適性から予測する競馬分析アプリ" };
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="ja"><body>{children}</body></html>}
