from nicegui import ui
from utils import gear_ratio
import math


class Gears:
    # TODO: get reference to telemetry frames from the capture component.

    def __init__(self, buffer=None):
        self.buffer = buffer

        # Title
        ui.label('Gears')
        # Button to analyze gear ratio
        ui.button('Analyze', on_click=self.analyze_gear_ratio)

        # Add label 'Final Drive'
        ui.label('Final Drive')
        # Add slider for final drive ratio
        self.final_drive = 4.0
        self.final_drive_slider = ui.slider(
            min=2.0, max=6.0, value=self.final_drive, step=0.01, on_change=self.update_final_drive)
        # Add and bind label for final drive ratio value
        self.final_drive_label = ui.label(f'{self.final_drive:.2f}')

        # Placeholder for gear sliders
        self.gear_sliders = {}
        self.gear_labels = {}

    def update_final_drive(self, e):
        self.final_drive = e.value
        self.final_drive_label.text = f'{self.final_drive:.2f}'
        # Optionally update gear sliders if needed

    async def analyze_gear_ratio(self):
        frames = await self.buffer.to_list()
        ratios = gear_ratio.analyze_gear_ratios(frames)
        for gear, ratio in ratios.items():
            if gear not in self.gear_sliders:
                self.gear_labels[gear] = ui.label(f'Gear {gear}')
                self.gear_sliders[gear] = ui.slider(
                    min=1.0, max=10.0, value=1.0, step=0.01)
                ui.label(
                    f'Value: {ratio/self.final_drive:.2f}' if ratio and not math.isnan(ratio) else 'N/A')
            else:
                slider = self.gear_sliders[gear]
                slider.value = ratio / \
                    self.final_drive if ratio and not math.isnan(
                        ratio) else 1.0
