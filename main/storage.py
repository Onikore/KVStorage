import hashlib
from typing import Union, NoReturn


class Storage:
    def __init__(self, key_file: str, value_file: str):
        self.key_file = key_file
        self.value_file = value_file

    @staticmethod
    def get_hash(x: str) -> bytes:
        hash_object = hashlib.sha256(x.encode())
        return hash_object.hexdigest().encode()

    @staticmethod
    def to_bytes(value: Union[str, int], length: int) -> bytes:
        return int.to_bytes(value, length, byteorder='big')

    @staticmethod
    def from_bytes(value: bytes) -> int:
        return int.from_bytes(value, byteorder='big')

    def set_data(self, key: str, value: str) -> NoReturn:
        if not self.get(key):
            with open(self.value_file, 'ab') as f:
                pos = f.tell()
                f.write(self.to_bytes(len(value), 4))
                f.write(value.encode())

            with open(self.key_file, 'ab') as f:
                f.write(self.get_hash(key))
                f.write(self.to_bytes(pos, 8))

    def get(self, find_key: str) -> Union[str, bool]:
        with open(self.key_file, 'rb') as f:
            while True:
                packet = f.read(72)
                key, offset = packet[:64], self.from_bytes(packet[64:])
                if key == self.get_hash(find_key):
                    # print(f'ключ нашелся {key}')
                    with open(self.value_file, 'rb') as a:
                        a.seek(offset)
                        length = self.from_bytes(a.read(4))
                        value = a.read(length)
                        return value.decode()
                if key == b'' and offset == 0:
                    # print('КЛЮЧА НЕТ')
                    return False

    def delete(self, key: str):
        pass  # сделать позже
