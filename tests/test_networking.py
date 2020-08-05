import time
import unittest

import jank


class TestNetworkingTCP(unittest.TestCase):
    def test_server(self):
        server = jank.networking.Server(windowless=True)
        server.connect("localhost", 5550, False)
        server.disconnect()

    def test_server_add_protocol(self):
        server = jank.networking.Server(windowless=True)

        @server.register_protocol
        def decorator_protocol(socket):
            pass

        def non_decorator_protocol(socket):
            pass
        server.register_protocol(non_decorator_protocol)

    def test_client_add_protocol(self):
        client = jank.networking.Client(windowless=True)

        @client.register_protocol
        def decorator_protocol():
            pass

        def non_decorator_protocol():
            pass
        client.register_protocol(non_decorator_protocol)

    def test_connect_client_dcc(self):
        server = jank.networking.Server(windowless=True)
        server.connect("localhost", 5551, False)

        client = jank.networking.Client(windowless=True)
        client.connect("localhost", 5551, False)

        client.disconnect()

    def test_connect_client_dcs(self):
        server = jank.networking.Server(windowless=True)
        server.connect("localhost", 5552, False)

        client = jank.networking.Client(windowless=True)
        client.connect("localhost", 5552, False)

        server.disconnect()

    def test_connect_multiple_clients_dcs(self):
        server = jank.networking.Server(windowless=True)
        server.connect("localhost", 5553, False)

        client1 = jank.networking.Client(windowless=True)
        client1.connect("localhost", 5553, False)

        client2 = jank.networking.Client(windowless=True)
        client2.connect("localhost", 5553, False)

        client3 = jank.networking.Client(windowless=True)
        client3.connect("localhost", 5553, False)

    def test_ping_pong(self):
        self.message = None
        message = "Hello World!"
        server = jank.networking.Server(windowless=True)

        @server.register_protocol
        def ping(socket, message):
            server.send(socket, "pong", {"message": message}, server.TCP)
        server.connect("localhost", 5554, False)

        client = jank.networking.Client(windowless=True)

        @client.register_protocol
        def pong(message):
            self.message = message
        client.connect("localhost", 5554, False)

        client.send("ping", {"message": message}, client.TCP)

        time.sleep(1)
        self.assertEqual(self.message, message)
        del self.message

    def test_broadcast(self):
        server = jank.networking.Server(windowless=True)
        server.connect("localhost", 5555, False)

        client1 = jank.networking.Client(windowless=True)
        client2 = jank.networking.Client(windowless=True)
        client3 = jank.networking.Client(windowless=True)

        @client1.register_protocol
        @client2.register_protocol
        @client3.register_protocol
        def say(message):
            print(message)

        client1.connect("localhost", 5555, False)
        client2.connect("localhost", 5555, False)
        client3.connect("localhost", 5555, False)

        server.broadcast("say", {"message": "Received."}, network_protocol=server.TCP)


class TestNetworkingUDP(unittest.TestCase):
    def test_server(self):
        server = jank.networking.Server(windowless=True)
        server.connect("localhost", 5560, True)
        server.disconnect()

    def test_connect_client_dcc(self):
        server = jank.networking.Server(windowless=True)
        server.connect("localhost", 5561, True)

        client = jank.networking.Client(windowless=True)
        client.connect("localhost", 5561, True)

        client.disconnect()

    def test_connect_client_dcs(self):
        server = jank.networking.Server(windowless=True)
        server.connect("localhost", 5562, True)

        client = jank.networking.Client(windowless=True)
        client.connect("localhost", 5562, True)

        server.disconnect()

    def test_connect_multiple_clients_dcs(self):
        server = jank.networking.Server(windowless=True)
        server.connect("localhost", 5563, True)

        client1 = jank.networking.Client(windowless=True)
        client1.connect("localhost", 5563, True)

        client2 = jank.networking.Client(windowless=True)
        client2.connect("localhost", 5563, True)

        client3 = jank.networking.Client(windowless=True)
        client3.connect("localhost", 5563, True)

    def test_ping_pong(self):
        self.message = None
        message = "Hello World!"
        server = jank.networking.Server(windowless=True)

        @server.register_protocol
        def ping(socket, message):
            server.send(socket, "pong", {"message": message}, server.UDP)
        server.connect("localhost", 5564, True)

        client = jank.networking.Client(windowless=True)

        @client.register_protocol
        def pong(message):
            self.message = message
        client.connect("localhost", 5564, True)

        client.send("ping", {"message": message}, client.UDP)

        time.sleep(1)
        self.assertEqual(self.message, message)
        del self.message

    def test_broadcast(self):
        server = jank.networking.Server(windowless=True)
        server.connect("localhost", 5565, True)

        client1 = jank.networking.Client(windowless=True)
        client2 = jank.networking.Client(windowless=True)
        client3 = jank.networking.Client(windowless=True)

        @client1.register_protocol
        @client2.register_protocol
        @client3.register_protocol
        def say(message):
            print(message)

        client1.connect("localhost", 5565, True)
        client2.connect("localhost", 5565, True)
        client3.connect("localhost", 5565, True)

        server.broadcast("say", {"message": "Received."}, network_protocol=server.UDP)


if __name__ == '__main__':
    unittest.main()
