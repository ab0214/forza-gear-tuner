import plotly
import plotly.graph_objs as go
from nicegui import ui


class GearChart:
    def __init__(self, buffer=None):
        self.buffer = buffer

        ui.label("Gear Chart")
        self.plot_container = ui.column()
        with self.plot_container:
            self.plot = self.draw_plot()

        # ui.button("Update", on_click=self.update)

    def draw_plot(self):
        x = [
            [8, 80],
            [10, 130],
            [16, 160],
            [20, 200],
            [30, 250],
            [40, 300],
        ]
        y = [
            [1500, 8000],
            [1500, 8000],
            [1500, 8000],
            [1500, 8000],
            [1500, 8000],
            [1500, 8000],
        ]

        fig = go.Figure()
        for i in range(len(x)):
            colors = plotly.colors.DEFAULT_PLOTLY_COLORS
            color = colors[i % len(colors)]

            # Add line for each gear
            fig.add_trace(
                go.Scatter(
                    x=x[i],
                    y=y[i],
                    mode="lines+markers",
                    name=f"Gear {i + 1}",
                    line=dict(color=color),
                )
            )

            if i == len(x) - 1:
                break  # No vertical line for last gear

            speed_at_shift = x[i][1]
            if x[i + 1][0] <= speed_at_shift <= x[i + 1][1]:
                x0, x1, y0, y1 = x[i + 1][0], x[i + 1][1], y[i + 1][0], y[i + 1][1]
                delta_x, delta_y = x1 - x0, y1 - y0
                d = delta_y / delta_x if delta_x != 0 else 0
                t = speed_at_shift - x0
                rpm_after_shift = y0 + d * t
            else:
                rpm_after_shift = 0

            # Add dashed vertical line
            fig.add_shape(
                type="line",
                x0=x[i][1],
                x1=x[i][1],
                y0=rpm_after_shift,
                y1=max(y[i]),
                line=dict(color=color, dash="dot"),
            )

        fig.update_layout(
            xaxis_title="MPH",
            yaxis_title="RPM",
            # title="Gear Chart",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
            ),
            template="plotly_dark",
            margin=dict(l=40, r=40, t=40, b=40),
        )

        return ui.plotly(fig)
