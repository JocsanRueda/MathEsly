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
