import typing as t

import jank

from .constants import BOTTOM, LEFT


class UIBase:
    _anchor_x: float = LEFT
    _anchor_y: float = BOTTOM
    _parent_anchor_x: float = LEFT
    _parent_anchor_y: float = BOTTOM
    _parent: t.Any = None

    children: t.List[t.Any]

    def __init__(self, parent: t.Any = None):
        self.children = []
        self.parent = parent
        jank.get_app().push_handlers(self)

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
    def anchor_x(self) -> float:
        return self._anchor_x

    @anchor_x.setter
    def anchor_x(self, anchor_x: float):
        self._anchor_x = anchor_x
        self.update_position()

    @property
    def anchor_y(self) -> float:
        return self._anchor_y

    @anchor_y.setter
    def anchor_y(self, anchor_y: float):
        self._anchor_y = anchor_y
        self.update_position()

    @property
    def parent_anchor_x(self) -> float:
        return self._parent_anchor_x

    @parent_anchor_x.setter
    def parent_anchor_x(self, parent_anchor_x: float):
        self._parent_anchor_x = parent_anchor_x
        self.update_position()

    @property
    def parent_anchor_y(self) -> float:
        return self._parent_anchor_y

    @parent_anchor_y.setter
    def parent_anchor_y(self, parent_anchor_y: float):
        self._parent_anchor_y = parent_anchor_y
        self.update_position()

    @property
    def real_x(self) -> float:
        real_x = self.x
        if self.parent is not None:
            real_x += self.parent.real_x
            parent = self.parent
        else:
            parent = jank.get_app().window

        real_x -= self.width*self.anchor_x

        real_x += parent.width*self.parent_anchor_x

        return real_x

    @property
    def real_y(self) -> float:
        real_y = self.y
        if self.parent is not None:
            real_y += self.parent.real_y
            parent = self.parent
        else:
            parent = jank.get_app().window

        real_y -= self.height*self.anchor_y

        real_y += parent.height*self.parent_anchor_y

        return real_y

    @property
    def parent(self) -> t.Any:
        return self._parent

    @parent.setter
    def parent(self, parent: t.Any):
        self._parent = parent
        if self.parent is not None:
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

    def on_resize(self, width, height):
        if self.parent is None:
            self.update_position()
