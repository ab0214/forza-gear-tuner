from components.capture import Capture

# from components.dyno_chart import DynoChart
from components.gear_chart import GearChart
from components.gears import Gears
from core.time_series_buffer import TimeSeriesBuffer
from nicegui import ui

# Create a shared buffer
shared_buffer = TimeSeriesBuffer()

# Pass the shared buffer to all components
with ui.row():
    for component_cls in (Capture, Gears, GearChart):
        with ui.card():
            component_cls(buffer=shared_buffer)

ui.run()
