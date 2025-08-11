from nicegui import ui
from utils import gear_ratio


class Gears:
    # TODO: get reference to telemetry frames from the capture component.

    def __init__(self, buffer=None):
        self.buffer = buffer

        # Title
        ui.label("Gears")

        # Button to analyze gear ratio
        ui.button("Analyze", on_click=self.analyze_gear_ratio)

        with ui.grid(columns="auto 200px auto") as self.grid:
            ui.label("Final Drive")
            self.final_drive = 4.0
            self.final_drive_slider = ui.slider(
                min=2.0,
                max=6.0,
                value=self.final_drive,
                step=0.01,
                on_change=self.update_final_drive,
            )
            self.final_drive_label = ui.label(f"{self.final_drive:.2f}")

        self.grid_contents = {}

    def update_final_drive(self, e):
        self.final_drive = e.value
        self.final_drive_label.text = f"{self.final_drive:.2f}"

    async def analyze_gear_ratio(self):
        frames = await self.buffer.to_list()
        ratios = gear_ratio.analyze_gear_ratios(frames)

        # Delete previous gear UI elements
        for row in self.grid_contents.values():
            for cell in row:
                cell.delete()
        self.grid_contents.clear()

        # Create UI elements for individual gears
        with self.grid:
            for gear, ratio in ratios.items():
                label = ui.label(str(gear))
                slider = ui.slider(min=1.0, max=10.0, value=1.0, step=0.01)
                ratio_label = ui.label(f"{(ratio / self.final_drive):.2f}")
                self.grid_contents[gear] = [label, slider, ratio_label]
