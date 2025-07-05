from manim import *
import numpy as np
import random

from object.holerrint import *


class scene1S(MovingCameraScene):
    default_font = "JetBrains Mono"
    perforatedCard = PerforatedCard().next_to(ORIGIN, UP, buff=-0.3).scale(0.64)
    censeCard = CenseCard().scale(0.81).next_to(ORIGIN, DOWN, buff=-0.2)

    def construct(self):
        self.part1()
        self.part2()

    def part1(self):

        # extract digits
        text_digits = self.perforatedCard.text_digits
        self.add(self.perforatedCard)

        self.camera.frame.move_to(self.perforatedCard).set(
            width=config.frame_width * 0.64
        )
        circle1 = (
            Circle(radius=0.07, color=BLACK, fill_opacity=1)
            .set_fill(color=BLACK)
            .move_to(text_digits[0][0].get_center())
        )

        circles = VGroup(
            *[
                Circle(radius=0.07, color=BLACK, fill_opacity=1)
                .set_fill(color=BLACK)
                .move_to(
                    text_digits[random.randint(0, len(text_digits) - 1)][
                        random.randrange(0, len(text_digits[0]), 2)
                    ].get_center()
                )
                for i in range(len(text_digits) - 1)
            ]
        )

        # self.add(self.perforatedCard)
        # self.add(circles)
        self.play(
            DrawBorderThenFill(self.perforatedCard),
        )

        self.wait(1)

        # zoom to the card
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.move_to(text_digits[0][0].get_center()).set(
                width=8
            )
        )
        self.wait(1)
        # draw the circle
        self.play(
            Create(circle1),
        )
        self.wait(1)
        # unzoom
        self.play(
            Restore(self.camera.frame),
        )
        self.wait(1)
        self.play(
            Create(circles),
        )
        self.wait(1)
        self.play(
            Uncreate(circles),
            Uncreate(circle1),
        )

    def part2(self):

        self.add(self.perforatedCard)

        self.camera.frame.move_to(self.perforatedCard).set(
            width=config.frame_width * 0.64
        )

        self.play(
            self.camera.frame.animate.move_to(self.censeCard).set(
                width=config.frame_width * 0.90
            )
        )
        self.play(
            DrawBorderThenFill(self.censeCard),
        )
        self.wait(1)

        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(
                width=config.frame_width * 1.3
            ),
        )

        self.wait(1)


class scene1(ZoomedScene):
    default_font = "JetBrains Mono"
    perforatedCard = PerforatedCard()
    censeCard = CenseCard()

    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=1,
            zoomed_display_width=1,
            image_frame_stroke_width=10,
            zoomed_camera_config={
                "default_frame_stroke_width": 4,
                "default_frame_color": RED,
            },
            **kwargs,
        )

    def construct(self):
        self.part1()

    def part1(self):
        def get_circles(column, row):
            return (
                Circle(radius=0.07, color=BLACK, fill_opacity=1)
                .set_fill(color=BLACK)
                .move_to(self.perforatedCard.text_digits[column][row * 2].get_center())
            )

        # extract digits
        self.perforatedCard.next_to(ORIGIN, UP, buff=-0.3).scale(0.84)
        self.censeCard.next_to(ORIGIN, DOWN, buff=-0.2).scale(0.81)
        self.camera.frame.set(width=config.frame_width * 1.3)
        self.add(self.perforatedCard)
        self.add(self.censeCard)

        # rectangle in perforatedCard
        p1 = self.perforatedCard.text_digits[0].get_y()
        p2 = self.perforatedCard.text_digits[-1].get_y()
        distance = abs(p2 - p1)

        rectPerforatedCard = (
            Rectangle(
                height=distance * 1.1,
                width=0.3,
                color=RED,
                fill_opacity=0,
            )
            .move_to(self.perforatedCard)
            .set_x(self.perforatedCard.text_digits[0][0].get_x())
        )

        # rectangle in censeCard
        text = self.censeCard.text

        rectCenseCard = self.zoomed_camera.frame
        rectCenseCard.move_to(text[51:52])
        rectCenseCard.set_stroke(width=4, color=RED)

        # animation for sex F M
        self.play(
            Create(rectCenseCard),
        )

        # activate zoom
        self.activate_zooming()
        self.play(self.get_zoomed_display_pop_out_animation())

        self.wait(1)

        self.play(
            Create(rectPerforatedCard),
        )
        self.wait(1)
        c1 = get_circles(0, 0)
        self.play(Create(c1), runtime=0.01)

        # change sex to M

        c2 = get_circles(1, 0)

        self.play(rectCenseCard.animate.move_to(text[67:68]))
        self.play(FadeOut(c1), Create(c2), runtime=0.01)

        # age

        self.play(
            rectCenseCard.animate.move_to(text[52:54]),
        )
        self.play(
            rectPerforatedCard.animate.stretch_to_fit_width(
                rectPerforatedCard.width * 1.3
            ).shift([rectPerforatedCard.width * 1.8, 0, 0]),
        )
        c2 = get_circles(3, 2)
        c3 = get_circles(2, 3)

        self.play(Create(c2), runtime=0.01)
        self.wait(1)
        self.play(Create(c3), runtime=0.01)

        # civil state

        self.play(
            rectCenseCard.animate.move_to(text[54:55]),
        )

        c4 = get_circles(2, 6)

        self.play(
            rectPerforatedCard.animate.stretch_to_fit_width(
                rectPerforatedCard.width / 1.3
            ).set_x(c4.get_x())
        )

        self.play(Create(c4), runtime=0.01)

        # ocup state
        self.play(
            rectCenseCard.animate.move_to(text[55:56]),
        )

        c5 = get_circles(1, 7)

        self.play(rectPerforatedCard.animate.set_x(c5.get_x()))

        self.play(Create(c5), runtime=0.01)

        # Nac state
        self.play(
            rectCenseCard.animate.move_to(text[56:57]),
        )
        c6 = get_circles(1, 8)

        self.play(rectPerforatedCard.animate.set_x(c6.get_x()))

        self.play(Create(c6), runtime=0.01)

        # INSTR state
        self.play(
            rectCenseCard.animate.move_to(text[57:58]),
        )

        c7 = get_circles(1, 9)

        self.play(
            rectPerforatedCard.animate.set_x(c7.get_x()),
        )

        self.play(Create(c7), runtime=0.01)

        # RELG state

        self.play(
            rectCenseCard.animate.move_to(text[58:59]),
        )
        c8 = get_circles(1, 10)
        self.play(
            rectPerforatedCard.animate.set_x(c8.get_x()),
        )
        self.play(Create(c8), runtime=0.01)

        self.wait(1)

        # add random circles

        randomCircles = VGroup(
            *[get_circles(random.randint(0, 9), i) for i in range(11, 45)]
        )

        # Crea animaciones para los círculos (FadeIn)
        circle_anims = [FadeIn(c) for c in randomCircles]

        # Crea una animación personalizada para mover el rectángulo a lo largo de los X

        # Agrupa todo: el rectángulo se mueve mientras los círculos aparecen con desfase
        self.play(
            AnimationGroup(
                rectPerforatedCard.animate.set_x(randomCircles[-1].get_x()),
                *circle_anims,
                lag_ratio=1
                / len(
                    circle_anims
                ),  # Ajusta para que los círculos aparezcan repartidos durante el movimiento
            ),
            run_time=3,  # Ajusta el tiempo total
        )

        self.wait(1)

        self.play(Uncreate(rectPerforatedCard))

        self.play(
            FadeOut(self.zoomed_display.display_frame),
            FadeOut(rectCenseCard),
        )

        self.wait(1)
