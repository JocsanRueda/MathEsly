from manim import *

from utils.text import WriteEquations3D


class Scene0(ThreeDScene):
    """
    Scene0 class that extends ThreeDScene to create a 3D animation.

    Methods:
        construct():
            Constructs the 3D scene with a cube and mathematical equations.
            - Initializes 3D axes and a cube with a specified size.
            - Sets the camera orientation.
            - Defines and positions mathematical equations related to the volume of a cube.
            - Adds fixed frame mobjects for the equations and cube dimensions.
            - Animates the appearance of the cube dimensions and equations.
            - Writes the equations in the 3D scene.
    """

    def construct(self):
        axes = ThreeDAxes()
        n = 1.5
        cube = Cube(n)
        cube2 = Cube(n * 2)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        # define form
        f0 = MathTex(
            f"{{A}}", "=", "{{L}}", "\cdot", "{{L}}", " \cdot", "{{L}}"
        ).to_edge(UP + RIGHT)
        f1 = MathTex(f"{{A}}", "=", "{{L}}^3").move_to(f0)
        f2 = MathTex(f"{{A}}", "=", "(2{{L}})^3")
        f3 = MathTex(f"{{A}}", "=", "2^3{{L}}^3")
        f4 = MathTex(f"{{A}}", "=", "8{{L}}^3")
        self.add_fixed_in_frame_mobjects(f0)
        f0.set_opacity(0)

        # definitions of length
        length1 = (f0[2]).copy().next_to(cube, RIGHT, buff=0.5)
        length2 = (f0[4]).copy().next_to(cube, DOWN, buff=0.5)
        length3 = (f0[6]).copy().next_to(length2, RIGHT, buff=0.5).shift([0.1, 0.4, 0])
        lengthGroup = VGroup(length1, length2, length3)
        formGroup = VGroup(f0, f1, f2, f3, f4)

        # add frame mobjects
        self.add_fixed_in_frame_mobjects(length1, length2, length3)

        lengthGroup.set_opacity(0)

        self.add(axes, cube)

        # write L
        self.play(lengthGroup.animate.set_opacity(1))

        lengthCopy = lengthGroup.copy()

        self.add_fixed_in_frame_mobjects(lengthCopy)

        # move length to original form
        self.play(
            f0.animate.set_opacity(1),
            lengthCopy[0].animate.move_to(f0[2]),
            lengthCopy[1].animate.move_to(f0[4]),
            lengthCopy[2].animate.move_to(f0[6]),
        )

        # remove copy

        self.remove(lengthCopy)

        self.wait(1)

        self.play(WriteEquations3D(self, formGroup[:2], 0.5, True, False))

        self.play(
            ReplacementTransform(cube, cube2),
            length1.animate.next_to(cube2, RIGHT, buff=1),
            length2.animate.next_to(cube2, DOWN, buff=1),
            length3.animate.next_to(
                length2.copy().next_to(cube2, DOWN, buff=1), RIGHT, buff=1
            ).shift([0.1, 0.4, 0]),
        )

        length1New = MathTex("2{{L}}").set_opacity(0)
        length2New = MathTex("2{{L}}").set_opacity(0)
        length3New = MathTex("2{{L}}").set_opacity(0)

        lengthNewGroup = VGroup(length1New, length2New, length3New)

        self.add_fixed_in_frame_mobjects(lengthNewGroup)
        length1New.move_to(length1)
        length2New.move_to(length2)
        length3New.move_to(length3)
        self.play(
            lengthGroup.animate.set_opacity(0),
            lengthNewGroup.animate.set_opacity(1),
        )

        self.play(WriteEquations3D(self, formGroup[1:], 0.5, True, False))

        self.wait(2)
        self.play(
            FadeOut(cube2),
            FadeOut(length1),
            FadeOut(length2),
            FadeOut(length3),
            FadeOut(length1New),
            FadeOut(length2New),
            FadeOut(length3New),
        )
        self.wait(1)
