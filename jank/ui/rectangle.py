import jank

from .base import Base


class Rect(Base):
    _x: float
    _y: float

    def __init__(
        self,
        x, y,
        width, height,
        colour=(255, 255, 255),
        opacity=255,
        parent=None,
        batch=None, group=None
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

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def set_width(self, width):
        self.rect.width = width

    def set_height(self, height):
        self.rect.height = height
