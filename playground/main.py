from manim import *
from typing import Final
import numpy as np


class ThreeDPlayGround(ThreeDScene):
    SIN_FUNC_SCALING_FACTOR: Final[float] = 0.4
    AXES_RANGE: Final[list[int]] = [-5, 5]

    def sin_func(self, x, y):
        return np.array([x, y, self.SIN_FUNC_SCALING_FACTOR * np.sin(x**2 + y**2)])

    def partial_x(self, x, y):
        return 2 * self.SIN_FUNC_SCALING_FACTOR * x * np.cos(x**2 + y**2)

    def partial_y(self, x, y):
        return 2 * self.SIN_FUNC_SCALING_FACTOR * y * np.cos(x**2 + y**2)

    def normal_func(self, x, y):
        return (-1 * self.partial_x(x, y), -1 * self.partial_y(x, y), 1)

    def parametric_sin_func(self, t):
        return (1, t, self.SIN_FUNC_SCALING_FACTOR * np.sin(1 + t**2))

    def construct(self):
        axes = ThreeDAxes(
            x_range=self.AXES_RANGE, y_range=self.AXES_RANGE, x_length=8, y_length=8
        )
        surface = Surface(
            lambda x, y: axes.c2p(*self.sin_func(x, y)),
            u_range=self.AXES_RANGE,
            v_range=self.AXES_RANGE,
            resolution=[8],
            fill_opacity=0.7,
        )
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        self.add(axes, surface)
        current_point_dot: Dot3D = Dot3D(axes.c2p(*self.sin_func(1, -1.5)))
        point_path: ParametricFunction = ParametricFunction(
            lambda t: axes.c2p(*self.parametric_sin_func(t)),
            t_range=(-1.5, 1.5),
        ).set_opacity(0)
        normal_vec = always_redraw(
            lambda: Arrow3D(
                start=current_point_dot.get_center(),
                end=axes.p2c(
                    self.normal_func(
                        current_point_dot.get_x(), current_point_dot.get_y()
                    )
                ),
                color=RED,
            )
        )
        self.add(normal_vec)
        self.play(
            MoveAlongPath(current_point_dot, point_path), run_time=2, rate_func=linear
        )

        self.wait(2)
