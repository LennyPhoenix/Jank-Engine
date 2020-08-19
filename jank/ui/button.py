import typing as t

import jank

from .base import Base


class Button(Base, jank.pyglet.event.EventDispatcher):
    _active: bool = True
    _x: float
    _y: float

    def __init__(
        self,
        x: float, y: float,
        out_img: jank.pyglet.image.AbstractImage,
        in_img: t.Optional[jank.pyglet.image.AbstractImage] = None,
        hover_img: t.Optional[jank.pyglet.image.AbstractImage] = None,
        inactive_img: t.Optional[jank.pyglet.image.AbstractImage] = None,
        parent: t.Optional[Base] = None,
        batch: t.Optional[jank.graphics.Batch] = None,
        group: t.Optional[jank.graphics.Group] = None
    ):
        self._x = x
        self._y = y
        self._out_img = out_img
        self._in_img = in_img
        self._hover_img = hover_img
        self._inactive_img = inactive_img
        self.sprite = jank.Sprite(
            out_img,
            x, y,
            batch=batch,
            group=group
        )
        self.pressed = False
        super().__init__(parent)

    def on_press(self):
        """ Called on button press. """

    def on_release(self):
        """ Called on button release. """

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
                self.sprite.image = self._in_img
            elif active:
                self.sprite.image = self._out_img
            else:
                self.sprite.image = self._inactive_img

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.check_hit(x, y) or not self.active:
            return
        if self._in_img is not None:
            self.sprite.image = self._in_img
        self.pressed = True
        self.dispatch_event("on_press")

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.active:
            self.sprite.image = self._inactive_img
        elif self.check_hit(x, y) and self._hover_img is not None:
            self.sprite.image = self._hover_img
        else:
            self.sprite.image = self._out_img
        self.pressed = False
        self.dispatch_event("on_release")

    def on_mouse_motion(self, x, y, dx, dy):
        if self.pressed or not self.active:
            return
        if self.check_hit(x, y) and self._hover_img is not None:
            self.sprite.image = self._hover_img
        else:
            self.sprite.image = self._out_img


Button.register_event_type("on_press")
Button.register_event_type("on_release")


class ToggleButton(Button):
    def __init__(
        self,
        x: float, y: float,
        out_img: jank.pyglet.image.AbstractImage,
        in_img: jank.pyglet.image.AbstractImage,
        hover_img: t.Optional[jank.pyglet.image.AbstractImage] = None,
        inactive_img: t.Optional[jank.pyglet.image.AbstractImage] = None,
        parent: t.Optional[Base] = None,
        batch: t.Optional[jank.graphics.Batch] = None,
        group: t.Optional[jank.graphics.Group] = None
    ):
        super().__init__(
            x, y, out_img, in_img=in_img, hover_img=hover_img,
            inactive_img=inactive_img, parent=parent, batch=batch, group=group
        )

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.check_hit(x, y) or not self.active:
            return
        self.pressed = not self.pressed
        if self.pressed and self._in_img is not None:
            self.sprite.image = self._in_img
        elif self._hover_img is not None:
            self.sprite.image = self._hover_img
        else:
            self.sprit.image = self._out_img
        self.dispatch_event("on_toggle", self.pressed)

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass


ToggleButton.register_event_type("on_toggle")
