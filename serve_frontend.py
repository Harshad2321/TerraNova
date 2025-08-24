#!/usr/bin/env python3
"""
Simple HTTP server to serve the TerraNova frontend
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from threading import Timer

PORT = 3000
DIRECTORY = "frontend"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def open_browser():
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 Serving TerraNova frontend at http://localhost:{PORT}")
        print(f"📁 Directory: {os.path.abspath(DIRECTORY)}")
        print("🔄 Make sure the backend is running on http://127.0.0.1:8000")
        print("📝 Press Ctrl+C to stop the server")
        print()
        
        # Open browser after a short delay
        Timer(1.0, open_browser).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            sys.exit(0)
