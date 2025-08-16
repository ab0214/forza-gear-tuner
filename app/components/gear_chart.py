from nicegui import ui


class GearChart:
    def __init__(self, buffer=None):
        self.buffer = buffer

        # Example data for the line graph
        x_data = [1, 2, 3, 4, 5]
        y_data = [2, 4, 1, 8, 7]

        ui.label("Gear Chart")
        self.plot_container = ui.column()
        with self.plot_container:
            self.line_plot = ui.line_plot(
                n=1, limit=200, update_every=1, figsize=(6, 4)
            )
            self.line_plot.with_legend(["Gear"], loc="upper center", ncol=1)
            self.line_plot.push(x=x_data, Y=[y_data])

        ui.button("Update", on_click=self.update)

    async def update(self):
        min_rpm = 1500
        max_rpm = 8000

        async for frame in self.buffer:
            if frame.IdleRPM and frame.MaxRPM:
                min_rpm = frame.IdleRPM
                max_rpm = frame.MaxRPM
                break

        self.line_plot.delete()
        with self.plot_container:
            self.line_plot = ui.line_plot(
                n=3, limit=200, update_every=1, figsize=(6, 4)
            )
        self.line_plot.with_legend(range(1, 7), loc="upper center", ncol=1)
        x = [0, 40, 40, 80, 80, 120]
        y = [
            [1500, 8000, 0, 0, 0, 0],
            [0, 0, 3000, 8000, 0, 0],
            [0, 0, 0, 0, 5000, 8000],
        ]
        self.line_plot.push(x, y)
