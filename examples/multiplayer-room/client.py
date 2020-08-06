import jank
import source

import time
import threading


IP = "localhost"
PORT = 25565


class Client(jank.Application):
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

        self.name_chosen = False
        self.username = None
        self.player = None

        self.client = jank.networking.Client()
        self.client.push_handlers(self)

        self.client.register_protocol(self.username_taken)
        self.client.register_protocol(self.add_player)
        self.client.register_protocol(self.remove_player)
        self.client.register_protocol(self.player_list)
        self.client.register_protocol(self.player_positions)

    def username_taken(self):
        print("Username Taken")

    def add_player(self, name):
        if self.name_chosen:
            player = source.Player(name)
            self.players[name] = player
            self.queue_soft(player.create_sprite, False)

    def remove_player(self, name):
        if self.name_chosen and name in self.players.keys():
            self.players[name].delete()
            del self.players[name]

    def player_list(self, **players):
        self.name_chosen = True
        for username, attributes in players.items():
            player = source.Player(username)

            self.queue_soft(player.create_sprite, False)

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
        if self.name_chosen and self.player is not None and self.client.connected:
            self.client.send(
                "player_controls", self.player.controls,
                network_protocol=self.client.UDP
            )

    def on_fixed_update(self, dt):
        for _ in range(5):
            self.physics_space.step(dt/5)

    def on_key_press(self, key, modifiers):
        if key == jank.key.GRAVE:
            self.debug_mode = not self.debug_mode

    def on_connection(self, socket):
        def name_loop():
            while not self.name_chosen:
                name = input("Choose Username: ")
                self.username = name
                self.client.send("choose_username", {"username": name})
                time.sleep(3)

        _name_loop = threading.Thread(
            target=name_loop,
            daemon=True
        )
        _name_loop.start()

    def run(self):
        self.client.connect(
            address=IP,
            port=PORT,
            enable_udp=True
        )
        super().run()


if __name__ == "__main__":
    client = Client()
    client.run()
