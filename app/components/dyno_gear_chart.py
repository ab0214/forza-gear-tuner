from nicegui import ui

import pandas as pd
import numpy as np
import plotly
from scipy import stats
from scipy.interpolate import interp1d
import plotly.graph_objects as go

from components.dyno_chart import do_thing
from utils import gear_ratio
from core.time_series_buffer import TimeSeriesBuffer


class DynoGearChart:
    def __init__(self, buffer: TimeSeriesBuffer = None):
        # Example data for the line graph
        # x_data = [1, 2, 3, 4, 5]
        # y_data = [2, 4, 1, 8, 7]

        # ui.label("Example Line Graph")
        # self.line_plot = ui.line_plot(n=1, limit=200, update_every=1, figsize=(6, 4))
        # self.line_plot.with_legend(["label"], loc="upper center", ncol=1)
        # self.line_plot.push(x=x_data, Y=[y_data])

        self.buffer = buffer
        self.chart = None
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
        self.chart.figure.data = ()
        for i in range(1, len(ratios)):
            color = colors[(i - 1) % len(colors)]
            self.chart.figure.add_trace(
                go.Scatter(
                    x=[rpm * ratios[i] for rpm in thing["rpm"]],
                    y=thing["power"],
                    mode="lines",
                    name=f"Gear {i}",
                    line=dict(color=color),
                )
            )
        ui.update(self.chart)
