from manim import *
from typing import Final

GLOBAL_SCALE: Final[float] = 0.45


class LinEqSolutions(Scene):
    def construct(self):
        text_scale: float = 0.40
        inf_text: Text = Text("Infinitely many points").scale(text_scale).to_edge(UP)
        one_point_text: Text = (
            Text("Exactly one point", color=YELLOW)
            .scale(text_scale)
            .next_to(inf_text, DOWN)
        )
        no_text: Text = (
            Text("No points").scale(text_scale).next_to(one_point_text, DOWN)
        )

        self.play(Write(inf_text), Write(one_point_text), Write(no_text))
        self.wait()
        self.play(Unwrite(inf_text), Unwrite(one_point_text), Unwrite(no_text))
