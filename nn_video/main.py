from itertools import pairwise
from typing import Final

from manim import *

SUMMARY_SCALE: Final[float] = 0.6

TEX_COLOR_MAP: Final[dict[str, ManimColor]] = {
    r"\mathbb{F}": PURPLE,
    r"\mathbb{Z}_+": BLUE,
}


class IntroScene(Scene):
    def construct(self):
        how_to_text: Text = Text("Formal Neural Network?")
        # haskell_code: Text = (
        #     Text("Haskell code >:D", color=BLUE)
        #     .next_to(how_to_text, DOWN * 2)
        #     .scale(0.7)
        # )

        self.play(Write(how_to_text))
        # self.play(Write(haskell_code))


class NeuralNetworkVisualScene(Scene):
    LAYER_SIZES: Final[list[int]] = [2, 3, 5, 4, 2]
    LAYER_SPACING: Final[float] = 2.5
    NODE_SPACING: Final[float] = 1.1
    NODE_RADIUS: Final[float] = 0.25
    NEON_GREEN: Final[ManimColor] = ManimColor("#39FF14")

    def construct(self):
        num_layers: int = len(self.LAYER_SIZES)

        # Build each layer as a vertical column of blue nodes, centred on the screen
        layers: list[VGroup] = []
        for layer_index, size in enumerate(self.LAYER_SIZES):
            x: float = (layer_index - (num_layers - 1) / 2) * self.LAYER_SPACING
            nodes: VGroup = VGroup(
                *[
                    Circle(
                        radius=self.NODE_RADIUS,
                        stroke_color=BLUE,
                        stroke_width=6,
                        fill_color=BLACK,
                        fill_opacity=1,
                    )
                    for _ in range(size)
                ]
            )
            nodes.arrange(DOWN, buff=self.NODE_SPACING - 2 * self.NODE_RADIUS)
            nodes.move_to([x, 0, 0])
            layers.append(nodes)

        # Fully connected: every node links to every node in the next layer
        # Edges are grouped by the pair of layers they connect, so each group
        # can be animated on its own
        edge_groups: list[VGroup] = [
            VGroup(
                *[
                    Line(
                        start.get_center(),
                        end.get_center(),
                        color=WHITE,
                        stroke_width=2,
                    )
                    for start in left
                    for end in right
                ]
            )
            for left, right in pairwise(layers)
        ]
        edges: VGroup = VGroup(*edge_groups)

        self.play(Create(edges), run_time=2)
        self.play(*[FadeIn(layer) for layer in layers])

        for group in edge_groups:
            self.play(
                group.animate(rate_func=there_and_back).set_color(self.NEON_GREEN),  # ty: ignore[call-non-callable]
            )

        self.wait(1)


class ForwardFormalizationStartScene(Scene):
    def construct(self):
        f_and_q_definition: Tex = Tex(
            r"Let $\mathbb{F} \subset \mathbb{Q}$ be a finite set containing "
            r"all 64-bit floating point values",
            tex_to_color_map=TEX_COLOR_MAP,
        )

        f_and_q_summary: Tex = Tex(
            r"$\mathbb{F} \subset \mathbb{Q}$ \\ (64 bit floats)",
            tex_to_color_map=TEX_COLOR_MAP,
            tex_environment="flushleft",
        ).scale(SUMMARY_SCALE)
        nk_definition: Tex = Tex(
            r"Let $k \in \mathbb{Z}_+$ and $n_1, n_2, \ldots, n_k \in \mathbb{Z}_+$.",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        nk_summary: Tex = Tex(
            r"$k \in \mathbb{Z}_+$ \\ $n_1, n_2, \ldots, n_k \in \mathbb{Z}_+$",
            tex_to_color_map=TEX_COLOR_MAP,
            tex_environment="flushleft",
        ).scale(SUMMARY_SCALE)

        matrix_definition: Tex = Tex(
            r"For some $p, q \in \mathbb{Z}_+$, let $\mathbb{F}^{p \times q}$ "
            r"denote the set of all matrices with $p$ rows and $q$ columns.",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        matrix_summary: Tex = Tex(
            r"$\mathbb{F}^{p \times q}$",
            tex_to_color_map=TEX_COLOR_MAP,
            tex_environment="flushleft",
        ).scale(SUMMARY_SCALE)

        # A generic p x q matrix, abbreviated with dots, followed by "in F^{p x q}"
        matrix_entries: Matrix = Matrix(
            [
                [r"x_{1,1}", r"x_{1,2}", r"\cdots", r"x_{1,q}"],
                [r"x_{2,1}", r"x_{2,2}", r"\cdots", r"x_{2,q}"],
                [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
                [r"x_{p,1}", r"x_{p,2}", r"\cdots", r"x_{p,q}"],
            ],
            v_buff=0.9,
            h_buff=1.5,
        )
        matrix_entries.get_entries().set_color(RED)
        matrix_membership: MathTex = MathTex(
            r"\in \mathbb{F}^{p \times q}",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        matrix_diagram: VGroup = VGroup(matrix_entries, matrix_membership)
        matrix_diagram.arrange(RIGHT, buff=0.4).move_to(ORIGIN)

        # A generic length-p column vector, followed by "in F^{p x 1}"
        vector_entries: Matrix = Matrix(
            [[r"x_{1}"], [r"x_{2}"], [r"\vdots"], [r"x_{p}"]],
            v_buff=0.9,
        )
        vector_entries.get_entries().set_color(RED)
        vector_membership: MathTex = MathTex(
            r"\in \mathbb{F}^{p \times 1}",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        vector_diagram: VGroup = VGroup(vector_entries, vector_membership)
        vector_diagram.arrange(RIGHT, buff=0.4).move_to(ORIGIN)

        function_set_definition: Tex = Tex(
            r"Let $\mathcal{F} = \{f: \mathbb{F}^{p \times 1} \rightarrow "
            r"\mathbb{F}^{q \times 1} \mid p, q \in \mathbb{Z}_+ \}$",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        function_set_summary: Tex = Tex(
            r"$\mathcal{F} = \{f: \mathbb{F}^{p \times 1} \rightarrow "
            r"\mathbb{F}^{q \times 1} \mid p, q \in \mathbb{Z}_+ \}$",
            tex_to_color_map=TEX_COLOR_MAP,
            tex_environment="flushleft",
        ).scale(SUMMARY_SCALE)

        # Every summary lives in this one stack: left-aligned, top left corner.
        # To add another summary later, build it above and append it here.
        # Earlier entries stay put because the stack grows downward from the corner.
        VGroup(
            f_and_q_summary, nk_summary, matrix_summary, function_set_summary
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL)

        # Keep the sentences inside the frame
        max_width: float = config.frame_width - 1
        for definition in (
            f_and_q_definition,
            nk_definition,
            matrix_definition,
            function_set_definition,
        ):
            if definition.width > max_width:
                definition.scale_to_fit_width(max_width)

        # A lone fraktur f appears first, then shrinks into the bottom right corner.
        # It returns at the end and expands into the full definition of the network.
        fraktur_f: MathTex = MathTex(r"\mathfrak{f}").scale(2)
        self.play(Write(fraktur_f))
        self.play(fraktur_f.animate.scale(SUMMARY_SCALE).to_corner(DR), run_time=1.25)

        self.play(Write(f_and_q_definition))

        self.play(
            ReplacementTransform(f_and_q_definition, f_and_q_summary), run_time=1.25
        )

        self.play(Write(nk_definition))

        self.play(ReplacementTransform(nk_definition, nk_summary), run_time=1.25)

        self.play(Write(matrix_definition))

        self.play(
            ReplacementTransform(matrix_definition, matrix_summary),
            Write(matrix_diagram),
            run_time=1.25,
        )

        self.play(ReplacementTransform(matrix_diagram, vector_diagram), run_time=1.5)
        self.wait(0.25)
        self.play(FadeOut(vector_diagram), run_time=1.25)

        self.play(Write(function_set_definition))

        self.play(
            ReplacementTransform(function_set_definition, function_set_summary),
            run_time=1.25,
        )

        # Finally, the neural network itself: a function from F^{n_1} to F^{n_k}
        # Edit a drumroll in here
        nn_intro: Tex = Tex("Finally, a neural network is:")
        nn_function: MathTex = MathTex(
            r"\mathfrak{f} :\mathbb{F}^{n_1} \rightarrow \mathbb{F}^{n_k}",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        nn_function.move_to(DOWN * 0.8)
        nn_intro.next_to(nn_function, UP, buff=0.5)

        self.play(Write(nn_intro))
        # The lone fraktur f returns to the center and expands into its final form
        self.play(fraktur_f.animate.scale(1 / SUMMARY_SCALE).move_to(nn_function))
        self.play(ReplacementTransform(fraktur_f, nn_function))

        # A small smiley face at the bottom of the screen
        smiley_face: Circle = Circle(radius=1, color=YELLOW)
        smiley_eyes: VGroup = VGroup(
            Dot(point=[-0.35, 0.3, 0], radius=0.08, color=YELLOW),
            Dot(point=[0.35, 0.3, 0], radius=0.08, color=YELLOW),
        )
        smiley_mouth: Arc = Arc(
            radius=0.6, start_angle=7 * PI / 6, angle=2 * PI / 3, color=YELLOW
        )
        smiley: VGroup = (
            VGroup(smiley_face, smiley_eyes, smiley_mouth).scale(0.5).to_edge(DOWN)
        )

        self.play(Create(smiley))
        self.wait(2)


class DenseLayerScene(Scene):
    def construct(self):
        dense_intro: Tex = Tex(
            r"For some $p, q \in \mathbb{Z}_+$, define a dense layer function, "
            r"$\ell_d \in \mathcal{F}$ such that",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        dense_signature: MathTex = MathTex(
            r"\ell_d: \mathbb{F}^{q \times 1} \rightarrow \mathbb{F}^{p \times 1}",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        dense_definition: VGroup = VGroup(dense_intro, dense_signature).arrange(
            DOWN, buff=0.5
        )

        # Keep the sentence inside the frame
        max_width: float = config.frame_width - 1
        if dense_definition.width > max_width:
            dense_definition.scale_to_fit_width(max_width)
        dense_definition.move_to(ORIGIN)

        dense_summary: Tex = Tex(
            r"$p, q \in \mathbb{Z}_+$ \\ $\ell_d \in \mathcal{F}$ \\ "
            r"$\ell_d: \mathbb{F}^{q \times 1} \rightarrow \mathbb{F}^{p \times 1}$",
            tex_to_color_map=TEX_COLOR_MAP,
            tex_environment="flushleft",
        ).scale(SUMMARY_SCALE)

        # The weight matrix, input vector and bias vector of the dense layer
        parameters_definition: MathTex = MathTex(
            r"\begin{aligned}"
            r"W &\in \mathbb{F}^{p \times q} \\"
            r"X &\in \mathbb{F}^{q \times 1} \\"
            r"B &\in \mathbb{F}^{p \times 1}"
            r"\end{aligned}",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        parameters_summary: MathTex = MathTex(
            r"\begin{aligned}"
            r"W &\in \mathbb{F}^{p \times q} \\"
            r"X &\in \mathbb{F}^{q \times 1} \\"
            r"B &\in \mathbb{F}^{p \times 1}"
            r"\end{aligned}",
            tex_to_color_map=TEX_COLOR_MAP,
        ).scale(SUMMARY_SCALE)

        # What the dense layer actually computes
        dense_rule_definition: MathTex = MathTex(
            r"\ell_d(X) = WX + B",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        dense_rule_summary: MathTex = MathTex(
            r"\ell_d(X) = WX + B",
            tex_to_color_map=TEX_COLOR_MAP,
        ).scale(SUMMARY_SCALE)

        # Every summary lives in this one stack: left-aligned, top left corner.
        # Earlier entries stay put because the stack grows downward from the corner.
        VGroup(dense_summary, parameters_summary, dense_rule_summary).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2
        ).to_corner(UL)

        self.play(Write(dense_definition))

        self.play(ReplacementTransform(dense_definition, dense_summary), run_time=1.25)

        self.play(Write(parameters_definition))

        self.play(
            ReplacementTransform(parameters_definition, parameters_summary),
            run_time=1.25,
        )

        self.play(Write(dense_rule_definition))

        self.play(
            ReplacementTransform(dense_rule_definition, dense_rule_summary),
            run_time=1.25,
        )
        self.wait(1)


class ActivationLayerScene(Scene):
    def construct(self):
        # A simple slide: the differentiable function g, then the activation layer
        g_line: Tex = Tex(
            r"$g: \mathbb{R} \rightarrow \mathbb{R}$ be differentiable",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        activation_lines: Tex = Tex(
            r"$p \in \mathbb{Z}_+$, \quad $\ell_a \in \mathcal{F}$ \\[0.4em] "
            r"$\ell_a: \mathbb{F}^{p \times 1} \rightarrow \mathbb{F}^{p \times 1}$",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        activation_slide: VGroup = VGroup(g_line, activation_lines)
        activation_slide.arrange(DOWN, buff=0.8).move_to(ORIGIN)

        activation_summary: Tex = Tex(
            r"$g: \mathbb{R} \rightarrow \mathbb{R}$ differentiable \\ "
            r"$p \in \mathbb{Z}_+$, $\ell_a \in \mathcal{F}$ \\ "
            r"$\ell_a: \mathbb{F}^{p \times 1} \rightarrow \mathbb{F}^{p \times 1}$",
            tex_to_color_map=TEX_COLOR_MAP,
            tex_environment="flushleft",
        ).scale(SUMMARY_SCALE)

        # How the activation layer uses g: elementwise, on the restriction to F
        elementwise_definition: Tex = Tex(
            r"$\ell_a$ applies the function $g|_{\mathbb{F}}: \mathbb{F} "
            r"\rightarrow \mathbb{F}$, the restriction of $g$ to $\mathbb{F}$, "
            r"to each element of an input vector.",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        elementwise_summary: Tex = Tex(
            r"$\ell_a$ applies $g|_{\mathbb{F}}: \mathbb{F} \rightarrow "
            r"\mathbb{F}$ elementwise",
            tex_to_color_map=TEX_COLOR_MAP,
            tex_environment="flushleft",
        ).scale(SUMMARY_SCALE)

        # Every summary lives in this one stack: left-aligned, top left corner.
        VGroup(activation_summary, elementwise_summary).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2
        ).to_corner(UL)

        # Keep the sentence inside the frame
        max_width: float = config.frame_width - 1
        if elementwise_definition.width > max_width:
            elementwise_definition.scale_to_fit_width(max_width)

        self.play(Write(g_line))
        self.play(Write(activation_lines))
        self.wait(1)

        self.play(
            ReplacementTransform(activation_slide, activation_summary), run_time=1.25
        )

        self.play(Write(elementwise_definition))

        self.play(
            ReplacementTransform(elementwise_definition, elementwise_summary),
            run_time=1.25,
        )

        # The input vector X in the top half, and what l_a does to it in the bottom
        input_vector: MathTex = MathTex(
            r"X = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_p \end{bmatrix} "
            r"\in \mathbb{F}^{p \times 1}",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        activation_action: MathTex = MathTex(
            r"\ell_a(X) = \ell_a\left(\begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ "
            r"x_p \end{bmatrix}\right) = \begin{bmatrix} g|_{\mathbb{F}}(x_1) \\ "
            r"g|_{\mathbb{F}}(x_2) \\ \vdots \\ g|_{\mathbb{F}}(x_p) "
            r"\end{bmatrix}",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        # Each must fit inside its own half of the frame
        half_height: float = config.frame_height / 2 - 0.5
        for equation in (input_vector, activation_action):
            if equation.height > half_height:
                equation.scale_to_fit_height(half_height)
        input_vector.move_to(UR * config.frame_height / 4)
        activation_action.move_to(DOWN * config.frame_height / 4)

        self.play(Write(input_vector))
        self.play(Write(activation_action))
        self.wait(1)
