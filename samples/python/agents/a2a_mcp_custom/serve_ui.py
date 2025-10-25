#!/usr/bin/env python3
"""
HTTP server for the A2A MCP test client.

This serves the static `test_client.html` page and proxies API requests to the
orchestrator so the browser never has to make cross-origin calls directly to
the agents.
"""
import http.server
import json
import os
import socketserver
import urllib.error
import urllib.request
from urllib.parse import urljoin

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.getenv('A2A_UI_PORT', '8001'))
ORCHESTRATOR_URL = os.getenv('A2A_ORCHESTRATOR_URL', 'http://localhost:10101')
API_PREFIX = os.getenv('A2A_UI_API_PREFIX', '/api/')


class ProxyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header(
            'Access-Control-Allow-Headers', 'Content-Type, Accept, Authorization'
        )
        super().end_headers()

    def do_OPTIONS(self):
        if self.path.startswith(API_PREFIX):
            self.send_response(200)
            self.end_headers()
            return
        super().do_OPTIONS()

    def do_POST(self):
        if self.path.startswith(API_PREFIX):
            self._proxy_to_orchestrator()
            return
        super().do_POST()

    def _proxy_to_orchestrator(self):
        """Forward the current request body to the orchestrator agent."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            relative_path = self.path[len(API_PREFIX) :]
            upstream_url = urljoin(
                ORCHESTRATOR_URL.rstrip('/') + '/',
                relative_path.lstrip('/'),
            )
            request = urllib.request.Request(
                upstream_url,
                data=body,
                headers={'Content-Type': 'application/json'},
                method='POST',
            )

            with urllib.request.urlopen(request) as response:
                response_body = response.read()
                self.send_response(response.status)
                for header, value in response.headers.items():
                    if header.lower() in {'transfer-encoding'}:
                        continue
                    self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response_body)

        except urllib.error.HTTPError as http_error:
            error_payload = http_error.read()
            self.send_response(http_error.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(error_payload)
        except Exception as exc:  # noqa: BLE001
            error_response = json.dumps(
                {
                    'error': {
                        'code': -32603,
                        'message': f'Proxy error: {exc}',
                    }
                }
            ).encode('utf-8')
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(error_response)


if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), ProxyRequestHandler) as httpd:
        print()
        print('================================================')
        print('  A2A MCP Test Client')
        print('================================================')
        print()
        print(f'  UI Server:    http://localhost:{PORT}/test_client.html')
        print(f'  Proxy:        http://localhost:{PORT}{API_PREFIX} -> {ORCHESTRATOR_URL}')
        print()
        print('  Environment overrides:')
        print('    A2A_UI_PORT             (default: 8001)')
        print('    A2A_ORCHESTRATOR_URL    (default: http://localhost:10101)')
        print('    A2A_UI_API_PREFIX       (default: /api/)')
        print()
        print('  Press Ctrl+C to stop')
        print('================================================')
        print()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nShutting down server...')
