import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'VentureOS',
  description: 'Launch your business idea with AI agents',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
