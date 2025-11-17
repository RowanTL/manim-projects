from manim import *
from manim_slides.slide import Slide

config.frame_rate = 15


# A slide that gives a general overview on how actix web actually works
class OverviewSlide(Slide):
    def construct(self):
        # Scene setup
        # ...

        # Definitions
        pi_user: SVGMobject = SVGMobject("assets/PiCreatures_erm.svg").to_edge(LEFT)

        box_scale: float = 0.7
        http_server_box: Square = Square(pi_user.width).to_edge(RIGHT)
        http_server_text: Text = (
            Text("HttpServer").next_to(http_server_box, UP * 0.5).scale(box_scale)
        )
        app_text: Text = Text("App").move_to(http_server_box).scale(box_scale)

        arrow_text_scale = 0.5
        http_request_arrow: Arrow = Arrow(
            start=pi_user.get_corner(DR),
            end=http_server_box.get_corner(DL),
            color=BLUE,
            stroke_width=2,
        )
        http_request_text: Text = (
            Text("impl FromRequest")
            .next_to(http_request_arrow, DOWN * 0.1)
            .scale(arrow_text_scale)
        )

        http_response_arrow: Arrow = Arrow(
            end=pi_user.get_corner(UR),
            start=http_server_box.get_corner(UL),
            color=BLUE,
            stroke_width=2,
        )
        http_response_text: Text = (
            Text("impl Responder")
            .next_to(http_response_arrow, UP * 0.1)
            .scale(arrow_text_scale)
        )

        basic_http_request_text: Text = (
            Text("HttpRequest").move_to(http_request_text).scale(arrow_text_scale)
        )
        basic_http_response_text: Text = (
            Text("HttpResponse").move_to(http_response_text).scale(arrow_text_scale)
        )

        # Animations
        self.play(
            FadeIn(pi_user),
            FadeIn(http_server_box),
            FadeIn(http_server_text),
            FadeIn(app_text),
        )
        self.next_slide()
        self.play(
            Write(http_request_arrow),
            Write(http_request_text),
            Write(http_response_arrow),
            Write(http_response_text),
            run_time=2,
        )
        self.next_slide()
        self.play(
            Transform(http_request_text, basic_http_request_text),
            Transform(http_response_text, basic_http_response_text),
            run_time=2,
        )
        self.next_slide()
        self.play(
            FadeOut(pi_user),
            FadeOut(http_server_box),
            FadeOut(http_server_text),
            FadeOut(app_text),
            Unwrite(http_request_arrow),
            Unwrite(http_request_text),
            Unwrite(http_response_arrow),
            Unwrite(http_response_text),
        )
        self.wait(0.5)
        self.next_slide()


# All of these types implement Responder
class ResponderSlide(Slide):
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

        self.next_slide()
        self.play(
            Unwrite(responder_text),
            Unwrite(cow_text),
            Unwrite(vec_u8_text),
            Unwrite(http_response_text),
            Unwrite(arrows),
        )
        self.wait(0.5)
        self.next_slide()


# Need a slide describing user HttpRequest and Response
# Basically go over responder implementation and how to do it
# https://docs.rs/actix-web/latest/actix_web/trait.Responder.html
