import typing as t

import jank

from .constants import BOTTOM, CENTER, LEFT, RIGHT, TOP


class UIBase:
    _anchor_x: str = LEFT
    _anchor_y: str = BOTTOM
    _parent_anchor_x: str = LEFT
    _parent_anchor_y: str = BOTTOM
    _parent: t.Any = None

    children: t.List[t.Any]

    def __init__(self, parent: t.Any = None):
        self.children = []
        self.parent = parent

    def update_sprite(self):
        pass

    def update_position(self):
        self.update_sprite()
        for child in self.children:
            child.update_position()

    def add_child(self, child: t.Any):
        child._parent = self
        self.children.append(child)
        child.update_position()

    def get_x(self) -> float:
        return 0.

    def set_x(self, x: float):
        pass

    @property
    def x(self) -> float:
        return self.get_x()

    @x.setter
    def x(self, x: float):
        self.set_x(x)
        self.update_position()

    def get_y(self) -> float:
        return 0.

    def set_y(self, y: float):
        pass

    @property
    def y(self) -> float:
        return self.get_y()

    @y.setter
    def y(self, y: float):
        self.set_y(y)
        self.update_position()

    def get_width(self) -> float:
        return 0.

    def set_width(self, width: float):
        pass

    @property
    def width(self) -> float:
        return self.get_width()

    @width.setter
    def width(self, width: float):
        self.set_width(width)
        self.update_position()

    def get_height(self) -> float:
        return 0.

    def set_height(self, height: float):
        pass

    @property
    def height(self) -> float:
        return self.get_height()

    @height.setter
    def height(self, height: float):
        self.set_height(height)
        self.update_position()

    @property
    def anchor_x(self) -> str:
        return self._anchor_x

    @anchor_x.setter
    def anchor_x(self, anchor_x: str):
        if anchor_x not in [jank.ui.LEFT, jank.ui.CENTER, jank.ui.RIGHT]:
            raise TypeError("anchor_x must be one of ui.LEFT, ui.CENTER, or ui.RIGHT.")
        self._anchor_x = anchor_x

    @property
    def anchor_y(self) -> str:
        return self._anchor_y

    @anchor_y.setter
    def anchor_y(self, anchor_y: str):
        if anchor_y not in [jank.ui.BOTTOM, jank.ui.CENTER, jank.ui.TOP]:
            raise TypeError("anchor_y must be one of ui.BOTTOM, ui.CENTER, or ui.TOP.")
        self._anchor_y = anchor_y

    @property
    def parent_anchor_x(self) -> str:
        return self._parent_anchor_x

    @parent_anchor_x.setter
    def parent_anchor_x(self, parent_anchor_x: str):
        if parent_anchor_x not in [LEFT, CENTER, RIGHT]:
            raise TypeError("parent_anchor_x must be one of ui.LEFT, ui.CENTER, or ui.RIGHT.")
        self._parent_anchor_x = parent_anchor_x

    @property
    def parent_anchor_y(self) -> str:
        return self._parent_anchor_y

    @parent_anchor_y.setter
    def parent_anchor_y(self, parent_anchor_y: str):
        if parent_anchor_y not in [BOTTOM, CENTER, TOP]:
            raise TypeError("parent_anchor_y must be one of ui.BOTTOM, ui.CENTER, or ui.TOP.")
        self._parent_anchor_y = parent_anchor_y

    @property
    def real_x(self) -> float:
        real_x = self.x
        if not isinstance(self.parent, jank.pyglet.window.Window):
            real_x += self.parent.real_x

        adjustments = {
            LEFT: lambda x: x,
            CENTER: lambda x: x-self.width/2,
            RIGHT: lambda x: x-self.width,
        }
        real_x = adjustments[self.anchor_x](real_x)

        parent_adjustments = {
            LEFT: lambda x: x,
            CENTER: lambda x: x+self.parent.width/2,
            RIGHT: lambda x: x+self.parent.width,
        }
        real_x = parent_adjustments[self.anchor_x](real_x)

        return real_x

    @property
    def real_y(self) -> float:
        real_y = self.y
        if not isinstance(self.parent, jank.pyglet.window.Window):
            real_y += self.parent.real_y

        adjustments = {
            LEFT: lambda x: x,
            CENTER: lambda x: x-self.height/2,
            RIGHT: lambda x: x-self.height,
        }
        real_y = adjustments[self.anchor_x](real_y)

        parent_adjustments = {
            LEFT: lambda x: x,
            CENTER: lambda x: x+self.parent.height/2,
            RIGHT: lambda x: x+self.parent.height,
        }
        real_y = parent_adjustments[self.anchor_x](real_y)

        return real_y

    @property
    def parent(self) -> t.Any:
        return self._parent

    @parent.setter
    def parent(self, parent: t.Any):
        if parent is None:
            parent = jank.get_app().window
        self._parent = parent
        self.parent.children.append(self)
        self.update_position()

    @property
    def bounding_box(self) -> jank.BoundingBox:
        return jank.BoundingBox(
            self.x,
            self.y,
            self.x+self.width,
            self.y+self.width
        )

    def check_hit(self, x, y):
        bb = self.bounding_box
        return bb.left <= x < bb.right and bb.bottom <= y < bb.top

    @property
    def bounding_box_real(self) -> jank.BoundingBox:
        return jank.BoundingBox(
            self.real_x,
            self.real_y,
            self.real_x+self.width,
            self.real_y+self.width
        )

    def check_hit_real(self, real_x, real_y):
        bb = self.bounding_box_real
        return bb.left <= real_x < bb.right and bb.bottom <= real_y < bb.top
