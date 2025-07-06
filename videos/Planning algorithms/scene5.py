from manim import *
from object.timeLine import Timeline
from object.arrayNumber import ArrayNumber


class Scene5(Scene):
    default_font = "JetBrains Mono"

    def construct(self):
        self.part1()

        self.part2()

    def part1(self):
        timeline = Timeline(
            start_year=1940, end_year=1950, step=1, extra_range=20, select_year=1945
        )

        self.play(timeline.Fade_In())
        self.wait(1)
        self.play(
            timeline.animate_select_year(
                1959, "Inicio de la segunda generación de computadoras", 25
            )
        )

        self.wait(1)

        self.play(
            timeline.Fade_Out(),
        )

    def part2(self):
        array = [50, 10, 7000, 3, 100]
        list_array = ArrayNumber(array, color=BLUE).scale(0.5).to_edge(UP)
        self.play(
            DrawBorderThenFill(list_array),
        )
        self.wait(1)

        # move pivote
        list_array.squares[0].save_state()
        self.play(list_array.squares[0].animate.set_color(RED))

        self.wait(1)

        list_array.squares[len(list_array.array) // 2].save_state()
        self.play(
            list_array.squares[len(list_array.array) // 2].animate.set_color(RED),
            Restore(list_array.squares[0]),
        )

        list_array.squares[-1].save_state()

        self.wait(1)

        self.play(
            list_array.squares[-1].animate.set_color(RED),
            Restore(list_array.squares[len(list_array.array) // 2]),
        )

        self.quick_sort_animation(list_array, self)

        self.wait(1)
        self.play(
            list_array.animate.set_color(BLUE).scale(1.2).move_to(ORIGIN + [0, 1, 0])
        )

        self.wait(1)

        # # computacional cost
        label = Text(
            "Complejidad de tiempo", font_size=36, color=WHITE, font=self.default_font
        ).next_to(list_array, DOWN, buff=0.5)
        text1 = MathTex("O(n^2)", font_size=48).next_to(label, DOWN)

        # computacional space
        label2 = Text(
            "Complejidad de espacio", font_size=36, color=WHITE, font=self.default_font
        ).move_to(label)
        text2 = MathTex(r"O(\log_{n})", font_size=48).next_to(label2, DOWN)

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
            FadeOut(label2),
            FadeOut(text2),
            FadeOut(list_array),
        )

        self.wait(1)

    def quick_sort_animation(self, array_group, scene, depth=0, show_text=False):

        if depth == 1 and show_text:
            print("Depth 1 reached, skipping animation")
            text = Text(
                "Divide y vencerás", font_size=26, color=WHITE, font=self.default_font
            ).next_to(array_group, DOWN, buff=0.5)

            self.play(Write(text))
            scene.wait(1.5)
            self.play(FadeOut(text))

        array = array_group.array
        n = len(array)

        if n <= 1:
            return array_group

        pivot_val = array[-1]
        pivot_square = array_group.squares[-1]
        pivot_square.generate_target()
        pivot_square.target.set_color(RED)
        scene.play(MoveToTarget(pivot_square))
        scene.wait(0.5)

        less_vals, greater_vals = [], []
        less_squares, greater_squares = [], []

        for i in range(n - 1):
            val = array[i]
            square = array_group.squares[i]
            if val <= pivot_val:
                less_vals.append(val)
                less_squares.append(square.copy())
                self.play(square.animate.set_color(GREEN))
            else:
                greater_vals.append(val)
                greater_squares.append(square.copy())
                self.play(square.animate.set_color(YELLOW))

        scene.wait(0.5)

        group_center = array_group.get_center()

        # Crear subarreglos visuales solo si tienen contenido
        if less_vals:
            less_array = array_group.separated_array(less_vals, show_lines=False)
            scene.play(less_array.animate.move_to(group_center + LEFT * 2 + DOWN * 1.5))
            sorted_less = self.quick_sort_animation(less_array, scene, depth + 1, True)
        else:
            sorted_less = ArrayNumber([], color=BLUE).scale(0.5)

        if greater_vals:
            greater_array = array_group.separated_array(greater_vals, show_lines=False)
            scene.play(
                greater_array.animate.move_to(group_center + RIGHT * 2 + DOWN * 1.5)
            )

            sorted_greater = self.quick_sort_animation(greater_array, scene, depth + 1)
        else:
            sorted_greater = ArrayNumber([], color=YELLOW).scale(0.5)

        # Pivote como ArrayNumber

        pivot_array = array_group.separated_array(
            [pivot_val], show_lines=False
        ).set_color(color=RED)
        scene.play(pivot_array.animate.move_to(group_center + DOWN * 2.5))
        scene.wait(0.5)

        merged_values = sorted_less.array + [pivot_val] + sorted_greater.array
        final_array = (
            array_group.separated_array(merged_values, show_lines=False)
            .set_color(color=GREEN)
            .move_to(group_center)
        )

        all_squares = (
            [s for s in sorted_less.squares]
            + [pivot_array.squares[0]]
            + [s for s in sorted_greater.squares]
        )
        modified_order = array_group.copy().modify_order(final_array.array)
        for i, s in enumerate(all_squares):
            s.generate_target()
            s.target.move_to(modified_order.squares[i].get_center())

        scene.play(
            *[MoveToTarget(s) for s in all_squares],
            array_group.new_order(final_array.array),
        )

        scene.play(FadeOut(*all_squares))
        self.wait(0.5)

        return array_group


class Scene6Part2(ThreeDScene):
    default_font = "JetBrains Mono"

    def construct(self):
        axes = ThreeDAxes()
        # Agregar nombres a los ejes
        x_label = Text("X").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("Y").next_to(axes.y_axis.get_end(), UP)
        z_label = Text("Z").next_to(axes.z_axis.get_end(), OUT)
        self.add(x_label, y_label, z_label, axes)

        self.set_camera_orientation(
            phi=65 * DEGREES, theta=40 * DEGREES, distance=16, zoom=1
        )

        image1 = ImageMobject("assets/hoare.jpg")

        image1.scale(0.5)

        rect = Rectangle(width=image1.width, height=image1.height).set_stroke(
            color=BLUE, width=5
        )

        rect.move_to(image1.get_center())

        name = Text(
            "Charles Antony Richard Hoare",
            font=self.default_font,
            font_size=32,
            color=WHITE,
            weight=BOLD,
        )

        name.next_to(image1, RIGHT, buff=2, aligned_edge=UP)

        years = Text(
            "1934 - ",
            font=self.default_font,
            font_size=16,
            color=WHITE,
        ).next_to(name, DOWN, buff=0.3)

        ocupation = Text(
            "Científico de la computación ",
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
            "QuickSort", font=self.default_font, font_size=48, color=BLUE, weight=BOLD
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

        # image2 = (
        #     ImageMobject("assets/von_neumann.webp")
        #     .scale(0.5)
        #     .move_to(image1.get_left(), aligned_edge=LEFT)
        # )

        # self.add_fixed_in_frame_mobjects(image2)

        # self.play(
        #     FadeIn(image2),
        #     rect.animate.stretch_to_fit_width(image2.width).move_to(
        #         [image2.get_left()[0], 0, 0],
        #         aligned_edge=LEFT,
        #     ),
        #     FadeOut(name),
        #     FadeOut(ocupation),
        #     FadeOut(years),
        #     FadeOut(text2),
        # )

        # text3 = (
        #     Text("EDVAC", font=self.default_font, font_size=48, color=BLUE, weight=BOLD)
        #     .next_to(rect, RIGHT, buff=3)
        #     .shift([0, 1, 0])
        # )

        # subText3 = Text(
        #     f"    Primeras computadoras \n electronicas programables",
        #     font=self.default_font,
        #     font_size=19,
        #     color=WHITE,
        # ).next_to(text3, DOWN, buff=0.25)

        # self.add_fixed_in_frame_mobjects(text3, subText3)

        # self.play(
        #     Write(text3),
        #     Write(subText3),
        # )

        # self.wait(1)
