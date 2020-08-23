import math
import typing as t

import jank

from . import shapes


class Entity:
    STATIC: int = jank.physics.Body.STATIC
    DYNAMIC: int = jank.physics.Body.DYNAMIC
    KINEMATIC: int = jank.physics.Body.KINEMATIC

    _space: t.Optional[jank.physics.Space] = None
    _renderer: t.Optional[jank.renderer.Renderer] = None

    colliders: t.List[jank.physics.Shape]
    body: jank.physics.Body

    def __init__(
        self,
        position: t.Union[jank.Vec2d, t.Tuple[float, float]] = jank.Vec2d(0, 0),
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
        self.body.position_func = self._position_func
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

    def _position_func(
        self,
        body: jank.physics.Body,
        dt: float
    ):
        self.position_func(body, dt)
        self.update_renderer()

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

    @property
    def space(self) -> jank.physics.Space:
        return self.get_space()

    @space.setter
    def space(self, space: jank.physics.Space):
        self.set_space(space)

    @property
    def position(self) -> jank.Vec2d:
        return self.body.position

    @position.setter
    def position(self, position: t.Union[jank.Vec2d, t.Tuple[float, float]]):
        self.body.position = position
        self.update_renderer()

    @property
    def velocity(self) -> jank.Vec2d:
        return self.body.velocity

    @velocity.setter
    def velocity(self, velocity: t.Union[jank.Vec2d, t.Tuple[float, float]]):
        self.body.velocity = velocity

    @property
    def angle(self) -> float:
        return self.body.angle

    @angle.setter
    def angle(self, angle: float):
        self.body.angle = angle
        self.update_renderer()

    @property
    def angle_degrees(self) -> float:
        return math.degrees(self.angle)

    @angle_degrees.setter
    def angle_degrees(self, angle_degrees: float):
        self.angle = math.radians(angle_degrees)

    def add_collider(self, shape: shapes.Base) -> jank.physics.Shape:
        col = shapes.initialise_shape(shape)
        col.body = self.body

        if self.space is not None:
            self.space.add(col)

        self.colliders.append(col)

        return col

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

    def update_renderer(self):
        if self.renderer is not None:
            self.renderer.update(
                position=self.position,
                rotation=self.angle_degrees,
                rotation_is_radians=False
            )

    @property
    def renderer(self) -> jank.renderer.Renderer:
        return self._renderer

    @renderer.setter
    def renderer(self, renderer: jank.renderer.Renderer):
        if self.renderer is not None:
            self.renderer.remove_handlers(self)
        self._renderer = renderer
        if self.renderer is not None:
            self.renderer.push_handlers(self)
        self.update_renderer()

    def draw(self):
        if self.renderer is not None:
            self.renderer.draw()

    def delete(self):
        self.space = None
        jank.get_app().remove_handlers(self)
        if self.renderer is not None:
            self.renderer.remove_handlers(self)
            self.renderer.delete()
