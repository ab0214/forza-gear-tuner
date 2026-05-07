from nicegui import ui

import pandas as pd
import numpy as np
from scipy import stats
from scipy.interpolate import interp1d
import plotly.graph_objects as go

from core.time_series_buffer import TimeSeriesBuffer


class DynoChart:
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

        ui.label("Dyno Chart")
        fig = go.Figure(
            [
                go.Scatter(
                    name="Power (kW)",
                    mode="lines",
                    line=dict(color="#ffe246", width=3, shape="spline"),
                ),
                go.Scatter(
                    name="Torque (Nm)",
                    mode="lines",
                    yaxis="y2",
                    line=dict(color="#ed2884", width=3, shape="spline"),
                ),
            ]
        )
        fig.update_layout(
            xaxis=dict(
                title="Engine RPM",
                # rangemode="tozero",
            ),
            yaxis=dict(title="Power (kW)", rangemode="tozero"),
            yaxis2=dict(
                title="Torque (Nm)", rangemode="tozero", overlaying="y", side="right"
            ),
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
        thing = do_thing(self.buffer)
        self.chart.figure.data[0].x = thing["rpm"]
        self.chart.figure.data[0].y = thing["power"]
        self.chart.figure.data[1].x = thing["rpm"]
        self.chart.figure.data[1].y = thing["torque"]
        ui.update(self.chart)


def do_thing(buffer: TimeSeriesBuffer):
    # Convert buffer to dataframe with only needed fields
    powercurve = pd.DataFrame(
        [
            {
                "rpm": frame.rpm,
                "torque": frame.torque,
                "power": frame.power / 1000,
            }
            for frame in buffer.contents
            if frame.throttle == 255
        ],
        columns=["rpm", "torque", "power"],
    )

    # Filter NA and outliers
    powercurve.dropna(inplace=True)
    if len(powercurve) > 0:
        z = np.abs(stats.zscore(powercurve, nan_policy="omit"))
        not_outlier = (z < 4).all(axis=1)
        powercurve = powercurve[not_outlier]

    # Sort
    powercurve = powercurve.sort_values(by="rpm")

    # Filter noisy data
    window_size = 10  # Adjust the window size as per your preference
    for name, values in powercurve.items():
        smoothed = values.rolling(window_size).max()
        powercurve[name] = smoothed

    powercurve.dropna(inplace=True)
    powercurve.drop_duplicates(subset=["rpm"], inplace=True)
    powercurve.sort_values(by="rpm", inplace=True, ignore_index=True)

    # resample and interpolate
    if len(powercurve) > 1:
        f_power = interp1d(
            powercurve["rpm"],
            powercurve["power"],
            kind="linear",
            fill_value="extrapolate",
        )
        f_torque = interp1d(
            powercurve["rpm"],
            powercurve["torque"],
            kind="linear",
            fill_value="extrapolate",
        )
        new_rpm = np.linspace(powercurve["rpm"].min(), powercurve["rpm"].max(), 100)
        powercurve = pd.DataFrame(
            {"rpm": new_rpm, "power": f_power(new_rpm), "torque": f_torque(new_rpm)}
        )

    return powercurve
