from typing import ParamSpec

from manim import *
from manim_slides.slide.manim import Slide


# Slide 0
class IntroSlide(Slide):
    def construct(self):
        # declarations
        title_text: Paragraph = Paragraph(
            "Dissuading E-Cigarette Use",
            "in Adolescents and Young Adults",
            alignment="center",
        ).to_edge(UP)
        name_text: Text = Text("Rowan Torbitzky-Lane").scale(0.5).set_color(BLUE)

        # animations
        self.next_slide()
        self.wait(0.25)
        self.next_slide()

        self.play(Write(name_text))

        self.next_slide()

        self.play(Write(title_text))

        self.next_slide()

        self.play(Unwrite(title_text), Unwrite(name_text), run_time=0.5)
        self.wait(0.25)

        self.next_slide()


# Slide 1
class WhyProblemSlide(Slide):
    def construct(self):
        # (most) declarations
        why_text: Text = Text("Why?").set_color(BLUE).to_edge(UP)
        juul_pod_image: ImageMobject = ImageMobject("images/juul_pod.jpg").scale(2.0)
        cigarette_image: SVGMobject = SVGMobject("images/cigarette.svg").scale(0.1)
        cigarette_list: list[SVGMobject] = [
            SVGMobject("images/cigarette.svg").scale(0.1) for _ in range(20)
        ]
        cigarette_vgroup: VGroup = VGroup(*cigarette_list)
        cigarette_vgroup.arrange_in_grid(rows=5, cols=4, buff=0.2)

        hs_total_rect: Rectangle = Rectangle(
            width=10, height=1, color=WHITE, fill_opacity=0.2
        ).shift(UP)
        hs_vaping_rect: Rectangle = (
            Rectangle(width=0.78, height=1, color=RED, fill_opacity=0.2)
            .shift(UP)
            .align_to(hs_total_rect, LEFT)
        )
        hs_text: Text = Text("% High Schoolers").scale(0.75).next_to(hs_total_rect, UP)
        hs_perc_text: Text = (
            Text("7.8%").scale(0.75).next_to(hs_total_rect, LEFT).set_color(RED)
        )
        hs_rect_group: VGroup = VGroup(hs_total_rect, hs_vaping_rect, hs_perc_text)

        # middle school (ms)
        ms_total_rect: Rectangle = Rectangle(
            width=10, height=1, color=WHITE, fill_opacity=0.2
        ).shift(DOWN * 2)
        ms_vaping_rect: Rectangle = (
            Rectangle(width=0.35, height=1, color=RED, fill_opacity=0.2)
            .shift(DOWN * 2)
            .align_to(ms_total_rect, LEFT)
        )
        ms_text: Text = (
            Text("% Middle Schoolers").scale(0.75).next_to(ms_total_rect, UP)
        )
        ms_perc_text: Text = (
            Text("3.5%").scale(0.75).next_to(ms_total_rect, LEFT).set_color(RED)
        )
        ms_rect_group: VGroup = VGroup(ms_total_rect, ms_vaping_rect, ms_perc_text)
        rice_citation: Text = (
            Text(
                "Rice, Timothy R., et al. “Adolescent Vaping: Revisiting Developmental Perspectives on Adolescent Substance Use in the Digital Age.” The Psychoanalytic Study of the Child, Taylor & Francis, July 2025, pp. 1–19, https://doi.org/10.1080/00797308.2025.2533680."
            )
            .set_color(GREY)
            .scale(0.15)
            .to_edge(DOWN)
        )

        # animations
        self.play(Write(why_text))

        self.next_slide()

        self.play(FadeIn(juul_pod_image))

        self.next_slide()

        self.play(juul_pod_image.animate.to_corner(LEFT))
        juul_pod_cigarette_image_arrow: Arrow = Arrow(
            start=juul_pod_image.get_right(), end=cigarette_image.get_left()
        )
        question_mark_text: Text = (
            Text("nicotine amount?")
            .scale(0.5)
            .next_to(juul_pod_cigarette_image_arrow, UP)
        )
        self.play(
            Write(cigarette_image),
            Write(juul_pod_cigarette_image_arrow),
            Write(question_mark_text),
            Write(rice_citation),
        )

        self.next_slide()

        cigarette_vgroup.next_to(juul_pod_cigarette_image_arrow, RIGHT)
        self.play(
            Transform(cigarette_image, cigarette_vgroup),
            Transform(question_mark_text, Text("20").move_to(question_mark_text)),
        )

        self.next_slide()

        self.play(
            FadeOut(juul_pod_image),
            Unwrite(juul_pod_cigarette_image_arrow),
            Unwrite(question_mark_text),
            Unwrite(cigarette_image),
            run_time=0.5,
        )
        self.wait(0.25)

        # now explain the ratios of hs smokers and middle school smokers
        self.next_slide()

        # These % look small but then the numbers come after
        self.play(
            Write(hs_text), Write(hs_rect_group), Write(ms_text), Write(ms_rect_group)
        )

        self.next_slide()

        # Now replace the %'s with numbers
        self.play(
            Transform(
                hs_text, Text("# of High Schoolers").move_to(hs_text).scale(0.75)
            ),
            Transform(
                ms_text, Text("# of Middle Schoolers").move_to(ms_text).scale(0.75)
            ),
            Transform(
                hs_rect_group,
                Text("1.2 million").move_to(hs_total_rect).set_color("RED"),
            ),
            Transform(
                ms_rect_group,
                Text("410,000").move_to(ms_total_rect).set_color("RED"),
            ),
        )
        self.wait(0.25)

        # clean up the scene
        self.next_slide()

        self.play(
            Unwrite(ms_rect_group),
            Unwrite(hs_rect_group),
            Unwrite(hs_text),
            Unwrite(ms_text),
            Unwrite(why_text),
            Unwrite(rice_citation),
            run_time=0.5,
        )
        self.wait(0.25)


# Slide 3
# Talks about how vaping allows to play out developmental conflicts
# Can see this in social media
class MentalHealthProblemSlide(Slide):
    def construct(self):
        # declarations
        mental_health_text: Text = Text("Mental Health").to_edge(UP).set_color(BLUE)
        wheresmyjuul_image: ImageMobject = (
            ImageMobject("./images/wheresmyjuul.jpg").scale(0.75).shift(DOWN)
        )
        wheresmyjuul_text: Text = Text('"Where\'s My Juul Saga"').next_to(
            wheresmyjuul_image, UP
        )

        externalization_text: Text = (
            Text("Externalization").shift(UP).set_color(GREEN).scale(0.75)
        )
        externalization_definition: Paragraph = (
            Paragraph(
                "The tendency to project one's internal",
                "states onto the outside world.",
                alignment="center",
            )
            .next_to(externalization_text, DOWN)
            .scale(0.75)
        )
        externalization_group: VGroup = VGroup(
            externalization_definition, externalization_text
        )
        rice_citation: Text = (
            Text(
                "Rice, Timothy R., et al. “Adolescent Vaping: Revisiting Developmental Perspectives on Adolescent Substance Use in the Digital Age.” The Psychoanalytic Study of the Child, Taylor & Francis, July 2025, pp. 1–19, https://doi.org/10.1080/00797308.2025.2533680."
            )
            .set_color(GREY)
            .scale(0.15)
            .to_edge(DOWN)
        )
        favorable_response_paragraph: Paragraph = Paragraph(
            '"This is a more convincing anti-vape ad than the real one"',
            '"If this isn’t a sign of addiction then idk [I don’t know] what is anymore"',
            '"this convinced me to quit"',
            alignment="left",
        ).scale(0.5)

        # animations
        self.play(
            Write(mental_health_text),
        )
        self.wait(0.25)

        self.next_slide()

        # self.play(FadeIn(wheresmyjuul_image), Write(wheresmyjuul_text))
        self.play(Write(externalization_group), Write(rice_citation))

        self.next_slide()

        # manifest this externalization into an e-cigarette
        # self.play(
        #     Transform(wheresmyjuul_text, externalization_group),
        #     FadeOut(wheresmyjuul_image),
        # )
        self.play(
            FadeIn(wheresmyjuul_image),
            Transform(externalization_group, wheresmyjuul_text),
        )

        self.next_slide()

        self.play(
            FadeOut(wheresmyjuul_image),
            # Transform(externalization_group, favorable_response_paragraph),
            Unwrite(externalization_group),
            Write(favorable_response_paragraph),
        )
        self.wait(0.25)

        self.next_slide()

        self.play(
            Unwrite(favorable_response_paragraph),
            # Unwrite(externalization_group),
            Unwrite(mental_health_text),
            Unwrite(rice_citation),
            run_time=0.5,
        )
        self.wait(0.25)


# Disallow the tagging of individuals under the age of 18
# or all together as cigarette companies aren't allowed
class CorporationInfluenceSlide(Slide):
    def construct(self):
        # definitions
        corporate_problem_text: Text = (
            Text("Corporation Influence").set_color(BLUE).to_edge(UP)
        )
        left_stick_person: SVGMobject = (
            SVGMobject("images/stick-person.svg").shift(LEFT * 2).set_color(WHITE)
        )
        right_stick_person: SVGMobject = (
            SVGMobject("images/stick-person.svg").shift(RIGHT * 2).set_color(WHITE)
        )
        stick_person_arrow: Arrow = Arrow(
            start=left_stick_person.get_right(), end=right_stick_person.get_left()
        )
        stick_person_arrow_text: Text = (
            Text("tags").scale(0.5).next_to(stick_person_arrow, UP)
        )
        incentivized_friend_tagging_text: Text = (
            Text("Incentivized Friend Tagging")
            .set_color(PURPLE)
            .scale(0.9)
            .next_to(corporate_problem_text, DOWN)
        )
        # arrow_cross: Cross = Cross(stick_person_arrow, stroke_color=RED).scale(1.2)
        lee_citation: Text = (
            Text(
                "Lee, Juhan, et al. “E-Cigarette Marketing on Social Media: A Scoping Review.” Current Addiction Reports, vol. 10, no. 1, 16 Jan. 2023, pp. 29–37, https://doi.org/10.1007/s40429-022-00463-2. "
            )
            .set_color(GREY)
            .scale(0.15)
            .to_edge(DOWN)
        )

        # animations
        self.play(Write(corporate_problem_text))

        self.next_slide()

        self.play(
            Write(incentivized_friend_tagging_text),
            Write(right_stick_person),
            Write(left_stick_person),
            Write(stick_person_arrow),
            Write(stick_person_arrow_text),
            Write(lee_citation),
        )

        self.next_slide()

        self.play(
            Unwrite(incentivized_friend_tagging_text),
            Unwrite(right_stick_person),
            Unwrite(left_stick_person),
            Unwrite(stick_person_arrow),
            Unwrite(stick_person_arrow_text),
            Unwrite(corporate_problem_text),
            Unwrite(lee_citation),
            run_time=0.5,
        )
        self.wait(0.25)


# Unhyped campaign vermont, should probably source that
# at the bottom of the screen
class ProperPresentSolutionSlide(Slide):
    def construct(self):
        # declarations
        in_class_solution_text: Text = (
            Text("Direct Solution").set_color(BLUE).to_edge(UP).scale(0.75)
        )
        board_rect: Rectangle = Rectangle(height=2, width=10).next_to(
            in_class_solution_text, DOWN
        )
        stick_teacher_tie: SVGMobject = (
            SVGMobject("images/stick-person-with-tie.svg").set_color(WHITE).scale(0.75)
        ).next_to(board_rect, DOWN)
        stick_students_vgroup: VGroup = (
            VGroup(
                *[
                    SVGMobject("images/stick-person.svg").set_color(WHITE).scale(0.4)
                    for _ in range(20)
                ]
            )
            .arrange_in_grid(rows=2, cols=10)
            .next_to(stick_teacher_tie, DOWN)
        )
        harm_perception_brace: Brace = Brace(
            stick_students_vgroup, direction=RIGHT, color=RED
        )
        harm_perception_text: Paragraph = (
            Paragraph("Harm", "Perceptions", alignment="left")
            .set_color(RED)
            .scale(0.6)
            .next_to(harm_perception_brace, RIGHT)
        )
        harm_perception_vgroup: VGroup = VGroup(
            harm_perception_brace, harm_perception_text
        )
        # Unhyped citation
        unhyped_citation: Text = (
            Text(
                "Glasser, Allison M., et al. “Effect of a State-Level Vaping Prevention Campaign on Beliefs and Behaviors in Young People.” Substance Use & Misuse, vol. 60, no. 5, 2025, pp. 659–68, https://doi.org/10.1080/10826084.2024.2446741."
            )
            .set_color(GREY)
            .scale(0.15)
            .to_edge(DOWN)
        )

        # Use with Skran example
        specific_example_text: Text = (
            Text("Use specific examples")
            .set_color(GREEN)
            .scale(0.8)
            .move_to(board_rect)
        )
        # skran citiation
        skran_citation: Text = (
            Text(
                "Skran, Sarah R. “The Effectiveness of Anti-Vaping Health Communication Campaigns among High School and College Students in the U.S.” Frontiers in Public Health, vol. 13, 5 Jan. 2026, https://doi.org/10.3389/fpubh.2025.1676181."
            )
            .set_color(GREY)
            .scale(0.15)
            .to_edge(DOWN)
        )

        # animations
        self.play(Write(in_class_solution_text))
        self.wait(0.25)

        self.next_slide()

        self.play(
            Write(stick_teacher_tie),
            Write(stick_students_vgroup),
            Write(board_rect),
        )
        self.wait(0.25)

        # harm perceptions portion
        self.next_slide()

        self.play(Write(unhyped_citation), Write(harm_perception_vgroup))

        # remove unhyped citation and harm_perceptions_vgroup
        self.next_slide()

        self.play(
            Unwrite(unhyped_citation), Unwrite(harm_perception_vgroup), run_time=0.75
        )
        self.wait(0.25)

        # remove harm perceptions text and citation
        # Move onto ways to properly educate students with specific examples
        self.next_slide()

        self.play(Write(specific_example_text), Write(skran_citation))

        self.next_slide()

        self.play(
            Transform(
                specific_example_text,
                Text("Blisters of air form in the lungs")
                .set_color(GREEN)
                .scale(0.8)
                .move_to(board_rect),
            )
        )

        # Clean up for indirect advertising campaign
        self.next_slide()

        self.play(
            Unwrite(in_class_solution_text),
            Unwrite(board_rect),
            Unwrite(stick_teacher_tie),
            Unwrite(stick_students_vgroup),
            Unwrite(skran_citation),
            Unwrite(specific_example_text),
            run_time=0.5,
        )
        self.wait(0.25)


class IndirectSolutionSlide(Slide):
    def construct(self):
        # declarations
        indirect_solution_text: Text = (
            Text("Indirect Solution").set_color(BLUE).to_edge(UP)
        )
        how_solve: Paragraph = Paragraph(
            "Continue to upload videos that",
            "illicit favorable responses",
            alignment="center",
        ).scale(0.75)
        rice_citation: Text = (
            Text(
                "Rice, Timothy R., et al. “Adolescent Vaping: Revisiting Developmental Perspectives on Adolescent Substance Use in the Digital Age.” The Psychoanalytic Study of the Child, Taylor & Francis, July 2025, pp. 1–19, https://doi.org/10.1080/00797308.2025.2533680."
            )
            .set_color(GREY)
            .scale(0.15)
            .to_edge(DOWN)
        )

        # animations
        self.play(Write(indirect_solution_text))

        self.next_slide()

        self.play(Write(how_solve), Write(rice_citation))

        self.next_slide()

        self.play(
            Unwrite(indirect_solution_text),
            Unwrite(how_solve),
            Unwrite(rice_citation),
            run_time=0.5,
        )
        self.wait(0.25)


class CorporationSolutionSlide(Slide):
    def construct(self):
        # declarations
        limit_corporation_text: Text = (
            Text("Limit Corporation Action").set_color(BLUE).to_edge(UP)
        )
        incentivized_friend_tagging_text: Text = (
            Text("Incentivized Friend Tagging").set_color(PURPLE).scale(0.9)
        )
        incentivized_friend_tagging_cross: Cross = Cross(
            incentivized_friend_tagging_text
        ).scale(1.2)
        lee_citation: Text = (
            Text(
                "Lee, Juhan, et al. “E-Cigarette Marketing on Social Media: A Scoping Review.” Current Addiction Reports, vol. 10, no. 1, 16 Jan. 2023, pp. 29–37, https://doi.org/10.1007/s40429-022-00463-2. "
            )
            .set_color(GREY)
            .scale(0.15)
            .to_edge(DOWN)
        )

        # animations
        self.play(Write(limit_corporation_text))

        self.next_slide()

        self.play(Write(incentivized_friend_tagging_text), Write(lee_citation))

        self.next_slide()

        self.play(Write(incentivized_friend_tagging_cross))

        self.next_slide()

        self.play(
            Unwrite(limit_corporation_text),
            Unwrite(incentivized_friend_tagging_cross),
            Unwrite(incentivized_friend_tagging_text),
            Unwrite(lee_citation),
            run_time=0.5,
        )
        self.wait()


class ThankYouSlide(Slide):
    def construct(self):
        # declarations
        thank_you_text: Text = Text("Thank You").set_color(BLUE)

        # animations
        self.play(Write(thank_you_text))
