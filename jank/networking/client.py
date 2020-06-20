import pickle
import socket
import threading
import time

from jank.application import Application


class Client(Application):
    _header_size = 64
    _protocols = {}

    def __init__(self, address: str, port: int, *args, **kwargs):
        self._address = address
        self._port = port

        self._socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

        super().__init__(*args, **kwargs)

    def protocol(self, name: str):
        def register_protocol(func):
            self._protocols[name] = func

        return register_protocol

    def _socket_thread(self):
        try:
            while True:
                header_bytes = self.recvall(self._header_size)
                header = header_bytes.decode("utf-8")
                length = int(header.strip())

                message = self.recvall(length)

                data = pickle.loads(message)
                if data["protocol"] in self._protocols.keys():
                    self._protocols[data["protocol"]](**data["data"])
                else:
                    print(
                        f"Recieved invalid/unregistered protocol type: {data['protocol']}"
                    )
        except (ConnectionAbortedError, ConnectionResetError, TimeoutError) as e:
            print("Disconnected.")

    def send(self, protocol: str, data: dict):
        message = pickle.dumps({
            "protocol": protocol,
            "data": data
        })
        header = bytes(f"{len(message):<{self._header_size}}", "utf-8")
        return self._socket.sendall(header + message)

    def recvall(self, buffer: int):
        message = b""
        while len(message) < buffer:
            message += self._socket.recv(
                buffer - len(message)
            )
        return message

    def run(self):
        # TODO: Make this Non-Blocking.
        while True:
            try:
                self._socket.connect((self._address. self._port))
                break
            except TimeoutError:
                print("Server did not respond, retrying.")

        socket_thread = threading.Thread(
            target=self._socket_thread,
            daemon=True
        )
        socket_thread.start()

        super().run()
