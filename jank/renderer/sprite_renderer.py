import typing as t

import jank

from .renderer import Renderer


class SpriteRenderer(Renderer):
    _flip_x: bool = False
    _flip_y: bool = False

    def __init__(
        self,
        image: jank.pyglet.image.AbstractImage,
        blend_src: int = jank.pyglet.gl.GL_SRC_ALPHA,
        blend_dest: int = jank.pyglet.gl.GL_ONE_MINUS_SRC_ALPHA,
        batch: t.Optional[jank.graphics.Batch] = None,
        group: t.Optional[jank.graphics.Group] = None,
        usage: str = "dynamic",
        subpixel: bool = False
    ):
        self.sprite = jank.Sprite(
            image,
            blend_src=blend_src,
            blend_dest=blend_dest,
            batch=batch,
            group=group,
            usage=usage,
            subpixel=subpixel
        )

    @staticmethod
    def create_from_sprite(sprite: jank.Sprite):
        sprite_renderer = SpriteRenderer.__new__(SpriteRenderer)
        sprite_renderer.sprite = sprite
        return sprite_renderer

    def push_handlers(self, *handlers: t.List[t.Any]):
        self.sprite.push_handlers(*handlers)

    def remove_handlers(self, *handlers: t.List[t.Any]):
        self.sprite.remove_handlers(*handlers)

    def set_position(self, position: jank.Vec2d):
        self.sprite.position = position

    def set_rotation(self, rotation_degrees: float):
        self.sprite.rotation = rotation_degrees

    def get_batch(self) -> t.Optional[jank.graphics.Batch]:
        return self.sprite.batch

    def set_batch(self, batch: t.Optional[jank.graphics.Batch]):
        self.sprite.batch = batch

    def get_group(self) -> t.Optional[jank.graphics.Group]:
        return self.sprite.group

    def set_group(self, group: t.Optional[jank.graphics.Group]):
        self.sprite.group = group

    def get_width(self) -> float:
        return self.scaled_width

    def get_height(self) -> float:
        return self.scaled_height

    def draw(self):
        self.sprite.draw()

    def delete(self):
        self.sprite.delete()

    @property
    def scale(self) -> float:
        return self.sprite.scale

    @scale.setter
    def scale(self, scale: float):
        self.sprite.scale = scale
        self.update()

    @property
    def scale_x(self) -> float:
        return self.sprite.scale_x

    @scale_x.setter
    def scale_x(self, scale_x: float):
        self.sprite.scale_x = scale_x
        self.update()

    @property
    def scale_y(self) -> float:
        return self.sprite.scale_y

    @scale_y.setter
    def scale_y(self, scale_y: float):
        self.sprite.scale_y = scale_y
        self.update()

    @property
    def base_width(self) -> float:
        return self.sprite.width / abs(self.scale_x) / abs(self.scale)

    @property
    def base_height(self) -> float:
        return self.sprite.height / abs(self.scale_y) / abs(self.scale)

    @property
    def scaled_width(self) -> float:
        return self.base_width * self.scale_x * self.scale

    @property
    def scaled_height(self) -> float:
        return self.base_height * self.scale_y * self.scale

    @property
    def flip_x(self) -> bool:
        return self._flip_x

    @flip_x.setter
    def flip_x(self, flip_x: bool):
        if self._flip_x != flip_x:
            if flip_x:
                self.scale_x = -(abs(self.scale_x))
            else:
                self.scale_x = abs(self.scale_x)
            self._flip_x = flip_x
            self.update()

    @property
    def flip_y(self) -> bool:
        return self._flip_y

    @flip_y.setter
    def flip_y(self, flip_y: bool):
        if self._flip_y != flip_y:
            if flip_y:
                self.scale_y = -(abs(self.scale_y))
            else:
                self.scale_y = abs(self.scale_y)
            self._flip_y = flip_y
            self.update()

    @property
    def colour(self) -> t.Tuple[int, int, int]:
        return self.sprite.color

    @colour.setter
    def colour(self, colour: t.Tuple[int, int, int]):
        self.sprite.color = colour

    @property
    def opacity(self) -> int:
        return self.sprite.opacity

    @opacity.setter
    def opacity(self, opacity: int):
        self.sprite.opacity = opacity
