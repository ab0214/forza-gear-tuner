from components.capture import Capture
from components.dyno_chart import DynoChart
from components.gears import Gears
from nicegui import ui

with ui.row():
    for component in (Capture, Gears, DynoChart):
        with ui.card():
            component()

ui.run()
