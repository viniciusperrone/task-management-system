import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { theme } from '@/theme/theme';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Task Management System - Orizon',
  description: 'Gerenciador de Tarefas',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
