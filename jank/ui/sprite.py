import typing as t

import jank

from .base import Base


class Sprite(Base):
    _x: float
    _y: float

    def __init__(
        self,
        image: jank.pyglet.image.AbstractImage,
        x: float, y: float,
        subpixel: bool = True,
        parent: t.Any = None,
        batch: jank.graphics.Batch = None,
        group: jank.graphics.Group = None
    ):
        self._x = x
        self._y = y
        self.sprite = jank.Sprite(
            image,
            x, y,
            batch=batch,
            group=group,
            subpixel=subpixel
        )
        super().__init__(parent)

    def update_sprite(self):
        self.sprite.position = (self.real_x, self.real_y)

    def delete_sprite(self):
        self.sprite.delete()

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_width(self):
        return self.sprite.width

    def get_height(self):
        return self.sprite.height

    def set_x(self, x: float):
        self._x = x

    def set_y(self, y: float):
        self._y = y

    @property
    def scale(self) -> float:
        return self.sprite.scale

    @scale.setter
    def scale(self, scale: float):
        self.sprite.scale = scale
        self.update_position()

    @property
    def scale_x(self) -> float:
        return self.sprite.scale_x

    @scale_x.setter
    def scale_x(self, scale_x: float):
        self.sprite.scale_x = scale_x
        self.update_position()

    @property
    def scale_y(self) -> float:
        return self.sprite.scale_y

    @scale_y.setter
    def scale_y(self, scale_y: float):
        self.sprite.scale_y = scale_y
        self.update_position()

    @property
    def visible(self) -> bool:
        return self.sprite.visible

    @visible.setter
    def visible(self, visible: bool):
        self.sprite.visible = visible
