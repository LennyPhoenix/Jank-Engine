import jank
import source


IP = "localhost"
PORT = 25565


class Server(jank.networking.Server):

    def __init__(self):
        super().__init__(windowless=True)
        self.players = {}
        self.usernames = {}

        self.register_protocol(self.choose_username)
        self.register_protocol(self.player_controls)

    def player_controls(self, socket, **controls):
        username = self.usernames[socket]
        player = self.players[username]

        player.controls = controls

    def choose_username(self, socket, username: str):
        if username in self.players.keys():
            self.send(
                socket, "username_taken"
            )
            return

        self.usernames[socket] = username
        self.players[username] = source.Player(username)
        self.broadcast("add_player", {"name": username}, exclude=[socket])
        self.send(
            socket, "player_list",
            {
                username: {
                    "position": tuple(player.position),
                    "velocity": tuple(player.body.velocity)
                }
                for username, player in self.players.items()
            }
        )

    def on_disconnection(self, socket):
        if socket in self.usernames.keys():
            username = self.usernames[socket]
            del self.usernames[socket]

            if username in self.players.keys():
                self.players[username].delete()
                del self.players[username]

            self.broadcast(
                "remove_player", {"name": username}
            )

    def on_fixed_update(self, dt):
        for _ in range(10):
            self.physics_space.step(1/1200)
        positions = {
            username: {
                "position": tuple(player.position),
                "velocity": tuple(player.body.velocity)
            }
            for username, player in self.players.items()
        }
        self.broadcast(
            "player_positions",
            positions,
            network_protocol=self.UDP
        )

    def run(self):
        self.connect(
            address=IP,
            port=PORT,
            enable_udp=True
        )
        super().run()


if __name__ == "__main__":
    server = Server()
    server.run()
