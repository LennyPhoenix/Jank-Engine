import typing as t

import jank

from .base import UIBase


class UIRenderer(UIBase):
    renderer: jank.renderer.Renderer

    def __init__(
        self,
        x: float, y: float,
        renderer: jank.renderer.Renderer,
        parent: t.Optional[UIBase] = None
    ):
        renderer.anchor = (0, 0)
        self.renderer = renderer
        super().__init__(x, y, parent)

    def set_position(self, x: float, y: float):
        self.renderer.update(jank.Vec2d(x, y))

    def run_cleanup(self):
        self.renderer.delete()

    def draw(self):
        self.renderer.draw()

    def get_width(self) -> float:
        return self.renderer.width

    def set_width(self, width: float):
        self.renderer.width = width

    def get_height(self) -> float:
        return self.renderer.height

    def set_height(self, height: float):
        self.renderer.height = height
