from manim import *
from typing import Final
import numpy as np

GLOBAL_SCALE: Final[float] = 0.38
TEXT_SCALE: Final[float] = 0.40


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

        self.play(Write(solutions_type))
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
        axes_group: VGroup = VGroup(axes)
        always_rotate(axes_group)
        # has infinitely many solutions
        eq_0_surface: Surface = Surface(
            lambda x, y: np.array([x, y, -x - y]),
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(16, 16),
            checkerboard_colors=[WHITE, GRAY_A, GRAY_B],
            fill_opacity=0.6,
        ).scale(GLOBAL_SCALE)
        axes_group.add(eq_0_surface)
        self.add_fixed_orientation_mobjects(eq_0)
        self.add_fixed_in_frame_mobjects(eq_0)
        self.play(FadeIn(axes), Write(eq_0), FadeIn(eq_0_surface))
        self.wait(4)

        # use a dot to show the infinitely many solutions
        # eq_0_dot: Dot = (
        #     Dot(axes.c2p(0, 0), radius=0.10, color=PURE_GREEN)
        #     .scale(GLOBAL_SCALE)
        #     .set_z_index(1)
        # )  # stops from being drawn over
        # self.play(FadeIn(eq_0_dot))
        # self.play(
        #     eq_0_dot.animate.move_to(axes.c2p(4, 4)), run_time=1.5, rate_func=linear
        # )
        # self.play(
        #     eq_0_dot.animate.move_to(axes.c2p(-4, -4)), run_time=2.0, rate_func=linear
        # )
        # self.play(
        #     eq_0_dot.animate.move_to(axes.c2p(0, 0)), run_time=1.5, rate_func=linear
        # )
        # self.wait()

        # # show off only one solution
        # eq_1: MathTex = (
        #     MathTex("x + y = 0", color=BLUE)
        #     .scale(TEXT_SCALE)
        #     .next_to(eq_0_wrong_form, DOWN * 0.5)
        # )
        # eq_1_line = axes.plot(lambda x: -x, color=BLUE, stroke_width=1)
        # self.play(Write(eq_1), Write(eq_1_line))
        # self.wait()

        # # Flash dot with red surroundings to show it can't move
        # # only one solution now
        # self.play(Flash(eq_0_dot, line_length=0.1, line_stroke_width=1, color=PURE_RED))
        # self.wait()

        # # Show a third line for only one solution
        # eq_2: MathTex = (
        #     MathTex("2x - y = 0", color=PURPLE)
        #     .scale(TEXT_SCALE)
        #     .next_to(eq_1, DOWN * 0.5)
        # )
        # eq_2_line = axes.plot(lambda x: 2 * x, color=PURPLE, stroke_width=1)
        # self.play(Write(eq_2), Write(eq_2_line))
        # self.wait(2)

        # # move the third line for no solutions
        # eq_2.save_state()  # revert back later if needed
        # eq_2_no_point: MathTex = (
        #     MathTex("2x - y = 2", color=PURPLE)
        #     .scale(TEXT_SCALE)
        #     .next_to(eq_1, DOWN * 0.5)
        # )
        # self.play(
        #     Transform(eq_2, eq_2_no_point),
        #     eq_2_line.animate.move_to(axes.c2p(0, -2)),
        #     Unwrite(eq_0_dot),
        # )
        # self.wait(3)

        # # remove everything from the scene
        # self.play(
        #     Unwrite(eq_0_wrong_form),
        #     Unwrite(eq_1),
        #     Unwrite(eq_2),
        #     Unwrite(axes),
        #     Unwrite(eq_0_line),
        #     Unwrite(eq_1_line),
        #     Unwrite(eq_2_line),
        #     run_time=0.75,
        # )
        # self.wait()
