import jank

from .base import Base


class Circle(Base):
    _x: float
    _y: float

    def __init__(
        self,
        x, y,
        radius,
        segments=None,
        colour=(255, 255, 255),
        opacity=255,
        parent=None,
        batch=None, group=None
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

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_width(self):
        return self.circle.radius*2

    def get_height(self):
        return self.circle.radius*2

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def set_width(self, width):
        pass

    def set_height(self, height):
        pass
