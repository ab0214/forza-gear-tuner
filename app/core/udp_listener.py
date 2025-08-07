import asyncio
import socket

from core.telemetry_frame import TelemetryFrame


class UdpListener:
    def __init__(self, ip="0.0.0.0", port=5300, require_race_on=True):
        self.ip = ip
        self.port = port
        self.require_race_on = require_race_on
        self.subscribers = []
        self.running = False


    async def start(self):
        self.running = True
        self._listen_task = asyncio.create_task(self._listen())

    async def stop(self):
        self.running = False
        if hasattr(self, "_listen_task"):
            await self._listen_task
        if hasattr(self, "sock"):
            self.sock.close()

    def subscribe(self, callback):
        self.subscribers.append(callback)

    async def _listen(self):
        loop = asyncio.get_running_loop()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.sock.bind((self.ip, self.port))
        print(f"Listening for FH5 telemetry on port {self.port}...")
        while self.running:
            try:
                data, _ = await loop.sock_recvfrom(self.sock, 1024)
                tf = TelemetryFrame.from_packet(data)
                if self.require_race_on and tf.IsRaceOn == 0:
                    continue
                for callback in self.subscribers:
                    if asyncio.iscoroutinefunction(callback):
                        asyncio.create_task(callback(tf))
                    else:
                        callback(tf)
            except Exception as e:
                if self.running:
                    print("UDP listener error:", e)
