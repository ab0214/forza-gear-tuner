from typing import cast

import plotly
import plotly.graph_objs as go
from nicegui import ui

from utils.gear_ratio import (
    analyze_rpm_to_kmh_ratios,
    get_engine_idle_rpm,
    get_engine_max_rpm,
)


class GearChart:
    def __init__(self, buffer):
        self.buffer = buffer
        self.buffer.subscribe(self.update_chart)

        ui.label("Gear Chart")
        fig = go.Figure()
        fig.update_layout(
            xaxis=dict(title="Speed (km/h)", rangemode="tozero"),
            yaxis=dict(title="Engine RPM", rangemode="tozero"),
            # title="Gear Chart",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
            ),
            template="plotly_dark",
            margin=dict(l=40, r=40, t=40, b=40),
        )
        self.chart = ui.plotly(fig)
        self.update_chart()

    def update_chart(self):
        tfs = list(self.buffer.contents)
        ratios = analyze_rpm_to_kmh_ratios(tfs)
        min_rpm = get_engine_idle_rpm(tfs)
        max_rpm = get_engine_max_rpm(tfs)

        colors = plotly.colors.DEFAULT_PLOTLY_COLORS
        fig: go.Figure = cast(go.Figure, self.chart.figure)
        fig.data = ()
        fig.layout.shapes = ()
        for i in range(1, len(ratios)):
            color = colors[(i - 1) % len(colors)]
            # Add line for each gear
            start_x = max_rpm * ratios[i - 1] if i > 1 else min_rpm * ratios[i]
            end_x = max_rpm * ratios[i]
            start_y = start_x / ratios[i]
            end_y = end_x / ratios[i]
            fig.add_trace(
                go.Scatter(
                    x=[start_x, end_x],
                    y=[start_y, end_y],
                    mode="lines",
                    name=f"Gear {i}",
                    line=dict(color=color, width=3),
                )
            )
            # Dashed line for unused range of the gear
            fig.add_shape(
                type="line",
                x0=min_rpm * ratios[i],
                x1=start_x,
                y0=min_rpm,
                y1=start_y,
                line=dict(color=color, dash="dot"),
                opacity=0.5,
            )
        ui.update(self.chart)
