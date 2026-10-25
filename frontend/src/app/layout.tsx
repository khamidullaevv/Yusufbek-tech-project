import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "StroyFix — смета ремонта в Ташкенте",
  description:
    "Бесплатно рассчитайте материалы и стоимость ремонта квартиры по ценам рынков Ташкента.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <body>{children}</body>
    </html>
  );
}
