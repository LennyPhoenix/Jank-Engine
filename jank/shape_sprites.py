import typing as t

import jank


class _ShapeProxy:
    def __init__(self):
        self._shape = jank.pyglet.shapes._ShapeBase()

    @property
    def x(self) -> float:
        return self._shape.x

    @x.setter
    def x(self, x: float):
        self._shape.x = x

    @property
    def y(self) -> float:
        return self._shape.y

    @y.setter
    def y(self, y: float):
        self._shape.y = y

    @property
    def position(self) -> t.Tuple[float, float]:
        return self._shape.position

    @position.setter
    def position(self, position: t.Tuple[float, float]):
        self._shape.position = position

    @property
    def rotation(self) -> float:
        return self._shape.rotation

    @rotation.setter
    def rotation(self, rotation: float):
        self._shape.rotation = rotation

    @property
    def draw(self) -> t.Callable[..., t.Any]:
        return self._shape.draw

    @property
    def delete(self) -> t.Callable[..., t.Any]:
        return self._shape.delete

    @property
    def batch(self) -> jank.pyglet.graphics.Batch:
        return self._shape._batch

    @batch.setter
    def batch(self, batch: jank.pyglet.graphics.Batch):
        self._shape._batch = batch

    @property
    def group(self) -> jank.pyglet.graphics.Group:
        return self._shape._group

    @group.setter
    def group(self, group: jank.pyglet.graphics.Group):
        self._shape._group = group

    @property
    def color(self) -> t.Tuple[int, int, int]:
        return self._shape.color

    @color.setter
    def color(self, color: t.Tuple[int, int, int]):
        self._shape.color = color

    @property
    def visible(self) -> bool:
        return self._shape.visible

    @visible.setter
    def visible(self, visible: bool):
        self._shape.visible = visible


class Circle(_ShapeProxy):
    _rotation = 0
    _scale = 1
    _scale_x = 1
    _scale_y = 1

    def __init__(
        self,
        x: float, y: float,
        radius: float,
        segments: int = None,
        color: t.Tuple[int, int, int] = (255, 255, 255),
        batch: jank.pyglet.graphics.Batch = None,
        group: jank.pyglet.graphics.Group = None
    ):
        self._shape = jank.pyglet.shapes.Circle(
            x, y,
            radius,
            segments,
            color,
            batch,
            group
        )
        self._set_anchor()

    def _set_anchor(self):
        self._shape.anchor_position = (
            -self._shape.radius,
            -self._shape.radius
        )

    @property
    def _scale_factor(self) -> float:
        return (self.scale*self.scale_x*self.scale_y)

    @property
    def radius(self) -> float:
        return self._shape.radius/self._scale_factor

    @radius.setter
    def radius(self, radius: float):
        self._shape.radius = radius*self._scale_factor
        self._set_anchor()

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: float):
        self._rotation = rotation

    @property
    def width(self) -> float:
        return self._shape.radius*2

    @property
    def height(self) -> float:
        return self.width

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, scale: float):
        self._shape.radius /= self._scale_factor
        self._scale = scale
        self._shape.radius *= self._scale_factor
        self._set_anchor()

    @property
    def scale_x(self) -> float:
        return self._scale_x

    @scale_x.setter
    def scale_x(self, scale_x: float):
        self._shape.radius /= self._scale_factor
        self._scale_x = scale_x
        self._shape.radius *= self._scale_factor
        self._set_anchor()

    @property
    def scale_y(self) -> float:
        return self._scale_y

    @scale_y.setter
    def scale_y(self, scale_y: float):
        self._shape.radius /= self._scale_factor
        self._scale_y = scale_y
        self._shape.radius *= self._scale_factor
        self._set_anchor()


class Rectangle(_ShapeProxy):
    _scale = 1
    _scale_x = 1
    _scale_y = 1

    def __init__(
        self,
        x: float, y: float,
        width: float, height: float,
        color: t.Tuple[int, int, int] = (255, 255, 255),
        batch: jank.pyglet.graphics.Batch = None,
        group: jank.pyglet.graphics.Group = None
    ):
        self._shape = jank.pyglet.shapes.Rectangle(
            x, y,
            width, height,
            color,
            batch, group
        )

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, scale: float):
        self._shape.width /= self.scale*self.scale_x
        self._shape.height /= self.scale*self.scale_y
        self._scale = scale
        self._shape.width *= self.scale*self.scale_x
        self._shape.height *= self.scale*self.scale_y

    @property
    def scale_x(self) -> float:
        return self._scale_x

    @scale_x.setter
    def scale_x(self, scale_x: float):
        self._shape.width /= self.scale*self.scale_x
        self._shape.height /= self.scale*self.scale_y
        self._scale_x = scale_x
        self._shape.width *= self.scale*self.scale_x
        self._shape.height *= self.scale*self.scale_y

    @property
    def scale_y(self) -> float:
        return self._scale_y

    @scale_y.setter
    def scale_y(self, scale_y: float):
        self._shape.width /= self.scale*self.scale_x
        self._shape.height /= self.scale*self.scale_y
        self._scale_y = scale_y
        self._shape.width *= self.scale*self.scale_x
        self._shape.height *= self.scale*self.scale_y

    @property
    def width(self) -> float:
        return self._shape.width*self.scale*self.scale_x

    @width.setter
    def width(self, width: float):
        self._shape.width = width

    @property
    def height(self) -> float:
        return self._shape.height*self.scale*self.scale_y

    @height.setter
    def height(self, height: float):
        self._shape.height = height
