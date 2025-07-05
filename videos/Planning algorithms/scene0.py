from manim import *


class scene0(Scene):
    default_font = "JetBrains Mono"
    text_config = {
        "font": default_font,
        "weight": BOLD,
        "font_size": 80,
    }

    def construct(self):
        self.intro()
        self.subScene1()
        self.subScene2()

    def intro(self):

        text1 = Text("1970", **self.text_config)

        text2 = Text("<9 Meses", **self.text_config)

        text3 = Text("1860", **self.text_config)

        self.play(Write(text1))
        self.wait(1)
        self.play(Transform(text1, text2))
        self.wait(2)
        self.play(Uncreate(text1))
        self.play(Write(text3))
        self.wait(2)

        self.play(FadeOut(text3))

    def subScene1(self):

        title = Text(
            "Poblacion de E.E.U.U", font_size=40, weight=BOLD, font=self.default_font
        ).to_edge(UP)
        years = ["1790", "1860"]
        values = [1, 10, 12.5]

        # Ejes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 14, 2],
            x_length=6,
            y_length=5.5,
            axis_config={
                "include_tip": False,
            },
        )

        # Barras
        bars = VGroup()
        bar_width = 0.6
        colors = [BLUE, YELLOW, GREEN]
        for i, value in enumerate(values):
            bar = Rectangle(
                width=bar_width,
                height=value * 0.45,  # Escala para que 10 llegue a tope del eje
                fill_color=colors[i],
                fill_opacity=1,
                stroke_width=0,
            )
            bar.move_to(axes.c2p(i * 2 + 1, 0) + [0, bar.height / 2, 0])
            bars.add(bar)

        # Etiquetas de años
        labels = VGroup(
            *[
                Text(year, font_size=36, font=self.default_font).next_to(
                    axes.c2p(i * 2 + 1, 0), DOWN
                )
                for i, year in enumerate(years)
            ]
        )

        # self.add(axes, bars, labels)
        self.play(Create(axes), Write(title))
        self.play(Create(bars[0]), Write(labels[0]))
        self.wait(1)
        tempBars = VGroup(*[bars[0].copy() for i in range(10)])
        self.play(
            *[
                tempBars[i]
                .animate.set_stroke(WHITE, 3)
                .move_to([bars[1].get_x(), bars[0].get_y() + (bars[0].height) * i, 0])
                for i in range(len(tempBars))
            ],
        )
        self.wait(1)
        self.play(ReplacementTransform(tempBars, bars[1]), Write(labels[1]))
        self.wait(1)
        self.play(Create(bars[2]))
        self.wait(2)
        self.play(
            *[Uncreate(i) for i in bars],
            *[Uncreate(i) for i in labels],
            Uncreate(axes),
            Uncreate(title),
        )
        self.wait(1)
        # self.wait(2)

    def subScene2(self):
        text = Text("1880", font_size=80, weight=BOLD, font=self.default_font).to_edge(
            UP
        )
        text2 = Text(
            "7 Años", font_size=100, weight=BOLD, font=self.default_font, color=RED
        )

        text2.set(font_size=9000).move_to(ORIGIN)
        self.add(text2)
        self.play(Write(text))
        self.wait(1)
        self.play(text2.animate.set(font_size=110).move_to(ORIGIN))
        self.wait(1)

        self.play(
            FadeOut(text, text2),
        )
