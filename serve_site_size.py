#!/usr/bin/env python3
"""Serve a single page showing the total size of the current folder.

Run:
    python3 serve_site_size.py

Then open http://localhost:8000
"""

import os
import http.server
import socketserver

PORT = 8000


def get_folder_size(path: str) -> int:
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                if os.path.islink(fp):
                    continue
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total


def format_bytes(num: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            return f"{num:,.2f} {unit}"
        num /= 1024.0
    return f"{num:,.2f} PB"


class SizeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            size = get_folder_size(os.getcwd())
            readable = format_bytes(size)
            html = f"""<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>Website Size</title>
    <style>
      body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 2rem; }}
      .card {{ max-width: 28rem; margin: 0 auto; padding: 2rem; border: 1px solid #ccc; border-radius: 0.5rem; background: #fff; }}
      h1 {{ margin: 0 0 1rem; font-size: 1.5rem; }}
      p {{ margin: 0.25rem 0; }}
      code {{ background: #f5f5f5; padding: 0.15rem 0.35rem; border-radius: 0.25rem; }}
    </style>
  </head>
  <body>
    <div class=\"card\">
      <h1>Website folder size</h1>
      <p><strong>Total size:</strong> <code>{readable}</code></p>
      <p><strong>Path:</strong> <code>{os.getcwd()}</code></p>
    </div>
  </body>
</html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return
        return super().do_GET()


if __name__ == "__main__":
    with socketserver.TCPServer(("127.0.0.1", PORT), SizeHandler) as httpd:
        print(f"Serving folder size on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
            httpd.server_close()
