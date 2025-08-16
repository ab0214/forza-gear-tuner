from dataclasses import fields
from nicegui import ui
from core.telemetry_frame import TelemetryFrame


class Inspector:
    def __init__(self, buffer=None):
        self.buffer = buffer

        self.selected_frame = None
        self.selected_field = None
        self.selected_value = None

        ui.label("Inspector")

        self.playhead_container = ui.grid(columns="200px")
        with self.playhead_container:
            self.playhead = ui.slider(
                min=0.0,
                max=1.0,
                value=1.0,
                step=0.000001,
                on_change=self.select_frame,
            )

        field_names = [f.name for f in fields(TelemetryFrame)]
        self.field_dropdown = ui.select(
            field_names, value=field_names[0], on_change=self.select_field
        )
        self.value_label = ui.label("N/A")
        ui.button("Refresh", on_click=self.update)

    def update(self):
        # self.select_frame(self.playhead.value)
        # self.select_field(self.field_dropdown.value)
        self.update_value_label()

    def update_value_label(self):
        if self.selected_frame and self.selected_field:
            self.value_label.text = str(
                getattr(self.selected_frame, self.selected_field, "N/A")
            )
        else:
            self.value_label.text = "N/A"

    def select_frame(self, e):
        if not self.buffer or len(self.buffer.buffer) == 0:
            self.selected_frame = None
            self.update_value_label()
            return

        position = e.value
        if position == 1.0:
            index = -1
        else:
            index = int((len(self.buffer.buffer) - 0.5) * position)
        self.selected_frame = self.buffer.buffer[index]
        self.update_value_label()

    def select_field(self, e):
        field_name = e.value
        self.selected_field = field_name
        self.update_value_label()
