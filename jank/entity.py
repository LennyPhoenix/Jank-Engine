import math
import typing as t

import jank

from . import shapes


class Entity:
    STATIC: int = jank.physics.Body.STATIC
    DYNAMIC: int = jank.physics.Body.DYNAMIC
    KINEMATIC: int = jank.physics.Body.KINEMATIC

    _space: t.Optional[jank.physics.Space] = None
    _flip_x: bool = False
    _flip_y: bool = False

    colliders: t.List[jank.physics.Shape]
    sprite_offset = jank.Vec2d.zero()

    def __init__(
        self,
        position: t.Tuple[float, float] = (0, 0),
        rotation_degrees: float = 0,
        body_type: int = DYNAMIC,
        mass: float = 1, moment: float = float("inf"),
        colliders: t.Optional[t.List[shapes.Base]] = None,
        collider: t.Optional[shapes.Base] = None,
        space: t.Optional[jank.physics.Space] = None
    ):
        self.colliders = []
        self.body = jank.physics.Body(mass=mass, moment=moment, body_type=body_type)
        self.position = position
        self.angle = math.radians(rotation_degrees)
        self.body.position_func = self.position_func
        self.body.velocity_func = self.velocity_func

        if colliders is not None:
            for col in colliders:
                self.add_collider(col)
        elif collider is not None:
            self.add_collider(collider)

        if space is not None:
            self.space = space

    def on_update(self, dt: float):
        """ Called as frequently as possible. Update input/graphics here. """

    def on_fixed_update(self, dt: float):
        """ Called 120 times a second at a fixed rate. Update physics here. """

    def position_func(
        self,
        body: jank.physics.Body,
        dt: float
    ):
        jank.physics.Body.update_position(body, dt)
        self.update_sprite()

    def velocity_func(
        self,
        body: jank.physics.Body,
        gravity: jank.Vec2d,
        damping: float,
        dt: float
    ):
        jank.physics.Body.update_velocity(body, gravity, damping, dt)

    def get_space(self) -> jank.physics.Space:
        return self._space

    def set_space(self, space: jank.physics.Space):
        if self.space is not None:
            self.space.remove(self.body, *self.colliders)

        self._space = space
        if self.space is not None:
            self.space.add(self.body, *self.colliders)

    space = property(get_space, set_space)

    @property
    def position(self) -> jank.Vec2d:
        return self.body.position

    @position.setter
    def position(self, position: jank.Vec2d):
        self.body.position = position
        self.update_sprite()

    @property
    def velocity(self) -> jank.Vec2d:
        return self.body.velocity

    @velocity.setter
    def velocity(self, velocity: jank.Vec2d):
        self.body.velocity = velocity

    @property
    def angle(self) -> float:
        return self.body.angle

    @angle.setter
    def angle(self, angle: float):
        self.body.angle = angle
        self.update_sprite()

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
                self.scale_x = -(abs(self.scale_x))
            else:
                self.scale_x = abs(self.scale_x)
            self._flip_x = flip_x
            self.update_sprite()

    @property
    def flip_y(self) -> bool:
        return self._flip_y

    @flip_y.setter
    def flip_y(self, flip_y: bool):
        if self._flip_y != flip_y:
            if flip_y:
                self.scale_y = -(abs(self.scale_y))
            else:
                self.scale_y = abs(self.scale_y)
            self._flip_y = flip_y
            self.update_sprite()

    @property
    def scale(self) -> float:
        return self.sprite.scale

    @scale.setter
    def scale(self, scale: float):
        self.sprite.scale = scale
        self.update_sprite()

    @property
    def scale_x(self) -> float:
        return self.sprite.scale_x

    @scale_x.setter
    def scale_x(self, scale_x: float):
        self.sprite.scale_x = scale_x
        self.update_sprite()

    @property
    def scale_y(self) -> float:
        return self.sprite.scale_y

    @scale_y.setter
    def scale_y(self, scale_y: float):
        self.sprite.scale_y = scale_y
        self.update_sprite()

    @property
    def base_width(self) -> float:
        return self.sprite.width / abs(self.scale_x) / abs(self.scale)

    @property
    def base_height(self) -> float:
        return self.sprite.height / abs(self.scale_y) / abs(self.scale)

    @property
    def scaled_width(self) -> float:
        return self.base_width * self.scale_x * self.scale

    @property
    def scaled_height(self) -> float:
        return self.base_height * self.scale_y * self.scale

    def add_collider(self, shape: shapes.Base) -> jank.physics.Shape:
        col = shapes.initialise_shape(shape)
        col.body = self.body

        if self.space is not None:
            self.space.add(col)

        self.colliders.append(col)

        return col

    def update_sprite(self):
        if hasattr(self, "sprite"):
            pos = jank.Vec2d(self.sprite_offset)
            pos.x -= self.scaled_width/2
            pos.y -= self.scaled_height/2
            pos = self.position+pos.rotated(self.angle)
            self.sprite.position = tuple(pos)
            self.sprite.rotation = -self.angle_degrees

    @property
    def sprite(self) -> jank.Sprite:
        return self._sprite

    @sprite.setter
    def sprite(self, sprite: jank.Sprite):
        self._sprite = sprite
        if hasattr(self.sprite, "push_handlers"):
            self.sprite.push_handlers(self)
        self.update_sprite()

    @property
    def grounded(self) -> bool:
        return self.get_grounding_details()["body"] is not None

    def get_grounding_details(self) -> dict:
        grounding = {
            "normal": jank.Vec2d.zero(),
            "penetration": jank.Vec2d.zero(),
            "impulse": jank.Vec2d.zero(),
            "position": jank.Vec2d.zero(),
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

    @property
    def bounding_box(self) -> jank.BoundingBox:
        return jank.BoundingBox(
            min(shape.bb.left for shape in self.colliders),
            min(shape.bb.bottom for shape in self.colliders),
            max(shape.bb.right for shape in self.colliders),
            max(shape.bb.top for shape in self.colliders)
        )

    def draw(self):
        if hasattr(self, "sprite"):
            self.sprite.draw()

    def delete(self):
        self.space = None
        jank.get_app().remove_handlers(self)
        if hasattr(self, "sprite"):
            if hasattr(self.sprite, "remove_handlers"):
                self.sprite.remove_handlers(self)
            self.sprite.delete()
