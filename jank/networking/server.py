import pickle
import socket
import threading
import time

from jank.application import Application


class Server(Application):
    _header_size = 64
    _protocols = {}
    connected = False

    def register_protocol(self, func, name: str = None):
        if name is None:
            name = func.__name__

        self._protocols[name] = func

    def on_connection(self, socket: socket.socket):
        """ Called on new connection. """

    def on_disconnection(self, socket: socket.socket):
        """ Called on socket disconnection. """

    def threaded_client(self, c_socket, c_address):
        print(f"Accepted new connection from {c_address[0]}:{c_address[1]}.")
        self.clients[c_address] = c_socket

        self.on_connection(c_socket)

        try:
            while True:
                header_bytes = self.recv_bytes(c_socket, self._header_size)
                header = header_bytes.decode("utf-8")
                length = int(header.strip())

                message = self.recv_bytes(c_socket, length)

                data = pickle.loads(message)
                if data["protocol"] in self._protocols.keys():
                    self._protocols[data["protocol"]](c_socket, **data["data"])
                else:
                    print(
                        f"Recieved invalid/unregistered protocol type: {data['protocol']}"
                    )
        except (ConnectionAbortedError, ConnectionResetError, TimeoutError) as e:
            print(
                f"Connection from {c_address[0]}:{c_address[1]} was reset."
            )
            c_socket.close()
            del self.clients[c_address]
            self.on_disconnection(c_socket)

    def broadcast(self, protocol: str, data: dict = None, exclude: list = None):
        for c_socket in self.clients.values():
            if exclude is None or c_socket not in exclude:
                try:
                    self.send(c_socket, protocol, data)
                except (ConnectionAbortedError, ConnectionResetError, TimeoutError) as e:
                    pass

    def send(self, socket: socket.socket, protocol: str, data: dict = None):
        if data is None:
            data = {}
        message = pickle.dumps({
            "protocol": protocol,
            "data": data
        })
        header = bytes(f"{len(message):<{self._header_size}}", "utf-8")
        socket.sendall(header + message)

    def recv_bytes(self, socket: socket.socket, buffer: int) -> bytes:
        message = b""
        while len(message) < buffer:
            message += socket.recv(
                buffer - len(message)
            )
        return message

    def _socket_thread(self):
        self._socket.listen()
        print(f"Listening on {self._address}:{self._port}.")

        while True:
            c_socket, c_address = self._socket.accept()

            c_thread = threading.Thread(
                target=self.threaded_client,
                args=(c_socket, c_address),
                daemon=True
            )
            c_thread.start()

    def connect(self, address: str, port: int):
        self._address = address
        self._port = port

        self._socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self._socket.bind((self._address, self._port))

        self.clients = {}

        socket_thread = threading.Thread(
            target=self._socket_thread,
            daemon=True
        )
        socket_thread.start()

        self.connected = True

    def disconnect(self):
        # TODO: Make this more elegant.
        self._socket.close()
        del self._socket

        self.connected = False
