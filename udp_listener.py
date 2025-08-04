import socket
import threading
from telemetry_frame import TelemetryFrame

class UdpListener:
    def __init__(self, ip="0.0.0.0", port=5300, require_race_on=True):
        self.ip = ip
        self.port = port
        self.require_race_on = require_race_on
        self.subscribers = []
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, "sock"):
            self.sock.close()

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def _listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        print(f"Listening for FH5 telemetry on port {self.port}...")
        while self.running:
            try:
                data, _ = self.sock.recvfrom(1024)
                tf = TelemetryFrame.from_packet(data)
                if self.require_race_on and tf.IsRaceOn == 0:
                    continue
                for callback in self.subscribers:
                    callback(tf)
            except Exception as e:
                if self.running:
                    print("Error:", e)
