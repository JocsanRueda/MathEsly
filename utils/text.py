from manim import *


class WriteEquations3D(Succession):
    """
    A custom animation class to write equations in 3D space using Manim.

    Parameters
    ----------
    scene : Scene
        The scene in which the animation will be played.
    textGroup : VGroup
        A group of text objects to be animated.
    delay : float
        The delay between each animation step.
    **kwargs : dict
        Additional keyword arguments to be passed to the Succession class.

    Methods
    -------
    prepare()
        Prepares the text group by adding it to the scene and setting its initial opacity to 0.
    """

    def __init__(
        self, scene, textGroup, delay, position=False, first_affected=True, **kwargs
    ):
        self.scene = scene  # save the scene
        self.textGroup = textGroup
        self.delay = delay
        self.first_affected = first_affected

        # prepare animation before animation

        self.prepare()

        # define animation sequence

        if position:
            for i in range(len(textGroup)):
                textGroup[i].move_to(textGroup[0])

        animations = []

        if self.first_affected:
            animations.append(Write(textGroup[0]), textGroup[0].animate.set_opacity(1)),

        for i in range(len(textGroup) - 1):
            animations.append(
                AnimationGroup(
                    textGroup[i + 1].animate.set_opacity(1),
                    ReplacementTransform(textGroup[i], textGroup[i + 1]),
                    lag_ratio=0,
                )
            )
            animations.append(Wait(self.delay))

        animations.append(Wait(self.delay))

        # Initialize Succession with the list of animations
        super().__init__(*animations, **kwargs)

    def prepare(self):
        self.scene.add_fixed_in_frame_mobjects(self.textGroup)
        if self.first_affected:
            self.textGroup.set_opacity(0)
        else:
            self.textGroup[1:].set_opacity(0)


class Write3D(Succession):
    """
    A class to create a 3D writing animation in a Manim scene.

    Attributes:
    -----------
    scene : Scene
        The Manim scene where the animation will be played.
    textGroup : Mobject
        The text to be animated.

    Methods:
    --------
    __init__(scene, text, **kwargs):
        Initializes the Write3D object with the given scene and text.

    prepare():
        Prepares the text for the animation by setting its opacity to 0 and adding it to the scene as a fixed object.
    """

    def __init__(self, scene, text, **kwargs):
        self.scene = scene  # save the scene
        self.textGroup = text

        # prepare animation before animation

        self.prepare()

        # define animation sequence

        animations = []

        animations.append(
            AnimationGroup(Write(self.textGroup), self.textGroup.animate.set_opacity(1))
        )
        # Initialize Succession with the list of animations
        super().__init__(*animations, **kwargs)

    def prepare(self):
        self.textGroup.set_opacity(0)
        self.scene.add_fixed_in_frame_mobjects(self.textGroup)


class Uncreate3D(Succession):
    """
    A class to create a succession of animations that uncreate a 3D text object.

    Parameters
    ----------
    scene : Scene
        The scene in which the animation will take place.
    text : Mobject
        The text object to be uncreated.
    **kwargs : dict
        Additional keyword arguments passed to the Succession class.

    Attributes
    ----------
    scene : Scene
        The scene in which the animation will take place.
    textGroup : Mobject
        The text object to be uncreated.
    """

    def __init__(self, scene, text, **kwargs):
        self.scene = scene  # save the scene
        self.textGroup = text

        # prepare animation before animation
        # define animation sequence

        animations = []

        animations.append(Uncreate(text), text.animate.set_opacity(0))
        # Initialize Succession with the list of animations
        super().__init__(*animations, **kwargs)


class FadeOut3D(Succession):
    """
    A class to create a succession of animations that fade out a 3D text object.

    Parameters
    ----------
    scene : Scene
        The scene in which the animation will take place.
    text : Mobject
        The text object to be faded out.
    **kwargs : dict
        Additional keyword arguments passed to the Succession class.

    Attributes
    ----------
    scene : Scene
        The scene in which the animation will take place.
    textGroup : Mobject
        The text object to be faded out.
    """

    def __init__(self, scene, text, **kwargs):
        self.scene = scene  # save the scene
        self.textGroup = text

        # prepare animation before animation
        # define animation sequence

        animations = []

        animations.append(FadeOut(text), text.animate.set_opacity(0))
        # Initialize Succession with the list of animations
        super().__init__(*animations, **kwargs)


class FadeIn3D(Succession):
    def __init__(self, scene, text, **kwargs):
        self.scene = scene  # save the scene
        self.textGroup = text

        # prepare animation before animation

        self.prepare()

        # define animation sequence

        animations = []

        animations.append(
            AnimationGroup(
                FadeIn(self.textGroup), self.textGroup.animate.set_opacity(1)
            )
        )
        # Initialize Succession with the list of animations
        super().__init__(*animations, **kwargs)

    def prepare(self):
        self.textGroup.set_opacity(0)
        self.scene.add_fixed_in_frame_mobjects(self.textGroup)
