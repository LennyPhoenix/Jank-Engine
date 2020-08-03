import typing as t

import jank


class Camera:
    """A simple 2D camera that contains the speed and offset."""
    application_id = 0

    def __init__(
        self,
        position: t.Tuple[float, float] = (0, 0),
        auto_adjust: bool = True
    ):
        self.x = position[0]
        self.y = position[1]
        self.zoom = 1
        self.auto_adjust = auto_adjust

    @property
    def position(self) -> t.Tuple[float, float]:
        """Query the current offset."""
        return self.x, self.y

    @position.setter
    def position(self, position: t.Tuple[float, float]):
        """Set the scroll offset directly."""
        self.x, self.y = position

    @property
    def bounding_box(self) -> jank.BoundingBox:
        window = jank.get_application(self.application_id).window

        zoom = self.zoom
        if self.auto_adjust:
            config = jank.get_application(self.application_id).config
            zoom *= min(
                window.width/config.default_size[0],
                window.height/config.default_size[1]
            )

        x = -window.width//2/zoom + self.x
        y = -window.height//2/zoom + self.y

        width = window.width/zoom
        height = window.height/zoom

        return jank.BoundingBox(
            x, y,
            width+x, height+y
        )

    def transform(self, dx: float, dy: float):
        """Move the camera by a given amount."""
        self.x += dx
        self.y += dy

    def begin(self):
        """Set the current camera offset so you can draw your scene."""
        window = jank.get_application(self.application_id).window

        zoom = self.zoom
        if self.auto_adjust:
            config = jank.get_application(self.application_id).config
            zoom *= min(
                window.width/config.default_size[0],
                window.height/config.default_size[1]
            )

        x = -window.width//2/zoom + self.x
        y = -window.height//2/zoom + self.y

        jank.pyglet.gl.glTranslatef(
            -x * zoom,
            -y * zoom, 0
        )

        jank.pyglet.gl.glScalef(
            zoom,
            zoom, 1
        )

    def end(self):
        """Since this is a matrix, you will need to reverse the translate after rendering otherwise
        it will multiply the current offset every draw update pushing it further and further away.
        """
        window = jank.get_application(self.application_id).window

        zoom = self.zoom
        if self.auto_adjust:
            config = jank.get_application(self.application_id).config
            zoom *= min(
                window.width/config.default_size[0],
                window.height/config.default_size[1]
            )

        x = -window.width//2/zoom + self.x
        y = -window.height//2/zoom + self.y

        jank.pyglet.gl.glScalef(
            1 / zoom,
            1 / zoom, 1
        )

        jank.pyglet.gl.glTranslatef(
            x * zoom,
            y * zoom, 0
        )

    def set_active(self):
        jank.get_application(self.application_id)._active_camera = self

    def __enter__(self):
        self.begin()

    def __exit__(self, exception_type, exception_value, traceback):
        self.end()
