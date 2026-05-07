import asyncio
import inspect
from collections import deque

from core.telemetry_frame import TelemetryFrame


class TimeSeriesBuffer:
    """A thread-safe buffer for storing telemetry frames."""

    # Magic methods

    def __init__(self, maxlen: int = None):
        """
        Initialize the buffer with an optional maximum length.
        If maxlen is specified, the buffer will behave like a circular buffer.
        """
        self.contents = deque(maxlen=maxlen)
        self._lock = asyncio.Lock()
        self._subscribers = []

    def __len__(self):
        """Return the number of items in the buffer."""
        return len(self.contents)

    async def __aiter__(self):
        """Asynchronous iterator to iterate over the buffer contents."""
        async with self._lock:
            for item in list(self.contents):
                yield item

    # Subscriber management

    def subscribe(self, callback: callable):
        """Register a (sync or async) callback to be called when the buffer changes."""
        self._subscribers.append(callback)

    def unsubscribe(self, callback: callable):
        """Unregister a callback."""
        self._subscribers.remove(callback)

    def _notify(self):
        """Notify all subscribers about a change in the buffer."""
        for cb in self._subscribers:
            if inspect.iscoroutinefunction(cb):
                asyncio.create_task(cb())
            else:
                cb()

    # Buffer operations

    async def add(self, frame: TelemetryFrame):
        """Add a TelemetryFrame to the buffer."""
        async with self._lock:
            self.contents.append(frame)
        self._notify()

    async def clear(self):
        """Clear the buffer."""
        async with self._lock:
            self.contents.clear()
        self._notify()

    # Data export

    async def to_list(self) -> list[TelemetryFrame]:
        """Return the buffer contents as a list."""
        async with self._lock:
            return list(self.contents)

    async def to_jsonl(self) -> str:
        """Convert the buffer contents to JSONL (JSON Lines) formatted string."""
        async with self._lock:
            lines = [frame.model_dump_json() for frame in self.contents]
            return "\n".join(lines)

    # Data import

    async def load_file(self, file_path: str, clear: bool = True):
        """
        Load JSONL file
        Args:
            file_path (str): Path to the JSONL file.
            clear (bool): Whether to clear the buffer before loading new data.
        """
        with open(file_path, "r") as file:
            jsonl = file.read()
        await self.load_jsonl(jsonl, clear)

    async def load_jsonl(self, jsonl: str, clear: bool = True):
        """
        Load JSONL formatted data from one or more lines of text.
        Args:
            jsonl (str): JSONL string to parse.
            clear (bool): Whether to clear the buffer before loading new data.
        """
        if clear:
            await self.clear()
        lines = jsonl.strip().splitlines()
        async with self._lock:
            for i, line in enumerate(lines):
                if not line.strip():
                    continue
                try:
                    frame = TelemetryFrame.model_validate_json(line)
                    self.contents.append(frame)
                except Exception as e:
                    print(f"Error parsing line {i}: {e}")
        self._notify()
