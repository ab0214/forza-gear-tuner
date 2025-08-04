import threading
from collections import deque
import time

class TimeSeriesBuffer:
    def __init__(self, maxlen=10000):
        self.buffer = deque(maxlen=maxlen)
        self.lock = threading.Lock()

    def add(self, frame):
        with self.lock:
            self.buffer.append((time.time(), frame))

    def get_all(self):
        with self.lock:
            return list(self.buffer)
