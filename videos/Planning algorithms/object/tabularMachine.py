from manim import *
from object.holerrint import FaceClockDial

# Ensure you are using Manim version 0.19.0 or compatible
# For older versions, imports and class names might differ slightly.


class TabularMachine(VGroup):
    def __init__(
        self,
        main_structure_opacity=1.0,
        drawers_opacity=1.0,
        desktop_opacity=1.0,
        platform_opacity=1.0,  # Opacity for the existing platform
        card_reader_opacity=1.0,  # Opacity for the new card reader parts
        back_panel_opacity=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)  # Call VGroup's __init__

        # --- Overall Proportions ---
        machine_base_width = 5.0
        machine_base_depth = 3.0

        # --- Colors ---
        dark_wood = ManimColor("#8B4513")
        medium_wood = ManimColor("#A0522D")
        panel_color = ManimColor("#654321")
        handle_color = ManimColor("#4a2c1a")  # For drawer handles and lever grip
        trim_color = ManimColor("#5C4033")  # For trims and some mechanical parts
        metal_color = ManimColor("#A9A9A9")  # Main metal for card reader
        dark_metal_color = ManimColor("#696969")  # For presser plate
        card_slot_color = ManimColor("#333333")

        stroke_color_val = BLACK
        stroke_width_val = 0.2

        # --- 1. Side Panels (Legs/Supports) ---
        leg_upper_part_height = 2.5
        leg_base_plinth_height = 0.15
        leg_base_slope_height = 0.15
        leg_base_detail_height = leg_base_plinth_height + leg_base_slope_height
        leg_panel_height = leg_upper_part_height + leg_base_detail_height
        leg_panel_thickness = 0.3
        leg_panel_depth = machine_base_depth * 0.9
        leg_y_center_upper = leg_base_detail_height + (leg_upper_part_height / 2)
        leg_y_center_base_plinth = leg_base_plinth_height / 2
        leg_y_center_base_slope = leg_base_plinth_height + (leg_base_slope_height / 2)
        body_inner_width = machine_base_width - 2 * leg_panel_thickness
        side_panels_group = VGroup()
        for side_multiplier in [-1, 1]:
            x_pos = side_multiplier * (
                (body_inner_width / 2) + (leg_panel_thickness / 2)
            )
            upper_leg = Prism(
                dimensions=[
                    leg_panel_thickness,
                    leg_upper_part_height,
                    leg_panel_depth,
                ],
                fill_color=dark_wood,
                stroke_color=stroke_color_val,
                stroke_width=stroke_width_val,
                fill_opacity=main_structure_opacity,
            ).move_to([x_pos, leg_y_center_upper, 0])
            side_panels_group.add(upper_leg)
            base_plinth_block = Prism(
                dimensions=[
                    leg_panel_thickness * 1.25,
                    leg_base_plinth_height,
                    leg_panel_depth * 1.1,
                ],
                fill_color=dark_wood,
                stroke_color=stroke_color_val,
                stroke_width=stroke_width_val,
                fill_opacity=main_structure_opacity,
            ).move_to([x_pos, leg_y_center_base_plinth, 0])
            side_panels_group.add(base_plinth_block)
            base_slope_block = Prism(
                dimensions=[
                    leg_panel_thickness * 1.1,
                    leg_base_slope_height,
                    leg_panel_depth * 1.05,
                ],
                fill_color=dark_wood,
                stroke_color=stroke_color_val,
                stroke_width=stroke_width_val,
                fill_opacity=main_structure_opacity,
            ).move_to([x_pos, leg_y_center_base_slope, 0])
            side_panels_group.add(base_slope_block)
            side_face_panel_thickness = 0.04
            side_face_panel_height = leg_upper_part_height * 0.75
            side_face_panel_depth = leg_panel_depth * 0.75
            panel_x_center = x_pos + side_multiplier * (
                (leg_panel_thickness / 2) + (side_face_panel_thickness / 2)
            )
            actual_side_panel = Prism(
                dimensions=[
                    side_face_panel_thickness,
                    side_face_panel_height,
                    side_face_panel_depth,
                ],
                fill_color=medium_wood,
                stroke_color=stroke_color_val,
                stroke_width=stroke_width_val * 0.7,
                fill_opacity=main_structure_opacity,
            ).move_to([panel_x_center, leg_y_center_upper, 0])
            side_panels_group.add(actual_side_panel)
        self.add(side_panels_group)

        # --- 2. Front Panels (Simulating Drawers) & Handles ---
        num_drawers = 4
        drawer_spacing = 0.05
        total_drawer_height_space = (
            leg_upper_part_height - (num_drawers + 1) * drawer_spacing
        )
        drawer_front_height = total_drawer_height_space / num_drawers
        drawer_front_depth = 0.15
        drawers_group = VGroup()
        handle_radius = 0.04
        handle_length = 0.05
        handle_base_radius = 0.06
        handle_base_thickness = 0.02
        for i in range(num_drawers):
            drawer_y_pos = (
                leg_base_detail_height
                + drawer_spacing
                + (drawer_front_height / 2)
                + i * (drawer_front_height + drawer_spacing)
            )
            # User's specific Z positioning for drawers
            drawer_z_front_face = (leg_panel_depth / 2) - (drawer_front_depth / 2) - 5

            drawer_front = Prism(
                dimensions=[body_inner_width, drawer_front_height, drawer_front_depth],
                fill_color=panel_color,
                stroke_color=stroke_color_val,
                stroke_width=stroke_width_val,
                fill_opacity=drawers_opacity,
            ).move_to([0, drawer_y_pos, drawer_z_front_face])
            drawers_group.add(drawer_front)

            handle_base_z = (
                drawer_z_front_face
                + (drawer_front_depth / 2)
                + (handle_base_thickness / 2)
                - 0.005
            )
            handle_plate = Cylinder(
                radius=handle_base_radius,
                height=handle_base_thickness,
                direction=Z_AXIS,
                fill_color=handle_color,
                stroke_color=BLACK,
                stroke_width=stroke_width_val * 0.3,
                resolution=(10, 10),
                fill_opacity=drawers_opacity,
            ).move_to([0, drawer_y_pos, handle_base_z])
            drawers_group.add(handle_plate)
            handle_cylinder_z = (
                handle_base_z + (handle_base_thickness / 2) + (handle_length / 2)
            )
            handle_grip = Cylinder(
                radius=handle_radius,
                height=handle_length,
                direction=Z_AXIS,
                fill_color=handle_color,
                stroke_color=BLACK,
                stroke_width=stroke_width_val * 0.5,
                resolution=(8, 8),
                fill_opacity=drawers_opacity,
            ).move_to([0, drawer_y_pos, handle_cylinder_z])
            drawers_group.add(handle_grip)

        # Manual Z offset for drawers as per user's code
        manual_drawers_z_offset = -2.5
        if manual_drawers_z_offset != 0:
            drawers_group.shift(IN * manual_drawers_z_offset)

        self.add(drawers_group)

        # --- 3. Desktop Surface with Edge Molding ---
        desktop_thickness = 0.2
        desktop_width = machine_base_width
        desktop_depth = machine_base_depth
        desktop_y_center = leg_panel_height + (desktop_thickness / 2)
        desktop = Prism(
            dimensions=[desktop_width, desktop_thickness, desktop_depth],
            fill_color=medium_wood,
            stroke_color=stroke_color_val,
            stroke_width=stroke_width_val,
            fill_opacity=desktop_opacity,
        ).move_to([0, desktop_y_center, 0])
        molding_thickness = 0.05
        molding_depth_ext = 0.05
        front_molding = Prism(
            dimensions=[desktop_width, molding_thickness, molding_depth_ext],
            fill_color=trim_color,
            stroke_width=0,
            fill_opacity=desktop_opacity,
        ).move_to(
            [0, desktop_y_center, (desktop_depth / 2) + (molding_depth_ext / 2) - 0.01]
        )
        left_molding = Prism(
            dimensions=[molding_depth_ext, molding_thickness, desktop_depth],
            fill_color=trim_color,
            stroke_width=0,
            fill_opacity=desktop_opacity,
        ).move_to(
            [-(desktop_width / 2) - (molding_depth_ext / 2) + 0.01, desktop_y_center, 0]
        )
        right_molding = Prism(
            dimensions=[molding_depth_ext, molding_thickness, desktop_depth],
            fill_color=trim_color,
            stroke_width=0,
            fill_opacity=desktop_opacity,
        ).move_to(
            [(desktop_width / 2) + (molding_depth_ext / 2) - 0.01, desktop_y_center, 0]
        )
        desktop_group = VGroup(desktop, front_molding, left_molding, right_molding)
        self.add(desktop_group)

        # --- 4. Raised Platform on Desktop (existing) ---
        platform_main_width = machine_base_width * 0.35
        platform_main_depth = machine_base_depth * 0.45
        platform_main_thickness = 0.15

        platform_y_base = desktop_y_center + (desktop_thickness / 2)

        desktop_platform_main = Prism(
            dimensions=[
                platform_main_width,
                platform_main_thickness,
                platform_main_depth,
            ],
            fill_color=dark_wood,
            stroke_color=stroke_color_val,
            stroke_width=stroke_width_val,
            fill_opacity=platform_opacity,
        )
        platform_main_y_center_on_desk = platform_y_base + platform_main_thickness / 2
        desktop_platform_main.move_to([0, platform_main_y_center_on_desk, 0])

        platform_x_offset = machine_base_width * 0.22
        platform_z_offset = machine_base_depth * 0.1

        desktop_platform_group = VGroup(desktop_platform_main)
        desktop_platform_group.move_to(
            [platform_x_offset, platform_main_y_center_on_desk, platform_z_offset]
        )
        self.add(desktop_platform_group)

        actual_platform_main_center = desktop_platform_main.get_center()
        actual_platform_main_top_y = (
            actual_platform_main_center[1] + platform_main_thickness / 2
        )

        # --- 4b. Card Reader Mechanism (Refined Side Lever) ---
        card_reader_assembly = VGroup()

        # Base of the card reader
        reader_lower_base_height = 0.15
        reader_lower_base_width = platform_main_width * 0.85
        reader_lower_base_depth = platform_main_depth * 0.75
        reader_lower_base_y = actual_platform_main_top_y + reader_lower_base_height / 2

        reader_lower_base = Prism(
            dimensions=[
                reader_lower_base_width,
                reader_lower_base_height,
                reader_lower_base_depth,
            ],
            fill_color=metal_color,
            stroke_color=stroke_color_val,
            stroke_width=stroke_width_val * 0.7,
            fill_opacity=card_reader_opacity,
        ).move_to(
            [
                actual_platform_main_center[0],
                reader_lower_base_y,
                actual_platform_main_center[2],
            ]
        )
        card_reader_assembly.add(reader_lower_base)

        # Upper platform for card insertion
        reader_upper_platform_height = 0.05
        reader_upper_platform_width = reader_lower_base_width * 0.9
        reader_upper_platform_depth = reader_lower_base_depth * 0.8
        reader_upper_platform_y = (
            reader_lower_base_y
            + reader_lower_base_height / 2
            + reader_upper_platform_height / 2
        )

        reader_upper_platform = Prism(
            dimensions=[
                reader_upper_platform_width,
                reader_upper_platform_height,
                reader_upper_platform_depth,
            ],
            fill_color=medium_wood,
            stroke_color=stroke_color_val,
            stroke_width=stroke_width_val * 0.5,
            fill_opacity=card_reader_opacity,
        ).move_to(
            [
                actual_platform_main_center[0],
                reader_upper_platform_y,
                actual_platform_main_center[2],
            ]
        )
        card_reader_assembly.add(reader_upper_platform)

        # Card Slot
        card_slot_width = reader_upper_platform_width * 0.6
        card_slot_height = reader_upper_platform_height * 1.2
        card_slot_depth = 0.03
        card_slot_y = reader_upper_platform_y
        card_slot_z = (
            reader_upper_platform.get_center()[2]
            - reader_upper_platform_depth / 2
            + card_slot_depth / 2
            + 0.02
        )

        card_slot = Prism(
            dimensions=[card_slot_width, card_slot_height, card_slot_depth],
            fill_color=card_slot_color,
            stroke_width=0,
            fill_opacity=card_reader_opacity,
        ).move_to([actual_platform_main_center[0], card_slot_y, card_slot_z])
        card_reader_assembly.add(card_slot)

        # Side Pivot Support Block (on the right of the reader_upper_platform)
        side_pivot_block_width = 0.15  # X-dimension
        side_pivot_block_height = 0.3  # Y-dimension
        side_pivot_block_depth = 0.2  # Z-dimension

        side_pivot_block_x = (
            reader_upper_platform.get_right()[0] + side_pivot_block_width / 2 + 0.02
        )
        side_pivot_block_y = (
            reader_upper_platform_y  # Align Y with upper platform for simplicity
        )
        side_pivot_block_z = (
            reader_upper_platform.get_center()[2]
            - reader_upper_platform_depth / 2
            + side_pivot_block_depth / 2
        )  # At the back of upper platform

        side_pivot_support_block = Prism(
            dimensions=[
                side_pivot_block_width,
                side_pivot_block_height,
                side_pivot_block_depth,
            ],
            fill_color=metal_color,
            fill_opacity=card_reader_opacity,
        ).move_to([side_pivot_block_x, side_pivot_block_y, side_pivot_block_z])
        card_reader_assembly.add(side_pivot_support_block)

        # Pivot Axle (Visual, inside the side_pivot_support_block)
        pivot_axle_radius = 0.025
        pivot_axle_length = (
            side_pivot_block_width * 1.2
        )  # Slightly longer to pass through
        self.lever_pivot_point = (
            side_pivot_support_block.get_center() + UP * 0.05
        )  # Pivot slightly above center of block

        pivot_axle_side = Cylinder(
            radius=pivot_axle_radius,
            height=pivot_axle_length,
            direction=X_AXIS,
            fill_color=dark_metal_color,
            fill_opacity=card_reader_opacity,
        ).move_to(self.lever_pivot_point)
        card_reader_assembly.add(pivot_axle_side)

        # Lever Assembly (Side Lever)
        lever_arm_length = (
            reader_upper_platform_depth * 0.9
        )  # Length of the main arm (extends forward)
        lever_arm_thickness = 0.08  # Thickness of the arm (Y and X dimensions)

        self.lever_arm_main = Prism(
            dimensions=[
                lever_arm_thickness,
                lever_arm_thickness,
                lever_arm_length,
            ],  # X, Y, Z
            fill_color=metal_color,
            stroke_color=stroke_color_val,
            stroke_width=stroke_width_val * 0.5,
            fill_opacity=card_reader_opacity,
        )
        # Position arm so its back edge pivots around self.lever_pivot_point
        # The arm extends along Z from the pivot
        self.lever_arm_main.move_to(
            self.lever_pivot_point
            + OUT
            * (
                lever_arm_length / 2 - lever_arm_thickness / 2
            )  # Shift forward from pivot
        )

        # Presser Plate (moves with the lever arm)
        presser_plate_width_x = reader_upper_platform_width * 0.7
        presser_plate_thickness_y = 0.05
        presser_plate_length_z = reader_upper_platform_depth * 0.5
        self.lever_presser_plate = Prism(
            dimensions=[
                presser_plate_width_x,
                presser_plate_thickness_y,
                presser_plate_length_z,
            ],
            fill_color=dark_metal_color,
            stroke_color=stroke_color_val,
            stroke_width=stroke_width_val * 0.3,
            fill_opacity=card_reader_opacity,
        )
        # Position relative to where the card slot is, and link its Y to the arm's Y
        presser_plate_x = actual_platform_main_center[0]  # Centered with card slot
        presser_plate_y = (
            self.lever_pivot_point[1]
            - lever_arm_thickness
            - presser_plate_thickness_y / 2
        )  # Below the arm's pivot height
        presser_plate_z = reader_upper_platform.get_center()[
            2
        ]  # Centered over the card area
        self.lever_presser_plate.move_to(
            [presser_plate_x, presser_plate_y, presser_plate_z]
        )

        # Handle Grip
        handle_grip_length = 0.4  # Length of the grip (along X)
        handle_grip_radius = 0.07

        # Position handle at the front end of the lever_arm_main
        handle_position_base = self.lever_arm_main.get_center() + OUT * (
            lever_arm_length / 2
        )
        self.handle_grip = Cylinder(
            radius=handle_grip_radius,
            height=handle_grip_length,
            direction=X_AXIS,
            fill_color=handle_color,
            fill_opacity=card_reader_opacity,
            resolution=(16, 16),
        ).move_to(
            handle_position_base + UP * 0.05
        )  # Slightly up from arm's center

        self.lever_assembly = VGroup(
            self.lever_arm_main, self.lever_presser_plate, self.handle_grip
        )
        card_reader_assembly.add(self.lever_assembly)
        self.add(card_reader_assembly)

        # --- 5. Back Panel Components ---
        back_panel_deco_base_height = 0.4
        back_panel_deco_base_depth = machine_base_depth * 0.15
        back_panel_deco_base_width = machine_base_width
        back_panel_deco_base_y_center = (
            desktop_y_center
            + (desktop_thickness / 2)
            + (back_panel_deco_base_height / 2)
        )
        back_panel_deco_base_z_position = -(desktop_depth / 2) + (
            back_panel_deco_base_depth / 2
        )
        decorative_back_base = Prism(
            dimensions=[
                back_panel_deco_base_width,
                back_panel_deco_base_height,
                back_panel_deco_base_depth,
            ],
            fill_color=dark_wood,
            stroke_color=stroke_color_val,
            stroke_width=stroke_width_val,
            fill_opacity=back_panel_opacity,
        ).move_to([0, back_panel_deco_base_y_center, back_panel_deco_base_z_position])
        self.add(decorative_back_base)
        main_back_panel_height = 3.0
        main_back_panel_thickness = 0.25
        main_back_panel_width = machine_base_width * 0.98
        main_back_panel_y_center = (
            back_panel_deco_base_y_center
            + (back_panel_deco_base_height / 2)
            + (main_back_panel_height / 2)
        )
        main_back_panel_z_position = back_panel_deco_base_z_position
        main_back_panel = Prism(
            dimensions=[
                main_back_panel_width,
                main_back_panel_height,
                main_back_panel_thickness,
            ],
            fill_color=dark_wood,
            stroke_color=stroke_color_val,
            stroke_width=stroke_width_val,
            fill_opacity=back_panel_opacity,
        ).move_to([0, main_back_panel_y_center, main_back_panel_z_position])
        self.add(main_back_panel)
        faceClockDial = FaceClockDial(
            main_back_panel_width,
            main_back_panel_height,
            0.1,
            dark_wood,
        ).move_to([0, main_back_panel_y_center, main_back_panel_z_position])
        self.add(faceClockDial)

        self.faceClockDial = faceClockDial  # Store the clock dial for later use
        # Adding the main back panel

        pillar_thickness = 0.15
        pillar_height = main_back_panel_height * 1.05
        back_panel_pillars_group = VGroup()
        for x_mult_bp in [-1, 1]:
            pillar_x_bp = x_mult_bp * (
                (main_back_panel_width / 2) + (pillar_thickness / 2) - 0.05
            )
            pillar_z_bp = (
                main_back_panel_z_position
                + (main_back_panel_thickness / 2)
                - (pillar_thickness / 2)
                + 0.02
            )
            pillar_bp = Prism(
                dimensions=[pillar_thickness, pillar_height, pillar_thickness],
                fill_color=trim_color,
                stroke_width=stroke_width_val * 0.5,
                fill_opacity=back_panel_opacity,
            ).move_to(
                [
                    pillar_x_bp,
                    main_back_panel_y_center
                    + (pillar_height - main_back_panel_height) / 2,
                    pillar_z_bp,
                ]
            )
            back_panel_pillars_group.add(pillar_bp)
        self.add(back_panel_pillars_group)
        cornice_base_height = 0.15
        cornice_top_height = 0.10
        cornice_base_depth_ext = 0.1
        cornice_top_depth_ext = 0.15
        cornice_base_width_ext = 0.1
        cornice_top_width_ext = 0.15
        cornice_base_actual_depth = main_back_panel_thickness + cornice_base_depth_ext
        cornice_base_actual_width = main_back_panel_width + cornice_base_width_ext
        cornice_top_actual_depth = main_back_panel_thickness + cornice_top_depth_ext
        cornice_top_actual_width = main_back_panel_width + cornice_top_width_ext
        cornice_base_y = (
            main_back_panel_y_center
            + (main_back_panel_height / 2)
            + (cornice_base_height / 2)
        )
        cornice_top_y = (
            cornice_base_y + (cornice_base_height / 2) + (cornice_top_height / 2)
        )
        cornice_base_z = main_back_panel_z_position - (cornice_base_depth_ext / 2)
        cornice_top_z = main_back_panel_z_position - (cornice_top_depth_ext / 2)
        back_panel_cornice_base = Prism(
            dimensions=[
                cornice_base_actual_width,
                cornice_base_height,
                cornice_base_actual_depth,
            ],
            fill_color=medium_wood,
            stroke_color=stroke_color_val,
            stroke_width=stroke_width_val,
            fill_opacity=back_panel_opacity,
        ).move_to([0, cornice_base_y, cornice_base_z])
        back_panel_cornice_top = Prism(
            dimensions=[
                cornice_top_actual_width,
                cornice_top_height,
                cornice_top_actual_depth,
            ],
            fill_color=medium_wood,
            stroke_color=stroke_color_val,
            stroke_width=stroke_width_val,
            fill_opacity=back_panel_opacity,
        ).move_to([0, cornice_top_y, cornice_top_z])
        detailed_cornice = VGroup(back_panel_cornice_base, back_panel_cornice_top)
        self.add(detailed_cornice)

        # Global rotations
        self.rotate(angle=PI / 2, axis=X_AXIS, about_point=self.get_center())
        self.rotate(angle=PI / 2, axis=Z_AXIS, about_point=self.get_center())
        self.move_to(ORIGIN)

    def open_reader(self, animate=True, animation_duration=0.4):
        angle_of_rotation = PI / 8
        animation_duration = 0.4
        if animate:
            return Rotate(
                self.lever_assembly,
                angle=-angle_of_rotation,
                axis=Y_AXIS,  # Rotating around an X-axis relative to the pivot
                about_point=-self.lever_pivot_point * 0.5,
                run_time=animation_duration,
            )
        else:
            self.lever_assembly.rotate(
                angle=-angle_of_rotation,
                axis=Y_AXIS,
                about_point=-self.lever_pivot_point * 0.5,
            )
            return None

    def close_reader(self, animate=True, animation_duration=0.4):
        angle_of_rotation = PI / 8
        animation_duration = 0.4
        if animate:
            return Rotate(
                self.lever_assembly,
                angle=+angle_of_rotation,
                axis=Y_AXIS,
                about_point=-self.lever_pivot_point * 0.5,
                run_time=animation_duration,
            )
        else:
            self.lever_assembly.rotate(
                angle=+angle_of_rotation,
                axis=Y_AXIS,
                about_point=-self.lever_pivot_point * 0.5,
            )
            return None

    def read_card(self):
        angle_of_rotation = PI / 8
        animation_duration = 0.4
        anim_down = Rotate(
            self.lever_assembly,
            angle=-angle_of_rotation,
            axis=Y_AXIS,  # Rotating around an X-axis relative to the pivot
            about_point=-self.lever_pivot_point * 0.5,
            run_time=animation_duration,
        )
        anim_up = Rotate(
            self.lever_assembly,
            angle=+angle_of_rotation,
            axis=Y_AXIS,
            about_point=-self.lever_pivot_point * 0.5,
            run_time=animation_duration,
        )
        return Succession(anim_down, Wait(0.25), anim_up, lag_ratio=1.0)


# class HollerithMachine3D(ThreeDScene):
#     def construct(self):
#         self.set_camera_orientation(
#             phi=65 * DEGREES, theta=40 * DEGREES, distance=16, zoom=0.8
#         )
#         machine = TabularMachineFace(
#             main_structure_opacity=1.0,
#             drawers_opacity=1.0,
#             desktop_opacity=1.0,
#             platform_opacity=1.0,
#             card_reader_opacity=1.0,
#             back_panel_opacity=1.0,
#         )
#         self.add(machine)
