from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import time

# Initialize camera and set video configuration
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

# Setup H.264 encoder
encoder = H264Encoder(bitrate=2_000_000)

# Start camera
picam2.start()
print("🎥 Recording started...")

# Start recording (encoder object, output file)
picam2.start_recording(encoder, "video_test.h264")

# Record for 5 seconds
time.sleep(5)

# Stop recording and camera
picam2.stop_recording()
picam2.stop()
print("✅ Recording complete. File saved as video_test.h264")

