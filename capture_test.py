from udp_listener import UdpListener
from time_series_buffer import TimeSeriesBuffer

listener = UdpListener()
buffer = TimeSeriesBuffer()

listener.subscribe(buffer.add)

listener.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    listener.stop()
    print("Stored frames:", len(buffer.get_all()))
