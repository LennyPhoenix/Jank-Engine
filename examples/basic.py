import jank  # Import the engine


class Application(jank.Application):
    PHYSICS_STEPS = 5  # Turn this up to increase simulation accuracy.
    PLAYER_SPEED = 200
    PLAYER_JUMP = 500

    def __init__(self):
        # Initialise the application
        super().__init__(debug_mode=True, show_fps=True)
        # Set the space's gravity
        self.physics_space.gravity = (0, -1000)

        # Create controls dictionary
        self.controls = {
            "up": False,
            "left": False,
            "right": False
        }

        # Create the floor
        self.floor = jank.Entity(
            position=(0, -325),
            body_type=jank.Entity.STATIC,
            collider=jank.shapes.Rect(
                width=950,
                height=50
            )
        )
        self.floor.space = self.physics_space

        # Create the player object. Note that the Entity class can be subclassed.
        self.player = jank.Entity(
            position=(0, 0),
            collider=jank.shapes.Rect(
                width=100,
                height=100
            )
        )
        self.player.space = self.physics_space

    # Called every 1/120 of a second. (Note this can occasionally be inaccurate.)
    def on_fixed_update(self, dt: float):

        # Step the physics simulation forwards.
        for _ in range(self.PHYSICS_STEPS):
            self.physics_space.step(dt/self.PHYSICS_STEPS)

        # Jump if the W key is pressed and the player is grounded.
        if self.controls["up"] and self.player.grounded:
            self.player.body.apply_impulse_at_local_point(
                (0, self.PLAYER_JUMP)
            )

        # Set the player's X velocity.
        vx = 0
        if self.controls["left"]:
            vx -= self.PLAYER_SPEED
        if self.controls["right"]:
            vx += self.PLAYER_SPEED
        self.player.velocity = (vx, self.player.velocity.y)

    # Called as frequently as possible.
    def on_update(self, dt: float):
        # Update controls dict
        self.controls = {
            "up": self.key_handler[jank.key.W],
            "left": self.key_handler[jank.key.A],
            "right": self.key_handler[jank.key.D]
        }


# Instantiate and run the application.
if __name__ == "__main__":
    application = Application()
    application.run()
