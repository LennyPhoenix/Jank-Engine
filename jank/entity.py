import math
import pickle

import pyglet
import pymunk

from .collider_dicts import dict_to_collider


class Entity(pymunk.Body):
    _space = None
    _active = True
    _flip = False

    def __init__(
        self,
        position=(0, 0), rotation=0,
        body_type=pymunk.Body.DYNAMIC,
        mass: float = 1, moment: float = float("inf"),
        colliders: list = None, collider: dict = None
    ):
        super().__init__(mass=mass, moment=moment, body_type=body_type)
        self.position = position
        self.angle = math.radians(rotation)
        self.colliders = []

        if colliders is not None:
            for col in colliders:
                self.add_collider(col)
        elif collider is not None:
            self.add_collider(collider)

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        if active:
            for collider in self.colliders:
                collider.body = self
        else:
            for collider in self.colliders:
                collider.body = None

        self._active = active

    @property
    def space(self):
        return self._space

    @space.setter
    def space(self, space):
        if self.space is not None:
            self.space.remove(self, *self.colliders)

        self._space = space
        if space is not None:
            self.space.add(self, *self.colliders)

    def add_collider(self, collider):
        col = dict_to_collider(collider)
        col.body = self

        if self.space is not None:
            self.space.add(col)

        self.colliders.append(col)

    def create_sprite(self, image, offset, batch=None, group=None):
        self.sprite_offset = pymunk.Vec2d(offset)
        pos = self.sprite_offset.rotated(self.angle)+self.position
        self.sprite = pyglet.sprite.Sprite(
            image,
            x=pos.x, y=pos.y,
            batch=batch,
            group=group
        )
        self.sprite.rotation = math.degrees(self.angle)

    @property
    def flip(self):
        return self._flip

    @flip.setter
    def flip(self, flip):
        if self._flip != flip:
            if flip:
                self.sprite.scale_x = -(abs(self.sprite.scale_x))
            else:
                self.sprite.scale_x = abs(self.sprite.scale_x)
            self._flip = flip
            self.update_sprite()

    def update_sprite(self):
        pos = self.sprite_offset
        if self.flip:
            pos.x += self.sprite.width
        pos = self.position+pos.rotated(self.angle)
        self.sprite.position = tuple(pos)
        self.sprite.rotation = math.degrees(self.angle)

    def delete(self):
        self.space = None
        self.sprite.delete()

    def __getstate__(self):
        d = super().__getstate__()

        d["special"].append(("active", self._active))

        return d

    def __setstate__(self, state):
        super().__setstate__(state)

        for k, v in state["special"]:
            if k == "active":
                self._active = v
