from manim import *


class ClockDial(VGroup):
    def __init__(self, radius=2, counter=0, stroke_width=5.5, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.counter = counter

        # Dial base (fondo color hueso)
        dial_bg = Circle(
            radius=self.radius, color=WHITE, fill_color="#F5F5DC", fill_opacity=1
        ).set_stroke(width=stroke_width, color=GRAY_E)
        self.add(dial_bg)

        # Números 0-9 en negro, tamaño de fuente proporcional al radio
        font_size = int(32 * self.radius / 2)
        self.numbers = VGroup()
        for i in range(10):
            angle = PI / 2 - i * 2 * PI / 10  # Start at top, clockwise
            pos = self.radius * 0.8 * np.array([np.cos(angle), np.sin(angle), 0])
            num = Text(
                str(i),
                font_size=font_size,
                font="JetBrains Mono",
                color=BLACK,
            ).move_to(pos)
            self.numbers.add(num)
        self.add(self.numbers)

        # Manecilla color rojo
        self.needle = Arrow(
            start=ORIGIN,
            end=self.radius * 0.7 * self._angle_to_vector(self.counter),
            buff=0,
            color=RED,
            max_tip_length_to_length_ratio=0.2,
            stroke_width=6,
        )
        self.add(self.needle)

        # Remache central (círculo pequeño gris oscuro)
        center_dot = Circle(
            radius=self.radius * 0.05,
            color=GREY_D,
            fill_color=GREY_E,
            fill_opacity=1,
        ).move_to(ORIGIN)
        self.add(center_dot)

    def _angle_to_vector(self, value):
        # Map value 0-9 to angle (0 at top, clockwise)
        angle = PI / 2 - value * 2 * PI / 10
        return np.array([np.cos(angle), np.sin(angle), 0])

    def set_counter(self, value):
        self.counter = value % 10
        new_end = self.radius * 0.7 * self._angle_to_vector(self.counter)
        self.needle.put_start_and_end_on(ORIGIN, new_end)

    def get_needle_update_anim(self, new_value, run_time=0.5, Is3D=False):
        start = self.counter % 10
        end = new_value % 10

        # Fuerza avance horario
        if end <= start:
            end += 10

        self.counter = new_value % 10  # Actualiza el contador solo con el dígito final

        if Is3D:

            def updater(mob, alpha):
                value = start + (end - start) * alpha
                angle = PI / 2 - value * 2 * PI / 10
                mob.rotate(
                    angle - mob.get_angle(), about_point=self.get_center(), axis=X_AXIS
                )
                mob.set_angle(angle)

            return UpdateFromAlphaFunc(self.needle, updater, run_time=run_time)
        else:

            def updater(mob, alpha):
                value = start + (end - start) * alpha
                angle = PI / 2 - value * 2 * PI / 10
                center = self.get_center()  # Centro actual del dial
                new_end = center + self.radius * 0.7 * np.array(
                    [np.cos(angle), np.sin(angle), 0]
                )
                mob.put_start_and_end_on(center, new_end)

            return UpdateFromAlphaFunc(self.needle, updater, run_time=run_time)

    def add_count(self, run_time=0.5, Is3D=False):
        return self.get_needle_update_anim(self.counter + 1, run_time=0.5, Is3D=Is3D)


class ClockScene(Scene):
    def construct(self):
        clock = ClockDial(radius=2).to_corner(UP + RIGHT, buff=0.1)

        self.add(clock)
        self.play(
            Succession(
                *[clock.add_count() for _ in range(20)],
            )
        )
