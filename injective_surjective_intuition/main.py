from typing import Final

from manim import *

GLOBAL_SCALE: Final[float] = 0.40
TEXT_SCALE: Final[float] = 0.40


# Scene that shows both injectivity and bijectivity together
# Hence the funny "UnBijectivity"
class UnBijectiveScene(ThreeDScene):
    def construct(self):
        # Scene Setup
        self.set_camera_orientation(phi=2 * PI / 5, theta=PI / 5)
        self.begin_ambient_camera_rotation()

        # Definitions

        # Axes that will contain a cube getting "squished" into a
        # plane by a function. After cube gets squished, bring back
        # to 3D. Probably with a different color.
        axes: ThreeDAxes = ThreeDAxes(x_range=(-3, 3), y_range=(-3, 3)).scale(
            GLOBAL_SCALE
        )

        # Cube to place on axes and transform into arbitrary 2d plane in
        # 3d space
        injective_cylinder: Cylinder = Cylinder(
            radius=1,
            height=3,
            fill_opacity=0.75,
            fill_color=BLUE,
            checkerboard_colors=False,
        )

        # The plane that the injective cylinder transforms into.
        # injective_plane: Surface = Surface(

        # )

        # Animations
        self.play(FadeIn(axes))
        self.wait(2)
        self.play(FadeIn(injective_cylinder))
        self.wait(2)
