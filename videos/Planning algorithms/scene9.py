from manim import *


class Scene9(Scene):
    default_font = "JetBrains Mono"

    def construct(self):
        self.intro()

    def intro(self):
        font_size = 25
        preguntas_respuestas = [
            (
                "¿Tus datos son numéricos con rango limitado?",
                "→ Usa CountingSort o RadixSort.",
            ),
            (
                "¿Necesitas estabilidad?",
                "→ Elige MergeSort o InsertionSort \n (solo para pocos datos).",
            ),
            (
                "¿Priorizas velocidad en promedio?",
                "→ Usa QuickSort, pero es inestable.",
            ),
            ("¿Memoria limitada?", "→ Usa HeapSort (in-place)."),
        ]

        bloques = VGroup()
        for pregunta, respuesta in preguntas_respuestas:
            pregunta_text = Text(
                pregunta,
                font=self.default_font,
                weight=BOLD,
                color=YELLOW_B,
                font_size=font_size,
                line_spacing=1,
            )
            respuesta_text = Text(
                respuesta,
                font=self.default_font,
                weight=BOLD,
                color=WHITE,
                font_size=font_size - 4,
                line_spacing=1,
            )
            bloque = VGroup(pregunta_text, respuesta_text).arrange(
                DOWN, aligned_edge=LEFT, buff=0.2
            )
            bloques.add(bloque)

        bloques.arrange(DOWN, aligned_edge=LEFT, buff=0.7).to_edge(UP)

        self.play(Write(bloques, run_time=4, lag_ratio=0.2))
        self.wait(2)
