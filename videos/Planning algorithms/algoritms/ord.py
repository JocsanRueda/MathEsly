from manim import *


def bubble_sort_mobObjects(
    self,
    rectangles: VGroup,
    dictionary: dict,
    stroke_length=0.1,
    animate=True,
    add_sound=True,
    rotate=False,
):
    n = len(rectangles)
    if rotate:
        self.play(
            rectangles.animate.rotate(PI / 2, about_point=rectangles.get_center()),
        )

        self.play(
            AnimationGroup(
                *[
                    k[1].animate.rotate(-PI / 2, about_point=k[1].get_center())
                    for k in rectangles
                ]
            ),
        )

    for i in range(n):
        for j in range(0, n - i - 1):
            rectangles[j][0].set_fill(RED_D).set_stroke(color=BLACK)
            rectangles[j + 1][0].set_fill(GREEN_C).set_stroke(color=BLACK)
            if add_sound:
                self.add_sound(
                    f"assets/sounds/s_val_{dictionary[rectangles[j].height]}.wav"
                )
            # self.add_sound(f"assets/sounds/s_val_{dictionary[rectangles[j+1].height]}.wav")

            value1 = rectangles[j].get_width() if rotate else rectangles[j].get_height()
            value2 = (
                rectangles[j + 1].get_width()
                if rotate
                else rectangles[j + 1].get_height()
            )

            if value1 > value2:
                p_r1 = rectangles[j].get_center()
                p_r2 = rectangles[j + 1].get_center()

                if animate:
                    self.play(
                        rectangles[j].animate.move_to(
                            [
                                p_r2[0] if not rotate else p_r1[0],
                                p_r1[1] if not rotate else p_r2[1],
                                0,
                            ]
                        ),
                        rectangles[j + 1].animate.move_to(
                            [
                                p_r1[0] if not rotate else p_r2[0],
                                p_r2[1] if not rotate else p_r1[1],
                                0,
                            ]
                        ),
                        run_time=1,
                    )
                else:
                    rectangles[j].move_to([p_r2[0], p_r1[1], 0])
                    rectangles[j + 1].move_to([p_r1[0], p_r2[1], 0])

                rectangles[j], rectangles[j + 1] = rectangles[j + 1], rectangles[j]
                self.wait(0.04)
            rectangles[j][0].set_color(WHITE).set_stroke(color=BLACK)
            rectangles[j + 1][0].set_color(WHITE).set_stroke(color=BLACK)

    return rectangles


def merge_sort_mobObjects(
    scene, rectangles: VGroup, dictionary: dict, stroke_length=0.1, animate=True
):
    def merge(left, right):
        result = VGroup()
        i = j = 0
        while i < len(left) and j < len(right):
            r1 = left[i]
            r2 = right[j]

            # Colorear los rectángulos
            r1.set_fill(RED_D)
            r2.set_fill(GREEN_C)

            scene.add_sound(f"assets/sounds/s_val_{dictionary[r1.height]}.wav")
            scene.wait(0.04)
            if r1.height < r2.height:

                result.add(r1)
                i += 1
            else:

                result.add(r2)
                j += 1
            r1.set_fill(WHITE)
            r2.set_fill(WHITE)
        # Agregar lo restante
        result.add(*left[i:])
        result.add(*right[j:])
        return result

    def recursive_sort(rects: VGroup):
        if len(rects) <= 1:
            return rects

        mid = len(rects) // 2
        left = recursive_sort(VGroup(*rects[:mid]))
        right = recursive_sort(VGroup(*rects[mid:]))

        merged = merge(left, right)

        # Calcular nueva posición X para cada rectángulo
        total_len = len(merged)
        frame_width = config.frame_width
        rect_width = rectangles[0].width

        for idx, rect in enumerate(merged):
            new_x = rect_width * idx - (frame_width - 0.5 - rect_width) / 2

            current_y = rect.get_center()[1]
            target_pos = [new_x, current_y, 0]

            if animate:
                scene.play(rect.animate.move_to(target_pos), run_time=0.5)
            else:
                rect.move_to(target_pos)

        return merged

    # Iniciar la recursión
    sorted_rects = recursive_sort(rectangles)
    return sorted_rects


def heap_sort_mobObjects(scene, rectangles: VGroup, dictionary: dict, animate=True):
    def heapify(arr: VGroup, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[l].height > arr[largest].height:
            largest = l

        if r < n and arr[r].height > arr[largest].height:
            largest = r

        if largest != i:
            # Colorear los rectángulos involucrados
            arr[i].set_fill(RED_D)
            arr[largest].set_fill(GREEN_C)

            scene.add_sound(f"assets/sounds/s_val_{dictionary[arr[i].height]}.wav")
            scene.wait(0.04)

            # Intercambiar visualmente las posiciones
            pos_i = arr[i].get_x()
            pos_largest = arr[largest].get_x()

            if animate:
                scene.play(
                    arr[i].animate.set_x(pos_largest),
                    arr[largest].animate.set_x(pos_i),
                    run_time=0.5,
                )
            else:
                arr[i].set_x(pos_largest)
                arr[largest].set_x(pos_i)

            # Intercambiar en la lista
            arr[i], arr[largest] = arr[largest], arr[i]

            arr[i].set_fill(WHITE)
            arr[largest].set_fill(WHITE)

            heapify(arr, n, largest)

    n = len(rectangles)

    # Construir max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(rectangles, n, i)

    # Extraer elementos uno por uno
    for i in range(n - 1, 0, -1):
        # Intercambiar el primero con el último
        rectangles[0].set_fill(RED_D)
        rectangles[i].set_fill(GREEN_C)

        scene.add_sound(f"assets/sounds/s_val_{dictionary[rectangles[i].height]}.wav")
        scene.wait(0.04)

        pos_0 = rectangles[0].get_x()
        pos_i = rectangles[i].get_x()

        if animate:
            scene.play(
                rectangles[0].animate.set_x(pos_i),
                rectangles[i].animate.set_x(pos_0),
                run_time=0.5,
            )
        else:
            rectangles[0].set_x(pos_i)
            rectangles[i].set_x(pos_0)

        rectangles[0], rectangles[i] = rectangles[i], rectangles[0]

        rectangles[0].set_fill(WHITE)
        rectangles[i].set_fill(WHITE)

        heapify(rectangles, i, 0)

    return rectangles


def timsort_mobObjects(
    scene, rectangles: VGroup, dictionary: dict, RUN=32, animate=True
):
    # Precalcular todas las posiciones X esperadas
    x_positions = [rect.get_x() for rect in rectangles]

    def insertion_sort(arr: VGroup, left, right):
        for i in range(left + 1, right + 1):
            key_rect = arr[i]
            j = i - 1
            while j >= left and arr[j].height > key_rect.height:
                # Colorear
                arr[j].set_fill(RED_D)
                arr[j + 1].set_fill(GREEN_C)
                scene.add_sound(f"assets/sounds/s_val_{dictionary[arr[j].height]}.wav")
                scene.wait(0.04)

                # Animar
                if animate:
                    scene.play(
                        arr[j].animate.set_x(x_positions[j + 1]),
                        arr[j + 1].animate.set_x(x_positions[j]),
                        run_time=0.5,
                    )
                else:
                    arr[j].set_x(x_positions[j + 1])
                    arr[j + 1].set_x(x_positions[j])

                arr[j], arr[j + 1] = arr[j + 1], arr[j]

                arr[j].set_fill(WHITE)
                arr[j + 1].set_fill(WHITE)

                j -= 1

    def merge(arr: VGroup, l, m, r):
        len1 = m - l + 1
        len2 = r - m

        left = VGroup(*arr[l : m + 1])
        right = VGroup(*arr[m + 1 : r + 1])

        i = j = 0
        k = l

        while i < len1 and j < len2:
            r1 = left[i]
            r2 = right[j]

            r1.set_fill(RED_D)
            r2.set_fill(GREEN_C)
            scene.add_sound(f"assets/sounds/s_val_{dictionary[r1.height]}.wav")
            scene.wait(0.04)

            if r1.height <= r2.height:
                target_x = x_positions[k]
                if animate:
                    scene.play(r1.animate.set_x(target_x), run_time=0.5)
                else:
                    r1.set_x(target_x)
                arr[k] = r1
                i += 1
            else:
                target_x = x_positions[k]
                if animate:
                    scene.play(r2.animate.set_x(target_x), run_time=0.5)
                else:
                    r2.set_x(target_x)
                arr[k] = r2
                j += 1

            r1.set_fill(WHITE)
            r2.set_fill(WHITE)
            k += 1

        while i < len1:
            target_x = x_positions[k]
            if animate:
                scene.play(left[i].animate.set_x(target_x), run_time=0.5)
            else:
                left[i].set_x(target_x)
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len2:
            target_x = x_positions[k]
            if animate:
                scene.play(right[j].animate.set_x(target_x), run_time=0.5)
            else:
                right[j].set_x(target_x)
            arr[k] = right[j]
            j += 1
            k += 1

    n = len(rectangles)

    for i in range(0, n, RUN):
        insertion_sort(rectangles, i, min(i + RUN - 1, n - 1))

    size = RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                merge(rectangles, left, mid, right)
        size *= 2

    return rectangles
