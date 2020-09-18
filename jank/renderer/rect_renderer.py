import typing as t

import jank

from .renderer import Renderer


class RectRenderer(Renderer):
    def __init__(
        self,
        width: float, height: float,
        colour: t.Tuple[int, int, int] = (255, 255, 255),
        batch: t.Optional[jank.graphics.Batch] = None,
        group: t.Optional[jank.graphics.Group] = None
    ):
        self.rect = jank.shape_sprites.Rectangle(
            0, 0,
            width, height,
            color=colour,
            batch=batch,
            group=group
        )

    @staticmethod
    def create_from_rect(rect: jank.shape_sprites.Rectangle):
        rect_renderer = RectRenderer.__new__(RectRenderer)
        rect_renderer.rect = rect
        return rect_renderer

    def set_position(self, position: jank.Vec2d):
        self.rect.position = position

    def set_rotation(self, rotation_degrees: float):
        self.rect.rotation = rotation_degrees

    def get_batch(self) -> t.Optional[jank.graphics.Batch]:
        return self.rect.batch

    def set_batch(self, batch: t.Optional[jank.graphics.Batch]):
        self.rect.batch = batch

    def get_group(self) -> t.Optional[jank.graphics.Group]:
        return self.rect.group

    def set_group(self, group: t.Optional[jank.graphics.Group]):
        self.rect.group = group

    def get_width(self) -> float:
        return self.rect.width

    def set_width(self, width: float):
        self.rect.width = width

    def get_height(self) -> float:
        return self.rect.height

    def set_height(self, height: float):
        self.rect.height = height

    def draw(self):
        self.rect.draw()

    def delete(self):
        self.rect.delete()

    @property
    def colour(self) -> t.Tuple[int, int, int]:
        return self.rect.color

    @colour.setter
    def colour(self, colour: t.Tuple[int, int, int]):
        self.rect.color = colour

    @property
    def opacity(self) -> int:
        return self.rect.opacity

    @opacity.setter
    def opacity(self, opacity: int):
        self.rect.opacity = opacity
