#!/usr/bin/env python3
import json
import os
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
import psutil


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
            return f"{num:,.0f} {unit}"
        num /= 1024.0
    return f"{num:,.0f} PB"


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/sysinfo':
            info = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'ram_percent': psutil.virtual_memory().percent,
                'mem_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'uptime_seconds': int(time.time() - psutil.boot_time()),
                'timestamp': time.time()
            }
            info['uptime'] = self.format_uptime(info['uptime_seconds'])
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for key, entries in temps.items():
                        if entries:
                            info['cpu_temp'] = entries[0].current
                            break
            except:
                pass
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(info).encode())
            return

        if self.path == '/site-size':
            size_bytes = get_folder_size(os.getcwd())
            size_str = format_bytes(size_bytes)
            # Keep it simple: return plain text like "182 MB"
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(size_str.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(size_str.encode('utf-8'))
            return

        return super().do_GET()

    def format_uptime(self, seconds):
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m {seconds}s"

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8000), Handler)
    print("Serving on port 8000")
    server.serve_forever()