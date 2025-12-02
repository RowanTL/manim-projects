from typing import Final

from manim import *
from manim_slides.slide import Slide

config.frame_rate = 15

GLOBAL_SCALE: Final[float] = 0.75


# A slide that gives a general overview on how actix web actually works
class OverviewSlide(Slide):
    def construct(self):
        # Scene setup
        # ...

        # Definitions
        pi_user: SVGMobject = (
            SVGMobject("assets/PiCreatures_erm.svg").to_corner(UL).scale(GLOBAL_SCALE)
        )

        # user sends request to actix http server
        http_server_text: Text = (
            Text("HttpServer").to_edge(UP + RIGHT * 2).scale(GLOBAL_SCALE)
        )
        pi_http_server_arrow: Arrow = Arrow(
            pi_user.get_right(), http_server_text.get_left()
        )

        # The http server takes an App factory
        app_text: Text = (
            Text("App").next_to(http_server_text, DOWN * 4).scale(GLOBAL_SCALE)
        )
        http_server_app_arrow: Arrow = Arrow(
            http_server_text.get_bottom(), app_text.get_top()
        )

        # The App holds many different services
        services_group: VGroup = (
            VGroup(
                Text("Service 1").scale(GLOBAL_SCALE),
                Text("Service 2").scale(GLOBAL_SCALE),
            )
            .arrange(RIGHT, buff=0.5)
            .next_to(app_text, DOWN * 4)
        )
        app_services_arrows: VGroup = VGroup()
        for service in services_group:
            app_services_arrows.add(Arrow(app_text.get_bottom(), service.get_top()))

        ## Consolidate services into one `service(s)` text
        service_s_text: Text = (
            Text("Service(s)").scale(GLOBAL_SCALE).move_to(services_group.get_center())
        )
        app_service_s_arrow: Arrow = Arrow(
            app_text.get_bottom(), service_s_text.get_top()
        )

        # The services point to different routes
        routes_group: VGroup = (
            VGroup(
                Text("Route 1").scale(GLOBAL_SCALE), Text("Route 2").scale(GLOBAL_SCALE)
            )
            .arrange(RIGHT, buff=0.5)
            .next_to(service_s_text, DOWN * 4)
        )
        service_s_routes_arrows: VGroup = VGroup()
        for route in routes_group:
            service_s_routes_arrows.add(
                Arrow(service_s_text.get_bottom(), route.get_top())
            )

        # Consolidate multiple routes into one
        route_s_text: Text = (
            Text("Route(s)").scale(GLOBAL_SCALE).move_to(routes_group.get_center())
        )
        service_s_route_s_arrow: Arrow = Arrow(
            service_s_text.get_bottom(), route_s_text.get_top()
        )

        # Handlers take in request defined by routes
        handler_text: Text = (
            Text("Handler").scale(GLOBAL_SCALE).next_to(route_s_text, DOWN * 4)
        )
        route_s_handler_arrow: Arrow = Arrow(
            route_s_text.get_bottom(), handler_text.get_top()
        )

        # Extractors extract data from the request
        extractor_text: Text = (
            Text("Extractor").scale(GLOBAL_SCALE).next_to(handler_text, LEFT * 4)
        )
        handler_to_extractor_arrow: Arrow = Arrow(
            handler_text.get_bottom(), extractor_text.get_bottom(), path_arc=-PI / 2
        )

        # Extractors "send" data back to the handler.
        extractor_to_handler_arrow: Arrow = Arrow(
            extractor_text.get_right(), handler_text.get_left()
        )

        # Have the handler send a response to the pi creature
        # (The pi creature is now happy because of said response)
        handler_to_user_arrow: Arrow = Arrow(
            handler_text.get_corner(UL), pi_user.get_corner(DR)
        )
        happy_pi_user: SVGMobject = (
            SVGMobject("assets/PiCreatures_hooray.svg")
            .to_corner(UL)
            .scale(GLOBAL_SCALE)
        )

        # Animations
        self.play(FadeIn(pi_user))
        self.wait(0.05)
        self.next_slide()
        self.play(Write(http_server_text), Write(pi_http_server_arrow))
        self.wait(0.05)
        self.next_slide()
        self.play(Write(app_text), Write(http_server_app_arrow))
        self.wait(0.05)
        self.next_slide()
        # lag_ratio=0 writes all submobjects at the same time
        self.play(
            Write(services_group, lag_ratio=0), Write(app_services_arrows, lag_ratio=0)
        )
        self.wait(0.05)
        self.next_slide()
        # Note the similar variable names here.
        self.play(
            ReplacementTransform(services_group, service_s_text),
            ReplacementTransform(app_services_arrows, app_service_s_arrow),
        )
        self.wait(0.5)
        self.next_slide()

        self.play(
            Write(routes_group, lag_ratio=0),
            Write(service_s_routes_arrows, lag_ratio=0),
        )
        self.wait(0.05)
        self.next_slide()

        self.play(
            ReplacementTransform(routes_group, route_s_text),
            ReplacementTransform(service_s_routes_arrows, service_s_route_s_arrow),
        )
        self.wait(0.5)
        self.next_slide()

        self.play(
            Write(handler_text),
            Write(route_s_handler_arrow),
        )
        self.wait(0.05)
        self.next_slide()

        self.play(Write(extractor_text), Write(handler_to_extractor_arrow))
        self.wait(0.05)
        self.next_slide()

        self.play(Write(extractor_to_handler_arrow))
        self.wait(0.05)
        self.next_slide()

        self.play(Write(handler_to_user_arrow), Transform(pi_user, happy_pi_user))
        self.wait(0.05)
        self.next_slide()

        self.play(
            FadeOut(pi_user),
            Unwrite(http_server_text),
            Unwrite(pi_http_server_arrow),
            Unwrite(app_text),
            Unwrite(http_server_app_arrow),
            Unwrite(service_s_text),
            Unwrite(app_service_s_arrow),
            Unwrite(route_s_text),
            Unwrite(service_s_route_s_arrow),
            Unwrite(handler_text),
            Unwrite(route_s_handler_arrow),
            Unwrite(extractor_text),
            Unwrite(handler_to_extractor_arrow),
            Unwrite(extractor_to_handler_arrow),
            Unwrite(handler_to_user_arrow),
        )
        self.wait(0.05)


# Application Slide
# Move the App from the previous slide to the top of the screen here later
class ApplicationSlide(Slide):
    def construct(self):
        # Scene setup
        # ...

        # Definitions
        app_text: Text = Text("actix_web::App").to_edge(UP)

        scope_text: Text = (
            Text("Scope", color=YELLOW).to_edge(LEFT).shift(RIGHT + DOWN * 1.5)
        )

        table_scale: float = 0.8
        routes_table: Table = (
            Table(
                [
                    ["Route", "Request Type"],
                    ["/index_html", "GET"],
                    ["/update_user", "POST"],
                    ["/delete_user", "DELETE"],
                    ["/head_requst", "HEAD"],
                ],
                include_outer_lines=True,
            )
            .scale(table_scale)
            .shift(DOWN)
        )

        # Eventually shift RIGHT by 2, color similar routes, then group them to explain
        # how scope works
        scope_table: Table = (
            Table(
                [["Route"], ["/users"], ["/users/{id}"], ["/dashboard"], ["/logs"]],
                include_outer_lines=True,
            )
            .scale(table_scale)
            .shift(DOWN)
        )

        api_v1_brace: Brace = Brace(
            scope_table.get_rows()[1:3], direction=LEFT, color=BLUE
        )
        admin_brace: Brace = Brace(
            scope_table.get_rows()[3:5], direction=LEFT, color=RED
        )
        api_v1_text: Text = Text("/api/v1", color=BLUE).scale(table_scale)
        admin_text: Text = Text("/admin", color=RED).scale(table_scale)

        # Animations
        self.play(Write(app_text))
        self.next_slide()
        self.play(Write(routes_table))
        self.next_slide()
        self.play(Unwrite(routes_table))
        self.play(Write(scope_table))
        self.next_slide()
        self.play(
            scope_table.animate.shift(RIGHT * 2),
        )
        # reposition the braces and associated text for the next animation
        api_v1_brace.next_to(scope_table.get_rows()[1:3], LEFT * 3.5)
        admin_brace.next_to(scope_table.get_rows()[3:5], LEFT * 3.5).set_x(
            api_v1_brace.get_x()  # makes the braces line up
        )
        api_v1_text.next_to(api_v1_brace, LEFT)
        admin_text.next_to(admin_brace, LEFT)
        # back to the animations
        self.play(
            scope_table.get_rows()[1:3].animate.set_color(BLUE),
            scope_table.get_rows()[3:5].animate.set_color(RED),
            Write(api_v1_brace),
            Write(admin_brace),
            Write(api_v1_text),
            Write(admin_text),
            Write(scope_text),
        )  # numbers are the similar routes to be scoped later
        self.wait(0.5)
        self.next_slide()
        self.play(
            Unwrite(app_text),
            Unwrite(scope_table, lag_ratio=0.02),
            Unwrite(api_v1_brace),
            Unwrite(admin_brace),
            Unwrite(api_v1_text),
            Unwrite(admin_text),
            Unwrite(scope_text),
        )
        self.wait(0.25)
        self.next_slide()


# A slide for explaining extractors (impl FromRequest)
class ExtractorSlide(Slide):
    def construct(self):
        # Scene setup
        # ...

        # Definitions
        impl_from_request_text: Text = Text("impl FromRequest").to_edge(UP)

        extractor_scale: float = 0.6
        extractor_table: Table = (
            Table(
                [
                    ["web::Path<T>", "Extracts path information (/users/{id})"],
                    [
                        "web::Query<T>",
                        "Extracts query parameters info: \n(https://website.com&parameter1=value)",
                    ],
                    [
                        "web::Json<T>",
                        "Extracts json from request's body \n(Extraction configurable)",
                    ],
                    [
                        "web::Form<T>",
                        'Extract form data when \n"x-www-form-urlencoded" \ncontent type header passed',
                    ],
                    ["web::Bytes", "Extract the bytes of the request directly"],
                ],
                include_outer_lines=True,
            )
            .scale(extractor_scale)
            .to_edge(DOWN)
        )
        # Animations
        self.play(Write(impl_from_request_text))
        self.next_slide()
        self.play(Write(extractor_table))
        self.next_slide()
        self.play(
            Unwrite(extractor_table), Unwrite(impl_from_request_text), run_time=0.5
        )
        self.wait(0.25)


# All of these types implement Responder
class ResponderSlide(Slide):
    def construct(self):
        # Scene setup
        # ...

        # Definitions
        responder_text_size: int = 60
        responder_text: Text = Text(
            "impl Responder", font_size=responder_text_size
        ).to_edge(UP)

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
