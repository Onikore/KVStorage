from pathlib import Path
from typing import NoReturn


class Defragmentation:
    def __init__(self, key_file: str, value_file: str):
        self.key_file = key_file
        self.value_file = value_file
        self.data = {}

    @staticmethod
    def to_bytes(value: int, length: int) -> bytes:
        return int.to_bytes(value, length, byteorder='big')

    @staticmethod
    def from_bytes(value: bytes) -> int:
        return int.from_bytes(value, byteorder='big')

    def scan_file(self) -> NoReturn:
        with open(self.key_file, 'rb') as f:
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

    def start(self) -> NoReturn:
        print('Начало дефрагментации')
        self.scan_file()
        key_path = Path(self.key_file)
        key_path.unlink(True)

        val_path = Path(self.value_file)
        val_path.unlink(True)

        temp_key = Path('keys.bin')
        temp_key.touch()
        temp_key.rename(self.key_file)

        temp_val = Path('values.bin')
        temp_val.touch()
        temp_val.rename(self.value_file)

        for i in self.data:
            with open(temp_val, 'ab') as f:
                pos = f.tell()
                f.write(self.to_bytes(len(self.data[i]), 4))
                f.write(self.data[i])

            with open(temp_key, 'ab') as f:
                f.write(i)
                f.write(self.to_bytes(pos, 8))
        print('Дефрагментация завершена')
