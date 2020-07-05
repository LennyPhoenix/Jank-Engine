import math
import pickle
from typing import List

import pyglet
import pymunk

import jank

from . import shapes


class Entity:
    _space = None
    _flip_horizontal = False
    _flip_vertical = False

    def __init__(
        self,
        position: tuple = (0, 0), rotation: float = 0,
        body_type: int = pymunk.Body.DYNAMIC,
        mass: float = 1, moment: float = float("inf"),
        colliders: List[shapes.Base] = None,
        collider: shapes.Base = None
    ):
        jank.get_application().push_handlers(self)

        self.body = pymunk.Body(mass=mass, moment=moment, body_type=body_type)
        self.position = position
        self.angle = math.radians(rotation)
        self.colliders = []

        if colliders is not None:
            for col in colliders:
                self.add_collider(col)
        elif collider is not None:
            self.add_collider(collider)

    def on_update(self, dt):
        """ Called as frequently as possible. Update input/graphics here. """

    def on_fixed_update(self, dt):
        """ Called 120 times a second at a fixed rate. Update physics here. """

    def set_friction(self, friction: float):
        for collider in self.colliders:
            collider.friction = friction

    @property
    def space(self) -> pymunk.Space:
        return self._space

    @space.setter
    def space(self, space: pymunk.Space):
        if self.space is not None:
            self.space.remove(self.body, *self.colliders)

        self._space = space
        if space is not None:
            self.space.add(self.body, *self.colliders)

    @property
    def position(self) -> pymunk.Vec2d:
        return self.body.position

    @position.setter
    def position(self, position: tuple):
        self.body.position = position

    @property
    def angle(self) -> float:
        return self.body.angle

    @angle.setter
    def angle(self, angle: float):
        self.body.angle = angle

    @property
    def angle_degrees(self) -> float:
        return math.degrees(self.angle)

    @angle_degrees.setter
    def angle_degrees(self, angle_degrees: float):
        self.angle = math.radians(angle_degrees)

    @property
    def flip_horizontal(self) -> bool:
        return self._flip_horizontal

    @flip.setter
    def flip_horizontal(self, flip_horizontal: bool):
        if self._flip_horizontal != flip_horizontal:
            if flip_horizontal:
                self.sprite.scale_x = -(abs(self.sprite.scale_x))
            else:
                self.sprite.scale_x = abs(self.sprite.scale_x)
            self._flip_horizontal = flip_horizontal
            self.update_sprite()

    @property
    def flip_vertical(self) -> bool:
        return self._flip_vertical

    @flip.setter
    def flip_vertical(self, flip_vertical: bool):
        if self._flip_vertical != flip_vertical:
            if flip_vertical:
                self.sprite.scale_x = -(abs(self.sprite.scale_x))
            else:
                self.sprite.scale_x = abs(self.sprite.scale_x)
            self._flip_vertical = flip_vertical
            self.update_sprite()

    def add_collider(self, shape: shapes.Base) -> pymunk.Shape:
        col = shapes.initialise_shape(shape)
        col.body = self.body

        if self.space is not None:
            self.space.add(col)

        self.colliders.append(col)

        return col

    def create_sprite(
        self,
        image, offset: tuple,
        batch: pyglet.graphics.Batch = None,
        group: pyglet.graphics.Group = None,
        subpixel: bool = False,
        usage: str = "dynamic"
    ):
        self.sprite_offset = pymunk.Vec2d(offset)
        pos = self.sprite_offset.rotated(self.angle)+self.position
        self.sprite = pyglet.sprite.Sprite(
            image,
            x=pos.x, y=pos.y,
            batch=batch,
            group=group,
            subpixel=subpixel,
            usage=usage
        )
        self.sprite.rotation = self.angle_degrees

    def update_sprite(self):
        if hasattr(self, "sprite"):
            pos = self.sprite_offset
            if self.flip_horizontal:
                pos.x += self.sprite.width
            if self.flip_vertical:
                pos.y += self.sprite.height
            pos = self.position+pos.rotated(self.angle)
            self.sprite.position = tuple(pos)
            self.sprite.rotation = math.degrees(self.angle)

    @property
    def grounded(self) -> bool:
        return self.get_grounding_details()["body"] is not None

    def get_grounding_details(self) -> dict:
        grounding = {
            "normal": pymunk.Vec2d.zero(),
            "penetration": pymunk.Vec2d.zero(),
            "impulse": pymunk.Vec2d.zero(),
            "position": pymunk.Vec2d.zero(),
            "body": None
        }

        def f(arbiter):
            n = -arbiter.contact_point_set.normal
            if n.y > grounding["normal"].y:
                grounding["normal"] = n
                grounding["penetration"] = - \
                    arbiter.contact_point_set.points[0].distance
                grounding["body"] = arbiter.shapes[1].body
                grounding["impulse"] = arbiter.total_impulse
                grounding["position"] = arbiter.contact_point_set.points[0].point_b

        self.body.each_arbiter(f)

        return grounding

    def delete(self):
        self.space = None
        jank.get_application().remove_handlers(self)
        if hasattr(self, "sprite"):
            self.sprite.delete()
