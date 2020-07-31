import math

import jank


class Ragdoll:
    TORSO_SIZE = (40, 100)
    TORSO_MASS = 20
    TORSO_FRICTION = 0.6

    HEAD_SIZE = 25
    HEAD_MASS = 6
    HEAD_FRICTION = 0.6
    HEAD_ANCHOR = (
        (0, -HEAD_SIZE),
        (0, TORSO_SIZE[1]/2)
    )
    HEAD_LIMIT = (-30, 30)

    R_ARM_SIZE = (25, 90)
    R_ARM_MASS = 8
    R_ARM_FRICTION = 0.3
    R_ARM_ANCHOR = (
        (0, R_ARM_SIZE[1]*0.45),
        (TORSO_SIZE[0]*0.4, TORSO_SIZE[1]*0.4)
    )
    R_ARM_LIMIT = (-150, -20)

    L_ARM_SIZE = (25, 90)
    L_ARM_MASS = 8
    L_ARM_FRICTION = 0.3
    L_ARM_ANCHOR = (
        (0, L_ARM_SIZE[1]*0.45),
        (-TORSO_SIZE[0]*0.4, TORSO_SIZE[1]*0.4)
    )
    L_ARM_LIMIT = (20, 150)

    R_LEG_SIZE = (20, 100)
    R_LEG_MASS = 15
    R_LEG_FRICTION = 0.3
    R_LEG_ANCHOR = (
        (0, R_LEG_SIZE[1]/2),
        (TORSO_SIZE[0]/2 - R_LEG_SIZE[0]/2, -TORSO_SIZE[1]*0.4)
    )
    R_LEG_LIMIT = (-135, 25)

    L_LEG_SIZE = (20, 100)
    L_LEG_MASS = 15
    L_LEG_FRICTION = 0.3
    L_LEG_ANCHOR = (
        (0, L_LEG_SIZE[1]/2),
        (-TORSO_SIZE[0]/2 + L_LEG_SIZE[0]/2, -TORSO_SIZE[1]*0.4)
    )
    L_LEG_LIMIT = (-25, 135)

    def __init__(self, position, head=True, r_arm=True, l_arm=True, r_leg=True, l_leg=True):
        position = jank.Vec2d(position)

        self.group = jank.physics.ShapeFilter(group=0b1)

        self.torso = jank.Entity(
            mass=self.TORSO_MASS,
            moment=jank.physics.moment_for_box(
                self.TORSO_MASS,
                self.TORSO_SIZE
            ),
            position=position,
            collider=jank.shapes.Rect(
                width=self.TORSO_SIZE[0],
                height=self.TORSO_SIZE[1],
                friction=self.TORSO_FRICTION,
                filter=self.group
            )
        )

        if head:
            self.head = jank.Entity(
                mass=self.HEAD_MASS,
                moment=jank.physics.moment_for_circle(
                    self.HEAD_MASS,
                    0, self.HEAD_SIZE
                ),
                position=position,
                collider=jank.shapes.Circle(
                    radius=self.HEAD_SIZE,
                    friction=self.HEAD_FRICTION,
                    filter=self.group
                )
            )
            self.head_join = jank.physics.PivotJoint(
                self.head.body,
                self.torso.body,
                self.HEAD_ANCHOR[0],
                self.HEAD_ANCHOR[1]
            )
            self.head_rotary = jank.physics.RotaryLimitJoint(
                self.head.body,
                self.torso.body,
                math.radians(self.HEAD_LIMIT[0]),
                math.radians(self.HEAD_LIMIT[1])
            )

        if r_arm:
            self.r_arm = jank.Entity(
                mass=self.R_ARM_MASS,
                moment=jank.physics.moment_for_box(
                    self.R_ARM_MASS,
                    self.R_ARM_SIZE
                ),
                position=position,
                collider=jank.shapes.Rect(
                    width=self.R_ARM_SIZE[0],
                    height=self.R_ARM_SIZE[1],
                    friction=self.R_ARM_FRICTION,
                    filter=self.group
                )
            )
            self.r_arm_join = jank.physics.PivotJoint(
                self.r_arm.body,
                self.torso.body,
                self.R_ARM_ANCHOR[0],
                self.R_ARM_ANCHOR[1]
            )
            self.r_arm_rotary = jank.physics.RotaryLimitJoint(
                self.r_arm.body,
                self.torso.body,
                math.radians(self.R_ARM_LIMIT[0]),
                math.radians(self.R_ARM_LIMIT[1])
            )

        if l_arm:
            self.l_arm = jank.Entity(
                mass=self.L_ARM_MASS,
                moment=jank.physics.moment_for_box(
                    self.L_ARM_MASS,
                    self.L_ARM_SIZE
                ),
                position=position,
                collider=jank.shapes.Rect(
                    width=self.L_ARM_SIZE[0],
                    height=self.L_ARM_SIZE[1],
                    friction=self.L_ARM_FRICTION,
                    filter=self.group
                )
            )
            self.l_arm_join = jank.physics.PivotJoint(
                self.l_arm.body,
                self.torso.body,
                self.L_ARM_ANCHOR[0],
                self.L_ARM_ANCHOR[1]
            )
            self.l_arm_rotary = jank.physics.RotaryLimitJoint(
                self.l_arm.body,
                self.torso.body,
                math.radians(self.L_ARM_LIMIT[0]),
                math.radians(self.L_ARM_LIMIT[1])
            )

        if r_leg:
            self.r_leg = jank.Entity(
                mass=self.R_LEG_MASS,
                moment=jank.physics.moment_for_box(
                    self.R_LEG_MASS,
                    self.R_LEG_SIZE
                ),
                position=position,
                collider=jank.shapes.Rect(
                    width=self.R_LEG_SIZE[0],
                    height=self.R_LEG_SIZE[1],
                    friction=self.R_LEG_FRICTION,
                    filter=self.group
                )
            )
            self.r_leg_join = jank.physics.PivotJoint(
                self.r_leg.body,
                self.torso.body,
                self.R_LEG_ANCHOR[0],
                self.R_LEG_ANCHOR[1]
            )
            self.r_leg_rotary = jank.physics.RotaryLimitJoint(
                self.r_leg.body,
                self.torso.body,
                math.radians(self.R_LEG_LIMIT[0]),
                math.radians(self.R_LEG_LIMIT[1])
            )

        if l_leg:
            self.l_leg = jank.Entity(
                mass=self.L_LEG_MASS,
                moment=jank.physics.moment_for_box(
                    self.L_LEG_MASS,
                    self.L_LEG_SIZE
                ),
                position=position,
                collider=jank.shapes.Rect(
                    width=self.L_LEG_SIZE[0],
                    height=self.L_LEG_SIZE[1],
                    friction=self.L_LEG_FRICTION,
                    filter=self.group
                )
            )
            self.l_leg_join = jank.physics.PivotJoint(
                self.l_leg.body,
                self.torso.body,
                self.L_LEG_ANCHOR[0],
                self.L_LEG_ANCHOR[1]
            )
            self.l_leg_rotary = jank.physics.RotaryLimitJoint(
                self.l_leg.body,
                self.torso.body,
                math.radians(self.L_LEG_LIMIT[0]),
                math.radians(self.L_LEG_LIMIT[1])
            )

    @property
    def space(self) -> jank.physics.Space:
        return self.torso.space

    @space.setter
    def space(self, space: jank.physics.Space):
        self.torso.space = space
        if hasattr(self, "head"):
            self.head.space = space
            space.add(self.head_join, self.head_rotary)
        if hasattr(self, "r_arm"):
            self.r_arm.space = space
            space.add(self.r_arm_join, self.r_arm_rotary)
        if hasattr(self, "l_arm"):
            self.l_arm.space = space
            space.add(self.l_arm_join, self.l_arm_rotary)
        if hasattr(self, "r_leg"):
            self.r_leg.space = space
            space.add(self.r_leg_join, self.r_leg_rotary)
        if hasattr(self, "l_leg"):
            self.l_leg.space = space
            space.add(self.l_leg_join, self.l_leg_rotary)


class Application(jank.Application):
    _paused = True

    def __init__(self):
        config = jank.Config()
        config.caption = "Ragdoll example."
        config.default_size = (800, 800)
        config.resizable = False
        config.vsync = False

        super().__init__(config, debug_mode=True, show_fps=True)
        self.physics_space.gravity = (0, -300)

        self._paused_label = jank.pyglet.text.Label(
            "Paused, Press Space",
            font_size=24,
            x=400, y=760,
            anchor_x="center",
            batch=self.ui_batch
        )

        self.ragdoll = Ragdoll(
            position=(0, 0),
            head=True,
            r_arm=True, l_arm=True,
            r_leg=True, l_leg=True)
        self.ragdoll.space = self.physics_space

        self.floor = jank.Entity(
            position=(0, -350),
            body_type=jank.Entity.STATIC,
            collider=jank.shapes.Rect(width=700, height=25, friction=0.8)
        )
        self.floor.space = self.physics_space

    def on_fixed_update(self, dt: float):
        if not self.paused:
            steps = 1
            for _ in range(steps):
                self.physics_space.step(1/120 / steps)

    def on_mouse_motion(self, x, y, *args):
        if not self.paused:
            pos = jank.Vec2d(self.screen_to_world((x, y)))
            pos -= self.ragdoll.torso.position
            # self.ragdoll.r_arm.angle = pos.angle

    def on_mouse_drag(self, x, y, *args):
        if not self.paused:
            pos = jank.Vec2d(self.screen_to_world((x, y)))
            pos -= self.ragdoll.torso.position
            self.ragdoll.torso.body.velocity = pos
            # self.ragdoll.r_arm.angle = pos.angle

    def on_key_press(self, button, modifiers):
        if button == jank.key.SPACE:
            self.paused = not self.paused

    @property
    def paused(self) -> bool:
        return self._paused

    @paused.setter
    def paused(self, paused: bool):
        self._paused = paused
        if paused:
            self._paused_label.text = "Paused, Press Space"
        else:
            self._paused_label.text = ""


if __name__ == "__main__":
    application = Application()
    application.run()
