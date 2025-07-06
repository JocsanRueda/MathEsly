from manim import *
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils.sound import generate_piano_note_wav
from utils.create_rectangles import create_rectangles
from algoritms.ord import *


class Scene6(Scene):
    default_font = "JetBrains Mono"

    def construct(self):
        self.parte1()
        self.parte2()

    def parte1(self):
        text = Text(
            "pero, ¿y que tan rápido son?",
            font_size=36,
            font=self.default_font,
        )

        self.play(
            Write(text, run_time=2, rate_func=rate_functions.slow_into),
        )

        self.wait(1)

        self.play(
            FadeOut(text, run_time=1, rate_func=rate_functions.slow_into),
        )

    def parte2(self):
        n = 5
        stroke_length = 0.5
        # numbers = [random.randint(1, 2 * n) for i in range(n)]
        numbers = [5, 3, 8, 6, 2]  # Example numbers for sorting

        text_array = MathTex(
            str(numbers),
            font_size=40,
        )
        text_array_sorted = MathTex(
            str(sorted(numbers)),
            font_size=40,
        )

        text_algorithm = Text(
            "Ordenamiento burbuja",
            font_size=24,
            font=self.default_font,
        )

        # show the array of numbers
        self.play(Write(text_array))

        rectangles, dictionary = create_rectangles(
            self, numbers, stroke_length=stroke_length, show_number=True
        )

        rectangles.shift([0, -1, 0])

        rectangles.scale(0.6)

        # move the text to the corner
        self.play(text_array.animate.to_corner(UP + LEFT))

        text_algorithm.next_to(text_array, RIGHT, buff=0.5)

        # show the algorithm name and the rectangles
        self.play(
            FadeIn(rectangles, run_time=2, rate_func=rate_functions.slow_into),
            Write(text_algorithm),
        )

        self.wait(1)

        # change the color of the rectangles

        rectangles[0][0].save_state()
        rectangles[1][0].save_state()

        self.play(
            rectangles[0][0].animate.set_color(RED),
        )
        self.wait(0.5)
        self.play(
            rectangles[1][0].animate.set_color(GREEN),
        )
        self.wait(0.1)

        for i in range(len(numbers)):
            generate_piano_note_wav(
                input_value=numbers[i], duration_sec=0.15, output_dir="assets/sounds"
            )

        self.wait(1)

        rectangles.save_state()

        sort = bubble_sort_mobObjects(
            self,
            rectangles=rectangles,
            dictionary=dictionary,
            animate=True,
            add_sound=False,
        )

        text_array_sorted.move_to(text_array.get_center())

        text_array_copy = text_array.copy()

        self.play(
            ReplacementTransform(text_array, text_array_sorted),
        )
        self.wait(1)

        self.play(Restore(rectangles))

        self.wait(1)

        text_array_sorted_copy = text_array_sorted.copy()

        self.play(
            ReplacementTransform(text_array_sorted, text_array_copy),
        )

        self.play(rectangles.animate.scale(0.8).to_edge(RIGHT).shift([0, 1, 0]))
        bubble_sort_mobObjects(
            self,
            rectangles=rectangles,
            dictionary=dictionary,
            animate=True,
            add_sound=False,
            rotate=True,
        )

        self.play(ReplacementTransform(text_array_copy, text_array_sorted_copy))

        self.wait(1)

        for rect in rectangles:
            print(rect[1])

        os.system("rm -rf assets/sounds")

        # # computacional cost
        label = Text(
            "Complejidad computacional",
            font_size=24,
            color=WHITE,
            font=self.default_font,
        ).next_to(rectangles, LEFT, 1)
        text1 = MathTex("O(n^2)", font_size=40).next_to(label, DOWN)

        # computacional space
        label2 = Text(
            "Complejidad de espacio", font_size=24, color=WHITE, font=self.default_font
        ).move_to(label)
        text2 = MathTex(r"O(1)", font_size=40).next_to(label2, DOWN)

        self.play(
            Write(label),
            Write(text1),
        )
        self.wait(1)

        self.play(
            ReplacementTransform(label, label2),
            ReplacementTransform(text1, text2),
        )

        self.wait(1)

        self.play(
            FadeOut(label2, text2, rectangles, text_array_sorted_copy, text_algorithm)
        )

        self.wait(1)

        text3 = Text("¿Pero que tan rapido es?", font_size=32, font=self.default_font)

        self.play(Write(text3))

        self.wait(1)
