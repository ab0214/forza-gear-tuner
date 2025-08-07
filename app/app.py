from components import dyno_chart
from components.capture import Capture
from nicegui import ui

with ui.row():
    with ui.card():
        Capture()
    with ui.card():
        dyno_chart.create()

ui.run()
