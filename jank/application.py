import typing as t
from queue import Queue

import pyglet
import pymunk
import pymunk.pyglet_util
from pyglet.window import key, mouse

from .camera import Camera
from .config import Config

pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST

_applications = []


class Application:
    _debug_draw_options: pymunk.SpaceDebugDrawOptions = pymunk.pyglet_util.DrawOptions()
    _handlers: t.List[t.Any] = []
    _function_queue_soft: Queue = Queue()
    _function_queue_hard: Queue = Queue()
    _function_queue_soft_fixed: Queue = Queue()
    _function_queue_hard_fixed: Queue = Queue()
    _active_camera: Camera = None

    def __init__(
        self,
        config: Config = Config(),
        windowless: bool = False,
        debug_mode: bool = False,
        show_fps: bool = False
    ):
        set_application(self)
        self.config = config
        self.windowless = windowless
        self.debug_mode = debug_mode
        self.show_fps = show_fps

        self.physics_space = pymunk.Space()

        if self.windowless:
            return

        self.create_layers(self.config.world_layers, self.config.ui_layers)

        self.window = pyglet.window.Window(
            width=self.config.default_size[0],
            height=self.config.default_size[1],
            caption=self.config.caption,
            resizable=self.config.resizable,
            vsync=self.config.vsync
        )
        if self.config.icon is not None:
            self.window.set_icon(self.config.icon)
        self.window.set_minimum_size(*self.config.minimum_size)
        self.push_handlers(self)

        self.fps_display = pyglet.window.FPSDisplay(window=self.window)
        if self.config.fps_label is not None:
            self.fps_display.label = self.config.fps_label

        self.key_handler = key.KeyStateHandler()
        self.mouse_handler = mouse.MouseStateHandler()
        self.push_handlers(self.key_handler, self.mouse_handler)

        self.world_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()
        self.camera = Camera()
        self.camera.set_active()

    def screen_to_world(self, position: t.Tuple[int, int]) -> t.Tuple[float, float]:
        """ Convert a screen position to a world position. """

        zoom = self._active_camera.zoom
        if self._active_camera.auto_adjust:
            zoom *= min(
                self.window.width/self.config.default_size[0],
                self.window.height/self.config.default_size[1]
            )

        x, y = position

        x -= self.window.width//2
        y -= self.window.height//2

        x /= zoom
        y /= zoom

        x += self._active_camera.x
        y += self._active_camera.y

        return (x, y)

    def world_to_screen(self, position: t.Tuple[float, float]) -> t.Tuple[int, int]:
        """ Convert a world position to a screen position. """

        zoom = self._active_camera.zoom
        if self._active_camera.auto_adjust:
            zoom *= min(
                self.window.width/self.config.default_size[0],
                self.window.height/self.config.default_size[1]
            )

        x, y = position

        x -= self._active_camera.x
        y -= self._active_camera.y

        x *= zoom
        y *= zoom

        x += self.window.width//2
        y += self.window.height//2

        return (round(x), round(y))

    def push_handlers(self, *handlers):
        for handler in handlers:
            self._handlers.append(handler)
            if not self.windowless:
                self.window.push_handlers(handler)

    def remove_handlers(self, *handlers):
        for handler in handlers:
            if handler in self._handlers:
                self._handlers.remove(handler)
                if not self.windowless:
                    self.window.remove_handlers(handler)

    def on_draw(self):
        self.window.clear()
        with self._active_camera:
            self.world_batch.draw()
            if self.debug_mode:
                self.physics_space.debug_draw(self._debug_draw_options)
        self.ui_batch.draw()
        if self.show_fps:
            self.fps_display.draw()

    def create_layers(self, world_layers: t.List[str], ui_layers: t.List[str]):
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

    def on_update(self, dt: float):
        """ Called as frequently as possible. Update input/graphics here. """

    def on_fixed_update(self, dt: float):
        """ Called 120 times a second at a fixed rate. Update physics here. """

    def queue_hard(self, func: t.Callable[..., t.Any], fixed_update: bool, *args, **kwargs):
        """ Adds a function to the hard queue. """
        item = (func, args, kwargs)
        if fixed_update:
            self._function_queue_hard_fixed.put_nowait(item)
        else:
            self._function_queue_hard.put_nowait(item)

    def queue_soft(self, func: t.Callable[..., t.Any], fixed_update: bool, *args, **kwargs):
        """ Adds a function to the soft queue. """
        item = (func, args, kwargs)
        if fixed_update:
            self._function_queue_soft_fixed.put_nowait(item)
        else:
            self._function_queue_soft.put_nowait(item)

    def _update(self, dt: float):
        if not self._function_queue_soft.empty():
            item = self._function_queue_soft.get_nowait()
            item[0](*item[1], **item[2])

        while not self._function_queue_hard.empty():
            item = self._function_queue_hard.get_nowait()
            item[0](*item[1], **item[2])

        self.on_update(dt)
        for handler in self._handlers:
            if hasattr(handler, "on_update") and handler is not self:
                handler.on_update(dt)

    def _fixed_update(self, dt: float):
        if not self._function_queue_soft_fixed.empty():
            func = self._function_queue_soft_fixed.get_nowait()
            func[0](*func[1], **func[2])

        while not self._function_queue_hard_fixed.empty():
            func = self._function_queue_hard_fixed.get_nowait()
            func[0](*func[1], **func[2])

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
