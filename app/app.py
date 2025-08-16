import asyncio
from nicegui import ui

# from components.dyno_chart import DynoChart
from components.capture import Capture
from components.gear_chart import GearChart
from components.gears import Gears
from components.inspector import Inspector
from core.time_series_buffer import TimeSeriesBuffer


# Create a shared buffer
shared_buffer = TimeSeriesBuffer()
# Load data for testing purposes
with open("data/telemetry.csv") as file:
    csv_data = file.read()
asyncio.run(shared_buffer.add_from_csv(csv_data))

# Pass the shared buffer to all components
with ui.row():
    for component_cls in (Capture, Gears, GearChart, Inspector):
        with ui.card():
            component_cls(buffer=shared_buffer)

ui.run()
