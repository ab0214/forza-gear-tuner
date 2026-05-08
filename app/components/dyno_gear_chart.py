from typing import cast

import plotly
import plotly.graph_objects as go
from nicegui import ui

from components.dyno_chart import do_thing
from core.time_series_buffer import TimeSeriesBuffer
from utils import gear_ratio


class DynoGearChart:
    def __init__(self, buffer: TimeSeriesBuffer) -> None:
        self.buffer = buffer
        self.buffer.subscribe(self.update_chart)

        ui.label("Dyno Gear Chart Thing")
        fig = go.Figure()
        fig.update_layout(
            xaxis_title="Speed (km/h)",
            yaxis_title="Power (kW)",
            template="plotly_dark",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
            ),
            margin=dict(l=40, r=40, t=40, b=40),
        )
        self.chart = ui.plotly(fig)
        self.update_chart()

    def update_chart(self):
        """Update the chart with current buffer data"""
        frames = list(self.buffer.contents)
        ratios = gear_ratio.analyze_rpm_to_kmh_ratios(frames)
        thing = do_thing(self.buffer)

        colors = plotly.colors.DEFAULT_PLOTLY_COLORS
        fig: go.Figure = cast(go.Figure, self.chart.figure)
        fig.data = ()
        for i in range(1, len(ratios)):
            color = colors[(i - 1) % len(colors)]
            fig.add_trace(
                go.Scatter(
                    x=[rpm * ratios[i] for rpm in thing["rpm"]],
                    y=thing["power"],
                    mode="lines",
                    name=f"Gear {i}",
                    line=dict(color=color),
                )
            )
        ui.update(self.chart)
