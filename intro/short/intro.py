from manim import *


config.frame_width = 16
config.frame_height = 9
config.pixel_width = 3840
config.pixel_height =2160 
config.frame_rate = 60


class intro(Scene):
    def construct(self):

        text = Text("MathEsl").scale(2)
        text2 = Text("Mt").scale(2)

        self.add(text)

        triangle = Triangle().scale(0.5)
        triangle.set_stroke(width=8)

        triangle.next_to(text[-1], RIGHT)
        triangle.rotate(PI)
        self.play(Write(text))

        self.wait()
        self.play(Create(triangle))
        self.play(Transform(text, text2), triangle.animate.next_to(text2[-1], RIGHT))

        self.wait(1)
