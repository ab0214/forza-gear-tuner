from core.time_series_buffer import TimeSeriesBuffer
from core.udp_listener import UdpListener
from nicegui import events, ui


class Capture:
    def __init__(self, buffer: TimeSeriesBuffer):
        # Set up capture and buffer
        self.listener = UdpListener()
        self.buffer = buffer
        self.listener.subscribe(self.buffer.add)
        self.listener.subscribe(self.update_frame_count)
        # Title
        ui.label("Capture / Save / Load")
        # Frame count label
        self.frame_count_label = ui.label("Frames: 0")
        self.listener.subscribe(self.update_frame_count)
        # Buttons
        with ui.button_group():
            toggle_button = ui.button(
                "Start", on_click=lambda: self.toggle_capture(toggle_button)
            )
            ui.button("Reset", on_click=self.reset_buffer)
            ui.button("Save", on_click=self.download)
        # JSONL upload
        ui.upload(
            label="Import JSONL file", on_upload=self.load_jsonl, max_files=1
        ).props('accept=".jsonl"')
        self.update_frame_count()

    async def load_jsonl(self, e: events.UploadEventArguments):
        try:
            text = await e.file.text()
            await self.buffer.load_jsonl(text)
        except Exception as e:
            error_msg = f"Error loading JSONL: {e}"
            print(error_msg)
            ui.notify(error_msg, color="red")
        finally:
            self.update_frame_count()

    def update_frame_count(self, _=None):
        count = len(self.buffer)
        self.frame_count_label.text = f"Frames: {count}"

    async def toggle_capture(self, button):
        if self.listener.running:
            await self.listener.stop()
            button.text = "Start"
            button.props('color="blue"')
            self.buffer._notify()  # Ensure UI updates with any final frames
        else:
            await self.listener.start()
            button.text = "Stop"
            button.props('color="red"')

    async def reset_buffer(self):
        await self.buffer.clear()
        self.update_frame_count()

    async def download(self):
        jsonl = await self.buffer.to_jsonl()
        ui.download(src=bytes(jsonl, "utf-8"), filename="telemetry.jsonl")
