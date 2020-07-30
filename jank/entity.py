import math
import pickle
import typing as t

import pyglet
import pymunk

import jank

from . import shapes


class Entity:
    STATIC: int = pymunk.Body.STATIC
    DYNAMIC: int = pymunk.Body.DYNAMIC
    KINEMATIC: int = pymunk.Body.KINEMATIC

    _space: pymunk.Space = None
    _flip_x: bool = False
    _flip_y: bool = False

    def __init__(
        self,
        position: t.Tuple[float, float] = (0, 0),
        rotation_degrees: float = 0,
        body_type: int = DYNAMIC,
        mass: float = 1, moment: float = float("inf"),
        colliders: t.List[shapes.Base] = None,
        collider: shapes.Base = None
    ):
        jank.get_application().push_handlers(self)

        self.body = pymunk.Body(mass=mass, moment=moment, body_type=body_type)
        self.position = position
        self.angle = math.radians(rotation_degrees)
        self.colliders: t.List[pymunk.Shape] = []

        if colliders is not None:
            for col in colliders:
                self.add_collider(col)
        elif collider is not None:
            self.add_collider(collider)

    def on_update(self, dt: float):
        """ Called as frequently as possible. Update input/graphics here. """
        self.update_sprite()

    def on_fixed_update(self, dt: float):
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
    def position(self, position: pymunk.Vec2d):
        self.body.position = position

    @property
    def velocity(self) -> pymunk.Vec2d:
        return self.body.velocity

    @velocity.setter
    def velocity(self, velocity: pymunk.Vec2d):
        self.body.velocity = velocity

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
    def flip_x(self) -> bool:
        return self._flip_x

    @flip_x.setter
    def flip_x(self, flip_x: bool):
        if self._flip_x != flip_x:
            if flip_x:
                self.sprite.scale_x = -(abs(self.sprite.scale_x))
            else:
                self.sprite.scale_x = abs(self.sprite.scale_x)
            self._flip_x = flip_x
            self.update_sprite()

    @property
    def flip_y(self) -> bool:
        return self._flip_y

    @flip_y.setter
    def flip_y(self, flip_y: bool):
        if self._flip_y != flip_y:
            if flip_y:
                self.sprite.scale_y = -(abs(self.sprite.scale_y))
            else:
                self.sprite.scale_y = abs(self.sprite.scale_y)
            self._flip_y = flip_y
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
        image,
        offset: t.Tuple[float, float] = (0, 0),
        batch: pyglet.graphics.Batch = None,
        group: pyglet.graphics.Group = None,
        subpixel: bool = False,
        usage: str = "dynamic"
    ):
        self.sprite_offset = pymunk.Vec2d(
            offset[0]-image.width//2,
            offset[1]-image.height//2
        )
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
            if self.flip_x:
                pos.x += self.sprite.width
            if self.flip_y:
                pos.y += self.sprite.height
            pos = self.position+pos.rotated(self.angle)
            self.sprite.position = tuple(pos)
            self.sprite.rotation = -self.angle_degrees

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
