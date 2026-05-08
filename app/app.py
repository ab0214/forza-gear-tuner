import asyncio

from components.capture import Capture
from components.dyno_chart import DynoChart
from components.dyno_gear_chart import DynoGearChart
from components.gear_chart import GearChart
from components.gears import Gears
from components.inspector import Inspector
from core.time_series_buffer import TimeSeriesBuffer
from nicegui import ui

# Create a shared buffer
shared_buffer = TimeSeriesBuffer()


async def main_page():
    asyncio.create_task(shared_buffer.load_file("data/testdata2.jsonl"))
    with ui.row():
        for component_cls in (
            Capture,
            Gears,
            GearChart,
            DynoChart,
            DynoGearChart,
            Inspector,
        ):
            with ui.card():
                component_cls(buffer=shared_buffer)


ui.page("/")(main_page)
ui.run(fastapi_docs=True, endpoint_documentation="all", dark=True)
