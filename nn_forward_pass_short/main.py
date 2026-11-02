from typing import Final

from manim import *

GLOBAL_SCALE: Final[float] = 0.38
TEXT_SCALE: Final[float] = 0.40


class NNVisualScene(Scene):
    LAYER_SIZES: Final[list[int]] = [4, 6, 3]
    NODE_RADIUS: Final[float] = 0.15
    NODE_SPACING: Final[float] = 0.55
    LAYER_SPACING: Final[float] = 1.5
    LABEL_SHIFT: Final[float] = 0.6
    LABEL_BUFF: Final[float] = 0.4
    LABEL_EDGE_MARGIN: Final[float] = 0.7

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

        # Make room on the right for the layer size labels.
        network = VGroup(self.edges, self.layers)
        self.play(network.animate.shift(LEFT * self.LABEL_SHIFT), run_time=0.75)

        self.size_labels = VGroup(
            *[
                Text(str(size), font_size=38, color=WHITE).next_to(
                    layer, RIGHT, buff=self.LABEL_BUFF
                )
                for layer, size in zip(self.layers, self.LAYER_SIZES)
            ]
        )
        self.play(Write(self.size_labels), run_time=0.75)
        self.wait(0.25)

        # Drop everything but the first layer (all edges touch a lower layer).
        self.play(
            FadeOut(self.edges, self.layers[1:], self.size_labels[1:]),
            run_time=0.75,
        )

        # Stack the remaining nodes vertically at the middle left, and move its
        # size to the right of the screen, both scaled up.
        first_layer = self.layers[0]
        first_label = self.size_labels[0]
        self.play(
            first_layer.animate.arrange(
                DOWN, buff=self.NODE_SPACING - 2 * self.NODE_RADIUS
            )
            .scale(2)
            .move_to(LEFT * config.frame_width * 0.25),
            first_label.animate.scale(2).move_to(
                RIGHT * (config.frame_width / 2 - self.LABEL_EDGE_MARGIN)
            ),
            run_time=0.75,
        )
        self.wait(0.25)

        # Collapse the nodes into the entries of a column vector at the centre.
        vector = Matrix(
            [[f"x_{i}"] for i in range(1, self.LAYER_SIZES[0] + 1)]
        ).move_to(ORIGIN)
        self.play(
            ReplacementTransform(first_layer, vector),
            Unwrite(first_label),
            run_time=0.75,
        )
        self.wait(0.25)

        # Morph the brackets into a question mark to the right of the entries.
        # Transform (not Replacement) so the brackets, which live inside
        # `vector`, are what ends up displayed as the question mark.
        question_mark = MathTex("?").next_to(vector.get_entries(), RIGHT, buff=1.0)
        # self.play(Transform(vector.get_brackets(), question_mark), run_time=0.75)
        self.play(FadeOut(vector.get_brackets()), FadeIn(question_mark))
        self.wait(0.25)


class BasicDeclarationScene(Scene):
    def construct(self):
        pass
