import typing as t

import jank


class UIBase:
    _x: float = 0.
    _y: float = 0.
    _width: float = 0.
    _height: float = 0.
    _anchor_x: float = 0.5
    _anchor_y: float = 0.5
    _parent_anchor_x: float = 0.5
    _parent_anchor_y: float = 0.5
    _parent: t.Optional["UIBase"] = None

    children: t.List["UIBase"]

    def __init__(self, x: float = 0, y: float = 0, parent: t.Optional["UIBase"] = None):
        self._x = x
        self._y = y
        self.children = []
        self.parent = parent
        jank.get_app().push_handlers(self)
        self.update()

    def set_position(self, x: float, y: float):
        """ Set the position of any sprites and/or renderers. """

    def run_cleanup(self):
        """ Run any deletion or garbage collection functions. """

    def draw(self):
        """ Draw any sprites or renderers manually. """

    def get_width(self) -> float:
        """ Get the width of the element. """
        return self._width

    def set_width(self, width: float):
        """ Set the width of the element. """
        self._width = width

    def get_height(self) -> float:
        """ Gets the height of the element. """
        return self._height

    def set_height(self, height: float):
        """ Sets the height of the element. """
        self._height = height

    def update(self):
        self.set_position(self.real_x, self.real_y)
        for child in self.children:
            child.update()

    def delete(self, recursive: bool = True):
        parent = self.parent
        self.parent = None
        for child in self.children:
            if recursive:
                child.delete(True)
            else:
                child.parent = parent
        jank.get_app().remove_handlers(self)
        self.run_cleanup()

    def add_child(self, child: t.Any):
        child._parent = self
        self.children.append(child)
        child.update()

    def on_resize(self, width, height):
        if self.parent is None:
            self.update()

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
    def anchor_x(self) -> float:
        return self._anchor_x

    @anchor_x.setter
    def anchor_x(self, anchor_x: float):
        self._anchor_x = anchor_x
        self.update()

    @property
    def anchor_y(self) -> float:
        return self._anchor_y

    @anchor_y.setter
    def anchor_y(self, anchor_y: float):
        self._anchor_y = anchor_y
        self.update()

    @property
    def anchor(self) -> t.Tuple[float, float]:
        return (self._anchor_x, self._anchor_y)

    @anchor.setter
    def anchor(self, anchor: t.Tuple[float, float]):
        self._anchor_x, self._anchor_y = anchor
        self.update()

    @property
    def parent(self) -> t.Optional["UIBase"]:
        return self._parent

    @parent.setter
    def parent(self, parent: t.Optional["UIBase"]):
        if self.parent is not None:
            self.parent.children.remove(self)
        self._parent = parent
        if self.parent is not None:
            self.parent.children.append(self)
        self.update()

    @property
    def parent_anchor_x(self) -> float:
        return self._parent_anchor_x

    @parent_anchor_x.setter
    def parent_anchor_x(self, parent_anchor_x: float):
        self._parent_anchor_x = parent_anchor_x
        self.update()

    @property
    def parent_anchor_y(self) -> float:
        return self._parent_anchor_y

    @parent_anchor_y.setter
    def parent_anchor_y(self, parent_anchor_y: float):
        self._parent_anchor_y = parent_anchor_y
        self.update()

    @property
    def parent_anchor(self) -> t.Tuple[float, float]:
        return (self._parent_anchor_x, self._parent_anchor_y)

    @parent_anchor.setter
    def parent_anchor(self, parent_anchor: t.Tuple[float, float]):
        self._parent_anchor_x, self._parent_anchor_y = parent_anchor
        self.update()

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, x: float):
        self._x = x
        self.update()

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, y: float):
        self._y = y
        self.update()

    @property
    def width(self) -> float:
        return self.get_width()

    @width.setter
    def width(self, width: float):
        self.set_width(width)
        self.update()

    @property
    def height(self) -> float:
        return self.get_height()

    @height.setter
    def height(self, height: float):
        self.set_height(height)
        self.update()

    @property
    def bounding_box(self) -> jank.BoundingBox:
        return jank.BoundingBox(
            self.real_x,
            self.real_y,
            self.real_x+self.width,
            self.real_y+self.height
        )

    @property
    def full_bounding_box(self) -> jank.BoundingBox:
        all_bounding_boxes = [
            child.full_bounding_box for child in self.children
        ]
        all_bounding_boxes.append(self.bounding_box)
        return jank.BoundingBox(
            min(bounding_box.left for bounding_box in all_bounding_boxes),
            min(bounding_box.bottom for bounding_box in all_bounding_boxes),
            max(bounding_box.right for bounding_box in all_bounding_boxes),
            max(bounding_box.top for bounding_box in all_bounding_boxes)
        )

    def check_hit(self, real_x: float, real_y: float):
        bb = self.bounding_box
        return bb.left <= real_x < bb.right and bb.bottom <= real_y < bb.top
