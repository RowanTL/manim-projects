from manim import *
from manim_exts import AugmentedMatrix
from typing import Final
import numpy as np

GLOBAL_SCALE: Final[float] = 0.38
TEXT_SCALE: Final[float] = 0.40


class LinEqTransformations(Scene):
    def construct(self):
        types_transforms_text: Text = (
            Text("Types of Transformations:", color=YELLOW)
            .scale(TEXT_SCALE)
            .to_edge(UP)
        )
        scaling_text: Text = (
            Text("Scaling").scale(TEXT_SCALE).next_to(solutions_type, DOWN)
        )
        interchange_text: Text = (
            Text("Interchange", color=BLUE).scale(TEXT_SCALE).next_to(inf_text, DOWN)
        )
        replacement_text: Text = (
            Text("Replacement", color=PURPLE)
            .scale(TEXT_SCALE)
            .next_to(one_point_text, DOWN)
        )

        self.play(Write(types_transforms_text), run_time=2)
        self.play(Write(scaling_text))
        self.play(Write(interchange_text))
        self.play(Write(replacement_text))
        self.play(
            Unwrite(types_transforms_text),
            Unwrite(scaling_text),
            Unwrite(interchange_text),
            Unwrite(replacement_text),
            run_time=0.5,
        )


class TwoDSystemExample(Scene):
    def right_scale(
        self,
        old_aug_matrix: AugmentedMatrix,
        new_aug_matrix: AugmentedMatrix,
        scale_tex: MathTex,
        row_num: int,
    ):
        self.play(old_aug_matrix.animate.to_edge(LEFT))
        scale_tex.next_to(old_aug_matrix.matrix.get_rows()[row_num], RIGHT * 2)
        self.play(Write(scale_tex))
        self.wait()
        self.play(Unwrite(scale_tex))
        self.play(
            Transform(old_aug_matrix, new_aug_matrix),
        )
        self.play(old_aug_matrix.animate.center())

    def construct(self):
        system_tex: MathTex = MathTex(
            r"{{-x + y = 2}}\\{{2x + 2y = 4}}"
        ).set_color_by_tex("2x + 2y = 4", BLUE)

        self.play(Write(system_tex))
        self.wait()

        aug_matrix: AugmentedMatrix = AugmentedMatrix(np.array([[-1, 1, 2], [2, 2, 4]]))
        aug_matrix.matrix.set_row_colors(WHITE, BLUE)

        self.play(ReplacementTransform(system_tex, aug_matrix))
        system_tex = aug_matrix
        self.wait()

        # show off scaling doesn't change anything
        aug_matrix_div_row_1_by_2: AugmentedMatrix = AugmentedMatrix(
            np.array([[-1, 1, 2], [1, 1, 2]])
        )
        aug_matrix_div_row_1_by_2.matrix.set_row_colors(WHITE, BLUE)
        self.right_scale(system_tex, aug_matrix_div_row_1_by_2, MathTex(r"\div 2"), 1)

        # Show adding one equation to another doesn't do anything
        aug_matrix_row_1_plus_row_2: AugmentedMatrix = AugmentedMatrix(
            np.array([[-1, 1, 2], [0, 2, 4]])
        )
        aug_matrix_row_1_plus_row_2.matrix.set_row_colors(WHITE, BLUE)
        # self.play(Transform(system_tex, aug_matrix_row_1_plus_row_2))
        # self.wait()


class TwoDSystem(Scene):
    def construct(self):
        axes = Axes(x_range=[-4, 4], y_range=[-4, 4], x_length=8, y_length=8).set_color(
            YELLOW
        )
        eq_0 = DoubleArrow(start=axes.c2p(-4, -4), end=axes.c2p(4, 4))
        eq_1 = DoubleArrow(start=axes.c2p(-2, 4), end=axes.c2p(4, -2), color=BLUE)
        self.play(Write(axes), Write(eq_0), Write(eq_1))
        self.wait()

        # restore this later
        eq_1.save_state()
        self.play(eq_1.animate.scale(0.5))
        self.wait()
        self.play(eq_1.animate.restore())

        # show solution to system
        sol_dot: Dot = Dot(axes.c2p(1, 1), color=PURE_RED)
        self.play(FadeIn(sol_dot))
        self.wait()
