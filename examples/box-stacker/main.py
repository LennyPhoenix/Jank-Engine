import typing as t

import jank

from player import Player


class Application(jank.Application):
    PHYSICS_STEPS = 5

    boxes: t.List[Player]
    floor: jank.Entity
    player: Player = None

    def __init__(self):
        config = jank.Config()
        config.antialiasing = 8
        config.caption = "Box Stacking Test"
        config.default_size = (800, 600)
        config.resizable = False
        config.vsync = False

        super().__init__(config, False, True, True)
        self.physics_space.gravity = (0, -1000)

        self.boxes = []

        self.make_floor()
        self.add_player()

    def make_floor(self):
        self.floor = jank.Entity(
            position=(
                0,
                self.camera.bounding_box.bottom
            ),
            body_type=jank.Entity.STATIC,
            collider=jank.colliders.Segment(
                a=(self.camera.bounding_box.left, 0),
                b=(self.camera.bounding_box.right, 0),
                friction=50
            ),
            space=self.physics_space
        )

    def add_player(self):
        if self.player is not None:
            self.player.controlling = False
            self.player.colliders[0].friction = 1
            self.boxes.append(self.player)
        self.player = Player()
        self.player.controlling = True

    def on_fixed_update(self, dt: float):
        for _ in range(self.PHYSICS_STEPS):
            self.physics_space.step(1/120/self.PHYSICS_STEPS)

    def on_key_press(self, button, modifiers):
        if button == jank.key.SPACE:
            self.add_player()


if __name__ == "__main__":
    application = Application()
    application.run()
