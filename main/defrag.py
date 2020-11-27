import hashlib
from pathlib import Path


class DefragmentationManager:
    def __init__(self, key_file: str, value_file: str):
        self.key_file = key_file
        self.value_file = value_file
        self.data = {}

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

    def scan_file(self):
        with open(self.key_file, 'rb')as f:
            while True:
                packet = f.read(72)
                key, offset = packet[:64], self.from_bytes(packet[64:])

                if key == b'' and offset == 0:
                    print('Скан закончен')
                    break

                with open(self.value_file, 'rb') as a:
                    a.seek(offset)
                    length = self.from_bytes(a.read(4))
                    value = a.read(length)
                    self.data[key] = value

    def defragmentation(self):
        key_path = Path(self.key_file)
        key_path.unlink(True)

        val_path = Path(self.key_file)
        val_path.unlink(True)

        temp_key = Path('temp_key.bin')
        temp_key.touch()

        temp_val = Path('temp_val.bin')
        temp_val.touch()

        with open(temp_val, 'ab') as f:
            pos = f.tell()
            f.write(self.to_bytes(len(value), 4))
            f.write(value.encode())
        #     TODO ДОДЕЛАТЬ
        with open(temp_key, 'ab') as f:
            f.write(self.get_hash(key))
            f.write(self.to_bytes(pos, 8))


a = DefragmentationManager('keys.bin', 'values.bin')
a.scan_file()
print(a.data)
