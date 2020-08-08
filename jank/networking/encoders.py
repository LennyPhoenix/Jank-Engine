import json
import pickle


class Encoder:
    @staticmethod
    def encode(data: dict) -> bytes:
        return b""

    @staticmethod
    def decode(data: bytes) -> dict:
        return {}


class PickleEncoder(Encoder):
    """ Warning, this is extremely insecure.
    It is recommended to write your own encoder or use the JsonEncoder.
    """
    @staticmethod
    def encode(data: dict) -> bytes:
        return pickle.dumps(data)

    @staticmethod
    def decode(data: bytes) -> dict:
        return pickle.loads(data)


class JsonEncoder(Encoder):
    @staticmethod
    def encode(data: dict) -> bytes:
        return json.dumps(data).encode("utf-8")

    @staticmethod
    def decode(data: bytes) -> dict:
        return json.loads(data.decode("utf-8"))
