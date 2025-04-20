from manim import *
from utils.text import *

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 2160
config.pixel_height = 3840
config.frame_rate = 60
class scene0(ThreeDScene):

    def create_region_shepere(self, num_theta_divs, num_phi_divs, resolution) -> VGroup:

        regions = VGroup()
        for i in range(num_theta_divs):
            for j in range(num_phi_divs):

                # Definir los rangos de theta y phi para esta región
                theta_min = i * (TAU / num_theta_divs)  # Theta mínimo
                theta_max = (i + 1) * (TAU / num_theta_divs)  # Theta máximo
                phi_min = j * (PI / num_phi_divs)  # Phi mínimo
                phi_max = (j + 1) * (PI / num_phi_divs)  # Phi máximo

                # Crear la región (parche de la esfera)
                region = Surface(
                    lambda u, v: np.array(
                        [np.sin(v) * np.cos(u), np.sin(v) * np.sin(u), np.cos(v)]
                    ),
                    u_range=(theta_min, theta_max),  # Rango en theta
                    v_range=(phi_min, phi_max),  # Rango en phi
                    resolution=(resolution, resolution),
                )

                # Asignar un color único a cada región (opcional)
                """region.set_color(
                    interpolate_color(
                        BLUE, RED, (i + j) / (num_theta_divs + num_phi_divs)
                    )
                )
                """
                regions.add(region)
        return regions

    def create_spheres(self, cant=1, radius=1, resolution=10, ubication=[]) -> VGroup:
        spheres = VGroup()
        for i in range(cant):
            tempSphere = Sphere(radius=radius, resolution=(resolution, resolution))
            tempSphere.move_to(ubication[i] if len(ubication) else ORIGIN)
            tempSphere.z_index = 100
            spheres.add(tempSphere)
        return spheres

    def construct(self):
        # Configurar la cámara
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes()
        self.add(axes)

        # Crear una esfera completa utilizando regiones
        regions = VGroup()  # Grupo para almacenar las regiones

        # Número de divisiones en theta (ángulo azimutal) y phi (ángulo polar)
        num_theta_divs = 5
        num_phi_divs = 1
        resolution = 30

        regions = self.create_region_shepere(num_theta_divs, num_phi_divs, resolution)

        regions2 = self.create_region_shepere(3, 1, resolution).shift(LEFT * 4)

        regions3 = self.create_region_shepere(2, 1, resolution).shift(RIGHT * 4)

        # Animación: Rotar cada región individualmente
        self.begin_ambient_camera_rotation(rate=0.1)

        self.play(Create(regions))

        self.wait(2)

        spheresFirst = VGroup(*regions[:3])
        spheresSecond = VGroup(*regions[3:])

        self.play(
            *[
                spheresFirst[i].animate.move_to(regions2[i].get_center())
                for i in range(len(spheresFirst))
            ],
            *[
                spheresSecond[i].animate.move_to(regions3[i])
                for i in range(len(spheresSecond))
            ],
        )

        self.wait(2)

        self.play(
            *[
                AnimationGroup(ReplacementTransform(spheresFirst[i], regions2[i]))
                for i in range(len(spheresFirst))
            ],
            *[
                ReplacementTransform(spheresSecond[i], regions3[i])
                for i in range(len(spheresSecond))
            ],
        )

        self.wait(10)
