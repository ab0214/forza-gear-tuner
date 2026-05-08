from typing import cast

import plotly
import plotly.graph_objs as go
from nicegui import ui

from utils.gear_ratio import analyze_rpm_to_kmh_ratios, get_engine_max_rpm


class GearChart:
    def __init__(self, buffer):
        self.buffer = buffer
        self.buffer.subscribe(self.update_chart)

        ui.label("Gear Chart")
        fig = go.Figure()
        fig.update_layout(
            xaxis_title="Speed (km/h)",
            yaxis_title="Engine RPM",
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
        min_rpm = 800
        max_rpm = get_engine_max_rpm(tfs)

        colors = plotly.colors.DEFAULT_PLOTLY_COLORS
        fig: go.Figure = cast(go.Figure, self.chart.figure)
        fig.data = ()
        fig.layout.shapes = ()
        for i in range(1, len(ratios)):
            color = colors[i % len(colors)]
            # Add line for each gear
            fig.add_trace(
                go.Scatter(
                    x=[min_rpm * ratios[i], max_rpm * ratios[i]],
                    y=[min_rpm, max_rpm],
                    mode="lines+markers",
                    name=f"Gear {i}",
                    line=dict(color=color),
                )
            )
            # Vertical line
            if i < len(ratios) - 1:
                speed = max_rpm * ratios[i]
                fig.add_shape(
                    type="line",
                    x0=speed,
                    x1=speed,
                    y0=speed / ratios[i + 1],
                    y1=max_rpm,
                    line=dict(color=color, dash="dot"),
                )
        ui.update(self.chart)
