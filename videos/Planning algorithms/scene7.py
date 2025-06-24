from manim import *


class Scene7(Scene):
    default_font = "JetBrains Mono"

    def construct(self):
        text = Text(
            "pero, ¿y que tan rápido son?",
            font_size=36,
            font=self.default_font,
        )

        self.play(
            Write(text, run_time=2, rate_func=rate_functions.slow_into),
        )

        self.wait(1)
