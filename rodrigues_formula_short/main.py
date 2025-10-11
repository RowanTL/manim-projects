from manim import *
from typing import Final

GLOBAL_SCALE: Final[float] = 0.45


class FormulaScene(Scene):
    def construct(self):
        rodrigues_formula: MathTex = (
            # cool little trick to make subgroups is to use {{}}
            MathTex(
                r"\mathbf{R}(\hat{n}, {{\theta}}) = I + \sin{{\theta}} [\mathbf{\hat{n}}]_\times + (1 - \cos{{\theta}}) [\mathbf{\hat{n}}]_\times^2"
            )
            .scale(0.5)
            .move_to(UP * 2)
        ).set_color_by_tex(r"\theta", YELLOW)
        n_hat: MathTex = (
            MathTex(
                r"\mathbf{[\hat n]}_\times = "
                r"\begin{bmatrix}"
                r"0 & -\hat n_z & \hat n_y \\"
                r"\hat n_z & 0 & -\hat n_x \\"
                r"-\hat n_y & \hat n_x & 0"
                r"\end{bmatrix}"
            )
            .scale(0.5)
            .next_to(rodrigues_formula, DOWN)
        )
        rodrigues_text: Text = (
            Text("Rodrigues' Formula", weight=BOLD)
            .next_to(rodrigues_formula, UP)
            .scale(GLOBAL_SCALE)
        )

        self.play(
            Write(rodrigues_formula), Write(n_hat), Write(rodrigues_text), run_time=2
        )
        self.wait()
        self.play(
            Unwrite(rodrigues_formula),
            Unwrite(n_hat),
            Unwrite(rodrigues_text),
            run_time=2,
        )


class RotationScene(ThreeDScene):
    def construct(self):
        x_range, y_range, z_range = (-4, 4, 1), (-4, 4, 1), (-4, 4, 1)
        axes = ThreeDAxes(x_range, y_range, z_range).scale(GLOBAL_SCALE)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Example vector in 3D
        main_vec = np.array([0, -2, 3], dtype=np.float64) * GLOBAL_SCALE
        arrow = Arrow3D(
            start=ORIGIN,
            end=main_vec,
            color=BLUE,
        )
        self.play(FadeIn(axes), FadeIn(arrow))
        self.begin_3dillusion_camera_rotation(rate=2)
        self.wait(PI / 2)
        self.stop_3dillusion_camera_rotation()
        angle_arc = Arc(
            radius=2.0 * GLOBAL_SCALE, start_angle=-PI / 2, angle=PI / 2, color=YELLOW
        )
        self.play(Write(angle_arc))
        self.play(Rotate(arrow, PI / 2, Z_AXIS, about_point=ORIGIN))
        self.play(FadeOut(axes), FadeOut(arrow))
