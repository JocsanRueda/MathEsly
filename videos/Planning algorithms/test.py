from manim import *

from object.tabularMachine import *
from object.holerrint import PerforatedCard


class test(MovingCameraScene):
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
