from manim import *
from manim_slides.slide.manim import Slide


# Slide 0
class IntroSlide(Slide):
    def construct(self):
        # declarations
        title_text: Text = Text("Dissuading E-Cigarette Use").to_edge(UP)
        name_text: Text = Text("Rowan Torbitzky-Lane").scale(0.5).set_color(BLUE)

        # animations
        self.play(Write(title_text))

        self.next_slide()

        self.play(Write(name_text))

        self.next_slide()

        self.play(Unwrite(title_text), Unwrite(name_text), run_time=0.5)
        self.wait(0.25)

        self.next_slide()


# Slide 1
class WhyProblemSlide(Slide):
    def construct(self):
        # declarations
        juul_pod_image: ImageMobject = ImageMobject("images/juul_pod.jpg").scale(2.0)
        cigarette_image: SVGMobject = SVGMobject("images/cigarette.svg").scale(0.1)

        # animations
        self.play(FadeIn(juul_pod_image))

        self.next_slide()

        self.play(juul_pod_image.animate.to_corner(LEFT))
        self.play(Write(cigarette_image))
