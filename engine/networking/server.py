import pickle
import socket
import threading
import time

from engine.application import Application


class Server(Application):
    _header_size = 64
    _protocols = {}

    def __init__(self, address: str, port: str, *args, **kwargs):
        self._address = address
        self._port = port

        self._socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self._socket.bind((self._address, self._port))

        self.clients = {}

        super().__init__(*args, **kwargs)

    def protocol(self, name: str):
        def register_protocol(func):
            self._protocols[name] = func

        return register_protocol

    def threaded_client(self, c_socket, c_address):
        print(f"Accepted new connection from {c_address[0]}:{c_address[1]}.")
        self.clients[c_address] = c_socket

        try:
            while True:
                header_bytes = b""
                while len(header_bytes) < self._header_size:
                    header_bytes += c_socket.recv(
                        self._header_size - len(header_bytes)
                    )
                header = header_bytes.decode("utf-8")
                length = int(header.strip())

                message = b""
                while len(message) < length:
                    message += c_socket.recv(length - len(message))

                data = pickle.loads(message)
                if data["protocol"] in self._protocols.keys():
                    self._protocols[data["protocol"]](**data["data"])
                else:
                    print(
                        f"Recieved invalid protocol type: {data['protocol']}"
                    )
        except (ConnectionAbortedError, ConnectionResetError, TimeoutError) as e:
            print(
                f"Connection from {c_address[0]}:{c_address[1]} was reset."
            )
            c_socket.close()
            del self.clients[c_address]

    def broadcast(self, protocol: str, data: dict):
        for c_socket in self.clients.values():
            self.send(c_socket, protocol, data)

    def send(self, socket, protocol: str, data: dict):
        message = pickle.dumps({
            "protocol": protocol,
            "data": data
        })
        header = bytes(f"{len(message):<{self._header_size}}", "utf-8")
        return self._socket.sendall(header + message)

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
