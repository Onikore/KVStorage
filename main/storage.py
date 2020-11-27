import hashlib
from pathlib import Path
from typing import NoReturn, Union


class Storage:
    def __init__(self, key_file: str, value_file: str):
        self.key_file = key_file
        self.value_file = value_file
        self._check_file_exists()

    def _check_file_exists(self) -> NoReturn:
        key = Path(self.key_file)
        value = Path(self.value_file)
        if not key.exists():
            key.touch()
        if not value.exists():
            value.touch()

    @staticmethod
    def get_hash(x: str) -> bytes:
        hash_object = hashlib.sha256(x.encode())
        return hash_object.hexdigest().encode()

    @staticmethod
    def to_bytes(value: int, length: int) -> bytes:
        return int.to_bytes(value, length, byteorder='big')

    @staticmethod
    def from_bytes(value: bytes) -> int:
        return int.from_bytes(value, byteorder='big')

    def _find_key(self, finder: str) -> Union[bool, int]:
        with open(self.key_file, 'rb') as f:
            while True:
                packet = f.read(72)
                key, offset = packet[:64], self.from_bytes(packet[64:])
                if key == self.get_hash(finder):
                    return offset
                if key == b'' and offset == 0:
                    return False

    def set_data(self, key: str, value: str) -> NoReturn:
        result = self._find_key(key)
        if result is False:
            with open(self.value_file, 'ab') as f:
                pos = f.tell()
                f.write(self.to_bytes(len(value), 4))
                f.write(value.encode())
            with open(self.key_file, 'ab') as f:
                f.write(self.get_hash(key))
                f.write(self.to_bytes(pos, 8))
        else:
            self.delete(key)
            with open(self.value_file, 'rb+') as f:
                f.seek(result)
                pos = f.tell()
                length = f.read(4)
                if len(value) < self.from_bytes(length):
                    f.seek(-4, 1)
                    f.write(self.to_bytes(len(value), 4))
                    f.write(value.encode())
                else:
                    with open(self.value_file, 'ab') as a:
                        pos = a.tell()
                        a.write(self.to_bytes(len(value), 4))
                        a.write(value.encode())
            with open(self.key_file, 'ab') as f:
                f.write(self.get_hash(key))
                f.write(self.to_bytes(pos, 8))

    def get(self, find_key: str) -> NoReturn:
        with open(self.key_file, 'rb') as f:
            while True:
                packet = f.read(72)
                key, offset = packet[:64], self.from_bytes(packet[64:])
                if key == self.get_hash(find_key):
                    with open(self.value_file, 'rb') as a:
                        a.seek(offset)
                        length = self.from_bytes(a.read(4))
                        value = a.read(length)
                        print(f'значение: {value.decode()}')
                        break
                if key == b'' and offset == 0:
                    print('Ключ не найден')
                    break

    def delete(self, find_key: str) -> NoReturn:
        new_data = None
        with open(self.key_file, 'rb+') as f:
            data = f.read()
            f.seek(0)
            while True:
                start = f.tell()
                packet = f.read(72)
                end = f.tell()
                key, offset = packet[:64], self.from_bytes(packet[64:])
                if key == self.get_hash(find_key):
                    new_data = data[:start] + data[end:]
                    break
                if key == b'' and offset == 0:
                    print('ключ не найден')
                    break
        if new_data is not None:
            p = Path(self.key_file)
            p.unlink(True)
            temp = Path('temp.bin')
            temp.touch()
            temp.write_bytes(new_data)
            temp.rename(self.key_file)
