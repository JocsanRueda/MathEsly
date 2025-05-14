from manim import *
import random
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils.sound import generate_piano_note_wav
from algoritms.ord import *
class scene0(Scene):
 

    def create_rectangles(self, numbers, stroke_length=0.1) -> VGroup:
        """
        Creates a group of rectangles based on the given list of numbers.

        Each rectangle's width is determined by dividing the frame width by the 
        number of elements in the list, and its height is proportional to the 
        corresponding number in the list relative to the maximum value in the list.

        Parameters:
            numbers (list of float): A list of numerical values used to determine 
                                     the height of each rectangle.
            stroke_length (float): The length of the stroke for each rectangle.

        Returns:
            VGroup: A group of rectangles with calculated dimensions and positions 
                    based on the input numbers.
        """
        rectangles = VGroup()
        frame_width = config.frame_width
    
        frame_height = config.frame_height
        for i in range(len(numbers)):
            rectangle_width = (frame_width-1) / len(numbers)
            max_height = max(numbers)
            rectangle_height = numbers[i]/(max_height) * (frame_height-0.1)
            rectangle = Rectangle(width=rectangle_width, height=rectangle_height, color=WHITE, fill_opacity=1)
            
      
            rectangle.set_stroke(color=BLACK, width=stroke_length)
            rectangle.move_to([rectangle_width * i - (frame_width-0.5-rectangle_width)/2, rectangle_height / 2 - frame_height / 2, 0])
            # text= Text(str(numbers[i]), font_size=20).set_color(BLACK)
            # text.move_to(rectangle.get_center())
            # text.set_z_index(10)
            # text.add_updater(lambda m, r=rectangle: m.move_to(r.get_center()))
            # rectangle.add(text)
            rectangles.add(rectangle)
            
        return rectangles
   
    
    def construct(self):
        n=250
        stroke_length=0.5
        numbers=[random.randint(1,2*n) for i in range(n)]


        


        rectangles= self.create_rectangles(numbers, stroke_length=stroke_length)
        dictionary = {}
        for i in range(len(numbers)):
            dictionary[rectangles[i].height] = numbers[i]
        # text = Text(f"Bubble Sort - {n} Elements", font_size=40)
        # text.to_corner(UP+LEFT)
        # self.add(text)
        self.add(rectangles)
        for i in range(len(numbers)):
            generate_piano_note_wav(
                input_value=numbers[i],
                duration_sec=0.15,
                output_dir="assets/sounds"
            )
       
      
        self.wait(1)
        

        sort=timsort_mobObjects(self,rectangles,dictionary, animate=False)

        # for i in range(len(sort)):
        #     print(sort[i].height)

        self.wait(1)
        os.system("rm -rf assets/sounds")


