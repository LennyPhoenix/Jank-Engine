import typing as t

import jank

from .renderer import Renderer


class TextRenderer(Renderer):
    CAN_ROTATE: bool = False

    ALIGN_LEFT: str = "left"
    ALIGN_CENTER: str = "center"
    ALIGN_RIGHT: str = "right"

    _text: str
    _visible: bool = True

    def __init__(
        self,
        text: str = "",
        colour: t.Tuple[int, int, int] = (255, 255, 255),
        bold: bool = False, italic: bool = False,
        align: str = ALIGN_LEFT,
        font_name: t.Optional[str] = None,
        font_size: t.Optional[float] = None,
        multiline: bool = False,
        max_width: t.Optional[int] = None,
        max_height: t.Optional[int] = None,
        dpi: t.Optional[float] = None,
        batch: t.Optional[jank.graphics.Batch] = None,
        group: t.Optional[jank.graphics.Group] = None
    ):
        self._text = text
        self.label = jank.pyglet.text.Label(
            x=0, y=0,
            text=text,
            font_name=font_name, font_size=font_size,
            bold=bold, italic=italic,
            width=max_width, height=max_height,
            align=align,
            multiline=multiline,
            dpi=dpi,
            batch=batch, group=group
        )
        self.colour = colour

    @staticmethod
    def create_from_label(label: jank.pyglet.text.Label):
        text_renderer = TextRenderer.__new__(TextRenderer)
        text_renderer._text = label.text
        text_renderer.label = label
        return text_renderer

    def set_position(self, position: jank.Vec2d):
        self.label.x, self.label.y = position

    def get_batch(self) -> t.Optional[jank.graphics.Batch]:
        return self.label.batch

    def set_batch(self, batch: t.Optional[jank.graphics.Batch]):
        self.label.batch = batch

    def get_group(self) -> t.Optional[jank.graphics.Group]:
        return self.label.group

    def set_group(self, group: t.Optional[jank.graphics.Group]):
        self.label.group = group

    def get_width(self) -> float:
        return self.label.content_width

    def get_height(self) -> float:
        return self.label.content_height

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

    def draw(self):
        self.label.draw()

    def delete(self):
        self.label.delete()

    @property
    def colour(self) -> t.Tuple[int, int, int]:
        return self.label.color[:3]

    @colour.setter
    def colour(self, colour: t.Tuple[int, int, int]):
        self.label.color = (*colour, self.opacity)

    @property
    def opacity(self) -> int:
        return self.label.color[3]

    @opacity.setter
    def opacity(self, opacity: int):
        self.label.color = (*self.colour, opacity)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text
        if self.visible:
            self.label.text = text

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
