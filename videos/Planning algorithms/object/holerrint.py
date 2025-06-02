from manim import *

import random
from .clock import ClockDial


class FaceClockDial(VGroup):
    def __init__(self, width=3, height=2, radius=0.1, color=LIGHT_BROWN):
        super().__init__()
        # Proporciones base
        base_width = width
        base_height = height

        self.count = [0] * 10

        rec = Rectangle(
            width=base_width,
            height=base_height,
            fill_color=color,
            fill_opacity=1,
            stroke_color=DARK_BROWN,
            stroke_width=0.5,
        )

        # Crear diales con proporciones originales
        x_space = 0.05
        radius = (base_width - 0.3 - 9 * x_space) / 20
        dial_rows = VGroup()
        for i in range(4):
            row = VGroup(
                *[ClockDial(radius=radius, stroke_width=1.5) for _ in range(10)]
            )
            row.arrange(RIGHT, buff=x_space)
            if i == 0:
                row.move_to(rec.get_top() + DOWN * (radius + 0.2))
            else:
                row.next_to(dial_rows[-1], DOWN, buff=0.2)
            dial_rows.add(row)
        self.dial_rows = dial_rows
        dial_rows.move_to(rec.get_center())
        self.add(rec, dial_rows)

    def add_count(self, col, Is3D=False):
        """
        Avanza el contador posicional en la columna col.
        Siempre suma 1 y anima el "acarreo" si es necesario.
        Retorna un AnimationGroup con las animaciones.
        """
        anims = []
        carry = True
        row = 0
        while carry and row < 4:
            dial = self.dial_rows[row][col]
            if dial.counter < 9:
                anims.append(dial.add_count(Is3D=Is3D))
                carry = False
            else:
                anims.append(dial.add_count())
                row += 1
        return AnimationGroup(*reversed(anims))

    def random_add_count(self, Is3D=False):

        col = random.sample(range(10), k=5)
        return AnimationGroup(*[self.add_count(col=c, Is3D=Is3D) for c in col])


class PerforatedCard(VGroup):

    def __init__(self, perforated=False):
        super().__init__()
        self.perforated = perforated
        width = config.frame_width - 1
        height = config.frame_height - 2
        notch = 0.5

        # Definir los puntos del polígono (rectángulo con todas las esquinas recortadas)
        points = [
            [
                -width / 2 + notch / 5.5,
                height / 2,
                0,
            ],  # Superior izquierda (recorte pequeño)
            [width / 2 - notch, height / 2, 0],  # Superior derecha (recorte grande)
            [width / 2, height / 2 - notch, 0],  # Superior derecha (recorte grande)
            [
                width / 2,
                -height / 2 + notch / 5.5,
                0,
            ],  # Inferior derecha (recorte pequeño)
            [
                width / 2 - notch / 5.5,
                -height / 2,
                0,
            ],  # Inferior derecha (recorte pequeño)
            [
                -width / 2 + notch / 5.5,
                -height / 2,
                0,
            ],  # Inferior izquierda (recorte pequeño)
            [
                -width / 2,
                -height / 2 + notch / 5.5,
                0,
            ],  # Inferior izquierda (recorte pequeño)
            [
                -width / 2,
                height / 2 - notch / 5.5,
                0,
            ],  # Superior izquierda (recorte pequeño)
        ]

        card = Polygon(*points, fill_color=YELLOW_B, fill_opacity=1).set_stroke(
            color=YELLOW_A
        )

        digits = [
            [str(i % 10) if j % 2 == 0 else r"\hspace{0.2cm}" for j in range(90)]
            for i in range(10)
        ]

        text_digits = VGroup(*[MathTex(*d, font_size=24, color=BLACK) for d in digits])

        text_digits.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        text_digits.to_edge(UP, buff=1.8)
        self.text_digits = text_digits
        number = MathTex(*[str(i + 1) for i in range(45)], font_size=17, color=BLACK)

        for i in range(45):
            number[i].next_to(text_digits[-1][i * 2], DOWN, buff=0.2)

        card.add(number)

        def get_line(end, fS=0.4, fI=0.4, stroke_width=1.5):

            p1 = text_digits[0][2 * end].get_center()
            p2 = text_digits[-1][2 * end].get_center()

            return (
                Line(
                    p1 + [0, fS, 0],
                    p2 - [0, fI, 0],
                )
                .set_color(BLACK)
                .shift([-0.135, 0, 0])
                .set_stroke(width=stroke_width)
            )

        line1 = get_line(2, 0.6, 0.2, 2.5)
        line2 = get_line(6, 0.6, 0.2, 2.5)
        line3 = get_line(10, 0.4, 0.2, 1.5)
        line4 = get_line(14, 0.6, 0.2, 2.5)
        line5 = get_line(18, 0.4, 0.2, 1.5)
        line6 = get_line(22, 0.6, 0.2, 2.5)
        line7 = get_line(25, 0.6, 0.2, 2.5)
        line8 = get_line(29, 0.4, 0.2, 1.5)
        line9 = get_line(33, 0.6, 0.2, 2.5)
        line10 = get_line(37, 0.4, 0.2, 1.5)
        line11 = get_line(41, 0.6, 0.2, 2.5)

        hline1 = (
            Line(line2.get_start() - [0, 0.2, 0], line6.get_start() - [0, 0.2, 0])
            .set_color(BLACK)
            .set_stroke(width=1.5)
        )
        hline2 = (
            Line(
                line7.get_start() - [0, 0.2, 0],
                get_line(44, 0.4).get_start() + [0.15, 0, 0],
            )
            .set_color(BLACK)
            .set_stroke(width=1.5)
        )

        text_hollerith = Text("-Hollerith-", font_size=20, color=BLACK).rotate(-PI / 2)
        text_hollerith.next_to(text_digits, RIGHT, buff=0.2)
        card.add(text_hollerith)
        card.add(text_digits)
        card.add(line1)
        card.add(line2)
        card.add(line3)
        card.add(line4)
        card.add(line5)
        card.add(line6)
        card.add(line7)
        card.add(line8)
        card.add(line9)
        card.add(line10)
        card.add(line11)
        card.add(hline1)
        card.add(hline2)

        def get_circles(column, row):
            return (
                Circle(radius=0.07, color=BLACK, fill_opacity=1)
                .set_fill(color=BLACK)
                .move_to(self.text_digits[column][row * 2].get_center())
            )

        if self.perforated:
            randomCircles = VGroup(
                *[get_circles(random.randint(0, 9), i) for i in range(0, 45)]
            )
            card.add(randomCircles)
        self.add(card)


class CenseCard(VGroup):
    def __init__(self):
        super().__init__()
        sheet = Rectangle(
            width=15,
            height=8,
            fill_color="#f8f5e3",
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2.5,
        ).set_z_index(0)

        # Encabezado superior
        header = MarkupText(
            "<tt>CÉDULA CENSAL SIMPLIFICADA</tt>",
            font_size=32,
            font="JetBrains Mono",
            color=BLACK,
        ).move_to(sheet.get_top() + DOWN * 0.6)

        sheet_num = (
            MarkupText(
                "<tt>Hoja Nro: 01</tt>",
                font_size=20,
                font="JetBrains Mono",
                color=BLACK,
            )
            .next_to(header, RIGHT, buff=0.7)
            .align_to(header, UP)
        )

        # Sub-encabezado
        subheader = MarkupText(
            "<tt>Lugar: Villa Manim      Fecha: 10/ENE/1890      Censista: A. Coder</tt>",
            font_size=18,
            font="JetBrains Mono",
            color=BLACK,
        ).next_to(header, DOWN, buff=0.25)

        # Tabla de datos (monoespaciada, sin líneas)
        table = (
            MarkupText(
                "<tt>"
                "LN  NOMBRE       SEXO  EDAD  EST.CIV  OCUP.  NAC.  INSTR.  RELIG.\n"
                " 1  Ana Sol      F      32     2        1     1      2       0\n"
                " 2  Luis Paz     M      45     1        2     2      2       1\n"
                " 3  Eva Luna     F      08     3        0     1      1       1\n"
                " 4  Juan Cruz    M      19     1        3     2      2       0\n"
                " 5  (Siguiente)\n"
                "</tt>",
                font_size=22,
                font="JetBrains Mono",
                color=BLACK,
            )
            .next_to(subheader, DOWN, buff=0.4, aligned_edge=LEFT)
            .shift([-1.5, 0, 0])
        )

        self.text = table

        # Códigos explicativos
        codes = MarkupText(
            "<tt>"
            "EST.CIV: 0=Soltero, 1=Casado, 2=Viudo\n"
            "OCUP.: 0=Ninguna/Estudiante, 1=Hogar, 2=Agricultor, 3=Artesano\n"
            "NAC.: 0=Local, 1=Provincia Norte, 2=País Vecino\n"
            "INSTR.: 0=Analfabeto, 1=Lee, 2=Lee y escribe\n"
            "RELIG.: 0=Católica, 1=Otra\n"
            "</tt>",
            font_size=15,
            font="JetBrains Mono",
            color=BLACK,
        ).next_to(table, DOWN, buff=0.35, aligned_edge=LEFT)

        # Simulación de perforaciones laterales
        holes = VGroup(
            *[
                Circle(radius=0.07, color=BLACK, fill_opacity=1).move_to(
                    sheet.get_left() + RIGHT * 0.13 + UP * (2.8 - i * 0.7)
                )
                for i in range(11)
            ]
            + [
                Circle(radius=0.07, color=BLACK, fill_opacity=1).move_to(
                    sheet.get_right() + LEFT * 0.13 + UP * (2.8 - i * 0.7)
                )
                for i in range(11)
            ]
        )

        # Líneas divisorias (opcional, para mayor realismo)
        line_top = Line(
            sheet.get_left() + RIGHT * 0.3 + DOWN * 0.7,
            sheet.get_right() + LEFT * 0.3 + DOWN * 0.7,
            color=GREY_B,
            stroke_width=1.5,
        )
        line_bottom = Line(
            sheet.get_left() + RIGHT * 0.3 + UP * 2.2,
            sheet.get_right() + LEFT * 0.3 + UP * 2.2,
            color=GREY_B,
            stroke_width=1.5,
        )

        self.add(
            sheet,
            header,
            sheet_num,
            subheader,
            line_top,
            table,
            codes,
            line_bottom,
            holes,
        )


class TabularMachine2D(VGroup):

    def __init__(self, width=3, opened=True):
        super().__init__()
        self.opened = opened
        dark_wood = ManimColor("#8B4513")
        hline = Line(
            [-width * 1.5, 0.2, 0],
            [width * 1.05, 0.2, 0],
            color=WHITE,
        ).set_stroke(width=8, color=GRAY_C)

        # add horizontal line operator lever

        oLine = Line(
            hline.get_center(),
            hline.get_center() + [0, 0.2, 0],
            color=WHITE,
        ).set_stroke(width=12, color=GRAY_C)

        # point
        oLinePoint = (
            Circle(radius=0.05, color=GRAY_A)
            .set_fill(color=WHITE, opacity=1)
            .move_to(oLine.get_end())
        )

        oLine2 = Line(
            oLine.get_end(), oLine.get_end() + [2, 0, 0], color=WHITE
        ).set_stroke(width=12, color=GRAY_C)

        oLine2Point = (
            Circle(radius=0.05, color=GRAY_A)
            .set_fill(color=WHITE, opacity=1)
            .move_to(oLine2.get_end())
        )

        oLine3 = Line(
            oLine2.get_end(), oLine2.get_end() + [0, 0.4, 0], color=WHITE
        ).set_stroke(width=12, color=GRAY_C)

        oLine3Point = (
            Circle(radius=0.05, color=GRAY_A)
            .set_fill(color=WHITE, opacity=1)
            .move_to(oLine3.get_end())
        )

        lever = VGroup(oLine, oLine2, oLine3, oLinePoint, oLine2Point, oLine3Point)
        rline = Line(
            [-width * 1.5, hline.get_y(), 0],
            [-width * 1.5, hline.get_y() - 0.3, 0],
            color=WHITE,
        ).set_stroke(width=8, color=GRAY_C)

        bline = Line(
            [-width * 1.5, hline.get_y() - 0.3, 0],
            [width * 1.5, hline.get_y() - 0.3, 0],
            color=WHITE,
        ).set_stroke(width=8, color=GRAY_C)

        c1 = (
            Circle(radius=0.05, color=GRAY_A)
            .set_fill(color=WHITE, opacity=1)
            .move_to(rline.get_start())
        )
        c2 = (
            Circle(radius=0.05, color=GRAY_A)
            .set_fill(color=WHITE, opacity=1)
            .move_to(rline.get_end())
        )

        vline = VGroup(
            *[
                Line(
                    [
                        -width * 0.8 + i * ((width * 0.8 * 2 - 10 * hline.height)) / 9,
                        hline.get_y(),
                        0,
                    ],
                    [
                        -width * 0.8 + i * ((width * 0.8 * 2 - 10 * hline.height)) / 9,
                        hline.get_y() - 0.25,
                        0,
                    ],
                )
                for i in range(10)
            ]
        )

        self.pins = vline

        topPart = VGroup(vline, hline, lever)

        cgroup = VGroup(
            *[
                Arc(
                    angle=PI,
                    radius=0.05,
                    color=WHITE,
                    fill_color=WHITE,
                    fill_opacity=1,
                )
                .move_to([vline[i].get_start()[0], bline.get_y() + 0.02, 0])
                .scale([1, 2, 1])
                for i in range(10)
            ]
        )
        bottomPart = VGroup(
            cgroup,
            rline,
            bline,
            c1,
            c2,
        )

        self.topPart = topPart
        self.bottomPart = bottomPart
        self.add(topPart, bottomPart)

        # limit for card
        limit1 = Line(
            [-width * 1.01, bline.get_y(), 0],
            [-width * 1.01, bline.get_y() + 0.2, 0],
        ).set_stroke(width=6, color=GRAY_C)

        limit2 = Line(
            [width * 1.01, bline.get_y() + 0, 0],
            [width * 1.01, bline.get_y() + 0.2, 0],
        ).set_stroke(width=6, color=GRAY_C)

        # add rectangle bottom
        rectBotom = Rectangle(
            color=dark_wood,  # tono marrón madera
            width=bline.width * 2,
            height=5,
            fill_color=dark_wood,
            fill_opacity=1,
        ).set_stroke(width=5, color=BLACK)

        # Agregar dos patas debajo del rectBotom
        leg_width = 0.25
        leg_height = 2
        leg_color = dark_wood
        # Posiciones relativas a los extremos del rectángulo inferior
        left_leg = (
            Rectangle(
                width=leg_width,
                height=leg_height,
                fill_color=leg_color,
                fill_opacity=1,
                color=leg_color,
            )
            .next_to(rectBotom, DOWN, buff=0)
            .align_to(rectBotom, LEFT)
        ).set_stroke(width=5, color=BLACK)
        right_leg = (
            Rectangle(
                width=leg_width,
                height=leg_height,
                fill_color=leg_color,
                fill_opacity=1,
                color=leg_color,
            )
            .next_to(rectBotom, DOWN, buff=0)
            .align_to(rectBotom, RIGHT)
        ).set_stroke(width=5, color=BLACK)

        # back wall

        back_wall = Rectangle(
            color=dark_wood,
            width=0.7,
            height=10,
            fill_color=dark_wood,
            fill_opacity=1,
        ).set_stroke(width=5, color=BLACK)
        back_wall.next_to(rectBotom, LEFT, buff=0, aligned_edge=UP)
        self.add(back_wall)

        self.add(left_leg, right_leg)

        rectBotom.next_to(bline, DOWN, buff=0)
        self.add(rectBotom)
        self.add(limit1, limit2)

        if opened:
            topPart.rotate(45 * DEGREES, about_point=topPart[1].get_start())

        self.add(topPart, bottomPart)

    def set_state(self, opened):
        if opened:
            self.opened = True
            self.topPart.rotate(45 * DEGREES, about_point=self.topPart[1].get_start())
        else:
            self.opened = False
            self.topPart.rotate(-45 * DEGREES, about_point=self.topPart[1].get_start())

    def openTopPart(self):

        if not self.opened:
            self.opened = True
            return self.topPart.animate.rotate(
                45 * DEGREES, about_point=self.topPart[1].get_start()
            )
        else:
            return AnimationGroup()

    def closeTopPart(self):
        if self.opened:
            self.opened = False
            return self.topPart.animate.rotate(
                -45 * DEGREES, about_point=self.topPart[1].get_start()
            )
        else:
            return AnimationGroup()
