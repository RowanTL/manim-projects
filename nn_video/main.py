from typing import Final

from manim import *


class IntroScene(Scene):
    def construct(self):
        how_to_text: Text = Text("How to Neural Network?")

        self.play(Write(how_to_text))
        self.wait(4)
