from glm import array
from manim import *


class SquareNumber(VGroup):
    default_font = "JetBrains Mono"
    square = None
    number_text = None
    number_string = None

    def get_square(self):
        return self.square

    def get_number_text(self):
        return self.number_text

    def get_number_string(self):
        return self.number_string

    def set_color(self, color=BLUE, **kwargs):
        # Solo cambia el color del cuadrado, nunca del texto
        self.square.set_color(color, **kwargs)
        # No tocar self.number_text
        return self

    def __init__(
        self,
        number=0,
        color=BLUE,
        width=1,
        height=1,
        resizable=False,
        font_size=24,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.number_string = str(number)

        number_text = Text(
            str(number),
            font=self.default_font,
            weight=BOLD,
            color=WHITE,
            font_size=font_size,
        )

        square = Rectangle(
            width=number_text.width + 0.2 if resizable else width,
            height=height,
            color=color,
            fill_opacity=0.5,
        )

        self.square = square
        self.number_text = number_text
        number_text.move_to(square.get_center())
        self.add(square, number_text)


class ArrayNumber(VGroup):
    default_font = "JetBrains Mono"
    squares = VGroup()
    lines = VGroup()
    head = None
    tail = None

    def __init__(
        self,
        array,
        color=BLUE,
        length_space=1,
        show_lines=True,
        vertical=False,
        width=1,
        height=1,
        font_size=24,
        **kwargs
    ):

        super().__init__(**kwargs)

        (self.squares, self.lines) = self.line_square(
            array,
            color=color,
            length_line=length_space,
            vertical=vertical,
            width=width,
            height=height,
            font_size=font_size,
        )

        self.head = array[0] if array else None
        self.tail = array[-1] if array else None
        self.array = array

        if show_lines:
            self.add(self.squares, self.lines)
        else:
            self.add(self.squares)

        self.move_to(ORIGIN)

    def modify_color(self, color, all_):
        if all_:
            return AnimationGroup(
                self.squares.animate.set_color(color),
                self.lines.animate.set_color(color),
            )
        else:
            return AnimationGroup(
                *[
                    square.get_square().animate.set_color(color)
                    for square in self.squares
                ]
            )

    def modify_order(self, array, positions=None):
        positions = (
            [square.get_center() for square in self.squares]
            if positions is None
            else positions
        )

        for i in range(len(array)):
            new_position = positions[i]

            self.squares[self.array.index(array[i])].move_to(new_position)

        copy_squares = []
        for i in range(len(array)):
            index = self.array.index(array[i])
            copy_squares.append(self.squares[index])
        self.squares = VGroup(*copy_squares)
        self.array = array

        return self

    def new_order(self, array, positions=None, lag_ratio=0):

        positions = (
            [square.get_center() for square in self.squares]
            if positions is None
            else positions
        )
        animation = list()

        for i in range(len(array)):
            new_position = positions[i]

            animation.append(
                self.squares[self.array.index(array[i])].animate.move_to(new_position)
            )

        copy_squares = []
        for i in range(len(array)):
            index = self.array.index(array[i])
            copy_squares.append(self.squares[index])
        self.squares = VGroup(*copy_squares)
        self.array = array
        return AnimationGroup(*animation, lag_ratio=lag_ratio)

    def line_square(
        self,
        array,
        color=BLUE,
        length_line=1,
        vertical=False,
        width=None,
        height=None,
        font_size=24,
    ):
        if not array:
            return VGroup(), VGroup()
        max_value = max(array)
        maxSquare = SquareNumber(
            max_value, color=color, resizable=True, font_size=font_size
        )
        square_length = maxSquare.width if width is None else width
        square_height = maxSquare.height if height is None else height

        squares = VGroup()
        lines = VGroup()
        position = DOWN if vertical else RIGHT

        for i, num in enumerate(array):
            square = SquareNumber(
                number=num,
                color=color,
                width=square_length,
                height=square_height,
            )
            if i == 0:
                square.move_to(ORIGIN)
            else:
                square.next_to(lines[i - 1], position, buff=0)

            squares.add(square)

            if i < len(array) - 1:
                line = Line(
                    ORIGIN,
                    ORIGIN + [0, length_line, 0] if vertical else [length_line, 0, 0],
                    color=color,
                )
                line.next_to(square, position, buff=0)
                lines.add(line)

        return squares, lines

    def calc_next(self, index):

        if index < len(self.array) - 1:
            return index
        else:
            return None

    def calc_prev(self, index):
        if index > 0:
            return index - 1
        else:
            return None

    def get_path(self, first_position, second_position, offset=1):
        path_array = [
            first_position,
            first_position + [0, 1, 0],
            [second_position[0], 1, 0],
            second_position,
        ]

        path_vgroup = VGroup()
        path_vgroup.set_points_as_corners([*path_array])
        return path_vgroup

    def move_element(self, index, new_position, animate=False):
        animation = []
        if 0 <= index < len(self.array):

            self.array[index], self.array[new_position] = (
                self.array[new_position],
                self.array[index],
            )

            first_element = self.squares[index]
            second_element = self.squares[new_position]

            first_position = first_element.get_center()
            second_position = second_element.get_center()

            if index > new_position:
                second_array = self.squares[new_position:index]
                path1 = self.get_path(first_position, second_position, offset=1)
                animation.append(MoveAlongPath(first_element, path1))
                animation.append(
                    second_array.animate.shift(
                        [first_element.width + self.lines[0].width, 0, 0]
                    )
                )
            else:
                second_array = self.squares[index + 1 : new_position + 1]
                path1 = self.get_path(first_position, second_position, offset=1)
                animation.append(MoveAlongPath(first_element, path1))

                animation.append(
                    second_array.animate.shift(
                        [-first_element.width - self.lines[0].width, 0, 0]
                    )
                )
            self.squares[index], self.squares[new_position] = (
                self.squares[new_position],
                self.squares[index],
            )

        return AnimationGroup(*animation)

    def separated_array(self, array, show_lines=True):
        newSquares = VGroup()
        newLines = VGroup()
        newArray = []
        for i in range(len(array)):
            for j in self.squares:
                if j.get_number_string() == str(array[i]):
                    newSquares.add(j.copy())
                    newArray.append(array[i])
                    if i < len(array) - 1 and show_lines:
                        newLines.add(self.lines[i].copy())
        newNumberAray = self.copy()
        newNumberAray.array = newArray
        newNumberAray.squares = newSquares
        newNumberAray.lines = newLines
        newNumberAray.submobjects = list(newSquares) + list(newLines)
        return newNumberAray

    def separated(self, start=None, end=None):
        newArray = []
        newSquares = VGroup()
        newLines = VGroup()
        if start is None and end is not None:
            newArray = self.array[:end]
            newSquares = self.squares[:end].copy()
            newLines = self.lines[: end - 1].copy()
        elif start is not None and end is None:
            newArray = self.array[start:]
            newSquares = self.squares[start:].copy()
            newLines = self.lines[start:].copy()
        elif start is not None and end is not None:
            newArray = self.array[start:end]
            newSquares = self.squares[start:end].copy()
            newLines = self.lines[start : end - 1].copy()

        newNumberAray = self.copy()
        newNumberAray.array = newArray
        newNumberAray.squares = newSquares
        newNumberAray.lines = newLines

        # ACTUALIZA LOS SUBMOBJECTS DEL VGROUP
        newNumberAray.submobjects = list(newSquares) + list(newLines)

        return newNumberAray
