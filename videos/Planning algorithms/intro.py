from manim import *
import random
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils.sound import generate_piano_note_wav
from utils.create_rectangles import create_rectangles
from algoritms.ord import *


class scene0(Scene):

    def construct(self):
        n = 10
        stroke_length = 0.5
        numbers = [random.randint(1, 2 * n) for i in range(n)]

        rectangles = create_rectangles(
            self, numbers, stroke_length=stroke_length, show_number=True
        )
        dictionary = {}
        for i in range(len(numbers)):
            dictionary[rectangles[i].height] = numbers[i]
        # text = Text(f"Bubble Sort - {n} Elements", font_size=40)
        # text.to_corner(UP+LEFT)
        # self.add(text)
        self.add(rectangles)
        for i in range(len(numbers)):
            generate_piano_note_wav(
                input_value=numbers[i], duration_sec=0.15, output_dir="assets/sounds"
            )

        self.wait(1)

        sort = timsort_mobObjects(self, rectangles, dictionary, animate=False)

        # for i in range(len(sort)):
        #     print(sort[i].height)

        self.wait(1)
        os.system("rm -rf assets/sounds")
