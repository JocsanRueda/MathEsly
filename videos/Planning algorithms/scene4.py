from manim import *
from object.arrayNumber import ArrayNumber


class Scene4(ThreeDScene):
    default_font = "JetBrains Mono"

    def construct(self):

        self.part1()

    def part1(self):
        axes = ThreeDAxes()
        # Agregar nombres a los ejes
        x_label = Text("X").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("Y").next_to(axes.y_axis.get_end(), UP)
        z_label = Text("Z").next_to(axes.z_axis.get_end(), OUT)
        self.add(x_label, y_label, z_label, axes)

        self.set_camera_orientation(
            phi=65 * DEGREES, theta=40 * DEGREES, distance=16, zoom=1
        )

        image1 = ImageMobject("assets/von_neumann.jpg")

        image1.scale(0.5)

        rect = Rectangle(width=image1.width, height=image1.height).set_stroke(
            color=BLUE, width=5
        )

        rect.move_to(image1.get_center())

        name = Text(
            "John von Neumann",
            font=self.default_font,
            font_size=32,
            color=WHITE,
            weight=BOLD,
        )

        name.next_to(image1, RIGHT, buff=2, aligned_edge=UP)

        years = Text(
            "1903 - 1957",
            font=self.default_font,
            font_size=16,
            color=WHITE,
        ).next_to(name, DOWN, buff=0.3)

        ocupation = Text(
            "Matemático, físico y científico de la computación ",
            font=self.default_font,
            font_size=18,
            color=WHITE,
        ).next_to(years, DOWN, buff=0.4)

        group = Group(rect, image1, name, ocupation, years)

        self.move_camera(
            frame_center=ORIGIN + [0, 3, 1],
            theta=self.camera.get_theta() - 25 * DEGREES,
            zoom=1.4,
        )

        self.add_fixed_in_frame_mobjects(group)
        image1.shift([0, 3, 0])
        group.move_to(ORIGIN + [0, 1.5, 0])

        text2 = Text(
            "Merge sort", font=self.default_font, font_size=48, color=BLUE, weight=BOLD
        ).next_to(ocupation, DOWN, buff=0.5)

        self.play(
            FadeIn(group[:2]),
            Write(name),
            Write(ocupation),
            Write(years),
        )
        self.wait(1)

        self.add_fixed_in_frame_mobjects(text2)

        self.play(Write(text2))

        self.wait(1)

        image2 = (
            ImageMobject("assets/von_neumann.webp")
            .scale(0.5)
            .move_to(image1.get_left(), aligned_edge=LEFT)
        )

        self.add_fixed_in_frame_mobjects(image2)

        self.play(
            FadeIn(image2),
            rect.animate.stretch_to_fit_width(image2.width).move_to(
                [image2.get_left()[0], 0, 0],
                aligned_edge=LEFT,
            ),
            FadeOut(name),
            FadeOut(ocupation),
            FadeOut(years),
            FadeOut(text2),
        )

        text3 = (
            Text("EDVAC", font=self.default_font, font_size=48, color=BLUE, weight=BOLD)
            .next_to(rect, RIGHT, buff=3)
            .shift([0, 1, 0])
        )

        subText3 = Text(
            f"    Primeras computadoras \n electronicas programables",
            font=self.default_font,
            font_size=19,
            color=WHITE,
        ).next_to(text3, DOWN, buff=0.25)

        self.add_fixed_in_frame_mobjects(text3, subText3)

        self.play(
            Write(text3),
            Write(subText3),
        )

        self.wait(1)

        self.play(
            FadeOut(image1),
            FadeOut(image2),
            FadeOut(rect),
            FadeOut(text3),
            FadeOut(subText3),
        )

        self.wait(1)


class Scene4Part2(Scene):
    default_font = "JetBrains Mono"

    def construct(self):
        array = [50, 10, 7000, 3, 100]
        list_array = ArrayNumber(array, color=BLUE).scale(0.5).to_edge(UP)
        order_array = (
            ArrayNumber([0, 1, 2, 3, 4], color=WHITE, show_lines=False)
            .scale(0.5)
            .next_to(list_array, DOWN, buff=0.5)
        )

        mtext1 = MathTex(
            r"\left\lfloor \frac{n}{2} \right\rfloor", font_size=26
        ).next_to(list_array, RIGHT, buff=0.5)

        mtext2 = MathTex(
            r"= \left\lfloor \frac{5}{2} \right\rfloor", font_size=26
        ).next_to(mtext1, RIGHT, buff=0.1)

        mtext3 = MathTex(r"= 2", font_size=26).next_to(mtext2, RIGHT, buff=0.1)

        self.play(DrawBorderThenFill(list_array))
        self.wait(1)

        self.play(
            Write(mtext1),
        )

        self.play(Write(mtext2))

        self.play(Write(mtext3))

        self.wait(1)

        self.play(
            DrawBorderThenFill(order_array),
        )

        list_array.squares.save_state()

        self.play(
            list_array.squares[:2].animate.set_color(YELLOW),
        )
        self.wait(1)
        self.play(
            list_array.squares[2:].animate.set_color(RED),
        )

        self.wait(1)

        self.play(
            Restore(list_array.squares),
        )

        self.play(
            FadeOut(mtext1),
            FadeOut(mtext2),
            FadeOut(mtext3),
            FadeOut(order_array),
        )

        self.wait(1)

        self.merge_sort_animation(list_array, self)

        self.play(
            list_array.animate.move_to(ORIGIN),
        )

        self.wait(2)

        self.play(
            FadeOut(list_array),
        )

        self.wait(1)

    def merge_sort_animation(
        self, array_group, scene, depth=0, x_offset=0, final_array=None
    ):
        array = array_group.array
        n = len(array)

        if n <= 1:
            return array_group

        mid = n // 2

        left_array = array_group.separated(end=mid)
        right_array = array_group.separated(start=mid)

        self.play(
            left_array.animate.move_to(
                array_group.get_center() + LEFT * 2 + DOWN * 1.5
            ),
            right_array.animate.move_to(
                array_group.get_center() + RIGHT * 2 + DOWN * 1.5
            ),
        )

        scene.wait(0.5)

        # Recursivamente dividir y ordenar
        sorted_left = self.merge_sort_animation(left_array, scene, depth + 1)
        sorted_right = self.merge_sort_animation(right_array, scene, depth + 1)

        # Fusionar visualmente
        merged_array = self.merge(sorted_left, sorted_right, scene)
        self.add(merged_array)

        scene.play(
            array_group.new_order(merged_array.array),
            merged_array.animate.move_to(array_group.get_center()),
        )

        scene.play(
            FadeOut(merged_array),
            FadeOut(left_array),
            FadeOut(right_array),
        )

        return merged_array

    def merge(self, left, right, scene):
        l_idx, r_idx = 0, 0
        merged = []
        animations = []

        left_numbers = left.array
        right_numbers = right.array

        merged_array = []

        while l_idx < len(left_numbers) and r_idx < len(right_numbers):
            l_val = left_numbers[l_idx]
            r_val = right_numbers[r_idx]

            if l_val <= r_val:
                square = left.squares[l_idx].copy()
                merged_array.append(l_val)
                animations.append(square)
                l_idx += 1
            else:
                square = right.squares[r_idx].copy()
                merged_array.append(r_val)
                animations.append(square)
                r_idx += 1

        for i in range(l_idx, len(left_numbers)):
            square = left.squares[i].copy()
            merged_array.append(left_numbers[i])
            animations.append(square)

        for i in range(r_idx, len(right_numbers)):
            square = right.squares[i].copy()
            merged_array.append(right_numbers[i])
            animations.append(square)

        result_array = ArrayNumber(merged_array, color=GREEN).scale(0.5)
        result_array.move_to(DOWN * 3)

        for i, square in enumerate(animations):
            square.generate_target()
            square.target.move_to(result_array.squares[i].get_center())

        scene.play(*[MoveToTarget(s) for s in animations])

        self.wait(1)
        scene.play(FadeOut(*animations), FadeIn(result_array))

        self.wait(1)
        return result_array
