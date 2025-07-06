from manim import *


class Timeline(VGroup):
    default_font = "JetBrains Mono"

    def __init__(
        self,
        start_year=360,
        end_year=330,
        step=5,
        initial_year=None,
        main_line_half_length=6,
        ticks_spacing=1.0,
        extra_range=20,
        select_year=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.start_year = start_year
        self.end_year = end_year
        self.real_start_year = start_year - extra_range
        self.real_end_year = end_year + extra_range
        self.step = abs(step)
        self.initial_year = initial_year if initial_year is not None else start_year
        self.ticks_spacing = ticks_spacing
        self.extra_range = extra_range

        self.current_start_year = self.real_start_year
        self.current_end_year = self.real_end_year

        # Calcula la longitud de la línea principal según el espaciado deseado
        self._update_main_line_length()

        self._build_main_line_and_extensions()

        self.ticks = VGroup()
        self.labels = VGroup()
        self.current_label = None
        self._build_ticks()

        self.dot = (
            Dot(self.year_to_position(self.initial_year), radius=0.1, color=BLUE)
            .set_glow_factor(1.5)
            .set_z_index(11)
        )
        self.marker = Line(
            [self.dot.get_x(), -0.28, 0],
            [self.dot.get_x(), 0.28, 0],
            color=BLUE,
            stroke_width=6,
        ).set_z_index(11)

        if select_year is not None:
            position = self.get_stick_year_position(select_year)
            self.marker.move_to([position, 0, 0])
            self.dot.move_to([position, 0, 0])

        self.add(
            self.left_extension,
            self.left_rectangle,
            self.right_rectangle,
            self.main_line,
            self.right_extension,
            self.ticks,
            self.labels,
            self.dot,
            self.marker,
        )

        self.timeLine = VGroup(
            self.main_line,
            self.ticks,
            self.labels,
        )

    def _update_main_line_length(self):
        # Calcula la cantidad de intervalos
        num_intervals = abs((self.end_year - self.start_year) // self.step)
        # La longitud total es intervalos * ticks_spacing
        total_length = num_intervals * self.ticks_spacing
        self.main_line_half_length = total_length / 2

    def _build_main_line_and_extensions(self):
        l = self.main_line_half_length
        self.main_line = Line(LEFT * l, RIGHT * l, color=WHITE)
        self.left_extension = (
            Line(LEFT * (l + 1), LEFT * l, stroke_color=[WHITE, GRAY_E])
            .set_z_index(10)
            .set_stroke(width=3.5)
        )
        self.right_extension = (
            Line(RIGHT * l, RIGHT * (l + 1), stroke_color=[GRAY_E, WHITE])
            .set_z_index(10)
            .set_stroke(width=3.5)
        )

        self.left_rectangle = (
            Rectangle(width=3, height=1.5, color=BLACK)
            .set_fill(color=BLACK, opacity=1)
            .next_to(self.left_extension, LEFT, buff=0)
        ).set_z_index(12)

        self.left_rectangle.move_to(
            [
                self.left_extension.get_right()[0] - self.left_extension.width * 0.90,
                self.left_extension.get_right()[1],
                0,
            ],
            aligned_edge=RIGHT,
        )

        self.right_rectangle = (
            Rectangle(width=3, height=1.5, color=BLACK)
            .set_fill(color=BLACK, opacity=1)
            .next_to(self.right_extension, RIGHT, buff=0)
        ).set_z_index(12)

        self.right_rectangle.move_to(
            [
                self.right_extension.get_left()[0] + self.right_extension.width * 0.90,
                self.right_extension.get_left()[1],
                0,
            ],
            aligned_edge=LEFT,
        )

        self.main_line = Line(LEFT * l * 20, RIGHT * l * 20, color=WHITE).set_stroke(
            width=3.5
        )

    def _build_ticks(self):
        if self.start_year > self.end_year:
            years = range(self.real_start_year, self.real_end_year - 1, -self.step)
        else:
            years = range(self.real_start_year, self.real_end_year + 1, self.step)

        for year in years:
            x = self.year_to_position(year)[0]
            tick = Line([x, -0.15, 0], [x, 0.15, 0], color=WHITE).set_stroke(width=2)
            label = Text(str(year), font=self.default_font, font_size=20).move_to(
                [x, -0.5, 0]
            )

            self.ticks.add(tick)
            self.labels.add(label)

            if year < self.start_year or year > self.end_year:
                label.set_opacity(0)
        self.labels.add_updater(self.updater_show_stick)

    def year_to_position(self, year):

        l = self.main_line_half_length
        alpha = (year - self.start_year) / (self.end_year - self.start_year)
        x = interpolate(-l, l, alpha)
        return [x, 0, 0]

    def updater_show_stick(self, mob):
        # 1950-1960

        # 1940-1960

        # current year 1945
        # 19
        range_start_years = abs(self.current_start_year - self.real_start_year)
        range_end_years = abs(self.current_end_year - self.real_start_year)

        # Oculta los ticks antes del rango
        mob[:range_start_years].set_opacity(0.0)
        # Muestra los ticks dentro del rango
        mob[range_start_years:range_end_years].set_opacity(1.0)
        # Oculta los ticks después del rango
        mob[range_end_years:].set_opacity(0.0)

    def get_stick_year_position(self, year):
        return self.ticks[abs(year - (self.real_start_year))].get_x()

    def Fade_In(self, *args, **kwargs):
        range_start_years = abs(self.current_start_year - self.real_start_year)
        range_end_years = abs(self.current_end_year - self.real_start_year)

        return AnimationGroup(
            AnimationGroup(
                FadeIn(self.left_rectangle, **kwargs),
                FadeIn(self.right_rectangle, **kwargs),
                run_time=0.05,
            ),
            AnimationGroup(
                FadeIn(self.left_extension, **kwargs),
                FadeIn(self.right_extension, **kwargs),
            ),
            AnimationGroup(
                FadeIn(self.main_line, **kwargs),
                FadeIn(self.ticks, **kwargs),
                FadeIn(self.labels[range_start_years:range_end_years], **kwargs),
                FadeIn(self.dot, **kwargs),
                FadeIn(self.marker, **kwargs),
            ),
            lag_ratio=0.2,
        )

    def Fade_Out(self, *args, **kwargs):
        range_start_years = abs(self.current_start_year - self.real_start_year)
        range_end_years = abs(self.current_end_year - self.real_start_year)

        return Succession(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(self.left_extension, **kwargs),
                    FadeOut(self.right_extension, **kwargs),
                ),
                AnimationGroup(
                    FadeOut(self.main_line, **kwargs),
                    FadeOut(self.ticks, **kwargs),
                    FadeOut(self.labels[range_start_years:range_end_years], **kwargs),
                    FadeOut(self.dot, **kwargs),
                    FadeOut(self.marker, **kwargs),
                    FadeOut(self.current_label, **kwargs),
                ),
                lag_ratio=0.2,
            ),
            AnimationGroup(
                FadeOut(self.left_rectangle, **kwargs),
                FadeOut(self.right_rectangle, **kwargs),
                run_time=0.05,
            ),
        )

    def animate_select_year(self, year, label_text=None, font_size=36):
        animation = []

        target_x = self.get_stick_year_position(year)

        self.current_start_year = year - (self.end_year - self.start_year) // 2
        self.current_end_year = year + (self.end_year - self.start_year) // 2

        shift_x = -target_x
        self.dot.save_state()
        label = Text(
            label_text or f"{year}",
            font_size=font_size,
            font=self.default_font,
            weight=BOLD,
        ).next_to(self, DOWN, buff=0.5)

        self.current_label = label

        animation.append(
            AnimationGroup(
                self.timeLine.animate.shift(RIGHT * shift_x),
                self.dot.animate.scale([1.5, 0.9, 1]),
                FadeIn(label),
                rate_func=rate_functions.rush_from,
                run_time=2,
            )
        )

        animation.append(
            AnimationGroup(
                self.dot.animate.move_to([0, 0, 0]),
                self.marker.animate.move_to([0, 0, 0]),
                self.dot.animate.restore(),
                rate_func=rate_functions.rush_from,
                run_time=1,
            )
        )

        return Succession(*animation)
