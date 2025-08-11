import asyncio
import io
from collections import deque

from core.telemetry_frame import TelemetryFrame


class TimeSeriesBuffer:
    def __init__(self, maxlen=None):
        self.buffer = deque(maxlen=maxlen)
        self.lock = asyncio.Lock()
        self._subscribers = []

    def subscribe(self, callback):
        """Register a callback (sync or async) to be called when buffer changes."""
        self._subscribers.append(callback)

    def unsubscribe(self, callback):
        self._subscribers.remove(callback)

    def _notify(self):
        for cb in self._subscribers:
            if asyncio.iscoroutinefunction(cb):
                asyncio.create_task(cb())
            else:
                cb()

    async def __aiter__(self):
        async with self.lock:
            for item in list(self.buffer):
                yield item

    async def add(self, frame):
        async with self.lock:
            self.buffer.append(frame)
        self._notify()

    async def clear(self):
        async with self.lock:
            self.buffer.clear()
        self._notify()

    async def to_list(self):
        async with self.lock:
            return list(self.buffer)

    async def to_csv(self):
        async with self.lock:
            output = io.StringIO()
            output.write(TelemetryFrame.csv_header() + "\n")  # Write headers
            for frame in self.buffer:
                output.write(frame.to_csv() + "\n")  # Write values (rows)
            return output.getvalue()

    async def add_from_csv(self, csv_string):
        lines = csv_string.splitlines()
        async with self.lock:
            for line in lines[1:]:  # Skip headers
                try:
                    frame = TelemetryFrame.from_csv(line)
                    self.buffer.append(frame)
                except Exception as e:
                    print(f"Error parsing CSV line: {e}")
        self._notify()
