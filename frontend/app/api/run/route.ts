import { NextRequest } from 'next/server';

const backendUrl = 'https://ventureos-4nga.onrender.com';

export async function POST(req: NextRequest) {
  const { idea } = await req.json();

  const response = await fetch(`${backendUrl}/api/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ idea }),
  });

  if (!response.ok || !response.body) {
    return new Response('Backend error', { status: 500 });
  }

  return new Response(response.body, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
