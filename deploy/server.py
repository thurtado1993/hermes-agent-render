#!/usr/bin/env python3
"""
Hermes Agent On-Server Web Gateway & Reverse Proxy
Serves chat.html at '/' and proxies '/v1/*' requests to the Hermes Gateway (localhost:8642)
"""

import http.server
import socketserver
import urllib.request
import urllib.error
import os
import sys

PORT = int(os.environ.get("PORT", 10000))
GATEWAY_PORT = int(os.environ.get("HERMES_GATEWAY_PORT", 8642))
CHAT_HTML_PATH = os.path.join(os.path.dirname(__file__), "../web/chat.html")
if not os.path.exists(CHAT_HTML_PATH):
    CHAT_HTML_PATH = "/opt/hermes/web/chat.html"

class HermesProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html", "/chat.html"):
            self.serve_chat_html()
        elif self.path == "/healthz" or self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.forward_request("GET")

    def do_POST(self):
        self.forward_request("POST")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def serve_chat_html(self):
        if os.path.exists(CHAT_HTML_PATH):
            with open(CHAT_HTML_PATH, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"chat.html not found.")

    def forward_request(self, method):
        target_url = f"http://127.0.0.1:{GATEWAY_PORT}{self.path}"
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else None

        req_headers = {k: v for k, v in self.headers.items() if k.lower() != "host"}
        req = urllib.request.Request(target_url, data=post_data, headers=req_headers, method=method)

        try:
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for header, value in response.headers.items():
                    if header.lower() not in ("transfer-encoding", "content-length"):
                        self.send_header(header, value)
                resp_body = response.read()
                self.send_header("Content-Length", str(len(resp_body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(resp_body)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for header, value in e.headers.items():
                if header.lower() not in ("transfer-encoding", "content-length"):
                    self.send_header(header, value)
            err_body = e.read()
            self.send_header("Content-Length", str(len(err_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(err_body)
        except Exception as ex:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(f'{{"error": "Gateway unavailable or waking up: {str(ex)}"}}'.encode("utf-8"))

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), HermesProxyHandler) as httpd:
        print(f"[*] Hermes Web UI running on http://0.0.0.0:{PORT} (Proxying /v1 to port {GATEWAY_PORT})")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
