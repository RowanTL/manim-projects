from typing import Final

from manim import *

GLOBAL_SCALE: Final[float] = 0.38
TEXT_SCALE: Final[float] = 0.40


class LinEqSolutions(Scene):
    def construct(self):
        # Scene setup
        # ...

        # Declarations
        number_plane: NumberPlane = NumberPlane()

        # Animations
        self.play(Write(number_plane))

        self.wait(2)
