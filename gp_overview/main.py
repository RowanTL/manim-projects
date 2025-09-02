"""
These classes should all be in order of slides appearing
"""

from manim import *
from manim_slides.slide import Slide
from typing import Final, Optional

CIRCLE_RADIUS: Final[float] = 0.7
CIRCLE_FONT_SIZE: Final[int] = 30
PSEUDOCODE: Final[str] = """
initialize population randomly
rank population
while (loop count < threshold) do
    select parents for recombination
    generate children from selected parents
    rank children
    loop count++
"""
PSEUDOCODE_FONT_SIZE: Final[int] = 30
PSEUDOCODE_LINE_CHARS: Final[dict[int, tuple[int, int]]] = {
    -1: (0, 0),  # do nothing
    0: (0, 28),  # init pop
    1: (28, 42),  # rank pop
    2: (42, 70),  # while loop
    3: (70, 99),  # select parents
    4: (99, 134),  # generate children
    5: (134, 146),  # rank children
    6: (146, 157),  # loop counter++
}  # error if out of indicies


def pseudocode_transition(
    start_line: int,
    end_line: int,
    from_scale: bool,
    to_scale: bool,
    from_up_left: bool,
    move_up_left: bool,
    slide: Slide,
    pseudocode_mobject: Optional[Text] = None,
    pause_after: bool = True,
    write_text: bool = False,
) -> Text:
    """
    This function transitions the color of lines in a text mobject
    containing the `PSEUDOCODE` string.

    If a pseudocode_mobject is passed, the function will use that one.
    If it is left to none, nothing will happen

    If -1 is passed to start_line or end_line, no color changing happens.

    parameters:
        start_line (int): The line to be turned white (transitioned from)
        end_line (int): The line to be turned blue (transition to)
        from_scale (bool): Whether to scale the text down to 0.5 after color transition
        to_scale (bool): Whether or not to scale the text up by 2.0 before color transition
        from_up_left (bool): Move code to center of screen before color transition
        move_up_left (bool): Move pseudocode to the upper left corner after color transition
        slide (Slide): The slide in which to operate in
        pseudocode_mobject (Optional[Text], default = None): The pseudocode mobject to use if provided.
            If one isn't provided, will just create one.
        pause_after (bool, default = True): Whether or not to call `self.next_slide()` before calling
            the "after" animations.
        write_text (bool, default = False): Whether or not to write the pseudocode_mobject to the screen or not.

    returns:
        (Text): The modified pseudocode object
    """
    if pseudocode_mobject is None:
        pseudocode_mobject = Text(PSEUDOCODE, font_size=PSEUDOCODE_FONT_SIZE)

    if write_text:
        slide.play(Write(pseudocode_mobject))

    start_chars: tuple[int, int] = PSEUDOCODE_LINE_CHARS[start_line]
    end_chars: tuple[int, int] = PSEUDOCODE_LINE_CHARS[end_line]

    pseudocode_mobject[start_chars[0] : start_chars[1]].set_color(BLUE)

    # Animations to play before the color transition
    pre_anim = pseudocode_mobject.copy()
    pre_anim_flag: bool = False  # no easy way to check for mobject equality
    if to_scale:
        pre_anim.scale(2.0)
        pre_anim_flag = True
    if from_up_left:
        pre_anim.center()
        pre_anim_flag = True
    if pre_anim_flag:
        slide.play(Transform(pseudocode_mobject, pre_anim))

    # Transition the color now
    slide.play(
        pseudocode_mobject[start_chars[0] : start_chars[1]].animate.set_color(WHITE),
        pseudocode_mobject[end_chars[0] : end_chars[1]].animate.set_color(BLUE),
    )

    post_anim = pseudocode_mobject.copy()
    post_anim_flag = False
    if from_scale:
        post_anim.scale(0.5)
        post_anim_flag = True
    if move_up_left:
        post_anim.to_edge(UL)
        post_anim_flag = True
    if pause_after:
        slide.next_slide()
    if post_anim_flag:
        slide.play(Transform(pseudocode_mobject, post_anim))

    return pseudocode_mobject


def create_node(
    text: str | int | float,
    radius=CIRCLE_RADIUS,
    color=BLUE,
    font_size=CIRCLE_FONT_SIZE,
    group: Optional[VGroup] = None,
) -> VGroup:
    """
    Creates a circle and text, adds an updater to text to the center of the
    circle.
    """
    node = Circle(radius=radius, color=color)
    text: Text = Text(str(text), font_size=font_size)
    text.add_updater(lambda x: x.move_to(node.get_center()))
    return VGroup(node, text)


def connect_layers(layer0: VGroup, layer1: VGroup) -> VGroup:
    temp_vgroup = VGroup()
    for node0 in layer0:
        for node1 in layer1:
            if (
                isinstance(node0, Circle)
                or isinstance(node0, VGroup)
                and isinstance(node1, Circle)
                or isinstance(node1, VGroup)
            ):
                temp_vgroup.add(Line(node0, node1))

    return temp_vgroup


# This class is test class. It is not intuitive to change the color
# of the text lol
class PseudocodeTest(Slide):
    def construct(self):
        ptext = (
            Text(PSEUDOCODE, font_size=PSEUDOCODE_FONT_SIZE).move_to(LEFT).scale(0.5)
        )
        self.play(Write(ptext))
        ptext = pseudocode_transition(-1, 1, True, True, True, False, self, ptext)


# This should be slide 1
class NNSlide(Slide):
    def construct(self):
        layer_one = (
            VGroup([create_node(text, color=GREEN) for text in ["", ""]])
            .arrange(DOWN, buff=2.0)
            .shift(LEFT * 5)
        )
        layer_two = VGroup(
            [create_node(text, color=GREEN) for text in ["", ""]]
        ).arrange(DOWN, buff=2.0)
        layer_three = create_node("", color=GREEN).shift(RIGHT * 5)
        one_two_lines = connect_layers(layer_one, layer_two)
        two_three_lines = connect_layers(layer_two, layer_three)

        self.play(
            Write(layer_one),
            Write(layer_two),
            Write(layer_three),
            Write(one_two_lines),
            Write(two_three_lines),
            run_time=2,
        )

        self.next_slide()

        # Create dots and their move-along-path animations in one go
        one_two_dots_animations = [
            MoveAlongPath(
                Dot(color=YELLOW).move_to(line.get_start()), line, remover=True
            )
            for line in one_two_lines
        ]
        one_two_dots = [anim.mobject for anim in one_two_dots_animations]

        # Write the dots, play the animations, and then unwrite them
        self.play(Write(VGroup(*one_two_dots)))
        self.play(AnimationGroup(*one_two_dots_animations, lag_ratio=0.2))
        self.next_slide()
        self.play(Unwrite(VGroup(*one_two_dots)))

        # second layer to output layer
        two_three_dots_animations = [
            MoveAlongPath(
                Dot(color=YELLOW).move_to(line.get_start()), line, remover=True
            )
            for line in two_three_lines
        ]
        two_three_dots = [anim.mobject for anim in two_three_dots_animations]
        self.play(Write(VGroup(*two_three_dots)))
        self.play(AnimationGroup(*two_three_dots_animations), lag_ratio=0.2)
        self.play(Unwrite(VGroup(*two_three_dots)))

        self.play(
            Unwrite(layer_one),
            Unwrite(layer_two),
            Unwrite(layer_three),
            Unwrite(one_two_lines),
            Unwrite(two_three_lines),
        )


# Slide 2
class ShowPopulation(Slide):
    def construct(self):
        rrects = VGroup()
        for _ in range(25):
            rrect = RoundedRectangle(color=BLUE).scale(0.5)
            rrects.add(rrect)

        rrects.arrange_in_grid(rows=5, cols=5, buff=0.6)
        self.play(Write(rrects))

        self.next_slide()

        recomb_lines: list[Line] = [
            Line(rrects[0].get_right(), rrects[1].get_left()),
            Line(rrects[6].get_bottom(), rrects[11].get_top()),
            Line(rrects[18].get_right(), rrects[19].get_left()),
        ]
        self.play(Write(VGroup(*recomb_lines)))

        # now to demonstrate recombination visually
        recomb_groups = [
            VGroup(rrects[0], rrects[1], recomb_lines[0]),
            VGroup(rrects[6], rrects[11], recomb_lines[1]),
            VGroup(rrects[18], rrects[19], recomb_lines[2]),
        ]

        recomb_anims = []
        for group in recomb_groups:
            recomb_anims.append(
                Transform(
                    group,
                    RoundedRectangle(color=PURPLE)
                    .scale(0.5)
                    .move_to((group[0].get_center() + group[1].get_center()) / 2),
                )
            )

        self.play(AnimationGroup(*recomb_anims))

        self.next_slide()

        # Change the color of one of the rounded rectangles
        # to demonstrate mutation

        self.play(
            Transform(
                rrects[20],
                RoundedRectangle(color=YELLOW).scale(0.5).move_to(rrects[20]),
            ),
            Transform(
                rrects[3], RoundedRectangle(color=YELLOW).scale(0.5).move_to(rrects[3])
            ),
        )


# Slide 3
# A slide showing a picture of something evolved
class EvolvedExample(Slide):
    def construct(self):
        image = ImageMobject("media/images/evolved_antenna.jpg").scale(2.0)
        self.play(FadeIn(image))
        self.next_slide()
        self.play(FadeOut(image))


# A slide I have no plans on using
class QuoteSlide(Slide):
    def construct(self):
        font_size = 25

        # quote from: https://en.wikisource.org/wiki/Mendel%27s_Principles_of_Heredity;_a_Defence/Chapter_2
        # Paper Title: Experiments in Plant-Hybridisation by Gregor Mendel
        # Translated from the original 1865 paper in 1901
        text0 = Text(
            '"...it is now clear that the hybrids form seeds having',
            font_size=font_size,
            slant=ITALIC,
        )
        text1 = Text(
            "one or other of the two differentiating characters, and of these one-half",
            font_size=font_size,
            slant=ITALIC,
        )
        text2 = Text(
            'develop again the hybrid form..."', font_size=font_size, slant=ITALIC
        )
        gregor_mendel = Text(
            "-Gregor Mendel", font_size=font_size + 10, weight=BOLD, color=BLUE
        )

        # orient the text Mobjects
        text0.shift(UP * 1.5)
        text1.next_to(text0, DOWN)
        text2.next_to(text1, DOWN)
        gregor_mendel.next_to(text2, DOWN)

        self.play(Write(text0), Write(text1), Write(text2), run_time=3.0)
        self.next_slide()
        self.play(Write(gregor_mendel), run_time=2.0)


# Slide 4
class TitleSlide(Slide):
    def construct(self):
        title = Text(
            "An Overview of Genetic Programming: Tree-Based GP and PushGP", font_size=30
        )
        name = Text("Rowan Torbitzky-Lane", font_size=25, color=BLUE)

        name.next_to(title, DOWN)

        self.play(Write(title), run_time=3.0)
        self.next_slide()
        self.play(Write(name), run_time=2.0)

        self.next_slide()

        self.play(Unwrite(title), Unwrite(name))


# Slide 5
# Corresponds to slide 2 in brainstorming notes
class GeneticProgrammingDescription(Slide):
    def construct(self):
        circle_radius: float = 0.7
        circle_font_size: int = 30

        full_code = Text("print((1 + 2) - 4)")
        print_circle = Circle(radius=circle_radius, color=BLUE)
        print_text = Text("print", font_size=circle_font_size)
        minus_circle = Circle(radius=circle_radius, color=BLUE)
        minus_text = Text("-", font_size=circle_font_size)
        four_minus_circle = Circle(radius=circle_radius, color=BLUE)
        four_minus_text = Text("4", font_size=circle_font_size)
        plus_circle = Circle(radius=circle_radius, color=BLUE)
        plus_text = Text("+", font_size=circle_font_size)
        left_one_circle = Circle(radius=circle_radius, color=BLUE)
        left_one_text = Text("1", font_size=circle_font_size)
        right_two_circle = Circle(radius=circle_radius, color=BLUE)
        right_two_text = Text("2", font_size=circle_font_size)

        full_code.shift(LEFT * 4)

        print_circle.shift(UP * 3 + RIGHT * 2.5)
        print_text.move_to(print_circle.get_center())
        print_text.add_updater(lambda x: x.move_to(print_circle.get_center()))

        minus_circle.shift(UP + RIGHT * 2.5)
        minus_text.move_to(minus_circle.get_center())
        minus_text.add_updater(lambda x: x.move_to(minus_circle.get_center()))

        four_minus_circle.shift(DOWN * 0.5 + RIGHT * 4.0)
        four_minus_text.move_to(four_minus_circle.get_center())
        four_minus_text.add_updater(lambda x: x.move_to(four_minus_circle.get_center()))

        plus_circle.shift(DOWN * 0.5 + RIGHT)
        plus_text.move_to(four_minus_circle.get_center())
        plus_text.add_updater(lambda x: x.move_to(plus_circle.get_center()))

        left_one_circle.shift(DOWN * 2.0 + LEFT * 0.5)
        left_one_text.move_to(left_one_circle.get_center())
        left_one_text.add_updater(lambda x: x.move_to(left_one_circle.get_center()))

        right_two_circle.shift(DOWN * 2.0 + RIGHT * 2.5)
        right_two_text.move_to(right_two_circle.get_center())
        right_two_text.add_updater(lambda x: x.move_to(right_two_circle.get_center()))

        # Create lines after all mobjects shifted
        print_minus_line = Line(print_circle, minus_circle)
        minus_plus_line = Line(minus_circle, plus_circle)
        minus_four_line = Line(minus_circle, four_minus_circle)
        plus_one_line = Line(plus_circle, left_one_circle)
        plus_two_line = Line(plus_circle, right_two_circle)

        self.play(Write(full_code))
        self.next_slide()
        self.play(
            Write(print_circle),
            Write(minus_circle),
            Write(four_minus_circle),
            Write(plus_circle),
            Write(left_one_circle),
            Write(right_two_circle),
        )
        self.play(
            Write(print_minus_line),
        )
        self.play(
            Write(minus_four_line),
            Write(minus_plus_line),
        )
        self.play(
            Write(plus_one_line),
            Write(plus_two_line),
        )
        self.play(
            Write(print_text),
            Write(minus_text),
            Write(four_minus_text),
            Write(plus_text),
            Write(left_one_text),
            Write(right_two_text),
        )
        self.next_slide()

        # Throughout the populations, the AST changes
        # The actual program itself could change too
        # This section animates those
        mult_text = Text("*", font_size=circle_font_size).move_to(minus_text)
        log_text = Text("log", font_size=circle_font_size).move_to(print_text)
        big_num_text = Text("9999", font_size=circle_font_size).move_to(right_two_text)
        full_mult_text = Text("print((1 + 2) * 4)").move_to(full_code)
        full_log_text = Text("log((1 + 2) * 4)").move_to(full_code)
        full_big_num_text = Text("log((1 + 9999) * 4)").move_to(full_code)

        self.play(
            Transform(minus_text, mult_text),
            TransformMatchingShapes(full_code, full_mult_text),
        )
        self.next_slide()
        self.play(
            Transform(print_text, log_text),
            TransformMatchingShapes(full_mult_text, full_log_text),
        )
        self.next_slide()
        self.play(
            Transform(right_two_text, big_num_text),
            TransformMatchingShapes(full_log_text, full_big_num_text),
        )

        self.next_slide()

        # Maybe remove the updaters for this later
        self.play(
            Unwrite(print_circle),
            Unwrite(print_text),
            Unwrite(minus_circle),
            Unwrite(minus_text),
            Unwrite(four_minus_circle),
            Unwrite(four_minus_text),
            Unwrite(plus_circle),
            Unwrite(plus_text),
            Unwrite(left_one_circle),
            Unwrite(left_one_text),
            Unwrite(right_two_circle),
            Unwrite(right_two_text),
            Unwrite(print_minus_line),
            Unwrite(minus_plus_line),
            Unwrite(minus_four_line),
            Unwrite(plus_one_line),
            Unwrite(plus_two_line),
            Unwrite(mult_text),
            Unwrite(log_text),
            Unwrite(big_num_text),
            Unwrite(full_big_num_text),
        )


# Slide 6
class ECLoopTreeInit(Slide):
    def construct(self):
        circle_radius: float = 0.7
        circle_font_size: int = 30

        # EC loop pseudocode
        # see the best possible individual in minimization problems personally
        ptext = pseudocode_transition(
            -1, 0, True, False, False, True, self, write_text=True
        )

        # Types program initialization
        # Grow, Full, and Ramped Half&Half

        # Full first
        # Nodes taken at random from a function set until maximum
        # tree depth reached. Beyond this limit, only terminals
        # can be selected.
        # Only going to a depth of 2 here
        # Can think about this as a depth first creation of sorts

        full_text = Text("Full").to_edge(UR)

        def gen_time_text(time: int | str) -> Text:
            return Text(f"t={time}", color=GREEN).next_to(full_text, LEFT)

        self.play(Write(full_text))

        depth_text = Text("Max Depth=2", font_size=20)
        depth_text.next_to(full_text, DOWN)
        self.play(Write(depth_text))

        time0_text = gen_time_text(0)

        self.play(Write(time0_text))

        self.next_slide()

        # Start of t=1
        time1_text = gen_time_text(1)
        self.play(TransformMatchingShapes(time0_text, time1_text))

        root_node = Circle(radius=circle_radius, color=BLUE).shift(UP * 3 + RIGHT)
        root_text = Text("+", font_size=circle_font_size)
        root_text.move_to(root_node.get_center())

        self.play(Write(root_node), Write(root_text))

        # end t=1
        # start t=2
        time2_text = gen_time_text(2)
        self.play(TransformMatchingShapes(time1_text, time2_text))

        mult_node = Circle(radius=circle_radius, color=BLUE).next_to(
            root_node, DOWN + LEFT
        )
        mult_text = Text("*", font_size=circle_font_size)
        mult_text.move_to(mult_node.get_center())
        self.play(Write(mult_node), Write(mult_text))

        root_mult_line = Line(root_node, mult_node)
        self.play(Write(root_mult_line))

        # end t=2
        # start t=3
        time3_text = gen_time_text(3)
        self.play(TransformMatchingShapes(time2_text, time3_text))

        x_node = Circle(radius=circle_radius, color=BLUE).next_to(
            mult_node, DOWN + LEFT
        )
        x_text = Text("x", font_size=circle_font_size)
        x_text.move_to(x_node.get_center())
        self.play(Write(x_node), Write(x_text))

        mult_x_line = Line(mult_node, x_node)
        self.play(Write(mult_x_line))

        # end t=3
        # start t=4
        time4_text = gen_time_text(4)
        self.play(TransformMatchingShapes(time3_text, time4_text))

        y_node = Circle(radius=circle_radius, color=BLUE).next_to(mult_node, DOWN * 2)
        y_text = Text("y", font_size=circle_font_size)
        y_text.move_to(y_node.get_center())
        self.play(Write(y_node), Write(y_text))

        mult_y_line = Line(mult_node, y_node)
        self.play(Write(mult_y_line))

        # end t=4
        # start t=5
        time5_text = gen_time_text(5)
        self.play(TransformMatchingShapes(time4_text, time5_text))

        div_node = Circle(radius=circle_radius, color=BLUE).next_to(
            root_node, DOWN + RIGHT
        )
        div_text = Text("/", font_size=circle_font_size)
        div_text.move_to(div_node.get_center())
        self.play(Write(div_text), Write(div_node))

        root_div_line = Line(root_node, div_node)
        self.play(Write(root_div_line))

        # end t=5
        # start t=6
        time6_text = gen_time_text(6)
        self.play(TransformMatchingShapes(time5_text, time6_text))

        one_node = Circle(radius=circle_radius, color=BLUE).next_to(div_node, DOWN * 2)
        one_text = Text("1", font_size=circle_font_size)
        one_text.move_to(one_node.get_center())
        self.play(Write(one_text), Write(one_node))

        div_one_line = Line(div_node, one_node)
        self.play(Write(div_one_line))

        # end t=6
        # start t=7
        time7_text = gen_time_text(7)
        self.play(TransformMatchingShapes(time6_text, time7_text))

        zero_node = Circle(radius=circle_radius, color=BLUE).next_to(
            div_node, DOWN + RIGHT
        )
        zero_text = Text("0", font_size=circle_font_size)
        zero_text.move_to(zero_node.get_center())
        self.play(Write(zero_text), Write(zero_node))

        div_zero_line = Line(div_node, zero_node)
        self.play(Write(div_zero_line))

        self.next_slide()

        # end t=7
        # fade the full tree out
        full_group = VGroup(
            root_node,
            root_text,
            mult_node,
            mult_text,
            div_node,
            div_text,
            x_node,
            x_text,
            y_node,
            y_text,
            one_node,
            one_text,
            zero_node,
            zero_text,
            root_mult_line,
            root_div_line,
            mult_x_line,
            mult_y_line,
            div_one_line,
            div_zero_line,
        )
        self.play(Unwrite(full_group), TransformMatchingShapes(time7_text, time0_text))

        # Onto grow
        # Like full but random chance to be a terminal anywhere
        # in the tree.
        grow_text = Text("Grow").to_edge(UR)
        self.play(
            TransformMatchingShapes(full_text, grow_text),
            time0_text.animate.next_to(grow_text, LEFT),
        )

        # start t=1
        time1_text.next_to(grow_text, LEFT)
        self.play(TransformMatchingShapes(time0_text, time1_text))

        root_node = Circle(radius=circle_radius, color=BLUE).shift(UP * 3 + RIGHT)
        root_text = Text("+", font_size=circle_font_size)
        root_text.move_to(root_node.get_center())

        self.play(Write(root_node), Write(root_text))

        # end t=1
        # start t=2
        time2_text.next_to(grow_text, LEFT)
        self.play(TransformMatchingShapes(time1_text, time2_text))

        x_node = Circle(radius=circle_radius, color=BLUE).next_to(
            root_node, DOWN + LEFT
        )
        x_text = Text("x", font_size=circle_font_size)
        x_text.move_to(x_node.get_center())
        self.play(Write(x_node), Write(x_text))

        root_x_line = Line(root_node, x_node)
        self.play(Write(root_x_line))

        # end t=2
        # start t=3
        time3_text.next_to(grow_text, LEFT)
        self.play(TransformMatchingShapes(time2_text, time3_text))

        minus_node = Circle(radius=circle_radius, color=BLUE).next_to(
            root_node, DOWN + RIGHT
        )
        minus_text = Text("-", font_size=circle_font_size)
        minus_text.move_to(minus_node.get_center())
        self.play(Write(minus_text), Write(minus_node))

        root_minus_line = Line(root_node, minus_node)
        self.play(Write(root_minus_line))

        # end t=3
        # start t=4 and t=5
        time5_text.next_to(grow_text, LEFT)
        self.play(TransformMatchingShapes(time3_text, time5_text))

        one_node = Circle(radius=circle_radius, color=BLUE).next_to(
            minus_node, DOWN * 2
        )
        one_text = Text("1", font_size=circle_font_size)
        one_text.move_to(one_node.get_center())
        minus_one_line = Line(minus_node, one_node)

        zero_node = Circle(radius=circle_radius, color=BLUE).next_to(
            minus_node, DOWN + RIGHT
        )
        zero_text = Text("0", font_size=circle_font_size)
        zero_text.move_to(zero_node.get_center())
        minus_zero_line = Line(minus_node, zero_node)

        self.play(Write(one_text), Write(one_node), Write(zero_node), Write(zero_text))
        self.play(Write(minus_one_line), Write(minus_zero_line))

        self.next_slide()

        # end t=4 and t=5
        grow_group = VGroup(
            root_node,
            root_text,
            x_node,
            x_text,
            minus_node,
            minus_text,
            one_node,
            one_text,
            zero_node,
            zero_text,
            root_x_line,
            root_minus_line,
            minus_one_line,
            minus_zero_line,
        )
        self.play(
            Unwrite(grow_group),
            Unwrite(time5_text),
            Unwrite(depth_text),
            Unwrite(grow_text),
        )

        # Need to mention ramped half and half somewhere
        # First half constructed with full then rest constructed
        # with grow
        rhandh_text = Text("Ramped Half-and-Half")
        rhandh_description_text = Text(
            "Generate 1st half with Full and 2nd half with Grow", font_size=20
        ).next_to(rhandh_text, DOWN)
        self.play(Write(rhandh_text), Write(rhandh_description_text))
        self.next_slide()
        self.play(FadeOut(rhandh_text), FadeOut(rhandh_description_text))

        # brings the pseudocode to the center of the screen
        pseudocode_transition(
            -1, -1, False, True, True, False, self, ptext, pause_after=False
        )


# Slide 7
# About ranking a population
class ECLoopRankPop(Slide):
    def construct(self):
        # ---------- Switch to rank population next
        ptext = pseudocode_transition(0, 1, True, False, True, True, self)

        # Will need to talk about fitness functions in this section.

        # Idea is to compress an arbitrary individual into a
        # rounded rectangle
        temp_group = VGroup()

        temp_root = Circle(radius=CIRCLE_RADIUS, color=BLUE).shift(UP * 3)
        temp_root_text = Text("+", font_size=CIRCLE_FONT_SIZE).move_to(
            temp_root.get_center()
        )
        temp_group.add(temp_root)
        temp_group.add(temp_root_text)

        temp_left = Circle(radius=CIRCLE_RADIUS, color=BLUE).next_to(
            temp_root, DOWN + LEFT
        )
        temp_left_text = Text("3", font_size=CIRCLE_FONT_SIZE).move_to(
            temp_left.get_center()
        )
        temp_group.add(temp_left)
        temp_group.add(temp_left_text)

        temp_right = Circle(radius=CIRCLE_RADIUS, color=BLUE).next_to(
            temp_root, DOWN + RIGHT
        )
        temp_right_text = Text("4", font_size=CIRCLE_FONT_SIZE).move_to(
            temp_right.get_center()
        )
        temp_group.add(temp_right)
        temp_group.add(temp_right_text)

        temp_root_left_line = Line(temp_root, temp_left)
        temp_root_right_line = Line(temp_root, temp_right)
        temp_group.add(temp_root_left_line)
        temp_group.add(temp_root_right_line)

        self.play(Write(temp_group))

        self.next_slide()

        # Take arbitrary individual and transform into rounded rectangle
        # Show different states of fitness for minimization/maximization problems
        # In animation: have fitness and individual explicitly shown in animation

        ind_text_size: int = 20

        ind_0 = RoundedRectangle(color=BLUE).scale(0.5).move_to(UP * 3)
        ind_0_text = Text("individual 0", font_size=ind_text_size)
        ind_0_text.add_updater(lambda x: x.move_to(temp_group.get_center()))
        # Display arbitrary individual as a rounded rectangle
        self.play(Transform(temp_group, ind_0), Write(ind_0_text))

        self.next_slide()

        ind_1 = RoundedRectangle(color=BLUE).scale(0.5).move_to(DOWN * 2 + LEFT * 1.5)
        ind_1_text = Text("individual 1", font_size=ind_text_size)
        ind_1_text.add_updater(lambda x: x.move_to(ind_1.get_center()))
        ind_2 = RoundedRectangle(color=BLUE).scale(0.5).move_to(DOWN * 2 + LEFT * -1.0)
        ind_2_text = Text("individual 2", font_size=ind_text_size)
        ind_2_text.add_updater(lambda x: x.move_to(ind_2.get_center()))
        ind_3 = RoundedRectangle(color=BLUE).scale(0.5).move_to(DOWN * 2 + LEFT * -3.5)
        ind_3_text = Text("individual 3", font_size=ind_text_size)
        ind_3_text.add_updater(lambda x: x.move_to(ind_3.get_center()))

        fitness_font_size: int = 30

        fitness_text = Text("Fitness:", font_size=fitness_font_size).move_to(
            DOWN + LEFT * 6
        )

        # temp group is now ind_0
        self.play(
            temp_group.animate.move_to(DOWN * 2 + LEFT * 4),
            Write(ind_1),
            Write(ind_1_text),
            Write(ind_2),
            Write(ind_2_text),
            Write(ind_3),
            Write(ind_3_text),
            Write(fitness_text),
        )

        self.next_slide()

        ind_0_fitness = Text("0.0", font_size=fitness_font_size)
        ind_0_fitness.add_updater(lambda x: x.next_to(temp_group, UP))
        ind_1_fitness = Text("23.3", font_size=fitness_font_size)
        ind_1_fitness.add_updater(lambda x: x.next_to(ind_1, UP))
        ind_2_fitness = Text("9999.0", font_size=fitness_font_size)
        ind_2_fitness.add_updater(lambda x: x.next_to(ind_2, UP))
        ind_3_fitness = Text("10.0", font_size=fitness_font_size)
        ind_3_fitness.add_updater(lambda x: x.next_to(ind_3, UP))

        self.play(
            Write(ind_0_fitness),
            Write(ind_1_fitness),
            Write(ind_2_fitness),
            Write(ind_3_fitness),
        )

        self.next_slide()

        # direction of search. Minimization or maximization
        direction_text = Text("Minimization")

        # transition to minimzation
        # ind_3 to ind_1
        # ind_2 to ind_3
        self.play(
            FadeIn(direction_text),
            ind_3.animate.move_to(DOWN * 2 + LEFT * 1.5),
            ind_1.animate.move_to(DOWN * 2 + LEFT * -1.0),
            ind_2.animate.move_to(DOWN * 2 + LEFT * -3.5),
            run_time=2,
        )

        self.next_slide()

        # transition to maximization
        self.play(
            temp_group.animate.move_to(DOWN * 2 + LEFT * -3.5),
            ind_1.animate.move_to(DOWN * 2 + LEFT * 1.5),
            ind_2.animate.move_to(DOWN * 2 + LEFT * 4),
            ind_3.animate.move_to(DOWN * 2 + LEFT * -1.0),
            Transform(direction_text, Text("Maximization")),
            run_time=2,
        )

        self.next_slide()

        # move onto select parents slides

        self.play(
            Unwrite(temp_group),
            Unwrite(ind_0_text),
            Unwrite(ind_0_fitness),
            Unwrite(ind_1),
            Unwrite(ind_1_text),
            Unwrite(ind_1_fitness),
            Unwrite(ind_2),
            Unwrite(ind_2_text),
            Unwrite(ind_2_fitness),
            Unwrite(ind_3),
            Unwrite(ind_3_text),
            Unwrite(ind_3_fitness),
            Unwrite(fitness_text),
            FadeOut(direction_text),
        )

        pseudocode_transition(
            -1, -1, False, True, True, False, self, ptext, pause_after=False
        )


# Slide 8
class ECLoopParentSelect(Slide):
    def construct(self):
        # Now that population is ranked, enter while loop.
        # Going to be a quick transition into *select parents for reproduction*

        # TODO: Switch these out to pseudocode_transition function.
        self.play(
            pseudocode_mobject.animate.center().scale(2.0),
        )
        # highlights the while loop
        self.play(
            pseudocode_mobject[:42].animate.set_color(WHITE),
            pseudocode_mobject[42:70].animate.set_color(BLUE),
        )
        self.next_slide()
        # highlights the `select parents for recombination` section
        self.play(
            pseudocode_mobject[:70].animate.set_color(WHITE),
            pseudocode_mobject[70:99].animate.set_color(BLUE),
        )
        self.next_slide()
        # shrinks the pseudocode text box so can start on the
        # parent selection portion
        self.play(
            pseudocode_mobject.animate.scale(0.5).to_edge(UL),
        )

        # Show the individuals again for roulette wheel/fitness proportionate selection
        # Have chosen four random individuals from the popualation

        individuals: list[RoundedRectangle] = []
        labels = []
        fitness_labels = []

        positions = [
            DOWN * 2 + LEFT * 4.0,
            DOWN * 2 + LEFT * 1.5,
            DOWN * 2 + LEFT * -1.0,
            DOWN * 2 + LEFT * -3.5,
        ]
        names = [f"individiual {x}" for x in [0, 1, 2, 3]]
        fitness_scores = [f"{x}.0" for x in [1, 2, 3, 4]]

        for n in range(len(positions)):
            rrect: RoundedRectangle = (
                RoundedRectangle(color=BLUE).scale(0.5).move_to(positions[n])
            )
            label = Text(names[n], font_size=ind_text_size)
            label.add_updater(lambda m, r=rrect: m.move_to(r.get_center()))
            fitness = Text(fitness_scores[n], font_size=fitness_font_size)
            fitness.add_updater(lambda m, r=rrect: m.next_to(r, UP))

            individuals.append(rrect)
            labels.append(label)
            fitness_labels.append(fitness)

        fitness_text = Text("Fitness:", font_size=fitness_font_size).move_to(
            DOWN + LEFT * 6
        )

        selection_group = VGroup(*individuals, *labels, *fitness_labels, fitness_text)

        # end selection group creation
        # May need to copy selection_group

        selection_text = Text("Fitness Proportionate").to_edge(UR)

        self.play(Write(selection_group), Write(selection_text), run_time=2)

        # fitness proportionate takes selects one parent from the population
        # proportional to their fitness. Is ran multiple times to select the
        # desired amount of parents. Repeats are allowed.

        selection_percs = ["10%", "20%", "30%", "40%"]
        sel_percs_mobjects = []
        # TODO: add updaters for selection percentages to each invididual
        for n in range(len(individuals)):
            temp_text = Text(selection_percs[n], font_size=fitness_font_size)
            temp_text.add_updater(lambda x, ind=individuals[n]: x.next_to(ind, UP * 3))
            sel_percs_mobjects.append(temp_text)

        # This isn't perfectly aligned horizontally
        # TODO: Fix this later. I'm going to continue for now.
        percentage_text = Text("% Chance:", font_size=fitness_font_size).next_to(
            fitness_text, UP
        )
        percs_group = VGroup(*sel_percs_mobjects, percentage_text)

        self.play(Write(percs_group))

        self.next_slide()

        # Onto tournament selection
        # Tournament selection pulled from https://en.wikipedia.org/wiki/Tournament_selection
        # Also 4 random individuals from the population
        #   Tournament size being 4 here
        self.play(
            Unwrite(percs_group),
            selection_text.animate.become(Text("Tournament").move_to(selection_text)),
        )

        self.play(Unwrite(selection_group))

        # basically, this just takes the best individual from a tournament and returns in.
        # The tournament is randomly selected from the population.
        # This is a presentation. Do I need to animate how this works?

        # Onto generate children from selected parents
        self.next_slide()
        self.play(pseudocode_mobject.animate.center().scale(2.0))
        self.play(
            pseudocode_mobject[:99].animate.set_color(WHITE),
            pseudocode_mobject[99:134].animate.set_color(BLUE),
        )
        self.next_slide()
        self.play(
            pseudocode_mobject.animate.scale(0.5).to_edge(UL),
        )

        # Going to have some sort of tree based recombination.
        # Will probably steal from the field guide
        # https://faculty.washington.edu/seattle/GA-2008/FieldGuideGP.pdf
        # Page 16 (30 if online)

        # Will probably need to have a different size tree for this :(
        def create_node(
            text: str, radius=circle_radius, color=BLUE, font_size=circle_font_size
        ) -> VGroup:
            """
            Creates a circle and text, adds an updater to text to the center of the
            circle
            """
            node = Circle(radius=radius, color=color)
            text = Text(text, font_size=font_size)
            text.add_updater(lambda x: x.move_to(node.get_center()))
            return VGroup(node, text)

        # parent 0
        p0_root = create_node("+", color=YELLOW)
        p0_plus_node = create_node("+", color=RED)  # left child of root node
        p0_three_node = create_node("3", color=YELLOW)  # right child of root node
        p0_x_node = create_node("x", color=RED)  # left child of plus node
        p0_y_node = create_node("y", color=RED)  # right child of root node
        line_p0_root_p0_plus = Line(
            p0_root, p0_plus_node
        )  # This one will need to be left out
        line_p0_root_p0_three = Line(p0_root, p0_three_node)
        line_p0_plus_p0_x = Line(p0_plus_node, p0_x_node)
        line_p0_plus_p0_y = Line(p0_plus_node, p0_y_node)
        p0_comb = VGroup(p0_root, p0_three_node, line_p0_root_p0_three)
        p0_delete = VGroup(
            p0_plus_node, p0_x_node, p0_y_node, line_p0_plus_p0_x, line_p0_plus_p0_y
        )

        # TODO: create lines for parent 1 and place them on the screen properly
        # parent 1
        p1_root = create_node("*", color=RED)
        p1_plus = create_node("+", color=RED)  # left child of root node
        p1_y = create_node("y", color=RED)  # left child of plus node
        p1_one = create_node("1", color=RED)
        pl_div = create_node("/", color=YELLOW)
        p1_x = create_node("x", color=YELLOW)
        p1_two = create_node("2", color=YELLOW)
        p1_comb = VGroup(pl_div, p1_x, p1_two)
        pl_delete = VGroup(
            p1_root,
            p1_plus,
            p1_y,
            p1_one,
        )
