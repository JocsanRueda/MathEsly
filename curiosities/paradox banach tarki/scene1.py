from manim import *

config.frame_width = 9
config.frame_height = 16
config.pixel_width = int(2160/1)
config.pixel_height = int(3840/1)
config.frame_rate = int(60/1)


class scene1(Scene):

    def construct(self):
        math = Tex(r"Dada una colección $\{A_{\alpha}\}_{\alpha}$  de\\ conjuntos  disjuntos  dos a dos, \\ podemos encontrar un conjunto \\ B que contiene  exactamente  \\ un elemento de cada uno \\ de los $A_{\alpha}$.",
            font_size=28,
        )

        math.scale_to_fit_width(config.frame_width - 0.7)

        rectangle = Rectangle(
            width=math.width + 0.5, height=math.height + 0.5, color=BLUE
        )

        
        symbol = MathTex(r"\{ \text{ }\}")
        symbol.scale(2) 
        symbol.to_corner(UR)  

        self.play(Create(symbol))
        self.play(Create(rectangle))
        self.play(Write(math))
        self.wait(4)
