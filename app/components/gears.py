from nicegui import ui
from utils import gear_ratio


class Gears:
    # TODO: get reference to telemetry frames from the capture component.

    def __init__(self):
        # Title
        ui.label('Gears')
        # Button to analyze gear ratio
        ui.button('Analyze', on_click=self.analyze_gear_ratio)

        # TODO: Add label 'Final Drive'
        # TODO: Add slider for final drive ratio
        # TODO: Add and bind label for final drive ratio value

    async def analyze_gear_ratio(self):
        # TODO: Use utils.gear_ratio to get list of gear ratios.
        # TODO: Add gear number label, slider and value label for each gear.
        # TODO: Set the value of each gear ratio slider to the calculated value,
        # divided by final drive ratio.
        pass
