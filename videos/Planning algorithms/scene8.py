from manim import *
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils.sound import generate_piano_note_wav
from utils.create_rectangles import create_rectangles
from algoritms.ord import *


class Scene8(Scene):
    default_font = "JetBrains Mono"
    text_config = {
        "font": default_font,
        "weight": BOLD,
        "font_size": 80,
    }

    def construct(self):
        self.part5()

    def intro(self):

        cap = Text(
            "Capitulo 3", font=self.default_font, weight=BOLD, color=TEAL, font_size=52
        ).to_edge(UP)

        full_text = "Conociendo la familia del orden "
        name = Text("", font=self.default_font, weight=BOLD, color=WHITE, font_size=40)
        name.next_to(cap, DOWN, buff=1)

        # Cursor guion alto
        cursor = Text(
            "|", font=self.default_font, weight=BOLD, color=TEAL, font_size=40
        )
        cursor.next_to(name, RIGHT, buff=0.05)

        self.play(
            Write(cap, run_time=2, rate_func=rate_functions.slow_into),
        )

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

    def part1(self):

        font_size = 30
        text1 = Text(
            "• Por Mecanismo de Ordenamiento",
            font=self.default_font,
            weight=BOLD,
            color=WHITE,
            font_size=font_size,
        )

        text2 = Text(
            "• Por Complejidad Computacional",
            font=self.default_font,
            weight=BOLD,
            color=WHITE,
            font_size=font_size,
        )

        text3 = Text(
            "• Por Estabilidad",
            font=self.default_font,
            weight=BOLD,
            color=WHITE,
            font_size=font_size,
        )

        list_Text = VGroup(text1, text2, text3).arrange(
            DOWN, aligned_edge=LEFT, buff=0.5
        )
        list_Text.move_to(ORIGIN)

        self.play(Write(list_Text, run_time=2, rate_func=rate_functions.slow_into))

        self.wait(1)

        self.play(
            FadeOut(list_Text[1:]),
            list_Text[0].animate.move_to(ORIGIN).scale(1.2),
            FadeOut(list_Text[0][0]),
        )

        self.wait(1)

    def part2(self):
        # Por mecanismo de ordenamiento

        font_size = 30

        text1 = Text(
            " Por Mecanismo de Ordenamiento",
            font=self.default_font,
            weight=BOLD,
            color=WHITE,
            font_size=font_size,
        ).scale(1.2)

        text2 = Text(
            "• Por Comparación",
            font=self.default_font,
            weight=BOLD,
            color=WHITE,
            font_size=font_size,
        )

        text3 = Text(
            "• No Por Comparación",
            font=self.default_font,
            weight=BOLD,
            color=WHITE,
            font_size=font_size,
        )

        list_Text = VGroup(text2, text3).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        subText1 = Text(
            "Ordena comparando elementos (A > B?)",
            font=self.default_font,
            color=WHITE,
            font_size=25,
        ).next_to(text2[1:], DOWN, aligned_edge=LEFT, buff=0)

        subText2 = Text(
            "Usa propiedades numéricas (dígitos/rangos)",
            font=self.default_font,
            color=WHITE,
            font_size=25,
        )

        self.add(text1)

        self.play(
            FadeOut(text1),
        )

        self.play(Write(list_Text, run_time=2, rate_func=rate_functions.slow_into))

        self.wait(1)

        self.play(
            text2.animate.shift([0, 0.2, 0]),
            text3.animate.shift([0, -0.2, 0]),
            Write(subText1, run_time=2, rate_func=rate_functions.slow_into),
        )

        subText2.next_to(text3[1:], DOWN, aligned_edge=LEFT, buff=0.2)
        self.wait(1)
        self.play(
            Write(subText2, run_time=2, rate_func=rate_functions.slow_into),
        )

        self.wait(1)

        self.play(FadeOut(subText2, text2, text3))

    def part3(self):

        text1 = Text(
            "Por Comparación",
            font=self.default_font,
            weight=BOLD,
            color=WHITE,
            font_size=25,
        )

        bubble_sort_text = Text(
            "Bubble Sort", font=self.default_font, font_size=25
        ).to_edge(UL)

        selection_sort_text = Text(
            "Selection Short", font=self.default_font, font_size=25
        ).to_edge(UL)

        insertion_sort_text = Text(
            "Insertion Sort", font=self.default_font, font_size=25
        ).to_edge(UL)

        self.add(text1)

        self.play(FadeOut(text1))

        self.play(Write(bubble_sort_text))

        self.wait(1)

        n = 15
        stroke_length = 0.5
        numbers = [random.randint(1, 2 * n) for i in range(n)]

        rectangles, dictionary = create_rectangles(
            self, numbers, stroke_length=stroke_length, show_number=True, scale=0.6
        )

        rectangles.shift([0, -1, 0])

        # show the algorithm name and the rectangles
        self.play(
            FadeIn(rectangles, run_time=2, rate_func=rate_functions.slow_into),
        )

        self.wait(1)

        for i in range(len(numbers)):
            generate_piano_note_wav(
                input_value=numbers[i], duration_sec=0.15, output_dir="assets/sounds"
            )

        rectangles.save_state()

        bubble_sort_mobObjects(
            self,
            rectangles=rectangles,
            dictionary=dictionary,
            animate=False,
            add_sound=True,
        )

        self.wait(1)

        self.play(
            ReplacementTransform(bubble_sort_text, selection_sort_text),
            Restore(rectangles),
        )

        self.wait(1)

        rectangles.save_state()

        selection_sort_mobObjects(
            self,
            rectangles=rectangles,
            dictionary=dictionary,
            animate=False,
            add_sound=True,
        )

        self.wait(1)

        self.play(
            ReplacementTransform(selection_sort_text, insertion_sort_text),
            Restore(rectangles),
        )

        insertion_sort_mobObjects(
            self,
            rectangles=rectangles,
            dictionary=dictionary,
            animate=False,
            add_sound=True,
        )

        self.wait(1)

        self.play(
            FadeOut(insertion_sort_text),
            FadeOut(rectangles),
        )

        os.system("rm -rf assets/sounds")

    def part4(self):
        text1 = Text(
            "Por No Comparación",
            font=self.default_font,
            weight=BOLD,
            color=WHITE,
            font_size=25,
        )

        counting_sort_text = Text(
            "Counting Sort", font=self.default_font, font_size=25
        ).to_edge(UL)

        radix_sort_text = Text(
            "Radix Sort", font=self.default_font, font_size=25
        ).to_edge(UL)

        self.play(Write(text1))
        self.wait(1)

        self.play(FadeOut(text1))

        self.play(Write(counting_sort_text))

        self.wait(1)

        n = 15
        stroke_length = 0.5
        numbers = [random.randint(1, 2 * n) for i in range(n)]

        rectangles, dictionary = create_rectangles(
            self, numbers, stroke_length=stroke_length, show_number=True, scale=0.6
        )

        rectangles.shift([0, -1, 0])

        # show the algorithm name and the rectangles
        self.play(
            FadeIn(rectangles, run_time=2, rate_func=rate_functions.slow_into),
        )

        self.wait(1)

        for i in range(len(numbers)):
            generate_piano_note_wav(
                input_value=numbers[i], duration_sec=0.15, output_dir="assets/sounds"
            )

        rectangles.save_state()

        counting_sort_mobObjects(
            self,
            rectangles=rectangles,
            dictionary=dictionary,
            animate=False,
            add_sound=True,
        )

        self.wait(1)

        self.play(
            ReplacementTransform(counting_sort_text, radix_sort_text),
            Restore(rectangles),
        )

        self.wait(1)

        rectangles.save_state()

        radix_sort_mobObjects(
            self,
            rectangles=rectangles,
            dictionary=dictionary,
            animate=False,
            add_sound=True,
        )

        self.wait(1)

        self.play(
            FadeOut(radix_sort_text),
            FadeOut(rectangles),
        )

        os.system("rm -rf assets/sounds")

    def part5(self):
        text1 = Text(
            "Por complejidad de Computacional",
            font=self.default_font,
            weight=BOLD,
            color=WHITE,
            font_size=25,
        )

        # Plano de coordenadas
        axes = (
            Axes(
                x_range=[0, 50, 5],
                y_range=[0, 400, 40],
                x_length=7,
                y_length=6,
                axis_config={"color": WHITE},
                tips=False,
            )
            .to_edge(DOWN)
            .shift(UP * 0.5)
        )

        # Funciones
        graph_n = axes.plot(lambda x: x, color=GREEN, x_range=[0, 50])

        graph_nlogn = axes.plot(
            lambda x: x * np.log2(x + 1), color=YELLOW, x_range=[0, 50]
        )
        graph_n2 = axes.plot(lambda x: x**2, color=RED, x_range=[0, 20])

        # Etiquetas de complejidad
        mtext1 = (
            MathTex("O(n)", font_size=29, color=WHITE)
            .move_to(axes.c2p(25, 34))
            .set_z_index(10)
        )
        mtext2 = (
            MathTex("O(n\\log n)", font_size=29, color=WHITE)
            .move_to(axes.c2p(31, 25 * np.log2(25) + 2))
            .set_z_index(10)
        )
        mtext3 = (
            MathTex("O(n^2)", font_size=29, color=WHITE)
            .move_to(axes.c2p(21, 18**2))
            .set_z_index(10)
        )

        self.play(Create(axes))
        self.play(Create(graph_n), Write(mtext1))
        self.play(Create(graph_nlogn), Write(mtext2))
        self.play(Create(graph_n2), Write(mtext3))
        self.wait(1)

        # self.add(axes, graph_n, graph_nlogn, graph_n2, mtext1, mtext2, mtext3)

        axes1 = axes.copy()
        axes2 = axes.copy()

        axes1.generate_target()
        axes2.generate_target()
        axes.generate_target()
        axes1.target.scale(0.5).to_edge(LEFT + UP)
        axes2.target.scale(0.5).to_edge(RIGHT + UP)
        axes.target.scale(0.5).to_edge(UP)

        graph_n_small = axes1.target.plot(lambda x: x, color=GREEN, x_range=[0, 50])
        graph_nlogn_small = axes.target.plot(
            lambda x: x * np.log2(x + 1), color=YELLOW, x_range=[0, 50]
        )
        graph_n2_small = axes2.target.plot(lambda x: x**2, color=RED, x_range=[0, 20])

        mtext1.generate_target()
        mtext2.generate_target()
        mtext3.generate_target()
        mtext1.target.next_to(axes1.target, DOWN, buff=0.2).scale(1.1)
        mtext2.target.next_to(axes.target, DOWN, buff=0.2).scale(1.1)
        mtext3.target.next_to(axes2.target, DOWN, buff=0.2).scale(1.1)

        self.play(
            MoveToTarget(axes1),
            MoveToTarget(axes2),
            MoveToTarget(axes),
            ReplacementTransform(
                graph_n,
                graph_n_small,
            ),
            ReplacementTransform(
                graph_nlogn,
                graph_nlogn_small,
            ),
            ReplacementTransform(graph_n2, graph_n2_small),
            MoveToTarget(mtext1),
            MoveToTarget(mtext2),
            MoveToTarget(mtext3),
        )

        # list algorithms
        n_algorithms = Text(
            "• Counting Sort\n• Radix Sort",
            font=self.default_font,
            color=WHITE,
            font_size=22,
        ).next_to(mtext1, DOWN, buff=0.5)

        nlogn_algorithms = Text(
            "• Merge Sort\n• Heap Sort",
            font=self.default_font,
            color=WHITE,
            font_size=22,
        ).next_to(mtext2, DOWN, buff=0.5)

        n2_algorithms = Text(
            "• Bubble Sort\n• Selection Sort\n• Insertion Sort \n• Quick Sort \n• Bucket Sort",
            font=self.default_font,
            color=WHITE,
            font_size=22,
        ).next_to(mtext3, DOWN, buff=0.5)

        self.wait(1)

        self.play(
            Write(n_algorithms, run_time=2, rate_func=rate_functions.slow_into),
            Write(nlogn_algorithms, run_time=2, rate_func=rate_functions.slow_into),
            Write(n2_algorithms, run_time=2, rate_func=rate_functions.slow_into),
        )

        self.wait(1)
