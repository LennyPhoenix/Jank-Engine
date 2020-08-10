import typing as t

import jank

from .base import Base


class Circle(Base):
    _x: float
    _y: float

    def __init__(
        self,
        x: float, y: float,
        radius: float,
        segments: int = None,
        colour: t.Tuple[int, int, int] = (255, 255, 255),
        opacity: int = 255,
        parent: t.Any = None,
        batch: jank.graphics.Batch = None,
        group: jank.graphics.Group = None
    ):
        self._x = x
        self._y = y
        self.circle = jank.shape_sprites.Circle(
            x, y,
            radius,
            segments,
            colour,
            batch, group
        )
        self.circle.opacity = opacity
        super().__init__(parent)

    def update_sprite(self):
        self.circle.x = self.real_x+self.width/2
        self.circle.y = self.real_y+self.height/2

    def delete_sprite(self):
        self.circle.delete()

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_width(self) -> float:
        return self.circle.radius*2

    def get_height(self) -> float:
        return self.circle.radius*2

    def set_x(self, x: float):
        self._x = x

    def set_y(self, y: float):
        self._y = y

    @property
    def radius(self) -> float:
        return self.circle.radius

    @radius.setter
    def radius(self, radius: float):
        self.circle.radius = radius

    @property
    def visible(self) -> bool:
        return self.circle.visible

    @visible.setter
    def visible(self, visible: bool):
        self.circle.visible = visible
