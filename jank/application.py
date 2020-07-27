from typing import List, Tuple
from queue import Queue

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
    _handlers = []
    _function_queue_soft = Queue()
    _function_queue_hard = Queue()
    _function_queue_soft_fixed = Queue()
    _function_queue_hard_fixed = Queue()

    # Config Options: these should be changed here.
    CAPTION: str = None
    DEFAULT_SIZE: Tuple[int, int] = (1000, 800)
    MINIMUM_SIZE: Tuple[int, int] = (100, 100)
    RESIZABLE: bool = True
    VSYNC: bool = True
    FPS_LABEL: pyglet.text.Label = None
    WORLD_LAYERS: List[str] = []
    UI_LAYERS: List[str] = []

    def __init__(
        self,
        windowless: bool = False,
        debug_mode: bool = False,
        show_fps: bool = False
    ):
        set_application(self)
        self.windowless = windowless
        self.debug_mode = debug_mode
        self.show_fps = show_fps

        self.physics_space = pymunk.Space()

        if self.windowless:
            return

        self.create_layers(self.WORLD_LAYERS, self.UI_LAYERS)

        self.window = pyglet.window.Window(
            width=self.DEFAULT_SIZE[0],
            height=self.DEFAULT_SIZE[1],
            caption=self.CAPTION,
            resizable=self.RESIZABLE,
            vsync=self.VSYNC
        )
        self.window.set_minimum_size(*self.MINIMUM_SIZE)
        self.push_handlers(self)

        self.fps_display = pyglet.window.FPSDisplay(window=self.window)
        if self.FPS_LABEL is not None:
            self.fps_display.label = self.FPS_LABEL

        self.key_handler = key.KeyStateHandler()
        self.mouse_handler = mouse.MouseStateHandler()
        self.push_handlers(self.key_handler, self.mouse_handler)

        self.world_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()
        self.world_camera = Camera(
            scroll_speed=0,
            min_zoom=0,
            max_zoom=float("inf")
        )
        self.position_camera()

    def screen_to_world(self, position: Tuple[float, float]) -> Tuple[float, float]:
        """ Convert a screen position to a world position. """
        x, y = position

        x /= self.world_camera.zoom
        y /= self.world_camera.zoom

        x += self.world_camera.offset_x
        y += self.world_camera.offset_y

        return (x, y)

    def world_to_screen(self, position: Tuple[float, float]) -> Tuple[float, float]:
        """ Convert a world position to a screen position. """
        x, y = position

        x -= self.world_camera.offset_x
        y -= self.world_camera.offset_y

        x *= self.world_camera.zoom
        y *= self.world_camera.zoom

        return (x, y)

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
        with self.world_camera:
            self.world_batch.draw()
            if self.debug_mode:
                self.physics_space.debug_draw(self._debug_draw_options)
        self.ui_batch.draw()
        if self.show_fps:
            self.fps_display.draw()

    def position_camera(
        self,
        position: tuple = (0, 0), zoom: float = 1,
        min_pos: tuple = (None, None), max_pos: tuple = (None, None)
    ):
        zoom = min(
            self.window.width/self.DEFAULT_SIZE[0],
            self.window.height/self.DEFAULT_SIZE[1]
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

    def create_layers(self, world_layers: list, ui_layers: list):
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

    def queue_hard(self, func, fixed_update: bool, *args, **kwargs):
        """ Adds a function to the hard queue. """
        item = (func, args, kwargs)
        if fixed_update:
            self._function_queue_hard_fixed.put_nowait(item)
        else:
            self._function_queue_hard.put_nowait(item)

    def queue_soft(self, func, fixed_update: bool, *args, **kwargs):
        """ Adds a function to the soft queue. """
        item = (func, args, kwargs)
        if fixed_update:
            self._function_queue_soft_fixed.put_nowait(item)
        else:
            self._function_queue_soft.put_nowait(item)

    def _update(self, dt):
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

    def _fixed_update(self, dt):
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
