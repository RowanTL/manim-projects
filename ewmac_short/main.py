from typing import Final

from manim import *

GLOBAL_SCALE: Final[float] = 0.50


class TwoDRowOpImpact(Scene):
    def construct(self):
        # Scene setup
        # ...

        # Declarations
        number_plane: NumberPlane = NumberPlane(
            x_range=[-5, 5], y_range=[-3, 10]
        ).scale(GLOBAL_SCALE)
        basis_vectors: VGroup = VGroup(
            Vector((1, 0), color=BLUE), Vector((0, 1), color=BLUE)
        )
        basis_matrix: Matrix = Matrix(
            [basis_vectors[0].get_vector(), basis_vectors[1].get_vector()]
        ).scale(GLOBAL_SCALE)

        # Animations
        # Show number plane
        self.play(Write(number_plane))

        self.wait(1)

        # show matrix and points on the plane
        self.play(Write(basis_matrix), Write(basis_vectors))

        self.wait(2)
