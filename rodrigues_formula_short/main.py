from manim import *


class FormulaScene(Scene):
    def construct(self):
        rodrigues_formula: MathTex = MathTex(
            r"\mathbf{R}(\hat{n}, \theta) = I + \sin\theta[\mathbf{\hat{n}}]_\times + (1 - \cos\theta)[\mathbf{\hat{n}}]_\times^2"
        ).scale(0.5)
        self.play(Write(rodrigues_formula), run_time=2)
        self.wait()
        self.play(Unwrite(rodrigues_formula), run_time=2)
