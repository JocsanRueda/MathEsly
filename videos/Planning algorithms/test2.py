from manim import *


class scene2(ZoomedScene):
    default_font = "JetBrains Mono"

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
        rect = Rectangle(
            width=5,
            height=4,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_width=0,
        )
        self.add(rect)
        self.add_sound("assets/retro_shot.wav")
        self.wait(1)
