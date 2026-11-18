/* PDS Creative free demo lock for VØIDTHORN (3 variants).
   Shared 18 Nov 2026, 6:15pm UK time. After EXPIRES every file in /demos/vt-q8m2x/ returns the "demo ended" page.
   To reopen, move EXPIRES (and sharedAt in client-login.html plus the demo pages). To release the paid site, delete this folder. */
const EXPIRES = Date.parse('2026-11-20T18:15:00Z');
const ended = `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Demo ended</title></head>
<body style="margin:0;min-height:100vh;display:grid;place-items:center;background:#0e1015;color:#eef0f5;font:16px system-ui,sans-serif;text-align:center;padding:24px">
<div><h1 style="font-size:24px;margin:0 0 10px">This free demo has ended</h1><p style="opacity:.75;margin:0">To go ahead with your new website, email pedro.de.sousa@hotmail.co.uk or call 07356 203744.</p></div></body></html>`;
export async function onRequest(context) {
  if (Date.now() >= EXPIRES) {
    return new Response(ended, { status: 410, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'x-robots-tag': 'noindex, nofollow' } });
  }
  const res = await context.next();
  const headers = new Headers(res.headers);
  headers.set('x-robots-tag', 'noindex, nofollow');
  headers.set('cache-control', 'no-store');
  headers.set('content-security-policy', "frame-ancestors 'self'");
  return new Response(res.body, { status: res.status, statusText: res.statusText, headers });
}
