from manim import *
from typing import Final

GLOBAL_SCALE: Final[float] = 0.38
TEXT_SCALE: Final[float] = 0.40
LINE_STROKE_WIDTH: Final[float] = 1.5


class EntireShort(Scene):
    def construct(self):
        ############## Definitions
        eq_0: MathTex = MathTex("x + y = 0").scale(TEXT_SCALE).to_edge(UP)
        eq_0_overlap: MathTex = (
            MathTex("2x + 2y = 0", color=GOLD)
            .scale(TEXT_SCALE)
            .next_to(eq_0, DOWN * 0.5)
        )  # will be displayed then removed before eq_1 is displayed
        eq_1: MathTex = (
            MathTex("x + 2y = 0", color=GREEN)
            .scale(TEXT_SCALE)
            .next_to(eq_0, DOWN * 0.5)
        )
        axes: Axes = (
            Axes(x_range=[-4, 4], y_range=[-4, 4], x_length=8, y_length=8)
            .scale(GLOBAL_SCALE)
            .set_color(BLUE)
        )
        eq_0_line: ParametricFunction = axes.plot(
            lambda x: -x, stroke_width=LINE_STROKE_WIDTH
        )
        eq_0_overlap_line: ParametricFunction = axes.plot(
            lambda x: -x, color=GOLD, stroke_width=LINE_STROKE_WIDTH
        )  # truly is just the same as eq_0
        eq_1_line: ParametricFunction = axes.plot(
            lambda x: -x / 2, color=GREEN, stroke_width=LINE_STROKE_WIDTH
        )
        solution_dot: Dot = (
            Dot(axes.c2p(0, 0), radius=0.15, color=YELLOW)
            .scale(GLOBAL_SCALE)
            .set_z_index(1)
        )
        inconsistent_eq_1: MathTex = (
            MathTex("x + y = 1", color=GREEN)
            .scale(TEXT_SCALE)
            .next_to(eq_0, DOWN * 0.5)
        )
        inconsistent_eq_1_line: ParametricFunction = axes.plot(
            lambda x: -x + 1, color=GREEN, stroke_width=LINE_STROKE_WIDTH
        )

        ################ Animations start here
        self.play(Write(eq_0), FadeIn(axes), FadeIn(eq_0_line), FadeIn(solution_dot))
        self.wait()

        # dot moves up and left and then back to the origin
        # system is consisent and not unique
        self.play(solution_dot.animate.move_to(axes.c2p(-4, 4)), rate_func=linear)
        self.play(solution_dot.animate.move_to(axes.c2p(0, 0)), rate_func=linear)
        self.wait()

        # show the overlap and still infinite solutions with two equations
        # dot moves down and right
        # system is consistent and still not unique
        self.play(Write(eq_0_overlap), FadeIn(eq_0_overlap_line))
        self.play(solution_dot.animate.move_to(axes.c2p(4, -4)), rate_func=linear)
        self.play(solution_dot.animate.move_to(axes.c2p(0, 0)), rate_func=linear)
        self.wait()
        self.play(Unwrite(eq_0_overlap), FadeOut(eq_0_overlap_line))

        self.wait()

        # Bring in eq_1 and show stuck in place.
        # solution is consistent and unique
        self.play(Write(eq_1), FadeIn(eq_1_line))
        self.wait()
        self.play(Indicate(solution_dot, color=PURE_RED))
        self.wait()

        # going to transform these into a different line to show
        # solution is inconsistent. In case want to revert back
        # to previous states later.
        # eq_1.save_state()
        # eq_1_line.save_state()

        # Transform eq_1 into its inconsistent version
        self.play(
            Transform(eq_1, inconsistent_eq_1),
            Transform(eq_1_line, inconsistent_eq_1_line),
        )
        self.wait()
