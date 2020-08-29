import typing as t
import time

import jank

from .base import UIBase
from .ui_renderer import UIRenderer


class Button(UIRenderer, jank.pyglet.event.EventDispatcher):
    _active: bool = True
    _time_pressed: float = 0

    renderer: jank.renderer.SpriteRenderer

    def __init__(
        self,
        x: float, y: float,
        out_img: jank.pyglet.image.AbstractImage,
        in_img: t.Optional[jank.pyglet.image.AbstractImage] = None,
        hover_img: t.Optional[jank.pyglet.image.AbstractImage] = None,
        inactive_img: t.Optional[jank.pyglet.image.AbstractImage] = None,
        parent: t.Optional[UIBase] = None,
        batch: t.Optional[jank.graphics.Batch] = None,
        group: t.Optional[jank.graphics.Group] = None
    ):
        self._out_img = out_img
        self._in_img = in_img
        self._hover_img = hover_img
        self._inactive_img = inactive_img

        self.pressed = False

        renderer = jank.renderer.SpriteRenderer(
            out_img,
            batch=batch,
            group=group
        )
        super().__init__(x, y, renderer, parent=parent)

    def on_press(self):
        """ Called on button press. """

    def on_release(self, time_held: float):
        """ Called on button release. """

    @property
    def scale(self) -> float:
        return self.renderer.scale

    @scale.setter
    def scale(self, scale: float):
        self.renderer.scale = scale
        self.update()

    @property
    def scale_x(self) -> float:
        return self.renderer.scale_x

    @scale_x.setter
    def scale_x(self, scale_x: float):
        self.renderer.scale_x = scale_x
        self.update()

    @property
    def scale_y(self) -> float:
        return self.renderer.scale_y

    @scale_y.setter
    def scale_y(self, scale_y: float):
        self.renderer.scale_y = scale_y
        self.update()

    @property
    def visible(self) -> bool:
        return self.renderer.visible

    @visible.setter
    def visible(self, visible: bool):
        self.renderer.visible = visible

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active
        if self._inactive_img is None:
            if active:
                self.visible = True
            else:
                self.visible = False
        else:
            if active and self.pressed and self._in_img is not None:
                self.renderer.image = self._in_img
            elif active:
                self.renderer.image = self._out_img
            else:
                self.renderer.image = self._inactive_img

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.check_hit(x, y) or not self.active:
            return
        if self._in_img is not None:
            self.renderer.image = self._in_img
        self.pressed = True
        self._time_pressed = time.perf_counter()
        self.dispatch_event("on_press")

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self.pressed:
            if not self.active:
                self.renderer.image = self._inactive_img
            elif self.check_hit(x, y) and self._hover_img is not None:
                self.renderer.image = self._hover_img
            else:
                self.renderer.image = self._out_img
            self.pressed = False
            time_held = time.perf_counter() - self._time_pressed
            self.dispatch_event("on_release", time_held)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.pressed or not self.active:
            return
        if self.check_hit(x, y) and self._hover_img is not None:
            self.renderer.image = self._hover_img
        else:
            self.renderer.image = self._out_img


Button.register_event_type("on_press")
Button.register_event_type("on_release")


class ToggleButton(Button):
    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.check_hit(x, y) or not self.active:
            return
        self.pressed = not self.pressed
        if self.pressed and self._in_img is not None:
            self.renderer.image = self._in_img
        elif self._hover_img is not None:
            self.renderer.image = self._hover_img
        else:
            self.renderer.image = self._out_img
        self.dispatch_event("on_toggle", self.pressed)

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass


ToggleButton.register_event_type("on_toggle")
