import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent.parent / "client"), **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def start_server(port=8000):
    """Start a local development server for the TTS website"""
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 TTS Website Server gestartet!")
            print(f"📍 URL: http://localhost:{port}")
            print(f"📁 Serving files from: {Path(__file__).parent.parent / 'client'}")
            print(f"🛑 Drücken Sie Ctrl+C zum Beenden")
            
            # Automatically open browser
            webbrowser.open(f"http://localhost:{port}")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server wurde beendet.")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Port {port} ist bereits belegt. Versuche Port {port + 1}...")
            start_server(port + 1)
        else:
            print(f"❌ Fehler beim Starten des Servers: {e}")

if __name__ == "__main__":
    start_server()
