import math

import jank


class Ragdoll:
    def __init__(self, position):
        position = jank.Vec2d(position)

        self.group = jank.physics.ShapeFilter(group=0b1)

        # Torso
        self.torso = jank.Entity(
            mass=1,
            moment=jank.physics.moment_for_box(1, (40, 100)),
            position=position,
            collider=jank.shapes.Rect(
                width=40,
                height=100,
                friction=0.6,
                filter=self.group
            )
        )

        # Head
        self.head = jank.Entity(
            mass=0.6,
            moment=jank.physics.moment_for_circle(0.6, 0, 25),
            position=position,
            collider=jank.shapes.Circle(
                radius=25,
                friction=0.6,
                filter=self.group
            )
        )
        self.head_join = jank.physics.PivotJoint(
            self.head.body,
            self.torso.body,
            (0, -25),
            (0, 50)
        )
        self.head_rotary = jank.physics.RotaryLimitJoint(
            self.head.body,
            self.torso.body,
            math.radians(-30),
            math.radians(30)
        )

        # Right Arm
        self.r_arm = jank.Entity(
            mass=0.4,
            moment=jank.physics.moment_for_box(0.4, (25, 90)),
            position=position,
            collider=jank.shapes.Rect(
                width=25,
                height=90,
                friction=0.3,
                filter=self.group
            )
        )
        self.r_arm_join = jank.physics.PivotJoint(
            self.r_arm.body,
            self.torso.body,
            (0, 42),
            (15, 42)
        )
        self.r_arm_rotary = jank.physics.RotaryLimitJoint(
            self.r_arm.body,
            self.torso.body,
            math.radians(-150),
            math.radians(-20)
        )

        # Left Arm
        self.l_arm = jank.Entity(
            mass=0.4,
            moment=jank.physics.moment_for_box(0.4, (25, 90)),
            position=position,
            collider=jank.shapes.Rect(
                width=25,
                height=90,
                friction=0.3,
                filter=self.group
            )
        )
        self.l_arm_join = jank.physics.PivotJoint(
            self.l_arm.body,
            self.torso.body,
            (0, 42),
            (-15, 42)
        )
        self.l_arm_rotary = jank.physics.RotaryLimitJoint(
            self.l_arm.body,
            self.torso.body,
            math.radians(20),
            math.radians(150)
        )

        # Right Leg
        self.r_leg = jank.Entity(
            mass=0.4,
            moment=jank.physics.moment_for_box(0.4, (20, 100)),
            position=position,
            collider=jank.shapes.Rect(
                width=20,
                height=100,
                friction=0.3,
                filter=self.group
            )
        )
        self.r_leg_join = jank.physics.PivotJoint(
            self.r_leg.body,
            self.torso.body,
            (0, 50),
            (10, -40)
        )
        self.r_leg_rotary = jank.physics.RotaryLimitJoint(
            self.r_leg.body,
            self.torso.body,
            math.radians(-135),
            math.radians(25)
        )

        # Left Leg
        self.l_leg = jank.Entity(
            mass=0.4,
            moment=jank.physics.moment_for_box(0.4, (20, 100)),
            position=position,
            collider=jank.shapes.Rect(
                width=20,
                height=100,
                friction=0.3,
                filter=self.group
            )
        )
        self.l_leg_join = jank.physics.PivotJoint(
            self.l_leg.body,
            self.torso.body,
            (0, 50),
            (-10, -40)
        )
        self.l_leg_rotary = jank.physics.RotaryLimitJoint(
            self.l_leg.body,
            self.torso.body,
            math.radians(-25),
            math.radians(135)
        )

    @property
    def space(self) -> jank.physics.Space:
        return self.torso.space

    @space.setter
    def space(self, space: jank.physics.Space):
        self.torso.space = space
        self.head.space = space
        space.add(self.head_join, self.head_rotary)
        self.r_arm.space = space
        space.add(self.r_arm_join, self.r_arm_rotary)
        self.l_arm.space = space
        space.add(self.l_arm_join, self.l_arm_rotary)
        self.r_leg.space = space
        space.add(self.r_leg_join, self.r_leg_rotary)
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

        self.ragdoll = Ragdoll(position=(0, 0))
        self.ragdoll.space = self.physics_space

        self.floor = jank.Entity(
            position=(0, -350),
            rotation_degrees=10,
            body_type=jank.Entity.STATIC,
            collider=jank.shapes.Rect(width=700, height=25, friction=0.8)
        )
        self.floor.space = self.physics_space

    def on_fixed_update(self, dt: float):
        if not self.paused:
            steps = 10
            for _ in range(steps):
                self.physics_space.step(1/120 / steps)

    def on_mouse_drag(self, x, y, *args):
        pos = jank.Vec2d(self.screen_to_world((x, y)))
        pos -= self.ragdoll.torso.position
        self.ragdoll.torso.body.velocity = pos

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
