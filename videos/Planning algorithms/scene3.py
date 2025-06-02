from manim import *
from object.holerrint import *
from object.clock import ClockDial
from object.tabularMachine import TabularMachine


class Scene3(ThreeDScene):
    def construct(self):
        self.part3()

    def part1(self):
        axes = ThreeDAxes()
        # Agregar nombres a los ejes
        x_label = Text("X").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("Y").next_to(axes.y_axis.get_end(), UP)
        z_label = Text("Z").next_to(axes.z_axis.get_end(), OUT)
        self.add(x_label, y_label, z_label)
        perforatedCard = PerforatedCard(True).scale(0.5)

        prism = (
            Prism(
                dimensions=[perforatedCard.width, perforatedCard.height, 0.05],
            )
            .set_fill(color=YELLOW_B, opacity=1)
            .shift([0, 0, -0.01])
        )

        self.add(axes, perforatedCard)

        self.move_camera(
            phi=90 * DEGREES,
            theta=-180 * DEGREES,
            run_time=2,
            added_anims=[FadeIn(prism)],
        )

        self.move_camera(frame_center=perforatedCard, zoom=3.5)
        self.wait(1)

    def part3(self):
        axes = ThreeDAxes()
        axes_labels = axes.get_axis_labels(Tex("x"), Tex("y"), Tex("z"))
        self.add(axes, axes_labels)
        self.set_camera_orientation(
            phi=65 * DEGREES, theta=40 * DEGREES, distance=16, zoom=0.7
        )
        machine = TabularMachine(
            main_structure_opacity=1.0,
            drawers_opacity=1.0,
            desktop_opacity=1.0,
            platform_opacity=1.0,
            card_reader_opacity=1.0,
            back_panel_opacity=1.0,
        )

        perforatedCard = (
            PerforatedCard()
            .scale(0.1)
            .move_to(machine.lever_assembly.get_center())
            .shift([-0.25, -0.45, -0.2])
        )
        perforatedCard.rotate(
            angle=PI / 2, axis=Z_AXIS, about_point=perforatedCard.get_center()
        )

        # self.play(
        #     DrawBorderThenFill(machine),
        # )

        # # self.move_camera(
        # #     theta=40 * DEGREES + 2 * PI,
        # #     run_time=4,
        # #     rate_func=linear,
        # # )

        self.add(perforatedCard)
        self.add(machine)
        self.add(perforatedCard.shift([12, 0, 0]))
        original_position = perforatedCard.get_center()
        position = machine.lever_assembly.get_center() + [-0.25, -0.45, -0.2]

        machine.open_reader(animate=False)
        ## scene reader card
        # for _ in range(3):

        #     # move card to reader
        #     self.play(perforatedCard.animate.move_to(position), rate_func=rush_into)

        #     # close reader card
        #     self.play(
        #         AnimationGroup(
        #             machine.close_reader(),
        #             perforatedCard.animate.set_fill(opacity=0.2).set_stroke(
        #                 opacity=0.2
        #             ),
        #             lag_ratio=0.1,
        #         )
        #     )
        #     # add count to clock dial
        #     self.play(machine.faceClockDial.random_add_count())

        #     # open rader card
        #     self.play(
        #         AnimationGroup(
        #             machine.open_reader(),
        #             perforatedCard.animate.set_fill(opacity=1).set_stroke(opacity=1),
        #             lag_ratio=0.1,
        #         )
        #     )

        #     # move card to out camera
        #     self.play(perforatedCard.animate.shift([0, 10, 0]), rate_func=rush_into)

        #     perforatedCard.move_to(original_position)

        ## scene view Dial

        # Mueve la cámara para que quede de frente a faceClockDial

        face_center = machine.faceClockDial.get_center()
        machine.get_ang
        self.move_camera(
            frame_center=face_center,
            phi=90 * DEGREES,
            theta=0 * DEGREES,
            zoom=2.5,
            run_time=2,
        )

        self.play(machine.faceClockDial.random_add_count(Is3D=True))

        self.wait()


class Scene3Part2(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=2,
            zoomed_display_width=2,
            image_frame_stroke_width=10,
            zoomed_camera_config={
                "default_frame_stroke_width": 4,
                "default_frame_color": RED,
            },
            **kwargs,
        )

    def construct(self):
        perforatedCard = PerforatedCard().scale(0.3)
        width = perforatedCard.width / 2

        # contact machine
        contacMachine2D = TabularMachine2D(width=width, opened=False)

        hole = contacMachine2D.pins[4].get_x()

        line1 = Line([-width, 0, 0], [hole - 0.1, 0, 0], color=YELLOW_B)
        line2 = Line([hole + 0.1, 0, 0], [width, 0, 0], color=YELLOW_B)

        card = VGroup(line1, line2).set_fill(color=YELLOW_B, opacity=1)

        clockDial = ClockDial(radius=1, counter=0).to_corner(UP + RIGHT, buff=0.1)
        self.add(clockDial)
        contacMachine2D.set_state(opened=True)
        self.add(card, contacMachine2D)

        zoomedFrame = self.zoomed_camera.frame

        zoomedFrame.move_to(contacMachine2D.bottomPart[0][4].get_center())
        zoomedFrame.set_stroke(width=4, color=RED)

        display = self.zoomed_display

        display.to_edge(LEFT + UP)
        self.activate_zooming()
        self.play(self.get_zoomed_display_pop_out_animation())

        self.add_sound("assets/retro_shot.wav")
        self.play(
            contacMachine2D.closeTopPart(),
        )

        self.play(clockDial.add_count())

        self.play(
            contacMachine2D.openTopPart(),
        )

        self.add_sound("assets/retro_shot.wav")

        self.play(
            contacMachine2D.closeTopPart(),
        )

        self.play(clockDial.add_count())

        self.play(ApplyMethod(display.replace, self.zoomed_camera.frame, stretch=True))

        self.play(FadeOut(display), FadeOut(zoomedFrame))

        self.wait(1)


class Scene3Part3(MovingCameraScene):
    def construct(self):

        faceClock = TabularMachine()
        faceClock.rotate(
            PI / 2, axis=Y_AXIS, about_point=faceClock.get_center()
        ).rotate(angle=PI / 2, axis=Z_AXIS, about_point=faceClock.get_center())

        self.camera.frame.scale(1 / 2.5).move_to(faceClock.faceClockDial)
        self.add(faceClock)
        self.play(
            Succession(*[faceClock.faceClockDial.random_add_count() for _ in range(20)])
        )
        self.wait(1)
