import pyglet
import pymunk
import pymunk.pyglet_util
from pyglet.window import key, mouse

from .camera import Camera

pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST


class Application:
    _header_size = 64
    _debug_mode = False

    def __init__(
        self,
        caption: str = None,
        default_size: tuple = (1000, 800),
        minimum_size: tuple = (100, 100),
        world_layers: list = [],
        ui_layers: list = [],
        resizable: bool = True,
        fps_counter: bool = False
    ):
        self.create_layers(world_layers, ui_layers)

        self.default_size = default_size
        self.window = pyglet.window.Window(
            width=self.default_size[0],
            height=self.default_size[1],
            caption=caption,
            resizable=resizable
        )
        self.window.set_minimum_size(*minimum_size)
        self.window.push_handlers(self)

        if fps_counter:
            self._fps_display = pyglet.window.FPSDisplay(window=self.window)
            self._fps_display.label.color = (255, 255, 255, 200)

        self.key_handler = key.KeyStateHandler()
        self.mouse_handler = mouse.MouseStateHandler()
        self.window.push_handlers(self.key_handler, self.mouse_handler)

        self.world_batch = pyglet.graphics.Batch()
        self.world_camera = Camera(
            scroll_speed=0,
            min_zoom=0,
            max_zoom=float("inf")
        )

        self.ui_batch = pyglet.graphics.Batch()
        if fps_counter:
            self._fps_display.label.batch = self.ui_batch

        self.physics_space = pymunk.Space()
        self.entities = []

    def on_draw(self):
        self.window.clear()
        with self.world_camera:
            self.world_batch.draw()
            if self._debug_mode:
                debug_draw_options = pymunk.pyglet_util.DrawOptions()
                self.physics_space.debug_draw(debug_draw_options)
        self.ui_batch.draw()

    def on_key_press(self, button, modifiers):
        if button == key.GRAVE:
            self._debug_mode = not self._debug_mode

    def update(self, dt):
        self.physics_space.step(dt)
        self.position_camera()

    def position_camera(self, position: tuple = (0, 0)):
        zoom = min(
            self.window.width/self.default_size[0],
            self.window.height/self.default_size[1]
        )

        if self.world_camera.zoom != zoom:
            self.world_camera.zoom = zoom

        x = -self.window.width//2/zoom
        y = -self.window.height//2/zoom

        x += position[0]
        y += position[1]

        x, y = round(x), round(y)

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

    def run(self):
        pyglet.clock.schedule(self.update)
        pyglet.app.run()


if __name__ == "__main__":
    application = Application()
    application.run()
