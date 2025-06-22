import http.server
import socketserver
import os
import signal
import sys

PORT = 8080
VIDEO_FILE = "video_test.h264"
MP4_FILE = "video_test.mp4"

# Convert H264 to MP4 if needed
if not os.path.exists(MP4_FILE):
    print("🎞️  Converting to MP4 for browser compatibility...")
    os.system(f"ffmpeg -y -i {VIDEO_FILE} -c:v copy {MP4_FILE}")

# Custom handler with CORS support
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

# Create server
httpd = socketserver.TCPServer(("", PORT), MyHandler)

def shutdown_handler(sig, frame):
    print("\n🛑 Ctrl+C detected. Shutting down server...")
    httpd.shutdown()
    sys.exit(0)

# Bind Ctrl+C to graceful shutdown
signal.signal(signal.SIGINT, shutdown_handler)

# Start server
print(f"🌍 Serving at http://{os.uname()[1]}.local:{PORT}/")
print(f"📺 Access: http://<your-pi-ip>:{PORT}/{MP4_FILE}")
httpd.serve_forever(poll_interval=0.1)

