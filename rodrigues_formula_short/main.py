from manim import *


class FormulaScene(Scene):
    def construct(self):
        rodrigues_formula: MathTex = MathTex(
            r"\mathbf{R}(\hat{n}, \theta) = I + \sin\theta[\mathbf{\hat{n}}]_\times + (1 - \cos\theta)[\mathbf{\hat{n}}]_\times^2"
        ).scale(0.5)
        self.play(Write(rodrigues_formula), run_time=2)
        self.wait()
        self.play(Unwrite(rodrigues_formula), run_time=2)


class Rotation(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes().scale(0.5)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Example vector in 3D
        v = np.array([-1, -2, 3])  # arbitrary vector
        arrow = Arrow3D(
            start=ORIGIN,
            end=v,
            color=YELLOW,
        )
        self.play(FadeIn(axes), FadeIn(arrow))
        self.begin_3dillusion_camera_rotation(rate=2)
        self.wait(PI / 2)
        self.stop_3dillusion_camera_rotation()
        self.play(Rotate(arrow, PI / 2, Z_AXIS, about_point=ORIGIN))
        self.play(FadeOut(axes), FadeOut(arrow))
