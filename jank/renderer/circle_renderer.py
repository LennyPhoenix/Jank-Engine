import typing as t

import jank

from .renderer import Renderer


class CircleRenderer(Renderer):
    CAN_ROTATE: bool = False

    def __init__(
        self,
        radius: float,
        segments: t.Optional[int] = None,
        colour: t.Tuple[int, int, int] = (255, 255, 255),
        batch: t.Optional[jank.graphics.Batch] = None,
        group: t.Optional[jank.graphics.Group] = None
    ):
        self.circle = jank.shape_sprites.Circle(
            0, 0,
            radius,
            segments=segments,
            color=colour,
            batch=batch,
            group=group
        )

    @staticmethod
    def create_from_circle(circle: jank.shape_sprites.Circle):
        circle_renderer = CircleRenderer.__new__(CircleRenderer)
        circle_renderer.circle = circle
        return circle_renderer

    def set_position(self, position: jank.Vec2d):
        position = jank.Vec2d(self.radius, self.radius) + position
        self.circle.position = position

    def set_rotation(self, rotation_degrees: float):
        self.circle.rotation = rotation_degrees

    def get_batch(self) -> t.Optional[jank.graphics.Batch]:
        return self.circle.batch

    def set_batch(self, batch: t.Optional[jank.graphics.Batch]):
        self.circle.batch = batch

    def get_group(self) -> t.Optional[jank.graphics.Group]:
        return self.circle.group

    def set_group(self, group: t.Optional[jank.graphics.Group]):
        self.circle.group = group

    def get_width(self) -> float:
        return self.circle.radius*2

    def get_height(self) -> float:
        return self.circle.radius*2

    def draw(self):
        self.circle.draw()

    def delete(self):
        self.circle.delete()

    @property
    def radius(self) -> float:
        return self.circle.radius

    @radius.setter
    def radius(self, radius: float):
        self.circle.radius = radius

    @property
    def colour(self) -> t.Tuple[int, int, int]:
        return self.circle.color

    @colour.setter
    def colour(self, colour: t.Tuple[int, int, int]):
        self.circle.color = colour

    @property
    def opacity(self) -> int:
        return self.circle.opacity

    @opacity.setter
    def opacity(self, opacity: int):
        self.circle.opacity = opacity
