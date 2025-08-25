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
        self.play(
            square.animate.set_fill(PINK, opacity=0.5)
        )

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
        text0 = Text("\"...it is now clear that the hybrids form seeds having", font_size=font_size, slant=ITALIC)
        text1 = Text("one or other of the two differentiating characters, and of these one-half", font_size=font_size, slant=ITALIC)
        text2 = Text("develop again the hybrid form...\"", font_size=font_size, slant=ITALIC)
        gregor_mendel = Text("-Gregor Mendel", font_size=font_size + 10, weight=BOLD, color=BLUE)
        
        # orient the text Mobjects
        text0.shift(UP * 1.5)
        text1.next_to(text0, DOWN)
        text2.next_to(text1, DOWN)
        gregor_mendel.next_to(text2, DOWN)

        self.play(Write(text0), Write(text1), Write(text2), run_time=3.0)
        self.play(Write(gregor_mendel), run_time=2.0)

class TitleSlide(Scene):
    def construct(self):
        title = Text("An Overview of Genetic Programming: Tree-Based GP and PushGP", font_size=30)
        name = Text("Rowan Torbitzky-Lane", font_size=25, color=BLUE)

        name.next_to(title, DOWN)

        self.play(Write(title), run_time=3.0)
        self.play(Write(name), run_time=2.0)

# Corresponds to slide 2 in brainstorming notes
class GeneticProgrammingDescription(Scene):
    def construct(self):
        pass