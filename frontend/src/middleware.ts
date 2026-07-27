import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('access_token')?.value;
  const { pathname } = request.nextUrl;

  if (pathname === '/') {
    if (token) {
      return NextResponse.redirect(new URL('/kanban', request.url));
    }
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if (pathname.startsWith('/kanban') && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if ((pathname.startsWith('/login') || pathname.startsWith('/register')) && token) {
    return NextResponse.redirect(new URL('/kanban', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/', '/kanban/:path*', '/login', '/register'],
};