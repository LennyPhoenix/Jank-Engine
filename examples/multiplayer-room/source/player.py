import jank
from jank import key

PLAYER_SPEED = 100


class Player(jank.Entity):
    v = jank.Vec2d.zero()

    def __init__(self, player_id: str):
        self.controlling = False
        self.controls = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }

        self.player_id = player_id
        self.label = None

        super().__init__(
            collider=jank.shapes.Rect(
                width=16,
                height=16
            )
        )
        self.space = jank.get_app().physics_space

        jank.get_app().push_handlers(self)

    def velocity_func(self, body, gravity, damping, dt):
        body.velocity = self.v

    def create_sprite(self):
        image = jank.resource.image("resources/player.png")
        self.sprite = jank.Sprite(
            image,
            0, 0,
            batch=jank.get_app().world_batch,
            subpixel=True
        )
        self.label = jank.pyglet.text.Label(
            text=self.player_id,
            font_size=8,
            anchor_x="center",
            batch=jank.get_app().world_batch,
            group=jank.get_app().world_layers["name_tags"]
        )

    def on_update(self, dt):
        if self.controlling:
            key_handler = jank.get_app().key_handler

            self.controls = {
                "up": key_handler[key.W],
                "down": key_handler[key.S],
                "left": key_handler[key.A],
                "right": key_handler[key.D]
            }

        self.v = jank.Vec2d.zero()

        if self.controls["up"]:
            self.v.y += PLAYER_SPEED
        if self.controls["down"]:
            self.v.y -= PLAYER_SPEED
        if self.controls["left"]:
            self.v.x -= PLAYER_SPEED
        if self.controls["right"]:
            self.v.x += PLAYER_SPEED

        if self.v.length > PLAYER_SPEED:
            scale = PLAYER_SPEED / self.v.length
            self.v = self.v * scale

    def update_sprite(self):
        super().update_sprite()
        if self.label is not None:
            self.label.x = self.position.x
            self.label.y = self.position.y + 10

    def delete(self):
        super().delete()
        if self.label is not None:
            self.label.delete()
