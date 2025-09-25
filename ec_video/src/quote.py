from manim import *
from manim_slides.slide import Slide
from typing import Final

QUOTE: Final[str] = (
    r"\begin{center} \large{The weak die out and the strong will survive, \\ and will live on forever} \end{center}"
)
AUTHOR: Final[str] = "-Anne Frank"
AUTHOR_FONT_SIZE: Final[int] = 30


class Quote(Slide):
    def construct(self):
        # quote from: https://en.wikisource.org/wiki/Mendel%27s_Principles_of_Heredity;_a_Defence/Chapter_2
        # Paper Title: Experiments in Plant-Hybridisation by Gregor Mendel
        # Translated from the original 1865 paper in 1901
        quote_tex = Tex(QUOTE)
        author_text = Text(AUTHOR, font_size=AUTHOR_FONT_SIZE, color=BLUE).next_to(
            quote_tex, DOWN
        )

        self.play(Write(quote_tex))

        self.next_slide()

        self.play(Write(author_text))

        self.next_slide()

        self.play(Unwrite(quote_tex), Unwrite(author_text))
        self.wait()

        self.next_slide()
