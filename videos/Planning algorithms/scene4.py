from manim import *
import random


class Scene3Part4(Scene):
    default_font = "JetBrains Mono"
    text_config = {
        "font": default_font,
        "weight": BOLD,
        "font_size": 80,
    }

    def construct(self):
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
