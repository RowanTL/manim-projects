from manim import *
from manim.typing import Point3D
from manim_voiceover import VoiceoverScene
import numpy as np
from typing import Final

SIN_FUNC_SCALING_FACTOR: Final[float] = 0.4
AXES_RANGE: Final[list[int]] = [-3, 3]
GLOBAL_SCALE: Final[float] = 0.55


def sin_func(x, y):
    return np.array([x, y, SIN_FUNC_SCALING_FACTOR * np.sin(x**2 + y**2)])


def partial_x(x, y):
    return 2 * SIN_FUNC_SCALING_FACTOR * x * np.cos(x**2 + y**2)


def partial_y(x, y):
    return 2 * SIN_FUNC_SCALING_FACTOR * y * np.cos(x**2 + y**2)


def normal_func(x, y):
    return (-1 * partial_x(x, y), -1 * partial_y(x, y), 1)


def parametric_sin_func(t):
    return (1, t, SIN_FUNC_SCALING_FACTOR * np.sin(1 + t**2))


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
            MathTex(r"z = \frac{2}{5}\sin(x^2 + y^2)", color=BLUE)
            .scale(GLOBAL_SCALE)
            .to_edge(UP)
        )

        # Fade the axis, surface, and equation in
        self.add_sound("voiceover/fade_a_s_e_in.wav")
        self.play(FadeIn(axes), FadeIn(surface))
        self.add_fixed_orientation_mobjects(sin_func_tex)
        self.add_fixed_in_frame_mobjects(sin_func_tex)
        self.play(Write(sin_func_tex))
        self.wait()

        # show a sphere representing the sun somewhere in the world with rays
        sun = Sphere(center=axes.c2p(3, -3, 3), radius=0.2).set_color(YELLOW)
        self.add_sound("voiceover/sun_sphere.wav")
        self.play(FadeIn(sun))
        sun_rays = VGroup(
            Arrow3D(start=sun.get_center(), end=axes.c2p(0, -3, 3), color=YELLOW),
            Arrow3D(start=sun.get_center(), end=axes.c2p(0, -3, 0), color=YELLOW),
            Arrow3D(start=sun.get_center(), end=axes.c2p(3, 0, 0), color=YELLOW),
            Arrow3D(start=sun.get_center(), end=axes.c2p(0, 0, 0), color=YELLOW),
        )
        self.play(FadeIn(sun_rays))
        self.wait(1.2)
        self.play(FadeOut(sun_rays))

        # Group everything and move everything closer to the camera
        scene_group: VGroup = VGroup(sun, axes, surface)
        self.add_sound("voiceover/close_camera.wav")
        self.play(scene_group.animate.shift(RIGHT * 2 + UP * 7 + OUT))
        self.play(Rotate(scene_group, PI / 2))

        current_point_dot: Dot3D = Dot3D(axes.c2p(*sin_func(1, -1.5))).set_opacity(0)
        point_path: ParametricFunction = ParametricFunction(
            lambda t: axes.c2p(*parametric_sin_func(t)),
            t_range=(-1.5, 1.5),
        ).set_opacity(0)
        incident_ray: Arrow3D = always_redraw(
            lambda: Arrow3D(
                start=sun.get_center(), end=current_point_dot.get_center(), color=YELLOW
            )
        )
        self.play(FadeIn(incident_ray))

        # Show normals of the surface
        # need to calculate them
        self.play(
            MoveAlongPath(current_point_dot, point_path), run_time=2, rate_func=linear
        )
        self.wait(2)
        # x never changes, so no need to track that
        # current_point_y = ValueTracker(1.5)
        # point_path: ParametricFunction = ParametricFunction(
        #     lambda t: axes.c2p(*parametric_sin_func(t)),
        #     t_range=(1.5, -1.5),
        # ).set_opacity(0)
        # current_point_y.add_updater()
        # normal_arrow: Arrow3D = always_redraw(
        #     lambda: Arrow3D(
        #         start=current_point_dot.get_center(),
        #         end=axes.c2p(
        #             normal_func(
        #                 axes.c2p(current_point_dot.get_center())[0],  # problem line
        #                 axes.c2p(current_point_dot.get_center())[
        #                     1
        #                 ],  # have no information on current position with respect to axis
        #             )
        #         ),
        #     )
        # )
        # self.play(FadeIn(normal_arrow))
        # self.wait()
        # self.play(FadeOut(normal_arrow))

        # Remove everything from the scene
        self.play(
            FadeOut(scene_group),
            Unwrite(sin_func_tex),
            FadeOut(incident_ray),
            run_time=1.2,
        )
        self.wait()
