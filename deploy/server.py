#!/usr/bin/env python3
"""
Hermes Agent On-Server Web Gateway & Reverse Proxy
Serves chat.html at '/' and proxies '/v1/*' requests to the Hermes Gateway (localhost:8642).
Includes graceful direct OpenRouter fallback and real-time gateway log reporting.
"""

import http.server
import socketserver
import urllib.request
import urllib.error
import json
import os
import sys

PORT = int(os.environ.get("PORT", 10000))
GATEWAY_PORT = int(os.environ.get("HERMES_GATEWAY_PORT", 8642))
API_SERVER_KEY = os.environ.get("API_SERVER_KEY", "").strip()
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()

CHAT_HTML_PATH = os.path.join(os.path.dirname(__file__), "../web/chat.html")
if not os.path.exists(CHAT_HTML_PATH):
    CHAT_HTML_PATH = "/opt/hermes/web/chat.html"

class HermesProxyHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def do_GET(self):
        if self.path in ("/", "/index.html", "/chat.html"):
            self.serve_chat_html()
        elif self.path in ("/healthz", "/health"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"OK")
        elif self.path.startswith("/v1/models"):
            self.handle_models()
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
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"chat.html not found.")

    def handle_models(self):
        # Try local gateway first
        target_url = f"http://127.0.0.1:{GATEWAY_PORT}/v1/models"
        try:
            req = urllib.request.Request(target_url, headers=self.build_forward_headers(), method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = resp.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
                return
        except Exception:
            pass

        # Return standard OpenAI-compatible free models list
        fallback_models = {
            "object": "list",
            "data": [
                {"id": "openrouter/free", "object": "model", "owned_by": "hermes-agent"},
                {"id": "meta-llama/llama-3.3-70b-instruct:free", "object": "model", "owned_by": "meta"},
                {"id": "google/gemini-2.0-flash-exp:free", "object": "model", "owned_by": "google"},
                {"id": "deepseek/deepseek-r1:free", "object": "model", "owned_by": "deepseek"},
                {"id": "qwen/qwen-2.5-coder-32b-instruct:free", "object": "model", "owned_by": "qwen"}
            ]
        }
        encoded = json.dumps(fallback_models).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(encoded)

    def build_forward_headers(self):
        headers = {}
        has_auth = False
        for k, v in self.headers.items():
            if k.lower() == "host":
                continue
            if k.lower() == "authorization":
                has_auth = True
                headers[k] = v
            else:
                headers[k] = v

        # Inject configured API_SERVER_KEY if client omitted or sent empty Bearer
        if (not has_auth or headers.get("Authorization") in ("Bearer", "Bearer null", "Bearer undefined")) and API_SERVER_KEY:
            headers["Authorization"] = f"Bearer {API_SERVER_KEY}"

        return headers

    def forward_request(self, method):
        target_url = f"http://127.0.0.1:{GATEWAY_PORT}{self.path}"
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else None

        req_headers = self.build_forward_headers()
        req = urllib.request.Request(target_url, data=post_data, headers=req_headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                self.send_response(response.status)
                for header, value in response.headers.items():
                    if header.lower() not in ("transfer-encoding", "content-length", "access-control-allow-origin"):
                        self.send_header(header, value)
                resp_body = response.read()
                self.send_header("Content-Length", str(len(resp_body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("X-Hermes-Backend", "Local-Gateway")
                self.end_headers()
                self.wfile.write(resp_body)
                return

        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for header, value in e.headers.items():
                if header.lower() not in ("transfer-encoding", "content-length", "access-control-allow-origin"):
                    self.send_header(header, value)
            err_body = e.read()
            self.send_header("Content-Length", str(len(err_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(err_body)
            return

        except Exception as ex:
            print(f"[!] Gateway 127.0.0.1:{GATEWAY_PORT} unreachable: {ex}")

            # Direct OpenRouter Fallback for chat completions if OPENROUTER_API_KEY exists
            if self.path.startswith("/v1/chat/completions") and OPENROUTER_API_KEY and post_data:
                try:
                    print("[*] Attempting direct OpenRouter upstream fallback...")
                    or_url = "https://openrouter.ai/api/v1/chat/completions"
                    or_headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "HTTP-Referer": "https://render.com",
                        "X-Title": "Hermes Agent Render"
                    }
                    or_req = urllib.request.Request(or_url, data=post_data, headers=or_headers, method="POST")
                    with urllib.request.urlopen(or_req, timeout=60) as or_res:
                        self.send_response(or_res.status)
                        for h, v in or_res.headers.items():
                            if h.lower() not in ("transfer-encoding", "content-length", "access-control-allow-origin"):
                                self.send_header(h, v)
                        or_body = or_res.read()
                        self.send_header("Content-Length", str(len(or_body)))
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.send_header("X-Hermes-Backend", "OpenRouter-Fallback")
                        self.end_headers()
                        self.wfile.write(or_body)
                        return
                except Exception as or_err:
                    print(f"[!] OpenRouter fallback failed: {or_err}")

            # If no fallback or fallback failed, return diagnostic JSON
            log_snippet = ""
            for log_file in ("/tmp/hermes-gateway.log", "/opt/data/gateway.log"):
                if os.path.exists(log_file):
                    try:
                        with open(log_file, "r", errors="ignore") as f:
                            lines = f.readlines()
                            log_snippet = "".join(lines[-40:])
                        break
                    except Exception:
                        pass

            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            payload = {
                "error": f"Hermes Gateway unavailable: {str(ex)}",
                "hint": "The internal gateway process is initializing or starting up. If the Render instance recently awoke from cold sleep, please wait 20-30 seconds and retry.",
                "gateway_log": log_snippet or "No gateway logs recorded."
            }
            self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), HermesProxyHandler) as httpd:
        print(f"[*] Hermes Web UI running on http://0.0.0.0:{PORT} (Proxying /v1 to port {GATEWAY_PORT})")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
