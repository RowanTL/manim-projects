from manim import *
from typing import Final
import numpy as np

GLOBAL_SCALE: Final[float] = 0.38
TEXT_SCALE: Final[float] = 0.40


class DoubleArrow3D(VGroup):
    def __init__(
        self,
        start,
        end,
        color=WHITE,
        buff=0,
        cut=0.2,  # distance to trim from each end along the line
        **kwargs,
    ):
        super().__init__()

        # Ensure numpy arrays
        start = np.array(start, dtype=float)
        end = np.array(end, dtype=float)

        # Direction vector from start → end
        direction = end - start
        length = np.linalg.norm(direction)

        if length == 0:
            raise ValueError(
                "Start and end points are identical; arrow has zero length."
            )

        # Normalize
        unit_dir = direction / length

        # Shift both ends inward by `cut` distance
        start_cut = start + unit_dir * cut
        end_cut = end - unit_dir * cut

        # Create two opposing 3D arrows
        arrow1 = Arrow3D(start=start_cut, end=end, color=color, **kwargs)
        arrow2 = Arrow3D(start=end_cut, end=start, color=color, **kwargs)
        self.add(arrow1, arrow2)


class LinEqSolutions(Scene):
    def construct(self):
        solutions_type: Text = (
            Text("System of Equations solutions:", color=YELLOW)
            .scale(TEXT_SCALE)
            .to_edge(UP)
        )
        inf_text: Text = (
            Text("Infinitely many points")
            .scale(TEXT_SCALE)
            .next_to(solutions_type, DOWN)
        )
        one_point_text: Text = (
            Text("Exactly one point", color=BLUE)
            .scale(TEXT_SCALE)
            .next_to(inf_text, DOWN)
        )
        no_text: Text = (
            Text("No points", color=PURPLE)
            .scale(TEXT_SCALE)
            .next_to(one_point_text, DOWN)
        )

        self.play(Write(solutions_type), run_time=2)
        self.play(Write(inf_text))
        self.play(Write(one_point_text))
        self.play(Write(no_text))
        self.play(
            Unwrite(inf_text),
            Unwrite(one_point_text),
            Unwrite(no_text),
            Unwrite(solutions_type),
            run_time=0.5,
        )
        self.wait(0.25)


class ThreeDSystems(ThreeDScene):
    def flash_color(
        self, mob: Mobject, color: ManimColor, wait_time: int | float = 0, **kwargs
    ) -> None:
        mob.save_state()
        self.play(mob.animate.set_color(color), **kwargs)
        if wait_time > 0:
            self.wait(wait_time)
        self.play(mob.animate.restore())

        return

    def construct(self):
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        eq_0: MathTex = MathTex("x + y + z = 0").scale(TEXT_SCALE).to_edge(UP)

        axes: ThreeDAxes = (
            ThreeDAxes(
                x_range=[-4, 4],
                y_range=[-4, 4],
                z_range=[-4, 4],
                x_length=8,
                y_length=8,
                z_length=8,
            )
            .scale(GLOBAL_SCALE)
            .set_color(YELLOW)
        )
        self.begin_ambient_camera_rotation(rate=0.15)
        # has infinitely many solutions
        eq_0_surface: Surface = Surface(
            lambda x, y: np.array([x, y, -x - y]),
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(16, 16),
            checkerboard_colors=[WHITE, GRAY_A, GRAY_B],
            fill_opacity=0.6,
        ).scale(GLOBAL_SCALE)
        self.add_fixed_orientation_mobjects(eq_0)
        self.add_fixed_in_frame_mobjects(eq_0)
        self.play(FadeIn(axes), Write(eq_0), FadeIn(eq_0_surface))

        # use a line to show the infinitely many solutions with multiple free variables
        # shows this by rotating the line PI radians around the surface
        eq_0_line: DoubleArrow3D = DoubleArrow3D(
            start=axes.c2p(-4, -4, 8),
            end=axes.c2p(4, 4, -8),
            color=PURE_GREEN,
        )
        normal_vec = np.array([1, 1, 1]) / np.sqrt(3)
        self.play(FadeIn(eq_0_line))
        self.play(
            Rotate(eq_0_line, angle=PI, axis=normal_vec, about_point=ORIGIN, run_time=4)
        )
        self.wait(1.75)

        # show infinitely many solutions with only one free variable
        eq_1: MathTex = (
            MathTex("-x - y + z = 0", color=BLUE)
            .scale(TEXT_SCALE)
            .next_to(eq_0, DOWN * 0.5)
        )
        eq_1_surface: Surface = Surface(
            lambda x, y: np.array([x, y, x + y]),
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(16, 16),
            checkerboard_colors=[BLUE_C, BLUE_D, BLUE_E],
            fill_opacity=0.6,
        ).scale(GLOBAL_SCALE)
        self.add_fixed_orientation_mobjects(eq_1)
        self.add_fixed_in_frame_mobjects(eq_1)
        self.play(FadeIn(eq_1_surface), Write(eq_1), FadeOut(eq_0_line))
        eq_1_line: DoubleArrow3D = DoubleArrow3D(
            start=axes.c2p(4, -4, 0),
            end=axes.c2p(-4, 4, 0),
            color=PURE_GREEN,
        )
        self.play(FadeIn(eq_1_line))
        self.wait(1)
        self.flash_color(
            eq_1_line, PURE_RED, wait_time=1
        )  # to show there infinite solutions along the x and y free variables
        self.wait(1)

        # show off only one solution
        eq_2: MathTex = (
            MathTex("x + 2y + 2z = 0", color=GOLD)
            .scale(TEXT_SCALE)
            .next_to(eq_1, DOWN * 0.5)
        )
        eq_2_surface: Surface = Surface(
            lambda x, y: np.array([x, y, -x / 2 + -y]),
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(16, 16),
            checkerboard_colors=[GOLD_A, GOLD_B, GOLD_C],
            fill_opacity=0.6,
        ).scale(GLOBAL_SCALE)
        self.add_fixed_orientation_mobjects(eq_2)
        self.add_fixed_in_frame_mobjects(eq_2)
        self.play(Write(eq_2), FadeIn(eq_2_surface), FadeOut(eq_1_line))
        self.wait(1)
        eq_3_dot: Dot3D = Dot3D(axes.c2p(0, 0, 0), color=PURE_RED)
        self.play(FadeIn(eq_3_dot))  # shows there's only one solution
        self.wait(32)
