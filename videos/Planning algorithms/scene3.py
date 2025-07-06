from manim import *
from object.arrayNumber import ArrayNumber
import random


class Scene3(Scene):
    default_font = "JetBrains Mono"
    text_config = {
        "font": default_font,
        "weight": BOLD,
        "font_size": 80,
    }

    def construct(self):
        self.intro()
        self.part1()

    def intro(self):
        cap = Text("Capitulo 2", **self.text_config, color=TEAL).to_edge(UP)

        full_text = "El orden nace con las computadoras"
        name = Text("", font=self.default_font, weight=BOLD, color=WHITE, font_size=40)
        name.next_to(cap, DOWN, buff=1)

        # Cursor guion alto
        cursor = Text(
            "|", font=self.default_font, weight=BOLD, color=TEAL, font_size=40
        )
        cursor.next_to(name, RIGHT, buff=0.05)

        self.add(cap, name, cursor)

        # Animación de escritura
        for i, char in enumerate(full_text):
            # Velocidad variable (más rápido)
            delay = random.uniform(0.015, 0.12)
            self.wait(delay)
            name.text += char
            name.become(
                Text(
                    name.text,
                    font=self.default_font,
                    weight=BOLD,
                    color=WHITE,
                    font_size=40,
                ).move_to(name)
            )
            cursor.next_to(name, RIGHT, buff=0.05)
            self.wait(0.01)  # Breve pausa para el cursor

        # Parpadeo final del cursor
        for _ in range(6):
            cursor.set_opacity(0)
            self.wait(0.25)
            cursor.set_opacity(1)
            self.wait(0.25)
        cursor.set_opacity(0)

        self.play(
            FadeOut(cap),
            FadeOut(name),
            FadeOut(cursor),
        )

    def part1(self):

        # radix sort
        array = [100, 50, 3, 7000, 10]

        array_order = list(range(10))
        #                 1 - 2 - 3 - 4 - 5
        list_array = ArrayNumber(array, color=BLUE).to_edge(UP).scale(0.6)
        list_order = (
            ArrayNumber(
                array_order,
                color=WHITE,
                vertical=True,
                show_lines=False,
                width=1,
                height=1,
                length_space=0.3,
                font_size=34,
            )
            .to_edge(LEFT)
            .scale(0.5)
            .shift([0, -0.5, 0])
        )
        self.play(
            DrawBorderThenFill(list_array),
        )

        # select element with max digits

        max_element = list_array.squares[3]
        max_element.save_state()

        self.wait(1)

        # text with numer digits
        text1 = Text("4", font=self.default_font, font_size=38).next_to(
            max_element, DOWN, buff=0.4
        )
        self.play(
            max_element.animate.set_color(YELLOW),
            Write(text1),
            run_time=0.5,
        )
        self.wait(1)

        self.play(
            Restore(max_element),
            FadeOut(text1),
        )

        self.wait(1)

        animation_become = []
        for i, square in enumerate(list_array.squares):
            len_str = 4 - len(square.get_number_string())

            newText = (
                Text(
                    "0" * len_str + square.get_number_string(),
                    font=self.default_font,
                    font_size=32,
                )
                .scale(0.5)
                .move_to(square.get_center())
            )

            animation_become.append(square.number_text.animate.become(newText))

        self.play(AnimationGroup(*animation_become, lag_ratio=0.2))

        self.play(
            DrawBorderThenFill(list_order),
        )

        self.wait(1)

        squareSelect = (
            Rectangle(width=0.15, height=0.3, color=RED, fill_opacity=0)
            .set_stroke(width=5)
            .set_z_index(10)
        )

        self.play(
            DrawBorderThenFill(squareSelect),
        )
        it = len(str(max(list_array.array)))
        cont_elements = [[] for _ in range(10)]

        for i in range(it + 1):

            if i > 0:
                new_order = [
                    int(l.get_number_string()) for e in cont_elements for l in e
                ]

                self.play(
                    list_array.new_order(new_order, positions=position, lag_ratio=0.35),
                )

                cont_elements = [[] for _ in range(10)]
                if i == it:
                    break

            position = [i.get_center() for i in list_array.squares]
            for j, jdx in enumerate(list_array.squares):

                self.play(
                    squareSelect.animate.move_to(
                        jdx.get_number_text()[-1 * (i + 1)].get_center()
                    ),
                )
                self.wait(0.5)
                position_index = (
                    int(jdx.get_number_string()[(-1 * (i + 1))])
                    if i + 1 == len(str(jdx.get_number_string()))
                    else 0
                )
                cont_elements[position_index].append(jdx)

                self.play(
                    jdx.animate.next_to(
                        list_order.squares[position_index],
                        RIGHT,
                        buff=((jdx.width + 0.1) * len(cont_elements[position_index])),
                    ),
                )

        self.play(
            FadeOut(squareSelect),
            FadeOut(list_order),
        )
        animation_become = []
        for i, square in enumerate(list_array.squares):
            len_str = 4 - len(square.get_number_string())

            newText = (
                Text(
                    square.get_number_string(),
                    font=self.default_font,
                    font_size=32,
                )
                .scale(0.5)
                .move_to(square.get_center())
            )

            animation_become.append(square.number_text.animate.become(newText))

        self.play(AnimationGroup(*animation_become, lag_ratio=0.2))
        self.play(list_array.animate.move_to(ORIGIN))

        self.wait(1)
