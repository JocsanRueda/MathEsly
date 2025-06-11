from manim import *
from object.timeLine import Timeline


class Scene6(Scene):
    def construct(self):
        timeline = Timeline(start_year=1950, end_year=1960, step=1, extra_range=20)
        self.add(timeline)

        self.play(
            timeline.animate_select_year(1940, label_text="360 M.Y.A."),
        )

        self.play(
            timeline.animate_select_year(1954, label_text="360 M.Y.A."),
        )

        # self.play(
        #     timeline.animate_select_year(1962, label_text="360 M.Y.A."),
        # )

        # self.play(timeline.animate_select_year(1980, label_text="360 M.Y.A."))

        # self.play(timeline.animate_select_year(1975, label_text="360 M.Y.A."))
        # self.wait(2)
