import socket
from TelemetryFrame import TelemetryFrame as tf

UDP_IP = "0.0.0.0"     # Listen on all interfaces
UDP_PORT = 5300        # Match this in FH5 "Data Out" settings

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for FH5 telemetry on port {UDP_PORT}...")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received {len(data)} bytes from {addr}")
        frame = tf.from_packet(data)
        print(frame)
except KeyboardInterrupt:
    print("\nStopped.")
finally:
    sock.close()
