import hashlib
from typing import NoReturn


class Storage:
    def __init__(self, key_file: str, value_file: str):
        self.key_file = key_file
        self.value_file = value_file

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

    def _find_key(self, finder: str) -> bool:
        with open(self.key_file, 'rb') as f:
            while True:
                packet = f.read(72)
                key, offset = packet[:64], self.from_bytes(packet[64:])
                if key == self.get_hash(finder):
                    return True
                if key == b'' and offset == 0:
                    return False

    def put(self, key: str, value: str) -> NoReturn:
        if not self._find_key(key):
            with open(self.value_file, 'ab') as f:
                pos = f.tell()
                f.write(self.to_bytes(len(value), 4))
                f.write(value.encode())
            with open(self.key_file, 'ab') as f:
                f.write(self.get_hash(key))
                f.write(self.to_bytes(pos, 8))
        else:
            print('ключ уже существует')

    def get(self, find_key: str) -> str:
        with open(self.key_file, 'rb') as f:
            while True:
                packet = f.read(72)
                key, offset = packet[:64], self.from_bytes(packet[64:])
                if key == self.get_hash(find_key):
                    with open(self.value_file, 'rb') as a:
                        a.seek(offset)
                        length = self.from_bytes(a.read(4))
                        value = a.read(length)
                        return value.decode()
                if key == b'' and offset == 0:
                    print('Ключ не найден')
                    break

    def delete(self, find_key: str) -> NoReturn:
        with open(self.key_file, 'rb+') as f:
            data = f.read()
            f.seek(0)
            while True:
                pos = f.tell()
                packet = f.read(72)
                key, offset = packet[:64], self.from_bytes(packet[64:])
                if key == self.get_hash(find_key):
                    new_data = data[:pos] + data[pos + 72:]
                    f.write(new_data)
                    print("Успешно")
                    break
                if key == b'' and offset == 0:
                    print('ключ не найден')
                    break


stor = Storage('keys.bin', 'values.bin')
stor.put('sas', '123')
print(stor.get('sas'))
stor.delete('sas')
