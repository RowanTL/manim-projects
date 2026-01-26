import itertools
from typing import Final

import numpy as np
from manim import *

GLOBAL_SCALE: Final[float] = 0.40
TEXT_SCALE: Final[float] = 0.40


# Scene that shows both injectivity and bijectivity together
# Hence the funny "UnBijectivity"
class UnBijectiveScene(Scene):
    def construct(self):
        ## Scene Setup
        # ...

        ## Definitions

        # Axes that demonstrates the injective and surject functions.
        axes: Axes = Axes(
            x_range=[-3, 3], y_range=[-3, 3], x_length=4, y_length=4, tips=False
        )

        # Linear Map (Transformation) that takes a number in R^2 and places it in R
        # Show at top of the screen
        lin_map: MathTex = MathTex(r"T: \mathbb{R}^2 \rightarrow \mathbb{R}").to_edge(
            UP
        )

        # Injectivity claim
        injectivity_claim: Tex = (
            Tex(
                r"T injective $\Leftrightarrow$ T maps \\ distinct inputs to distinct outputs"
            )
            .next_to(lin_map, DOWN)
            .scale(0.5)
        )

        # The actual equation of the linear map
        lin_map_equation: MathTex = (
            MathTex(r"T = x_1").next_to(lin_map, DOWN).scale(0.9)
        )

        # Dots in R^2 to be mapped into R
        injective_dots = VGroup()
        injective_dots.add(Dot(axes.c2p(1, 2), color=BLUE))
        injective_dots.add(Dot(axes.c2p(1, -2), color=BLUE))

        # Line that injective_dots gets mapped into
        r_1_line = Line(axes.c2p(-3, 0), axes.c2p(3, 0), color=YELLOW, stroke_width=2)

        # Lines that connect the dots to the r_1_line
        injective_lines: VGroup = VGroup()
        for dot in injective_dots:
            line: Line = Line(
                dot.get_center(), axes.c2p(1, 0), color=PURPLE, stroke_width=2
            )
            injective_lines.add(line)

        # Dot in which the two lines in injective_lines join at in R
        r_1_dot: Dot = Dot(axes.c2p(1, 0), color=PURPLE)

        ## Animations
        # Write function down
        self.play(Write(lin_map))
        self.wait(1)

        # Show statement attempting to "prove"
        self.play(Write(injectivity_claim))
        self.wait(1)
        self.play(Unwrite(injectivity_claim))

        # Show axes for a "visual proof"
        self.play(Write(axes))
        self.wait(1)

        # Write dots to screen. Will be morphed into 2d later.
        self.play(Write(injective_dots))
        self.wait(1)

        # The equation used to map the dots onto the real line.
        # Placed below the T: R^2 to R tex at the top of the screen
        self.play(Write(lin_map_equation))
        self.wait(1)

        # Write the R line on top of the axes
        self.play(Write(r_1_line))
        self.wait(1)

        # Show that both points correspond to one location in R.
        # Therefore, not injective
        self.play(Write(injective_lines))
        self.play(Write(r_1_dot))
        self.play(Unwrite(injective_lines))
        self.wait(1)
