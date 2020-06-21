import pyglet
import pymunk
import pymunk.pyglet_util
from pyglet.window import key, mouse

from .camera import Camera

pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST

_applications = []


class Application:
    _debug_draw_options = pymunk.pyglet_util.DrawOptions()

    def __init__(
        self,
        caption: str = None,
        default_size: tuple = (1000, 800),
        minimum_size: tuple = (100, 100),
        world_layers: list = [],
        ui_layers: list = [],
        resizable: bool = True,
        fps_counter: bool = False,
        debug_mode: bool = False,
        windowless: bool = False
    ):
        set_application(self)
        self.debug_mode: bool = debug_mode
        self.windowless: bool = windowless

        self.physics_space = pymunk.Space()
        self.entities = []

        if self.windowless:
            return

        self.create_layers(world_layers, ui_layers)

        self.default_size = default_size
        self.window = pyglet.window.Window(
            width=self.default_size[0],
            height=self.default_size[1],
            caption=caption,
            resizable=resizable
        )
        self._handlers = []
        self.window.set_minimum_size(*minimum_size)
        self.push_handlers(self)

        if fps_counter:
            self.fps_display = pyglet.window.FPSDisplay(window=self.window)
            self.fps_display.label.color = (255, 255, 255, 200)

        self.key_handler = key.KeyStateHandler()
        self.mouse_handler = mouse.MouseStateHandler()
        self.push_handlers(self.key_handler, self.mouse_handler)

        self.world_batch = pyglet.graphics.Batch()
        self.world_camera = Camera(
            scroll_speed=0,
            min_zoom=0,
            max_zoom=float("inf")
        )
        self.position_camera()

        self.ui_batch = pyglet.graphics.Batch()
        if fps_counter:
            self.fps_display.label.batch = self.ui_batch

    def push_handlers(self, *handlers):
        for handler in handlers:
            self._handlers.append(handler)
            self.window.push_handlers(handler)

    def remove_handlers(self, *handlers):
        for handler in handlers:
            if handler in self._handlers:
                self._handlers.remove(handler)
                self.window.remove_handlers(handler)

    def on_draw(self):
        self.window.clear()
        with self.world_camera:
            self.world_batch.draw()
            if self.debug_mode:
                self.physics_space.debug_draw(self._debug_draw_options)
        self.ui_batch.draw()

    def position_camera(
        self,
        position: tuple = (0, 0), zoom: float = 1,
        min_pos: tuple = (None, None), max_pos: tuple = (None, None)
    ):
        zoom = min(
            self.window.width/self.default_size[0],
            self.window.height/self.default_size[1]
        ) * zoom

        if self.world_camera.zoom != zoom:
            self.world_camera.zoom = zoom

        x = -self.window.width//2/zoom
        y = -self.window.height//2/zoom

        target_x = position[0]
        target_y = position[1]

        if min_pos[0] is not None:
            target_x = max(target_x, min_pos[0])
        if min_pos[1] is not None:
            target_y = max(target_y, min_pos[1])
        if max_pos[0] is not None:
            target_x = min(target_x, max_pos[0])
        if max_pos[1] is not None:
            target_y = min(target_y, max_pos[1])

        x += target_x
        y += target_y

        if self.world_camera.position != (x, y):
            self.world_camera.position = (x, y)

    def create_layers(self, world_layers, ui_layers):
        self.world_layers = {}
        self.world_layers["master"] = pyglet.graphics.Group()
        for layer in world_layers:
            self.world_layers[layer] = pyglet.graphics.OrderedGroup(
                world_layers.index(layer)+1,
                parent=self.world_layers["master"]
            )

        self.ui_layers = {}
        self.ui_layers["master"] = pyglet.graphics.Group()
        for layer in ui_layers:
            self.ui_layers[layer] = pyglet.graphics.OrderedGroup(
                ui_layers.index(layer)+1,
                parent=self.ui_layers["master"]
            )

    def on_update(self, dt):
        """ Called as frequently as possible. Update input/graphics here. """

    def on_fixed_update(self, dt):
        """ Called 120 times a second at a fixed rate. Update physics here. """

    def _update(self, dt):
        self.on_update(dt)
        for handler in self._handlers:
            if hasattr(handler, "on_update") and handler is not self:
                handler.on_update(dt)

    def _fixed_update(self, dt):
        self.physics_space.step(dt)
        self.on_fixed_update(dt)
        for handler in self._handlers:
            if hasattr(handler, "on_fixed_update") and handler is not self:
                handler.on_fixed_update(dt)

    def run(self):
        pyglet.clock.schedule_interval(self._fixed_update, 1/120)
        pyglet.clock.schedule(self._update)
        pyglet.app.run()


def get_application(index: int = 0) -> Application:
    try:
        return _applications[index]
    except IndexError:
        return None


def set_application(application: Application):
    _applications.append(application)
