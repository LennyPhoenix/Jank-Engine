import pickle
import socket
import threading
import typing as t

from jank.application import Application


class Server(Application):
    TCP: int = 1
    UDP: int = 2

    _header_size: int = 32
    _udp_buffer: int = 2048
    _address: str = None
    _port: int = None
    _protocols: t.Dict[str, t.Callable[..., t.Any]] = {}
    _udp_addresses: t.Dict[socket.socket, t.Tuple[str, int]] = {}

    clients: t.Dict[t.Tuple[str, int], socket.socket] = {}
    connected: bool = False
    udp_enabled: bool = False

    def __init__(self, *args, **kwargs):
        self.register_protocol(self._assign_udp_port)
        super().__init__(*args, **kwargs)

    def register_protocol(self, func: t.Callable[..., t.Any], name: str = None):
        if name is None:
            name = func.__name__

        self._protocols[name] = func

        return func

    def on_connection(self, socket: socket.socket):
        """ Called on new connection. """

    def on_disconnection(self, socket: socket.socket):
        """ Called on socket disconnection. """

    def threaded_client_tcp(self, c_socket: socket.socket, c_address: t.Tuple[str, int]):
        print(f"Accepted new connection from {c_address[0]}:{c_address[1]}.")
        self.clients[c_address] = c_socket

        self.on_connection(c_socket)

        try:
            while True:
                header_bytes = self.recv_bytes_tcp(c_socket, self._header_size)
                header = header_bytes.decode("utf-8")
                length = int(header.strip())

                message = self.recv_bytes_tcp(c_socket, length)

                data = pickle.loads(message)
                if data["protocol"] in self._protocols.keys():
                    self._protocols[data["protocol"]](
                        c_socket, **data["data"]
                    )
                else:
                    print(f"Recieved invalid/unregistered protocol type: {data['protocol']}")
        except ConnectionResetError as e:
            print(f"Connection from {c_address[0]}:{c_address[1]} was reset:\n    {e}")
            del self.clients[c_address]
            if c_socket in self._udp_addresses.keys():
                del self._udp_addresses[c_socket]
            c_socket.close()
            self.on_disconnection(c_socket)
        except OSError as e:
            if e.errno == 10038:
                print(f"""
Client socket closed, aborting:
    {e}

""")
            else:
                print(e)

    def broadcast(
        self,
        protocol: str,
        data: dict = None,
        exclude: t.List[socket.socket] = None,
        network_protocol: int = TCP
    ):
        if network_protocol != self.TCP and network_protocol != self.UDP:
            raise TypeError("Invalid network_protocol type. Must be TCP or UDP.")

        for c_socket in self.clients.copy().values():
            if exclude is None or c_socket not in exclude:
                try:
                    self.send(
                        c_socket,
                        protocol, data,
                        network_protocol=network_protocol
                    )
                except ConnectionResetError:
                    continue

    def send(
        self,
        socket: socket.socket,
        protocol: str,
        data: dict = None,
        network_protocol: int = TCP
    ):
        if network_protocol != self.TCP and network_protocol != self.UDP:
            raise TypeError("Invalid network_protocol type. Must be TCP or UDP.")

        if data is None:
            data = {}
        message = pickle.dumps({
            "protocol": protocol,
            "data": data
        })

        if network_protocol == self.TCP:
            header = bytes(f"{len(message):<{self._header_size}}", "utf-8")
            socket.sendall(header + message)
        else:
            if socket not in self._udp_addresses.keys():
                print("Cannot send packet to user as UDP port has not yet been assigned.")
                return
            address = self._udp_addresses[socket]
            self._socket_udp.sendto(message, address)

    def recv_bytes_tcp(self, socket: socket.socket, buffer: int) -> bytes:
        message = b""
        while len(message) < buffer:
            message += socket.recv(buffer - len(message))
        return message

    def connect(self, address: str, port: int, enable_udp: bool = False):
        self._address = address
        self._port = port

        self.clients = {}
        self.connected = True
        self.udp_enabled = enable_udp

        self._socket_tcp = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self._socket_tcp.bind((self._address, self._port))

        socket_thread_tcp = threading.Thread(
            target=self._socket_thread,
            daemon=True
        )
        socket_thread_tcp.start()

        if self.udp_enabled:
            self._socket_udp = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM
            )
            self._socket_udp.bind(self._socket_tcp.getsockname())

            socket_thread_udp = threading.Thread(
                target=self._socket_thread,
                daemon=True,
                kwargs={"network_protocol": self.UDP}
            )
            socket_thread_udp.start()

    def disconnect(self):
        self.connected = False
        self.udp_enabled = False

        self._socket_tcp.close()
        if self.udp_enabled:
            self._socket_udp.close()

        for client_socket in self.clients.values():
            client_socket.close()

        self.clients = {}
        self._udp_addresses = {}

    def _socket_thread(self, network_protocol: int = TCP):
        if network_protocol != self.TCP and network_protocol != self.UDP:
            raise TypeError("Invalid network_protocol type. Must be TCP or UDP.")  # noqa: E501

        if network_protocol == self.TCP:
            self._socket_tcp.listen()
            print(f"Listening on {self._address}:{self._port}.")

            try:
                while True:
                    c_socket, c_address = self._socket_tcp.accept()

                    c_thread = threading.Thread(
                        target=self.threaded_client_tcp,
                        args=(c_socket, c_address),
                        daemon=True
                    )
                    c_thread.start()
            except OSError as e:
                if e.errno == 10038:
                    print(f"""
Main socket closed, aborting:
    {e}

""")
                else:
                    print(e)
        else:
            while True:
                try:
                    message, c_address = self._socket_udp.recvfrom(self._udp_buffer)
                except ConnectionResetError as e:
                    print(f"""
Failed to send packet to client:
    {e}
    Make sure that UDP is enabled on the server.

""")
                    continue

                if not self.connected:
                    print("No longer connected. Ending UDP thread.")
                    break

                data = pickle.loads(message)
                if c_address not in self._udp_addresses.values():
                    print(f"Recieved message from unconnected user: {c_address}")
                elif data["protocol"] in self._protocols.keys():
                    socket_list = list(self._udp_addresses.keys())
                    address_list = list(self._udp_addresses.values())
                    socket = socket_list[address_list.index(c_address)]
                    self._protocols[data["protocol"]](
                        socket, **data["data"]
                    )
                else:
                    print(f"Recieved invalid/unregistered protocol type: {data['protocol']}")

    def _assign_udp_port(self, socket: socket.socket, port: int):
        address_list = list(self.clients.keys())
        socket_list = list(self.clients.values())
        address = (
            address_list[socket_list.index(socket)][0],
            port
        )
        self._udp_addresses[socket] = address
