from manim import *

from object.tabularMachine import *
from object.holerrint import PerforatedCard


class test(Scene):
    def construct(self):

        circle = Circle().shift(LEFT * 2.5)
        square = Square()
        triangle = Triangle().shift(RIGHT * 2.5)
        group = VGroup(circle, square, triangle)

        group2 = group.copy()
        group2.remove(group2[1])
        self.add(group2)
