from typing import Final

from manim import *

GLOBAL_SCALE: Final[float] = 0.38
TEXT_SCALE: Final[float] = 0.40


class NNVisualScene(Scene):
    LAYER_SIZES: Final[list[int]] = [4, 6, 3]
    NODE_RADIUS: Final[float] = 0.15
    NODE_SPACING: Final[float] = 0.55
    LAYER_SPACING: Final[float] = 1.5

    def construct(self):
        # Layers are stacked vertically (input on top, output on bottom) with the
        # nodes of each layer centred horizontally.
        self.layers = VGroup(
            *[
                VGroup(
                    *[
                        Circle(
                            radius=self.NODE_RADIUS,
                            color=BLUE,
                            fill_color=BLACK,
                            fill_opacity=1,
                        )
                        for _ in range(size)
                    ]
                ).arrange(RIGHT, buff=self.NODE_SPACING - 2 * self.NODE_RADIUS)
                for size in self.LAYER_SIZES
            ]
        ).arrange(DOWN, buff=self.LAYER_SPACING)

        # Dense: every node connects to every node in the next layer.
        self.edges = VGroup(
            *[
                Line(
                    upper.get_bottom(),
                    lower.get_top(),
                    stroke_width=1.5,
                    stroke_opacity=0.6,
                )
                for upper_layer, lower_layer in zip(self.layers, self.layers[1:])
                for upper in upper_layer
                for lower in lower_layer
            ]
        )

        # Edges first so the nodes are drawn on top of them.
        self.play(Write(self.edges), Write(self.layers), run_time=0.75)
        self.wait(0.25)


class BasicDeclarationScene(Scene):
    def construct(self):
        pass
