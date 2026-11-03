from typing import Final

from manim import *

# Colors for the recurring sets, applied to any Tex/MathTex that contains them
TEX_COLORS: Final[dict[str, ManimColor]] = {
    r"\mathbb{F}": ORANGE,
    r"\mathbb{Q}": RED,
    r"\mathbb{Z}_+": BLUE,
    r"\mathcal{F}": PURPLE,
    r"\ell_a": GREEN,
    r"\ell_d": GREEN,
}


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


class FloatingPointSubset(Scene):
    def construct(self):
        # Represents the floating point values
        fancy_f: Tex = Tex(
            r"Let $\mathbb{F}$ be a \\ finite subset of $\mathbb{Q}$",
            tex_to_color_map=TEX_COLORS,
        )
        # Used as a counter
        k_dec: Tex = Tex(r"Let $k \in \mathbb{Z}_+$", tex_to_color_map=TEX_COLORS)
        # Used later, you will see
        n_sequence: Tex = Tex(
            r"Let \\ $n_1, n_2, ..., n_k \in \mathbb{Z}_+$",
            tex_to_color_map=TEX_COLORS,
        )

        # Shrink only if it would still overflow the frame width.
        max_width = config.frame_width - 2 * MED_SMALL_BUFF
        if fancy_f.width > max_width:
            fancy_f.scale_to_fit_width(max_width)
        fancy_f.to_edge(UP)

        k_dec.next_to(fancy_f, DOWN)
        n_sequence.next_to(k_dec, DOWN)

        self.play(Write(fancy_f))
        self.play(Write(k_dec))
        self.play(Write(n_sequence))

        # A column vector over F, at the bottom of the screen
        column_vector_f: Tex = Tex(
            r"$\begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}"
            r" \in \mathbb{F}^n$ \\ for some $n \in \mathbb{Z}_+$"
            r" \\ and $x_1, x_2, ..., x_n \in \mathbb{F}$",
            tex_to_color_map=TEX_COLORS,
        )
        if column_vector_f.width > max_width:
            column_vector_f.scale_to_fit_width(max_width)
        column_vector_f.to_edge(DOWN)

        self.play(Write(column_vector_f))
        self.wait(4)


class NaiveNNDefinitionScene(Scene):
    def construct(self):
        # A concrete column vector of three values in F^3
        vector_3: MathTex = MathTex(
            r"\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}",
            r"\in",
            r"\mathbb{F}",
            r"^3",
            tex_to_color_map=TEX_COLORS,
        )
        self.play(Write(vector_3))
        self.wait(0.5)

        # Generalise to dimension n
        vector_n: MathTex = MathTex(
            r"\begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}",
            r"\in",
            r"\mathbb{F}",
            r"^n",
            tex_to_color_map=TEX_COLORS,
        )
        n_dec: Tex = Tex(
            r"for some $n \in \mathbb{Z}_+$", tex_to_color_map=TEX_COLORS
        ).next_to(vector_n, DOWN, buff=MED_LARGE_BUFF)

        self.play(TransformMatchingTex(vector_3, vector_n))
        self.play(Write(n_dec))
        self.wait(0.25)


class LayerFunctionsScene(Scene):
    def construct(self):
        set_f: Tex = Tex(
            r"Let $\mathcal{F} = \{f \mid f : \mathbb{F}^p \to \mathbb{F}^q$ \\"
            r" $\text{for all } p, q \in \mathbb{Z}_+\}$",
            tex_to_color_map=TEX_COLORS,
        ).to_edge(UP)

        # Shrink only if it would still overflow the frame width.
        max_width = config.frame_width - 2 * MED_SMALL_BUFF
        if set_f.width > max_width:
            set_f.scale_to_fit_width(max_width)

        self.play(Write(set_f), run_time=0.75)

        # Dimensions and parameters of a layer, laid out in a 2x2 grid at the bottom
        definitions = VGroup(
            *[
                MathTex(definition, tex_to_color_map=TEX_COLORS)
                for definition in (
                    r"n, m \in \mathbb{Z}_+",
                    r"W \in \mathbb{F}^{n \times m}",
                    r"X \in \mathbb{F}^m",
                    r"B \in \mathbb{F}^n",
                )
            ]
        ).arrange_in_grid(rows=2, cols=2, buff=(MED_LARGE_BUFF, MED_SMALL_BUFF))
        if definitions.width > max_width:
            definitions.scale_to_fit_width(max_width)
        definitions.to_edge(DOWN)

        self.play(Write(definitions), run_time=0.75)

        # The affine layer function, in the centre of the screen
        layer_function: Tex = Tex(
            r"Let $\ell_d \in \mathcal{F}$ \\ such that $\ell_d(X) = WX + B$",
            tex_to_color_map=TEX_COLORS,
        ).move_to(ORIGIN)
        if layer_function.width > max_width:
            layer_function.scale_to_fit_width(max_width)

        self.play(Write(layer_function), run_time=0.75)
        self.wait(0.25)
        self.play(Unwrite(layer_function), Unwrite(definitions), run_time=0.75)

        # The activation layer function, in the centre of the screen. Broken into
        # short lines and set smaller since there is a lot of text for a narrow frame.
        layer_activation: Tex = Tex(
            r"Define $\ell_a \in \mathcal{F}$ \\"
            r"to apply some \\"
            r"function $g: \mathbb{F} \to \mathbb{F}$ \\"
            r"to each element in $X$. \\[1.5ex]"
            r"$g'$ must be defined",
            font_size=36,
            tex_to_color_map=TEX_COLORS,
        ).move_to(ORIGIN)
        if layer_activation.width > max_width:
            layer_activation.scale_to_fit_width(max_width)

        self.play(Write(layer_activation), run_time=0.75)
        self.wait(0.25)
        self.play(Unwrite(layer_activation), run_time=0.75)

        # The activation applied element-wise to a column vector
        activation_example: MathTex = MathTex(
            r"\ell_a\left(\begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_m \end{bmatrix}\right)"
            r" = \begin{bmatrix} g(x_1) \\ g(x_2) \\ \vdots \\ g(x_m) \end{bmatrix}",
            tex_to_color_map=TEX_COLORS,
        ).move_to(ORIGIN)
        if activation_example.width > max_width:
            activation_example.scale_to_fit_width(max_width)

        self.play(Write(activation_example), run_time=0.75)
        self.wait(4)
