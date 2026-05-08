import asyncio

from nicegui import events, ui

from core.telemetry_frame import TelemetryFrame
from core.time_series_buffer import TimeSeriesBuffer


class Capture:
    def __init__(self, buffer: TimeSeriesBuffer):
        self.buffer = buffer
        self.transport = None
        self.buffer.subscribe(self.update_frame_count)

        with ui.row():
            with ui.column():
                ui.label("Capture / Save / Load")
                self.frame_count_label = ui.label("Frames: 0")
                with ui.button_group():
                    toggle_button = ui.button(
                        "Start", on_click=lambda: self.toggle_capture(toggle_button)
                    )
                    ui.button("Reset", on_click=self.reset_buffer)
                    ui.button("Save", on_click=self.download)
            # JSONL upload
            ui.upload(
                label="Import JSONL file",
                on_upload=self.load_jsonl,
                max_files=1,
                auto_upload=True,
                multiple=False,
            ).props('accept=".jsonl"')

    async def load_jsonl(self, upload_event: events.UploadEventArguments):
        try:
            text = await upload_event.file.text()
            await self.buffer.load_jsonl(text)
        except Exception as e:
            error_msg = f"Error loading JSONL: {e}"
            print(error_msg)
            ui.notify(error_msg, color="red")

    def update_frame_count(self, _=None):
        count = len(self.buffer)
        self.frame_count_label.text = f"Frames: {count}"

    async def toggle_capture(self, button):
        if self.transport:
            self.transport.close()
            self.transport = None
            button.text = "Start"
            button.props('color="blue"')
            self.buffer._notify()  # Ensure UI updates with any final frames
        else:
            loop = asyncio.get_running_loop()
            self.transport, _ = await loop.create_datagram_endpoint(
                lambda: TelemetryProtocol(self.buffer), local_addr=("0.0.0.0", 5300)
            )
            button.text = "Stop"
            button.props('color="red"')

    async def reset_buffer(self):
        await self.buffer.clear()

    async def download(self):
        jsonl = await self.buffer.to_jsonl()
        ui.download(src=bytes(jsonl, "utf-8"), filename="telemetry.jsonl")


class TelemetryProtocol(asyncio.DatagramProtocol):
    def __init__(self, buffer: TimeSeriesBuffer, require_race_on=True):
        self.buffer = buffer
        self.require_race_on = require_race_on

    def datagram_received(self, data, addr):
        try:
            tf = TelemetryFrame.model_validate(data)
            if self.require_race_on and not tf.is_race_on:
                return
            asyncio.create_task(self.buffer.add(tf))
        except Exception as e:
            print("Error processing telemetry frame:", e)
