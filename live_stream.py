import io
import threading
import http.server
import socketserver
import signal
import sys
from picamera2 import Picamera2
import time

PORT = 8080

# MJPEG Frame Buffer
frame_lock = threading.Lock()
jpeg_bytes = b''

def output_frame():
    with frame_lock:
        return jpeg_bytes

def update_frame_loop(picam2):
    global jpeg_bytes
    stream = io.BytesIO()
    while True:
        stream.seek(0)
        stream.truncate()
        picam2.capture_file(stream, format="jpeg")
        with frame_lock:
            jpeg_bytes = stream.getvalue()

# MJPEG Stream HTTP Handler
class StreamingHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/stream.mjpg':
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
        self.end_headers()

        try:
            while True:
                frame = output_frame()
                self.wfile.write(b'--FRAME\r\n')
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', len(frame))
                self.end_headers()
                self.wfile.write(frame)
                self.wfile.write(b'\r\n')
                time.sleep(0.1)
        except (BrokenPipeError, ConnectionResetError):
            pass

# TCPServer with immediate port reuse
class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

# Start camera
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

# Start frame loop in background thread
threading.Thread(target=update_frame_loop, args=(picam2,), daemon=True).start()

# Create HTTP server
httpd = ReusableTCPServer(("", PORT), StreamingHandler)

# Handle Ctrl+C cleanly
def shutdown_handler(sig, frame):
    print("\n🛑 Ctrl+C received. Shutting down server...")
    httpd.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)

# Start serving
print(f"🌍 MJPEG Live stream available at: http://<your-pi-ip>:{PORT}/stream.mjpg")
httpd.serve_forever(poll_interval=0.05)

