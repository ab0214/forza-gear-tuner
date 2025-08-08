from nicegui import ui


class DynoChart:
    def __init__(self):
        # Example data for the line graph
        x_data = [1, 2, 3, 4, 5]
        y_data = [2, 4, 1, 8, 7]

        ui.label('Example Line Graph')
        self.line_plot = ui.line_plot(
            n=1,
            limit=200,
            update_every=1,
            figsize=(6, 4)
        )
        self.line_plot.with_legend(['label'], loc='upper center', ncol=1)
        self.line_plot.push(x=x_data, Y=[y_data])
