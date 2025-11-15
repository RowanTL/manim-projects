from manim import *
from manim_slides.slide import Slide

config.frame_rate = 15

# Need a slide describing user HttpRequest and Response
# Basically go over responder implementation and how to do it
# https://docs.rs/actix-web/latest/actix_web/trait.Responder.html


# All of these types implement Responder
class ResponderSlide(Scene):
    def construct(self):
        # Scene setup
        # ...

        # Definitions
        responder_text_size: int = 60
        responder_text: Text = Text("Responder", font_size=responder_text_size).to_edge(
            UP
        )

        implementors_text_size: int = 30
        cow_text: Text = (
            Text("Cow<'_, str>", font_size=implementors_text_size)
            .to_edge(LEFT)
            .shift(DOWN * 2)
        )
        vec_u8_text: Text = Text("Vec<u8>", font_size=implementors_text_size).shift(
            DOWN * 2
        )
        http_response_text: Text = (
            Text("HttpResponse", font_size=implementors_text_size)
            .to_edge(RIGHT)
            .shift(DOWN * 2)
        )

        arrows: VGroup = VGroup(
            Arrow(end=responder_text.get_bottom(), start=cow_text.get_top()),
            Arrow(end=responder_text.get_bottom(), start=vec_u8_text.get_top()),
            Arrow(end=responder_text.get_bottom(), start=http_response_text.get_top()),
        ).set_color(BLUE)

        # Animations
        self.play(
            Write(responder_text),
            Write(cow_text),
            Write(vec_u8_text),
            Write(http_response_text),
        )
        self.play(Write(arrows), run_time=2)
        self.wait(2)
