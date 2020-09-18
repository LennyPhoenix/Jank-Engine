import math
import typing as t

import jank


class Renderer:
    CAN_ROTATE: bool = True

    _anchor_x: float = 0.5
    _anchor_y: float = 0.5
    _last_position: jank.Vec2d = jank.Vec2d.zero()
    _last_rotation: float = 0
    _offset: jank.Vec2d = jank.Vec2d.zero()

    def push_handlers(self, *handlers: t.List[t.Any]):
        """ Push the handlers to the renderable. """

    def remove_handlers(self, *handlers: t.List[t.Any]):
        """ Remove the handlers from the renderable. """

    def draw(self):
        """ Draw the renderable manually. """

    def delete(self):
        """ Delete the renderable. """

    def set_position(self, position: t.Union[jank.Vec2d, t.Tuple[float, float]]):
        """ Set the position of the renderable. """

    def set_rotation(self, rotation: float):
        """ Set the rotation of the renderable. """

    def get_width(self) -> float:
        """ Gets the width of the renderable. """
        return 0.

    def set_width(self, width: float):
        """ Sets the width of the renderable. (Optional) """

    @property
    def width(self) -> float:
        """ The width of the renderable. """
        return self.get_width()

    @width.setter
    def width(self, width: float):
        self.set_width(width)
        self.update()

    def get_height(self) -> float:
        """ Gets the height of the renderable. """
        return 0.

    def set_height(self, height: float):
        """ Sets the height of the renderable. (Optional) """

    @property
    def height(self) -> float:
        """ The height of the renderable. """
        return self.get_height()

    @height.setter
    def height(self, height: float):
        self.set_height(height)
        self.update()

    def get_batch(self) -> t.Optional[jank.graphics.Batch]:
        """ Gets the batch for the renderable. """
        return None

    def set_batch(self, batch: t.Optional[jank.graphics.Batch]):
        """ Sets the batch for the renderable. """

    @property
    def batch(self) -> t.Optional[jank.graphics.Batch]:
        """ The batch for the renderable. """
        return self.get_batch()

    @batch.setter
    def batch(self, batch: t.Optional[jank.graphics.Batch]):
        self.set_batch(batch)

    def get_group(self) -> t.Optional[jank.graphics.Group]:
        """ Gets the group for the renderable. """
        return None

    def set_group(self, group: t.Optional[jank.graphics.Group]):
        """ Sets the group for the renderable. (Optional) """

    @property
    def group(self) -> t.Optional[jank.graphics.Group]:
        """ The group for the renderable. """
        return self.get_group()

    @group.setter
    def group(self, group: t.Optional[jank.graphics.Group]):
        self.set_group(group)

    @property
    def offset(self) -> jank.Vec2d:
        return self._offset

    @offset.setter
    def offset(self, offset: t.Union[jank.Vec2d, t.Tuple[float, float]]):
        if type(offset) == tuple:
            offset = jank.Vec2d(offset)
        self._offset = offset
        self.update()

    def update(
        self,
        position: t.Optional[t.Union[jank.Vec2d, t.Tuple[float, float]]] = None,
        rotation: t.Optional[float] = None,
        rotation_is_radians: bool = False
    ):
        """ Update the renderable. """
        if type(position) == tuple:
            position = jank.Vec2d(position)

        if position is None:
            position = self._last_position
        else:
            self._last_position = position

        if rotation is None:
            rotation = self._last_rotation
        else:
            if rotation_is_radians:
                rotation = math.degrees(rotation)
            self._last_rotation = rotation

        offset = self.offset-self._anchor_offset

        if self.CAN_ROTATE:
            offset = offset.rotated(rotation)

        self.set_position(position+offset)
        self.set_rotation(-rotation)

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
        return self._anchor_x, self._anchor_y

    @anchor.setter
    def anchor(self, anchor: t.Tuple[float, float]):
        self._anchor_x, self._anchor_y = anchor
        self.update()

    @property
    def _anchor_offset(self) -> jank.Vec2d:
        return jank.Vec2d(
            self.width*self.anchor_x,
            self.height*self.anchor_y
        )
