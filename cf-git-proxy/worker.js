/**
 * Cloudflare Worker: GitHub Git Push Proxy
 * 
 * Purpose: Reverse-proxy GitHub's smart HTTP transport so git push works
 * from China without VPN. Routes through Cloudflare's global network.
 * 
 * Bound to: git.tcmway.org
 * Usage: git remote set-url origin https://git.tcmway.org/Fauntleroy-Z/tcmway.git
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Only allow POST/GET (git smart HTTP uses these)
    const method = request.method;
    if (!['GET', 'POST'].includes(method)) {
      return new Response('Method not allowed', { status: 405 });
    }

    // Build the target GitHub URL
    const githubUrl = `https://github.com${url.pathname}${url.search}`;

    // Clone the request headers, removing CF-specific ones
    const headers = new Headers(request.headers);
    headers.delete('host');
    headers.delete('cf-connecting-ip');
    headers.delete('cf-ipcountry');
    headers.delete('cf-ray');
    headers.delete('cf-visitor');
    headers.delete('cf-worker');
    headers.delete('forwarded');
    headers.delete('x-forwarded-for');
    headers.delete('x-forwarded-proto');
    headers.delete('x-real-ip');

    // Forward the request to GitHub
    try {
      const response = await fetch(githubUrl, {
        method: method,
        headers: headers,
        body: request.body,
      });

      // Clone response headers back, removing hop-by-hop headers
      const respHeaders = new Headers(response.headers);
      respHeaders.delete('transfer-encoding');
      respHeaders.delete('connection');
      respHeaders.set('access-control-allow-origin', '*');

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: respHeaders,
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: 'Proxy error', message: err.message }), {
        status: 502,
        headers: { 'content-type': 'application/json' },
      });
    }
  },
};
