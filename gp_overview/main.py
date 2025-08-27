from manim import *


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.3)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.rotate(PI / 4)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.set_fill(PINK, opacity=0.5)

        square.next_to(circle, RIGHT, buff=0.5)
        self.play(Create(circle), Create(square))


class AnimatedSquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
        self.play(Transform(square, circle))
        self.play(square.animate.set_fill(PINK, opacity=0.5))


class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            left_square.animate.rotate(PI), Rotate(right_square, angle=PI), run_time=2
        )
        self.wait()


class HelloWorld(Scene):
    def construct(self):
        text = Text("Hello World", font_size=144)
        # How to slow the .play function down?
        self.play(Write(text), run_time=2.0)
        self.wait(3)


class TwoTransform(Scene):
    def transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(Transform(a, b))
        self.play(Transform(a, c))
        self.play(FadeOut(a))

    def replacement_transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(ReplacementTransform(a, b))
        self.play(ReplacementTransform(b, c))
        self.play(FadeOut(c))

    # Use transform a majority of the time
    def construct(self):
        self.transform()
        self.wait(0.5)
        self.replacement_transform()


class Shapes(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        circle.shift(LEFT)
        square.shift(UP)
        triangle.shift(RIGHT)

        self.add(circle, square, triangle)
        self.wait(1)


class MobjectPlacement(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        circle.move_to(LEFT * 2)
        square.next_to(circle, LEFT)
        triangle.align_to(circle, LEFT)

        self.add(circle, square, triangle)
        self.wait(1)


# Start of GP presentation


class QuoteSlide(Scene):
    def construct(self):
        font_size = 25

        # quote from: https://en.wikisource.org/wiki/Mendel%27s_Principles_of_Heredity;_a_Defence/Chapter_2
        # Paper Title: Experiments in Plant-Hybridisation
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
        self.play(Write(gregor_mendel), run_time=2.0)


class TitleSlide(Scene):
    def construct(self):
        title = Text(
            "An Overview of Genetic Programming: Tree-Based GP and PushGP", font_size=30
        )
        name = Text("Rowan Torbitzky-Lane", font_size=25, color=BLUE)

        name.next_to(title, DOWN)

        self.play(Write(title), run_time=3.0)
        self.play(Write(name), run_time=2.0)


# Corresponds to slide 2 in brainstorming notes
class GeneticProgrammingDescription(Scene):
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

        self.play(Write(full_code), run_time=3)
        self.play(
            Write(print_circle),
            Write(minus_circle),
            Write(four_minus_circle),
            Write(plus_circle),
            Write(left_one_circle),
            Write(right_two_circle),
            run_time=3,
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
            run_time=2,
        )

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
        self.play(
            Transform(print_text, log_text),
            TransformMatchingShapes(full_mult_text, full_log_text),
        )
        self.play(
            Transform(right_two_text, big_num_text),
            TransformMatchingShapes(full_log_text, full_big_num_text),
        )


class ECLoop(Scene):
    def construct(self):
        circle_radius: float = 0.7
        circle_font_size: int = 30

        # EC loop pseudocode
        # see the best possible individual in minimization problems personally
        pseudocode: str = """
initialize population randomly
rank population
while (loop count < threshold) do
    select parents for reproduction
    generate children from selected parents
    evaluate children
    select individuals for the next population
    loop counter++
"""
        pseudocode_mobject = Text(pseudocode, font_size=30)
        self.play(Write(pseudocode_mobject))
        self.play(
            pseudocode_mobject.animate.scale(0.5).to_edge(UL),
        )
        self.play(pseudocode_mobject[:28].animate.set_color(BLUE))

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

        y_node = Circle(radius=circle_radius, color=BLUE).next_to(
            mult_node, DOWN * 2
        )
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

        one_node = Circle(radius=circle_radius, color=BLUE).next_to(
            div_node, DOWN * 2
        )
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
            div_zero_line
        )
        self.play(Unwrite(full_group), TransformMatchingShapes(time7_text, time0_text))

        # Onto grow
        # Like full but random chance to be a terminal anywhere
        # in the tree.
        grow_text = Text("Grow").to_edge(UR)
        self.play(
            TransformMatchingShapes(full_text, grow_text),
            time0_text.animate.next_to(grow_text, LEFT)
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

        self.play(
            Write(one_text), 
            Write(one_node),
            Write(zero_node),
            Write(zero_text)
        )
        self.play(
            Write(minus_one_line),
            Write(minus_zero_line)
        )

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
            minus_zero_line
        )
        self.play(Unwrite(grow_group), 
                  Unwrite(time5_text),
                  Unwrite(depth_text),
                  Unwrite(grow_text),
        )

        # Need to mention ramped half and half somewhere
        # First half constructed with full then rest constructed
        # with grow
        rhandh_text = Text("Ramped Half-and-Half")
        rhandh_description_text = Text("Generate 1st half with Full and 2nd half with Grow", font_size=20).next_to(rhandh_text, DOWN)
        self.play(Write(rhandh_text), Write(rhandh_description_text))
        # probably put a slide split here for later
        self.play(FadeOut(rhandh_text), FadeOut(rhandh_description_text))

        #---------- Switch to rank population next
        self.play(
            pseudocode_mobject.animate.center().scale(2.0),
        )
        # slide split here
        self.play(
            pseudocode_mobject[:28].animate.set_color(WHITE),
            pseudocode_mobject[28:42].animate.set_color(BLUE)    
        )
        # slide split here
        self.play(
            pseudocode_mobject.animate.scale(0.5).to_edge(UL),
        )

        # Will need to talk about fitness functions in this section.
        
        # Idea is to compress an arbitrary individual into a
        # rounded rectangle
        temp_group = VGroup()
        
        temp_root = Circle(radius=circle_radius, color=BLUE).shift(UP * 3)
        temp_root_text = Text("+", font_size=circle_font_size).move_to(temp_root.get_center())
        temp_group.add(temp_root)
        temp_group.add(temp_root_text)
        
        temp_left = Circle(radius=circle_radius, color=BLUE).next_to(temp_root, DOWN + LEFT)
        temp_left_text = Text("3", font_size=circle_font_size).move_to(temp_left.get_center())
        temp_group.add(temp_left)
        temp_group.add(temp_left_text)

        temp_right = Circle(radius=circle_radius, color=BLUE).next_to(temp_root, DOWN + RIGHT)
        temp_right_text = Text("4", font_size=circle_font_size).move_to(temp_right.get_center())
        temp_group.add(temp_right)
        temp_group.add(temp_right_text)

        temp_root_left_line = Line(temp_root, temp_left)
        temp_root_right_line = Line(temp_root, temp_right)
        temp_group.add(temp_root_left_line)
        temp_group.add(temp_root_right_line)

        self.play(Write(temp_group))

        # Take arbitrary individual and transform into rounded rectangle
        # Show different states of fitness for minimization/maximization problems
        # In animation: have fitness and individual explicitly shown in animation

        ind_0 = RoundedRectangle(color=BLUE).scale(0.5).move_to(DOWN + LEFT * 5)

        self.play(Transform(temp_group, ind_0))
