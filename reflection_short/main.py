from manim import *
import numpy as np
from typing import Final

SIN_FUNC_SCALING_FACTOR: Final[float] = 0.2
AXES_RANGE: Final[list[int]] = [-4, 4]
GLOBAL_SCALE: Final[float] = 0.45
GLOBAL_RUN_TIME: Final[float] = 0.75


def sin_func(x, y):
    return np.array([x, y, SIN_FUNC_SCALING_FACTOR * np.sin(x**2 + y**2)])


def partial_x(x, y):
    return 2 * SIN_FUNC_SCALING_FACTOR * x * np.cos(x**2 + y**2)


def partial_y(x, y):
    return 2 * SIN_FUNC_SCALING_FACTOR * y * np.cos(x**2 + y**2)


def normal_func(x, y):
    return (-1 * partial_x(x, y), -1 * partial_y(x, y), 1)


class SinSurface(ThreeDScene):
    def construct(self):
        # create axis, surface, and set camrea orientation
        axes = ThreeDAxes(
            x_range=AXES_RANGE, y_range=AXES_RANGE, x_length=8, y_length=8
        ).scale(GLOBAL_SCALE)
        surface = Surface(
            lambda x, y: axes.c2p(*sin_func(x, y)),
            u_range=AXES_RANGE,
            v_range=AXES_RANGE,
            resolution=8,
            fill_opacity=0.7,
        )
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)

        # create surface equation text
        sin_func_tex = (
            MathTex(r"z = 0.2\sin(x^2 + y^2)", color=BLUE)
            .scale(GLOBAL_SCALE)
            .to_edge(UP)
        )
        self.add_fixed_orientation_mobjects(sin_func_tex)
        self.add_fixed_in_frame_mobjects(sin_func_tex)

        # Fade the axis, surface, and equation in
        self.play(
            FadeIn(axes), FadeIn(surface), Write(sin_func_tex), run_time=GLOBAL_RUN_TIME
        )
        self.wait()

        self.play(
            FadeOut(axes),
            FadeOut(surface),
            Unwrite(sin_func_tex),
            run_time=GLOBAL_RUN_TIME,
        )
