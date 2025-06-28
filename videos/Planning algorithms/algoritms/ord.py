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
                    f"assets/sounds/s_val_{dictionary[round(rectangles[j].height,5)]}.wav"
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

            scene.add_sound(f"assets/sounds/s_val_{dictionary[round(r1.height,5)]}.wav")
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

            scene.add_sound(
                f"assets/sounds/s_val_{dictionary[round(arr[i].height,5)]}.wav"
            )
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

        scene.add_sound(
            f"assets/sounds/s_val_{dictionary[round(rectangles[i].height,5)]}.wav"
        )
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
    scene, rectangles: VGroup, dictionary: dict, RUN=32, animate=True, add_sound=True
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
                if add_sound:
                    scene.add_sound(
                        f"assets/sounds/s_val_{dictionary[round(arr[j].height,5)]}.wav"
                    )
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
            scene.add_sound(f"assets/sounds/s_val_{dictionary[round(r1.height,5)]}.wav")
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


def insertion_sort_mobObjects(
    scene, rectangles: VGroup, dictionary: dict, animate=True, add_sound=True
):
    n = len(rectangles)
    x_positions = [rect.get_x() for rect in rectangles]

    for i in range(1, n):
        key = rectangles[i]
        key_x = x_positions[i]
        key_height = key.height
        j = i - 1

        # Destacar el rectángulo actual
        key[0].set_fill(YELLOW).set_stroke(color=BLACK)

        while j >= 0 and rectangles[j].height > key_height:
            # Colorear elementos que se comparan
            rectangles[j][0].set_fill(RED_D).set_stroke(color=BLACK)
            rectangles[j + 1][0].set_fill(GREEN_C).set_stroke(color=BLACK)

            if add_sound:
                scene.add_sound(
                    f"assets/sounds/s_val_{dictionary[round(rectangles[j].height,5)]}.wav"
                )
            scene.wait(0.04)

            # Animar movimiento
            if animate:
                scene.play(
                    rectangles[j].animate.set_x(x_positions[j + 1]),
                    rectangles[j + 1].animate.set_x(x_positions[j]),
                    run_time=0.5,
                )
            else:
                rectangles[j].set_x(x_positions[j + 1])
                rectangles[j + 1].set_x(x_positions[j])

            # Intercambiar
            rectangles[j], rectangles[j + 1] = rectangles[j + 1], rectangles[j]
            j -= 1

            # Restaurar color
            rectangles[j + 1][0].set_fill(WHITE).set_stroke(color=BLACK)
            if j >= 0:
                rectangles[j][0].set_fill(WHITE).set_stroke(color=BLACK)

        key[0].set_fill(WHITE).set_stroke(color=BLACK)

    list(map(lambda rect: rect[0].set_fill(WHITE).set_stroke(color=BLACK), rectangles))
    return rectangles


def selection_sort_mobObjects(
    scene, rectangles: VGroup, dictionary: dict, animate=True, add_sound=True
):
    n = len(rectangles)
    x_positions = [rect.get_x() for rect in rectangles]

    for i in range(n):
        min_index = i
        rectangles[min_index][0].set_fill(GREEN_C).set_stroke(color=BLACK)

        for j in range(i + 1, n):
            # Colorear los rectángulos que se comparan
            rectangles[j][0].set_fill(RED_D).set_stroke(color=BLACK)
            if add_sound:
                scene.add_sound(
                    f"assets/sounds/s_val_{dictionary[round(rectangles[j].height,5)]}.wav"
                )
            scene.wait(0.04)

            if rectangles[j].height < rectangles[min_index].height:
                rectangles[min_index][0].set_fill(WHITE).set_stroke(
                    color=BLACK
                )  # Restaurar color
                min_index = j
                rectangles[min_index][0].set_fill(GREEN_C).set_stroke(color=BLACK)

            else:
                rectangles[j][0].set_fill(WHITE).set_stroke(color=BLACK)

        if min_index != i:
            # Intercambiar posiciones visualmente
            pos_i = x_positions[i]
            pos_min = x_positions[min_index]

            if animate:
                scene.play(
                    rectangles[i].animate.set_x(pos_min),
                    rectangles[min_index].animate.set_x(pos_i),
                    run_time=0.5,
                )
            else:
                rectangles[i].set_x(pos_min)
                rectangles[min_index].set_x(pos_i)

            # Intercambiar en el VGroup
            rectangles[i], rectangles[min_index] = rectangles[min_index], rectangles[i]

        # Restaurar colores
        rectangles[i][0].set_fill(WHITE).set_stroke(color=BLACK)
        if min_index != i:
            rectangles[min_index][0].set_fill(WHITE).set_stroke(color=BLACK)

    return rectangles


def radix_sort_mobObjects(
    scene, rectangles: VGroup, dictionary: dict, animate=True, add_sound=True
):
    import math

    def get_max_digit_count(rects: VGroup):
        return len(str(int(max(dictionary.values()))))

    def get_digit(value: float, digit_index: int) -> int:
        return (int(value) // (10**digit_index)) % 10

    x_positions = [rect.get_x() for rect in rectangles]
    max_digits = get_max_digit_count(rectangles)

    for d in range(max_digits):
        # Crear 10 "buckets" visuales
        buckets = [[] for _ in range(10)]

        for rect in rectangles:
            digit = get_digit(dictionary[round(rect.height, 5)], d)

            # Colorear el rectángulo por acceso
            rect[0].set_fill(RED_D).set_stroke(color=BLACK)
            if add_sound:
                scene.add_sound(
                    f"assets/sounds/s_val_{dictionary[round(rect.height,5)]}.wav"
                )
            scene.wait(0.04)
            buckets[digit].append(rect)
            rect[0].set_fill(WHITE).set_stroke(color=BLACK)

        # Juntar todos los buckets en orden
        new_order = [rect for bucket in buckets for rect in bucket]

        # Actualizar posiciones visuales
        for i, rect in enumerate(new_order):
            target_x = x_positions[i]
            if animate:
                scene.play(rect.animate.set_x(target_x), run_time=0.5)
            else:
                rect.set_x(target_x)
            # Colorear mientras se posiciona
            rect[0].set_fill(GREEN_C).set_stroke(color=BLACK)
            scene.wait(0.04)
            rect[0].set_fill(WHITE).set_stroke(color=BLACK)

        # Actualizar el grupo de rectángulos
        rectangles = VGroup(*new_order)

    return rectangles


def quick_sort_mobObjects(scene, rectangles: VGroup, dictionary: dict, animate=True):
    x_positions = [rect.get_x() for rect in rectangles]

    def partition(arr: VGroup, low: int, high: int):
        pivot = arr[high]
        pivot_value = pivot.height
        pivot[0].set_fill(GREEN_C).set_stroke(color=BLACK)

        i = low - 1
        for j in range(low, high):
            arr[j][0].set_fill(RED_D).set_stroke(color=BLACK)
            scene.add_sound(
                f"assets/sounds/s_val_{dictionary[round(arr[j].height,5)]}.wav"
            )
            scene.wait(0.04)

            if arr[j].height < pivot_value:
                i += 1
                if i != j:
                    # Intercambiar arr[i] con arr[j]
                    if animate:
                        scene.play(
                            arr[i].animate.set_x(x_positions[j]),
                            arr[j].animate.set_x(x_positions[i]),
                            run_time=0.5,
                        )
                    else:
                        arr[i].set_x(x_positions[j])
                        arr[j].set_x(x_positions[i])

                    arr[i], arr[j] = arr[j], arr[i]

            arr[j][0].set_fill(WHITE).set_stroke(color=BLACK)

        # Colocar el pivote en su posición final
        if (i + 1) != high:
            if animate:
                scene.play(
                    arr[i + 1].animate.set_x(x_positions[high]),
                    arr[high].animate.set_x(x_positions[i + 1]),
                    run_time=0.5,
                )
            else:
                arr[i + 1].set_x(x_positions[high])
                arr[high].set_x(x_positions[i + 1])

            arr[i + 1], arr[high] = arr[high], arr[i + 1]

        pivot[0].set_fill(WHITE).set_stroke(color=BLACK)
        return i + 1

    def quick_sort_recursive(arr: VGroup, low: int, high: int):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_recursive(arr, low, pi - 1)
            quick_sort_recursive(arr, pi + 1, high)

    quick_sort_recursive(rectangles, 0, len(rectangles) - 1)
    return rectangles


def counting_sort_mobObjects(
    scene, rectangles: VGroup, dictionary: dict, animate=True, add_sound=True
):
    import os

    # Obtener alturas como enteros
    heights = dictionary.values()
    x_positions = [rect.get_x() for rect in rectangles]

    max_val = max(heights)
    count = [0] * (max_val + 1)

    # Mapa de altura entera para cada rectángulo
    height_map = {rect: dictionary[round(rect.height, 5)] for rect in rectangles}

    # Paso 1: Conteo con color y sonido
    for rect in rectangles:
        h = height_map[rect]
        rect[0].set_fill(RED_D).set_stroke(color=BLACK)

        # Verifica si existe el archivo de sonido antes de reproducir
        if h in dictionary:
            sound_file = f"assets/sounds/s_val_{dictionary[round(rect.height, 5)]}.wav"
            if os.path.exists(sound_file) and add_sound:
                scene.add_sound(sound_file)

        scene.wait(0.04)
        count[h] += 1
        rect[0].set_fill(WHITE).set_stroke(color=BLACK)

    # Paso 2: Crear arreglo ordenado de alturas
    sorted_heights = []
    for h, c in enumerate(count):
        sorted_heights.extend([h] * c)

    # Paso 3: Reordenar visualmente
    used_rects = set()
    final_group = VGroup()

    for i, target_height in enumerate(sorted_heights):
        for rect in rectangles:
            if rect in used_rects:
                continue
            if height_map[rect] == target_height:
                used_rects.add(rect)

                # Mover rectángulo a su nueva posición
                rect[0].set_fill(GREEN_C).set_stroke(color=BLACK)
                if animate:
                    scene.play(rect.animate.set_x(x_positions[i]), run_time=0.5)
                else:
                    rect.set_x(x_positions[i])
                scene.wait(0.04)
                rect[0].set_fill(WHITE).set_stroke(color=BLACK)

                final_group.add(rect)
                break

    return final_group
