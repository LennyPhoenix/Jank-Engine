import jank


class Player(jank.Entity):
    SPEED = 200
    JUMP = 500

    controlling: bool = False
    controls: dict = {
        "left": False,
        "right": False
    }

    def __init__(self):
        super().__init__(
            collider=jank.colliders.Rect(
                width=50, height=50, friction=0.1, radius=25
            ),
            space=jank.get_app().physics_space
        )
        jank.get_app().push_handlers(self)

    def velocity_func(self, body, gravity, damping, dt):
        super().velocity_func(body, gravity, damping, dt)
        if self.controlling:
            vx = 0
            if self.controls["left"]:
                vx -= self.SPEED
            if self.controls["right"]:
                vx += self.SPEED
            self.velocity = (vx, self.velocity.y)

    def on_key_press(self, button, modifiers):
        if self.controlling and button == jank.key.W and self.grounded:
            self.body.apply_impulse_at_local_point(
                (0, self.JUMP)
            )

    def on_update(self, dt: float):
        if self.controlling:
            self.controls = {
                "left": jank.get_app().key_handler[jank.key.A],
                "right": jank.get_app().key_handler[jank.key.D]
            }
