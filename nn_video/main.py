from itertools import pairwise
from typing import Final

from manim import *

TEX_COLOR_MAP: Final[dict[str, ManimColor]] = {
    r"\mathbb{F}": PURPLE,
    r"\mathbb{Z}_+": BLUE,
}


class IntroScene(Scene):
    def construct(self):
        how_to_text: Text = Text("How to Neural Network?")
        haskell_code: Text = (
            Text("Haskell code >:D", color=BLUE)
            .next_to(how_to_text, DOWN * 2)
            .scale(0.7)
        )

        self.play(Write(how_to_text))
        self.play(Write(haskell_code))


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
    SUMMARY_SCALE: Final[float] = 0.6

    def construct(self):
        f_and_q_defition: Tex = Tex(
            r"Let $\mathbb{F} \subset \mathbb{Q}$ be a finite set containing "
            r"all 64-bit floating point values",
            tex_to_color_map=TEX_COLOR_MAP,
        )

        f_and_q_summary: Tex = Tex(
            r"$\mathbb{F} \subset \mathbb{Q}$ \\ (64 bit floats)",
            tex_to_color_map=TEX_COLOR_MAP,
            tex_environment="flushleft",
        ).scale(self.SUMMARY_SCALE)
        nk_definition: Tex = Tex(
            r"Let $k \in \mathbb{Z}_+$ and $n_1, n_2, \ldots, n_k \in \mathbb{Z}_+$.",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        nk_summary: Tex = Tex(
            r"$k \in \mathbb{Z}_+$ \\ $n_1, n_2, \ldots, n_k \in \mathbb{Z}_+$",
            tex_to_color_map=TEX_COLOR_MAP,
            tex_environment="flushleft",
        ).scale(self.SUMMARY_SCALE)

        matrix_definition: Tex = Tex(
            r"For some $p, q \in \mathbb{Z}_+$, let $\mathbb{F}^{p \times q}$ "
            r"denote the set of all matrices with $p$ rows and $q$ columns.",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        matrix_summary: Tex = Tex(
            r"$\mathbb{F}^{p \times q}$",
            tex_to_color_map=TEX_COLOR_MAP,
            tex_environment="flushleft",
        ).scale(self.SUMMARY_SCALE)

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

        # A generic length-p column vector, followed by "in F^p"
        vector_entries: Matrix = Matrix(
            [[r"x_{1}"], [r"x_{2}"], [r"\vdots"], [r"x_{p}"]],
            v_buff=0.9,
        )
        vector_entries.get_entries().set_color(RED)
        vector_membership: MathTex = MathTex(
            r"\in \mathbb{F}^{p}",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        vector_diagram: VGroup = VGroup(vector_entries, vector_membership)
        vector_diagram.arrange(RIGHT, buff=0.4).move_to(ORIGIN)

        # Every summary lives in this one stack: left-aligned, top left corner.
        # To add another summary later, build it above and append it here.
        # Earlier entries stay put because the stack grows downward from the corner.
        VGroup(f_and_q_summary, nk_summary, matrix_summary).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2
        ).to_corner(UL)

        # Keep the sentences inside the frame
        max_width: float = config.frame_width - 1
        for definition in (f_and_q_defition, nk_definition, matrix_definition):
            if definition.width > max_width:
                definition.scale_to_fit_width(max_width)

        self.play(Write(f_and_q_defition))

        self.play(
            ReplacementTransform(f_and_q_defition, f_and_q_summary), run_time=1.25
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

        # Finally, the neural network itself: a function from F^{n_1} to F^{n_k}
        # Edit a drumroll in here
        nn_intro: Tex = Tex("Finally, a neural network is:")
        nn_function: MathTex = MathTex(
            r"\mathfrak{f} :\mathbb{F}^{n_1} \rightarrow \mathbb{F}^{n_k}",
            tex_to_color_map=TEX_COLOR_MAP,
        )
        VGroup(nn_intro, nn_function).arrange(DOWN, buff=0.5).move_to(ORIGIN)

        self.play(Write(nn_intro))
        self.play(Write(nn_function))

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
            VGroup(smiley_face, smiley_eyes, smiley_mouth)
            .scale(0.5)
            .to_edge(DOWN)
        )

        self.play(Create(smiley))
        self.wait(2)
