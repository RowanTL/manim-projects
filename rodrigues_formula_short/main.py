from manim import *
from typing import Final
import numpy as np
import numpy.typing as npt

GLOBAL_SCALE: Final[float] = 0.45
X_RANGE, Y_RANGE, Z_RANGE = (-4, 4, 1), (-4, 4, 1), (-4, 4, 1)


def compute_rodrigues(
    v: npt.NDArray[np.floating | np.integer],
    n: npt.NDArray[np.floating | np.integer],
    theta: int | float | np.floating | np.integer,
    return_steps: bool = False,
) -> (
    npt.NDArray[np.floating | np.integer]
    | tuple[
        npt.NDArray[np.integer],  # identity matrix
        npt.NDArray[np.integer | np.floating],  # n_mat
        npt.NDArray[np.integer | np.floating],  # n_mat_sq
        npt.NDArray[np.integer | np.floating],  # sin_n_mat
        npt.NDArray[np.integer | np.floating],  # cos_n_mat_sq
        npt.NDArray[np.integer | np.floating],  # u
    ]
):
    """
    v and n must be a 1x3 matrix as this only works for 3D matricies

    parameters:
        v (npt.NDArray[np.floating | np.integer]): The vector to rotate
        n (npt.NDArray[np.floating | np.integer]): The axis to rotate about
        theta (int | float | np.floating | np.integer): The angle of the rotation in radians
        return_steps (bool): Returns each individual calculation in a tuple if requested.

    returns:
        npt.NDArray[np.floating | np.integer]: The rotated vector
        | tuple[
            npt.NDArray[np.integer],  # identity matrix
            npt.NDArray[np.integer | np.floating],  # n_mat
            npt.NDArray[np.integer | np.floating],  # n_mat_sq
            npt.NDArray[np.integer | np.floating],  # sin_n_mat
            npt.NDArray[np.integer | np.floating],  # cos_n_mat_sq
            npt.NDArray[np.integer | np.floating],  # u
        ]
    """
    # 3x3 identity matrix
    identity = np.identity(3)
    # n_matrix
    n_mat = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    # n matrix squared
    n_mat_sq = np.matmul(n_mat, n_mat)

    sin_n_mat = np.sin(theta) * n_mat
    cos_n_mat_sq = (1 - np.cos(theta)) * n_mat_sq

    u = np.matmul(v, (identity + sin_n_mat + cos_n_mat_sq))
    if return_steps:
        return (identity, n_mat, n_mat_sq, sin_n_mat, cos_n_mat_sq, u)
    else:
        return u


# unused function
def mat_to_mathtex(
    arr: list[list[int | float]] | npt.NDArray[npt.NDArray[np.floating | np.integer]],
) -> str:
    """
    A simple function that formats a 2D matrix inside of a latex bmatrix
    """
    ret_str = r"\start{bmatrix}"
    for row in arr:
        for col in row:
            ret_str += f"{col}& "
        else:
            # remove trailing & and replace with \cr
            ret_str = ret_str[:-2]
            ret_str += r" \cr "
    else:
        ret_str += r"\end{bmatrix}"
    return ret_str


if __name__ == "__main__":
    v = np.array([0, 2, -3])
    n = np.array([0, 0, 1])
    theta = np.pi / 2
    print(compute_rodrigues(v, n, theta))


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
        axes = ThreeDAxes(X_RANGE, Y_RANGE, Z_RANGE).scale(GLOBAL_SCALE)
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


class DoTheMathScene(ThreeDScene):
    def construct(self):
        # n_hat in the formula
        axes = (
            ThreeDAxes(X_RANGE, Y_RANGE, Z_RANGE)
            .scale(GLOBAL_SCALE)
            .move_to(DOWN * 2 + RIGHT * 2)
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        axis_of_rotation = [0, 0, 1]
        rotation_arrow = Arrow3D(
            axes.c2p(*(0, 0, 0)), axes.c2p(*axis_of_rotation), height=0.1, color=RED
        )
        axis_rotation_text = (
            MathTex(r"\mathbf{\hat{n}} = " + str(axis_of_rotation), color=RED)
            .scale(GLOBAL_SCALE)
            .to_edge(UR)
        )
        # v in the formula (vector to be rotated)
        v = [0, -2, 3]
        v_arrow = Arrow3D(axes.c2p(*(0, 0, 0)), axes.c2p(*v), color=BLUE)
        v_text = (
            MathTex(r"\mathbf{v} = " + str(v), color=BLUE)
            .scale(GLOBAL_SCALE)
            .to_edge(UL)
        )
        theta_tex = (
            MathTex(r"\theta = \pi / 2", color=YELLOW).scale(GLOBAL_SCALE).to_edge(UP)
        )
        theta = PI / 2
        self.add_fixed_orientation_mobjects(v_text, axis_rotation_text, theta_tex)
        self.add_fixed_in_frame_mobjects(v_text, axis_rotation_text, theta_tex)

        # Show all of the available information to the viewer
        self.play(
            FadeIn(axes),
            FadeIn(rotation_arrow),
            Write(v_text),
            FadeIn(v_arrow),
            Write(axis_rotation_text),
            Write(theta_tex),
        )
        # Show the angle calculation
        rotation_arc = ArcBetweenPoints(
            start=axes.c2p(0, -2, 0), end=axes.c2p(2, 0, 0), stroke_color=YELLOW
        )
        self.play(Write(rotation_arc))

        # calculate the full rodrigues transformation
        (identity, n_mat, n_mat_sq, sin_n_mat, cos_n_mat_sq, u) = compute_rodrigues(
            np.array(v), np.array(axis_of_rotation), theta, True
        )
        # show n_mat
        n_mat_matrix = Matrix(n_mat).scale(GLOBAL_SCALE).move_to(UP * 2)
        n_equal_tex = (
            MathTex(r"\mathbf{[\hat{n}]}_\times = ")
            .scale(GLOBAL_SCALE)
            .next_to(n_mat_matrix, LEFT * 0.75)
        )
        self.add_fixed_orientation_mobjects(n_equal_tex, n_mat_matrix)
        self.add_fixed_in_frame_mobjects(n_equal_tex, n_mat_matrix)
        self.play(Write(n_equal_tex), Write(n_mat_matrix))
        self.wait()
        # show n_mat_sq
        #   transform n_equal_tex and n_mat_matrix into the squared equivalent
        n_sq_mat_matrix = Matrix(n_mat_sq).scale(GLOBAL_SCALE).move_to(UP * 2)
        n_sq_equal_tex = (
            MathTex(r"\mathbf{[\hat{n}]}_\times^2 = ")
            .scale(GLOBAL_SCALE)
            .next_to(n_sq_mat_matrix, LEFT * 0.75)
        )
        self.play(Unwrite(n_equal_tex), Unwrite(n_mat_matrix), run_time=0.5)
        self.add_fixed_orientation_mobjects(n_sq_equal_tex, n_sq_mat_matrix)
        self.add_fixed_in_frame_mobjects(n_sq_equal_tex, n_sq_mat_matrix)
        self.play(Write(n_sq_equal_tex), Write(n_sq_mat_matrix), run_time=0.5)
        self.wait()
        # Destroy the entire scene
        self.play(
            FadeOut(axes),
            FadeOut(rotation_arrow),
            Unwrite(v_text),
            FadeOut(v_arrow),
            Unwrite(axis_rotation_text),
            Unwrite(theta_tex),
            Unwrite(rotation_arc),
        )
