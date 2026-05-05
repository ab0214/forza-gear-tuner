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


async def main_page():
    asyncio.create_task(shared_buffer.load_file("data/telemetry.csv"))
    with ui.row():
        for component_cls in (Capture, Gears, GearChart, Inspector):
            with ui.card():
                component_cls(buffer=shared_buffer)


ui.page("/")(main_page)
ui.run(fastapi_docs=True, endpoint_documentation="all")
