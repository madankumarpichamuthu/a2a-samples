#!/usr/bin/env python3
"""
HTTP server that serves the test_client.html and proxies requests to the orchestrator.
This avoids CORS issues.
"""
import http.server
import socketserver
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs
import os

PORT = 8001
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ORCHESTRATOR_URL = "http://localhost:10101"

class ProxyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        # Proxy requests to /api/* to the orchestrator
        if self.path.startswith('/api/'):
            self.proxy_to_orchestrator()
        else:
            super().do_POST()

    def proxy_to_orchestrator(self):
        """Proxy the request to the orchestrator agent"""
        try:
            # Read the request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            # Forward to orchestrator
            req = urllib.request.Request(
                ORCHESTRATOR_URL + '/',
                data=body,
                headers={'Content-Type': 'application/json'}
            )

            with urllib.request.urlopen(req) as response:
                response_data = response.read()

                # Send response back to client
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(response_data)

        except urllib.error.HTTPError as e:
            error_data = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(error_data)

        except Exception as e:
            error_response = json.dumps({
                'error': {
                    'code': -32603,
                    'message': f'Proxy error: {str(e)}'
                }
            }).encode('utf-8')

            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(error_response)

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), ProxyRequestHandler) as httpd:
        print(f"")
        print(f"================================================")
        print(f"  A2A MCP Test Client with Proxy")
        print(f"================================================")
        print(f"")
        print(f"  UI Server:    http://localhost:{PORT}/test_client.html")
        print(f"  Proxy:        http://localhost:{PORT}/api/ -> {ORCHESTRATOR_URL}")
        print(f"")
        print(f"  Press Ctrl+C to stop")
        print(f"================================================")
        print(f"")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
