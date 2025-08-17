import asyncio
import io
from collections import deque

from core.telemetry_frame import TelemetryFrame


class TimeSeriesBuffer:
    def __init__(self, maxlen: int = None):
        self.contents = deque(maxlen=maxlen)
        self._lock = asyncio.Lock()
        self._subscribers = []

    def subscribe(self, callback: callable):
        """Register a callback (sync or async) to be called when buffer changes."""
        self._subscribers.append(callback)

    def unsubscribe(self, callback: callable):
        self._subscribers.remove(callback)

    def _notify(self):
        for cb in self._subscribers:
            if asyncio.iscoroutinefunction(cb):
                asyncio.create_task(cb())
            else:
                cb()

    def __len__(self):
        return len(self.contents)

    async def __aiter__(self):
        async with self._lock:
            for item in list(self.contents):
                yield item

    async def add(self, frame: TelemetryFrame):
        async with self._lock:
            self.contents.append(frame)
        self._notify()

    async def clear(self):
        async with self._lock:
            self.contents.clear()
        self._notify()

    async def to_list(self) -> list[TelemetryFrame]:
        async with self._lock:
            return list(self.contents)

    async def to_csv(self) -> str:
        async with self._lock:
            output = io.StringIO()
            output.write(TelemetryFrame.csv_header() + "\n")  # Write headers
            for frame in self.contents:
                output.write(frame.to_csv() + "\n")  # Write values (rows)
            return output.getvalue()

    async def add_from_csv(self, csv_string: str):
        lines = csv_string.splitlines()
        async with self._lock:
            for line in lines[1:]:  # Skip headers
                try:
                    frame = TelemetryFrame.from_csv(line)
                    self.contents.append(frame)
                except Exception as e:
                    print(f"Error parsing CSV line: {e}")
        self._notify()
