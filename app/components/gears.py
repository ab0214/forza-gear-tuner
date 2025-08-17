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

        # Grid layout for gear ratio sliders
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

        # Dictionary for keeping track of dynamically created UI elements
        self.grid_contents = {}

    def update_final_drive(self, e):
        # Update the final drive variable and label
        self.final_drive = e.value
        self.final_drive_label.text = f"{self.final_drive:.2f}"
        # Update ratio labels for all gears based on the new final drive
        for _, elements in self.grid_contents.items():
            slider = elements[1]
            ratio_label = elements[2]
            ratio_label.text = f"{slider.value / self.final_drive:.2f}"

    def update_gear_ratio(self, e, label):
        ratio = e.value / self.final_drive
        label.text = f"{ratio:.2f}"

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
            for gear, ratio in enumerate(ratios[1:], start=1):  # Skip 0th gr (reverse)
                label = ui.label(str(gear))  # Gear number

                slider = ui.slider(min=0.1, max=20.0, value=ratio, step=0.01)

                # Ratio label that updates based on the slider value
                ratio_label = ui.label().bind_text_from(
                    slider, "value", backward=lambda v: f"{v / self.final_drive:.2f}"
                )

                # Store the UI elements in the grid_contents dictionary,
                # so we can update/delete them later.
                self.grid_contents[gear] = [label, slider, ratio_label]

    def get_ratios(self):
        return {
            elements[0].text: elements[1].value
            for elements in self.grid_contents.items()
        }

    def get_final_drive(self):
        return self.final_drive
