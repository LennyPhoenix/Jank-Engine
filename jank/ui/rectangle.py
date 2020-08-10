import typing as t

import jank

from .base import Base


class Rect(Base):
    _x: float
    _y: float

    def __init__(
        self,
        x: float, y: float,
        width: float, height: float,
        colour: t.Tuple[int, int, int] = (255, 255, 255),
        opacity: int = 255,
        parent: t.Any = None,
        batch: jank.graphics.Batch = None,
        group: jank.graphics.Group = None
    ):
        self._x = x
        self._y = y
        self.rect = jank.shape_sprites.Rectangle(
            x, y,
            width,
            height,
            colour,
            batch,
            group
        )
        self.rect.opacity = opacity
        super().__init__(parent)

    def update_sprite(self):
        self.rect.x = self.real_x
        self.rect.y = self.real_y

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_width(self) -> float:
        return self.rect.width

    def get_height(self) -> float:
        return self.rect.height

    def set_x(self, x: float):
        self._x = x

    def set_y(self, y: float):
        self._y = y

    def set_width(self, width: float):
        self.rect.width = width

    def set_height(self, height: float):
        self.rect.height = height
