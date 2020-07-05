import random

import pyglet
import pymunk

import jank
from jank import key

PLAYER_SPEED = 100


class Player(jank.Entity):
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
        self.space = jank.get_application().physics_space

        self.velocity = pymunk.Vec2d.zero()

        def velocity_func(body: pymunk.Body, gravity, damping, dt):
            body.velocity = self.velocity

        self.body.velocity_func = velocity_func

        def position_func(body: pymunk.Body, dt):
            pymunk.Body.update_position(body, dt)

        self.body.position_func = position_func

    def create_sprite(self):
        image = pyglet.image.load("resources/player.png")
        super().create_sprite(
            image,
            offset=(-8, -8),
            batch=jank.get_application().world_batch,
            group=jank.get_application().world_layers["player"],
            subpixel=True
        )
        self.label = pyglet.text.Label(
            text=self.player_id,
            font_size=8,
            anchor_x="center",
            batch=jank.get_application().world_batch,
            group=jank.get_application().world_layers["name_tags"]
        )

    def on_update(self, dt):
        if self.controlling:
            key_handler = jank.get_application().key_handler

            self.controls = {
                "up": key_handler[key.W],
                "down": key_handler[key.S],
                "left": key_handler[key.A],
                "right": key_handler[key.D]
            }

        self.velocity = pymunk.Vec2d.zero()

        if self.controls["up"]:
            self.velocity.y += PLAYER_SPEED
        if self.controls["down"]:
            self.velocity.y -= PLAYER_SPEED
        if self.controls["left"]:
            self.velocity.x -= PLAYER_SPEED
        if self.controls["right"]:
            self.velocity.x += PLAYER_SPEED

        if self.velocity.length > PLAYER_SPEED:
            scale = PLAYER_SPEED / self.velocity.length
            self.velocity = self.velocity * scale

    def on_fixed_update(self, dt):
        self.update_sprite()
        if self.label is not None:
            self.label.x = self.position.x
            self.label.y = self.position.y + 10
