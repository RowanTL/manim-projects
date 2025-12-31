from typing import Final

import numpy as np
import polars as pl
from manim import *

GLOBAL_SCALE: Final[float] = 0.50
EWM_FAST_LOOKBACK: Final[int] = 2
EWM_SLOW_LOOKBACK: Final[int] = 8


class WarningScene(Scene):
    def construct(self):
        # Scene construction
        # ...

        # Scene Variables
        warning_text: Text = Text("This is NOT financial advise!", color=RED).scale(
            GLOBAL_SCALE
        )

        # Scene Animations
        self.play(Write(warning_text))
        self.wait(2)
        self.play(Unwrite(warning_text, run_time=0.5))
        self.wait(0.5)


class EwmacScene(MovingCameraScene):
    def construct(self):
        # Scene construction
        # ...

        # Scene Variables
        time_series_df: pl.DataFrame = pl.read_csv("AMD.csv")
        close_series: pl.Series = time_series_df["close.amount"]
        fast_lookback = close_series.ewm_mean(span=EWM_FAST_LOOKBACK)
        slow_lookback = close_series.ewm_mean(span=EWM_SLOW_LOOKBACK)

        ## Convert these to numpy arrays so can be plotted
        close_series = close_series.to_numpy()
        fast_lookback = fast_lookback.to_numpy()
        slow_lookback = slow_lookback.to_numpy()

        max_time = 1000

        axes = Axes(
            x_range=[0, 300, 100],  # Price Range
            y_range=[0, max_time, 100],  # Time Range
            x_length=7,  # Width fits inside frame width (9.0)
            y_length=13,  # Height fits inside frame height (16.0)
            axis_config={
                "color": WHITE,
                "include_numbers": False,  # We will add custom numbers
                "tip_shape": StealthTip,
            },
        ).scale(0.45)

        # Position axes: "L" shape at Bottom-Left of screen
        axes.to_edge(DOWN, buff=1.0).to_edge(LEFT, buff=1.0)

        # Scene Animations
        self.play(
            Create(axes),
            # Write(labels),
            run_time=1.5,
        )

        self.wait(3)
