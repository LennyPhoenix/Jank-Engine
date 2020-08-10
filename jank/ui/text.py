import typing as t

import jank

from .base import Base


class Text(Base):
    ALIGN_LEFT: str = "left"
    ALIGN_CENTER: str = "center"
    ALIGN_RIGHT: str = "right"

    _x: float
    _y: float
    _text: str
    _visible: bool = True

    def __init__(
        self,
        x: float, y: float,
        text: str = "",
        colour: t.Tuple[int, int, int, int] = (255, 255, 255, 255),
        bold: bool = False, italic: bool = False,
        align: str = ALIGN_LEFT,
        font_name: t.Optional[str] = None,
        font_size: t.Optional[float] = None,
        multiline: bool = False,
        max_width: t.Optional[int] = None,
        max_height: t.Optional[int] = None,
        dpi: t.Optional[float] = None,
        parent: t.Optional[Base] = None,
        batch: t.Optional[jank.graphics.Batch] = None,
        group: t.Optional[jank.graphics.Group] = None
    ):
        self._x = x
        self._y = y
        self._text = text
        self.label = jank.pyglet.text.Label(
            text=text,
            font_name=font_name, font_size=font_size,
            bold=bold, italic=italic,
            color=colour,
            x=x, y=y,
            width=max_width, height=max_height,
            align=align,
            multiline=multiline,
            dpi=dpi,
            batch=batch, group=group
        )
        super().__init__(parent)

    def update_sprite(self):
        self.label.x = self.real_x
        self.label.y = self.real_y

    def delete_sprite(self):
        self.label.delete()

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_width(self) -> float:
        return self.label.content_width

    def get_height(self) -> float:
        return self.label.content_height

    def set_x(self, x: float):
        self._x = x

    def set_y(self, y: float):
        self._y = y

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text
        if self.visible:
            self.label.text = text

    @property
    def max_width(self) -> float:
        return self.label.width

    @max_width.setter
    def max_width(self, max_width: float):
        self.label.width = max_width

    @property
    def max_height(self) -> float:
        return self.label.height

    @max_height.setter
    def max_height(self, max_height: float):
        self.label.height = max_height

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, visible: bool):
        self._visible = visible
        if visible:
            self.label.text = self.text
        else:
            self.label.text = ""
