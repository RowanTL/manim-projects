from manim import *
import numpy as np
import numpy.typing as npt
from typing import Final

SIN_FUNC_SCALING_FACTOR: Final[float] = 0.4
AXES_RANGE: Final[list[int]] = [-3, 3]
PARAMETRIC_RANGE: Final[tuple[float, float]] = (-1.5, 1.5)
GLOBAL_SCALE: Final[float] = 0.55


def sin_func(x, y):
    return np.array([x, y, SIN_FUNC_SCALING_FACTOR * np.sin(x**2 + y**2)])


def partial_x(x, y):
    return 2 * SIN_FUNC_SCALING_FACTOR * x * np.cos(x**2 + y**2)


def partial_y(x, y):
    return 2 * SIN_FUNC_SCALING_FACTOR * y * np.cos(x**2 + y**2)


def normal_func(x, y):
    return np.array([-1 * partial_x(x, y), -1 * partial_y(x, y), 1])


def parametric_sin_func(t):
    return (1, t, SIN_FUNC_SCALING_FACTOR * np.sin(1 + t**2))


def rev_parametric_sin_func(t):
    return (1, -t, SIN_FUNC_SCALING_FACTOR * np.sin(1 + t**2))


def my_unit(v):
    return v / np.linalg.norm(v)


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
            resolution=[8],
            fill_opacity=0.7,
        )
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)

        # create surface equation text
        sin_func_tex = (
            MathTex(r"z = \frac{2}{5}\sin(x^2 + y^2)", color=BLUE)
            .scale(GLOBAL_SCALE)
            .to_edge(UP)
        )
        reflection_tex = (
            MathTex(r"{{L_r}} = {{L_i}} - 2({{L_i}} \cdot {{N}}){{N}}")
            .scale(GLOBAL_SCALE)
            .next_to(sin_func_tex, DOWN)
        )

        # Fade the axis, surface, and equation in
        self.play(FadeIn(axes), FadeIn(surface))
        self.add_fixed_orientation_mobjects(sin_func_tex)
        self.add_fixed_in_frame_mobjects(sin_func_tex)
        self.play(Write(sin_func_tex))
        self.wait()

        # show a sphere representing the sun somewhere in the world with rays
        sun = Sphere(center=axes.c2p(3, -3, 3), radius=0.2).set_color(YELLOW)
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
        self.play(scene_group.animate.shift(RIGHT * 2 + UP * 5.5 + OUT))
        self.play(Rotate(scene_group, PI / 2))

        self.add_fixed_orientation_mobjects(reflection_tex)
        self.add_fixed_in_frame_mobjects(reflection_tex)
        self.play(Write(reflection_tex), run_time=2.0)

        current_point_dot: Dot3D = Dot3D(axes.c2p(*sin_func(1, -1.5))).set_opacity(0)
        point_path: ParametricFunction = ParametricFunction(
            lambda t: axes.c2p(*parametric_sin_func(t)),
            t_range=PARAMETRIC_RANGE,
        ).set_opacity(0)
        incident_ray = always_redraw(
            lambda: Arrow3D(
                start=sun.get_center(), end=current_point_dot.get_center(), color=YELLOW
            )
        )
        self.play(
            FadeIn(incident_ray), reflection_tex.animate.set_color_by_tex("L_i", YELLOW)
        )

        # Show normals of the surface
        self.play(
            MoveAlongPath(current_point_dot, point_path), run_time=2, rate_func=linear
        )
        self.wait(2)
        point_path_rev: ParametricFunction = ParametricFunction(
            lambda t: axes.c2p(*rev_parametric_sin_func(t)),
            t_range=PARAMETRIC_RANGE,
        ).set_opacity(0)
        normal_arrow = always_redraw(
            lambda: Arrow3D(
                start=current_point_dot.get_center(),
                end=(
                    lambda p: (
                        lambda x, y, z: axes.c2p(
                            x + normal_func(x, y)[0],
                            y + normal_func(x, y)[1],
                            z + normal_func(x, y)[2],
                        )
                    )(*axes.p2c(p))
                )(current_point_dot.get_center()),
                color=RED,
            )
        )
        self.play(
            FadeIn(normal_arrow), reflection_tex.animate.set_color_by_tex("N", RED)
        )
        self.play(
            MoveAlongPath(current_point_dot, point_path_rev),
            run_time=2,
            rate_func=linear,
        )
        self.wait()

        # show the reflected ray now
        reflected_ray = always_redraw(
            lambda: (
                # This outer lambda just calls the inner one with the current values
                lambda start_world, inc_ray_vec_logical, normal_vec_logical: Arrow3D(
                    start=start_world,
                    # We calculate the end point in logical coordinates first,
                    # then convert the *final point* to world coordinates.
                    end=axes.c2p(
                        *(
                            # 1. Get the logical coordinates of the start point
                            axes.p2c(start_world)
                            # 2. Calculate the reflected vector in logical space
                            + (
                                # This is the correct reflection formula: I - 2*dot(I,N)*N
                                inc_ray_vec_logical
                                - 2
                                * np.dot(normal_vec_logical, inc_ray_vec_logical)
                                * normal_vec_logical
                            )
                            * 2.0
                        )
                    ),
                    color=GREEN,
                )
            )(
                # These are the arguments for the inner lambda:
                current_point_dot.get_center(),  # start_world (world space)
                my_unit(  # inc_ray_vec_logical (logical space)
                    axes.p2c(incident_ray.get_end())
                    - axes.p2c(incident_ray.get_start())
                ),
                my_unit(  # normal_vec_logical (logical space)
                    axes.p2c(normal_arrow.get_end())
                    - axes.p2c(normal_arrow.get_start())
                ),
            )
        )
        self.play(
            FadeIn(reflected_ray), reflection_tex.animate.set_color_by_tex("L_r", GREEN)
        )
        point_path: ParametricFunction = ParametricFunction(
            lambda t: axes.c2p(*parametric_sin_func(t)),
            t_range=PARAMETRIC_RANGE,
        ).set_opacity(0)
        self.play(
            MoveAlongPath(current_point_dot, point_path),
            run_time=2,
            rate_func=linear,
        )

        # Remove everything from the scene
        self.play(
            FadeOut(scene_group),
            Unwrite(sin_func_tex),
            FadeOut(incident_ray),
            FadeOut(normal_arrow),
            FadeOut(reflected_ray),
            Unwrite(reflection_tex),
            run_time=1.2,
        )
        self.wait()
