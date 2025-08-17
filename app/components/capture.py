from core.udp_listener import UdpListener
from nicegui import events, ui


class Capture:
    def __init__(self, buffer=None):
        # Set up capture and buffer
        self.listener = UdpListener()
        self.buffer = buffer  # or TimeSeriesBuffer()
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
        # CSV upload
        ui.upload(label="Import CSV file", on_upload=self.load_csv).props(
            'accept=".csv"'
        )
        self.update_frame_count()

    async def load_csv(self, e: events.UploadEventArguments):
        try:
            await self.buffer.load_string(e.content.read().decode())
        except Exception as e:
            error_msg = f"Error loading CSV: {e}"
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
        else:
            await self.listener.start()
            button.text = "Stop"
            button.props('color="red"')

    async def reset_buffer(self):
        await self.buffer.clear()
        self.update_frame_count()

    async def download(self):
        csv = await self.buffer.to_csv()
        ui.download.content(csv, filename="telemetry.csv")
