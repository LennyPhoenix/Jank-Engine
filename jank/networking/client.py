import pickle
import socket
import threading
import time
import typing as t

from jank.application import Application


class Client(Application):

    TCP: int = 1
    UDP: int = 2

    _header_size: int = 32
    _udp_buffer: int = 2048
    _address: str = None
    _port: int = None
    _protocols: t.Dict[str, t.Callable[..., t.Any]] = {}

    connected: bool = False
    udp_enabled: bool = False

    def register_protocol(self, func: t.Callable[..., t.Any], name: str = None):
        if name is None:
            name = func.__name__

        self._protocols[name] = func

    def on_connection(self, socket):
        """ Called on successfull connection. """

    def on_disconnection(self, socket):
        """ Called on disconnection. """

    def send(self, protocol: str, data: dict = None, network_protocol: int = TCP):
        if network_protocol != self.TCP and network_protocol != self.UDP:
            raise TypeError("Invalid network_protocol type. Must be TCP or UDP.")  # noqa: E501

        if data is None:
            data = {}
        message = pickle.dumps({
            "protocol": protocol,
            "data": data
        })

        if network_protocol == self.TCP:
            header = bytes(f"{len(message):<{self._header_size}}", "utf-8")
            self._socket_tcp.sendall(header + message)
        else:
            address = (self._address, self._port)
            self._socket_udp.sendto(message, address)

    def recv_bytes_tcp(self, buffer: int) -> bytes:
        message = b""
        while len(message) < buffer:
            message += self._socket_tcp.recv(
                buffer - len(message)
            )
        return message

    def connect(self, address: str, port: int, enable_udp: bool = False):
        self._address = address
        self._port = port

        self._socket_tcp = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        while True:
            try:
                self._socket_tcp.connect((self._address, self._port))
                break
            except TimeoutError:
                print("Server did not respond, retrying.")

        socket_thread_tcp = threading.Thread(
            target=self._socket_thread,
            daemon=True
        )
        socket_thread_tcp.start()

        if enable_udp:
            self._socket_udp = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM
            )
            self._socket_udp.bind(("0.0.0.0", 0))
            _, port = self._socket_udp.getsockname()
            self.send("_assign_udp_port", {"port": port})
            self.send(
                "_assign_udp_port", {"port": port},
                network_protocol=self.UDP
            )

            socket_thread_udp = threading.Thread(
                target=self._socket_thread,
                daemon=True,
                kwargs={"network_protocol": self.UDP}
            )
            socket_thread_udp.start()

        self.connected = True
        self.udp_enabled = enable_udp

        self.on_connection(self._socket_tcp)

    def disconnect(self):
        # TODO: Make this more elegant.
        self._socket_tcp.close()
        del self._socket_tcp
        if self.udp_enabled:
            self._socket_udp.close()
            del self._socket_udp

        self.connected = False
        self.udp_enabled = False

    def _socket_thread(self, network_protocol: int = TCP):
        if network_protocol != self.TCP and network_protocol != self.UDP:
            raise TypeError("Invalid network_protocol type. Must be TCP or UDP.")  # noqa: E501

        try:
            if network_protocol == self.TCP:
                while True:
                    header_bytes = self.recv_bytes_tcp(self._header_size)
                    header = header_bytes.decode("utf-8")
                    length = int(header.strip())

                    message = self.recv_bytes_tcp(length)

                    data = pickle.loads(message)
                    if data["protocol"] in self._protocols.keys():
                        self._protocols[data["protocol"]](**data["data"])
                    else:
                        print(
                            f"Recieved invalid/unregistered protocol type: {data['protocol']}"
                        )
            else:
                while True:
                    message, c_address = self._socket_udp.recvfrom(
                        self._udp_buffer
                    )
                    print(len(message))

                    data = pickle.loads(message)
                    if c_address != self._socket_tcp.getpeername():
                        print(
                            f"Recieved message from unconnected user (not the connected server): {c_address}"
                        )
                    elif data["protocol"] in self._protocols.keys():
                        self._protocols[data["protocol"]](**data["data"])
                    else:
                        print(
                            f"Recieved invalid/unregistered protocol type: {data['protocol']}"
                        )
        except (ConnectionAbortedError, ConnectionResetError, TimeoutError) as e:
            if self.connected:
                print("Disconnected.")
                self.connected = False
                self.udp_enabled = False
                self.on_disconnection(self._socket_tcp)
