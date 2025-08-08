import asyncio
import io
from collections import deque

from core.telemetry_frame import TelemetryFrame


class TimeSeriesBuffer:
    def __init__(self, maxlen=None):
        self.buffer = deque(maxlen=maxlen)
        self.lock = asyncio.Lock()

    async def __aiter__(self):
        async with self.lock:
            for item in list(self.buffer):
                yield item

    async def add(self, frame):
        async with self.lock:
            self.buffer.append(frame)

    async def clear(self):
        async with self.lock:
            self.buffer.clear()

    async def to_list(self):
        async with self.lock:
            return list(self.buffer)

    async def to_csv(self):
        async with self.lock:
            output = io.StringIO()
            # Write headers
            field_names = [
                f.name
                for f in TelemetryFrame.__dataclass_fields__.values()
            ]
            output.write(','.join(field_names) + '\n')
            # Write values
            for frame in self.buffer:
                values = [str(getattr(frame, name)) for name in field_names]
                output.write(','.join(values) + '\n')
            return output.getvalue()

    async def add_from_csv(self, csv_string):
        lines = csv_string.splitlines()
        async with self.lock:
            for line in lines[1:]:  # skip headers
                try:
                    values = line.split(',')
                    frame = TelemetryFrame(*values)
                    # print(f"Adding frame: {frame}")
                    # await buffer.add(frame)
                    self.buffer.append(frame)
                except Exception as e:
                    print(f"Error parsing line: {e}")
