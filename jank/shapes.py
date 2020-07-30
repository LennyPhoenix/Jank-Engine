import pymunk

from dataclasses import dataclass, field
import typing as t


@dataclass
class Base:
    radius: float = 0.0
    collision_type: int = 0
    elasticity: float = 0.0
    friction: float = 0.0
    filter: pymunk.ShapeFilter = None
    sensor: bool = False


@dataclass
class Rect(Base):
    width: float = 10.0
    height: float = 10.0
    offset: t.Tuple[float, float] = (0.0, 0.0)


@dataclass
class Poly(Base):
    vertices: t.List[t.Tuple[float, float]] = field(default_factory=list)


@dataclass
class Circle(Base):
    offset: t.Tuple[float, float] = (0.0, 0.0)


@dataclass
class Segment(Base):
    a: t.Tuple[float, float] = (-5, 0)
    b: t.Tuple[float, float] = (5, 0)


def init_rect(data: Rect) -> pymunk.Poly:
    transform = pymunk.Transform(
        tx=-data.width/2,
        ty=-data.height/2
    )
    collider = pymunk.Poly(
        None,
        vertices=[
            (
                data.offset[0],
                data.offset[1]
            ),
            (
                data.offset[0]+data.width,
                data.offset[1]
            ),
            (
                data.offset[0]+data.width,
                data.offset[1]+data.height
            ),
            (
                data.offset[0],
                data.offset[1]+data.height
            )
        ],
        transform=transform,
        radius=data.radius
    )
    return collider


def init_poly(data) -> pymunk.Poly:
    collider = pymunk.Poly(
        None,
        vertices=data.vertices,
        radius=data.radius
    )
    return collider


def init_circle(data) -> pymunk.Circle:
    collider = pymunk.Circle(
        None,
        radius=data.radius,
        offset=data.offset
    )
    return collider


def init_segment(data) -> pymunk.Segment:
    collider = pymunk.Segment(
        None,
        a=data.a,
        b=data.b,
        radius=data.radius
    )
    return collider


def initialise_shape(shape) -> pymunk.Shape:
    shapes = {
        Rect: init_rect,
        Poly: init_poly,
        Circle: init_circle,
        Segment: init_segment
    }

    collider: pymunk.Shape = shapes[type(shape)](shape)

    collider.collision_type = shape.collision_type
    collider.friction = shape.friction
    collider.elasticity = shape.elasticity
    collider.sensor = shape.sensor
    if shape.filter is not None:
        collider.filter = shape.filter

    return collider
