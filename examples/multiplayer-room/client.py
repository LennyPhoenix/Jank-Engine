import jank
import source

import time
import threading


IP = "localhost"
PORT = 25565


class Client(jank.networking.Client):
    def __init__(self):
        config = jank.Config(
            caption="Jank Engine, Multiplayer Example",
            default_size=(800, 800),
            minimum_size=(400, 400),
            world_layers=[
                "floor",
                "player",
                "name_tags",
                "objects"
            ]
        )

        super().__init__(config=config, show_fps=True)
        self.camera.zoom = 5
        self.players = {}
        self.sprite_queue = []

        self.name_chosen = False
        self.username = None
        self.player = None

        self.register_protocol(self.username_taken)
        self.register_protocol(self.add_player)
        self.register_protocol(self.remove_player)
        self.register_protocol(self.player_list)
        self.register_protocol(self.player_positions)

    def username_taken(self):
        print("Username Taken")

    def add_player(self, name):
        if self.name_chosen:
            player = source.Player(name)
            self.players[name] = player
            self.sprite_queue.append(player)

    def remove_player(self, name):
        if self.name_chosen and name in self.players.keys():
            self.players[name].delete()
            del self.players[name]

    def player_list(self, **players):
        self.name_chosen = True
        for username, attributes in players.items():
            player = source.Player(username)

            self.sprite_queue.append(player)

            self.players[username] = player
            player.position = attributes["position"]
            player.body.velocity = attributes["velocity"]
            if username == self.username:
                player.controlling = True
                self.player = player

    def player_positions(self, **players):
        if self.player is not None:
            for username, attributes in players.items():
                if username not in self.players.keys():
                    continue
                player = self.players[username]
                player.position = attributes["position"]
                player.body.velocity = attributes["velocity"]

    def on_update(self, dt):
        if self.name_chosen and self.player is not None and self.connected:
            self.send(
                "player_controls", self.player.controls,
                network_protocol=self.UDP
            )

        if len(self.sprite_queue) > 0:
            sprite = self.sprite_queue[0]
            sprite.create_sprite()
            self.sprite_queue.remove(sprite)

    def on_fixed_update(self, dt):
        for _ in range(5):
            self.physics_space.step(dt/5)

    def on_key_press(self, key, modifiers):
        if key == jank.key.GRAVE:
            self.debug_mode = not self.debug_mode
        if key == jank.key.ENTER:
            self.disconnect()
        if key == jank.key.BACKSPACE:
            self.send("dc")

    def on_connection(self, socket):
        def name_loop():
            while not self.name_chosen:
                name = input("Choose Username: ")
                self.username = name
                self.send("choose_username", {"username": name})
                time.sleep(3)

        _name_loop = threading.Thread(
            target=name_loop,
            daemon=True
        )
        _name_loop.start()

    def run(self):
        self.connect(
            address=IP,
            port=PORT,
            enable_udp=True
        )
        super().run()


if __name__ == "__main__":
    client = Client()
    client.run()
