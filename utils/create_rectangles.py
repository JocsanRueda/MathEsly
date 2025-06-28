from manim import *


def create_rectangles(
    self, numbers, stroke_length=0.1, show_number=False, scale=1
) -> VGroup:
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
        rectangle_width = (frame_width - 1) / len(numbers)
        max_height = max(numbers)
        rectangle_height = numbers[i] / (max_height) * (frame_height - 0.1)
        rectangle = Rectangle(
            width=rectangle_width, height=rectangle_height, color=WHITE, fill_opacity=1
        )

        rectangle.set_stroke(color=BLACK, width=stroke_length)
        rectangle.move_to(
            [
                rectangle_width * i - (frame_width - 0.5 - rectangle_width) / 2,
                rectangle_height / 2 - frame_height / 2,
                0,
            ]
        )
        if show_number:
            text = Text(str(numbers[i]), font_size=20, color=BLACK).set_color(BLACK)
            text.move_to(rectangle.get_center())
            text.set_z_index(10)

        group = VGroup(rectangle, text)
        rectangles.add(group)

    rectangles.scale(scale)

    dictionary = {}
    for i in range(len(numbers)):
        dictionary[round(rectangles[i][0].height, 5)] = numbers[i]

    return rectangles, dictionary
