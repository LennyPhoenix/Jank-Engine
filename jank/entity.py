import math
import pickle

import pyglet
import pymunk

from .collider_dicts import dict_to_collider


class Entity:
    _space = None
    _flip = False

    def __init__(
        self,
        position: tuple = (0, 0), rotation: float = 0,
        body_type: int = pymunk.Body.DYNAMIC,
        mass: float = 1, moment: float = float("inf"),
        colliders: list = None, collider: dict = None
    ):
        self.body = pymunk.Body(mass=mass, moment=moment, body_type=body_type)
        self.position = position
        self.angle = math.radians(rotation)
        self.colliders = []

        if colliders is not None:
            for col in colliders:
                self.add_collider(col)
        elif collider is not None:
            self.add_collider(collider)

    @property
    def space(self):
        return self._space

    @space.setter
    def space(self, space: pymunk.Space):
        if self.space is not None:
            self.space.remove(self.body, *self.colliders)

        self._space = space
        if space is not None:
            self.space.add(self.body, *self.colliders)

    @property
    def position(self):
        return self.body.position

    @position.setter
    def position(self, position: tuple):
        self.body.position = position

    @property
    def angle(self):
        return self.body.angle

    @angle.setter
    def angle(self, angle: float):
        self.body.angle = angle

    @property
    def angle_degrees(self):
        return math.degrees(self.angle)

    @angle_degrees.setter
    def angle_degrees(self, angle_degrees: float):
        self.angle = math.radians(angle_degrees)

    @property
    def flip(self):
        return self._flip

    @flip.setter
    def flip(self, flip: bool):
        if self._flip != flip:
            if flip:
                self.sprite.scale_x = -(abs(self.sprite.scale_x))
            else:
                self.sprite.scale_x = abs(self.sprite.scale_x)
            self._flip = flip
            self.update_sprite()

    def add_collider(self, collider: dict):
        col = dict_to_collider(collider)
        col.body = self.body

        if self.space is not None:
            self.space.add(col)

        self.colliders.append(col)

    def create_sprite(
        self,
        image, offset: tuple,
        batch: pyglet.graphics.Batch = None,
        group: pyglet.graphics.Group = None
    ):
        self.sprite_offset = pymunk.Vec2d(offset)
        pos = self.sprite_offset.rotated(self.angle)+self.position
        self.sprite = pyglet.sprite.Sprite(
            image,
            x=pos.x, y=pos.y,
            batch=batch,
            group=group
        )
        self.sprite.rotation = self.angle_degrees

    def update_sprite(self):
        pos = self.sprite_offset
        if self.flip:
            pos.x += self.sprite.width
        pos = self.position+pos.rotated(self.angle)
        self.sprite.position = tuple(pos)
        self.sprite.rotation = math.degrees(self.angle)

    @property
    def grounded(self):
        return self.get_grounding_details()["body"] is not None

    def get_grounding_details(self):
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
        self.sprite.delete()
