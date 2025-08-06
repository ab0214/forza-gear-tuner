from nicegui import ui
from components import dyno_chart

with ui.row():
    for component in [dyno_chart, dyno_chart]:
        with ui.card():
            component.create()

ui.run()
