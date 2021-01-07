from pathlib import Path
from typing import NoReturn

from kvstorage.consts import KEY_BLOCK_LEN, \
    KEY_LEN, VALUE_OFFSET_LEN, KEY_OFFSET_LEN


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

    def prepare(self) -> NoReturn:
        with open(self.key_file, 'rb') as f:
            while True:
                packet = f.read(KEY_BLOCK_LEN)
                key = packet[:KEY_LEN]
                offset = self.from_bytes(packet[KEY_LEN:])
                if key == b'':
                    print('Скан закончен')
                    break

                with open(self.value_file, 'rb') as a:
                    a.seek(offset)
                    length = self.from_bytes(a.read(VALUE_OFFSET_LEN))
                    value = a.read(length)
                    self.data[key] = value

    def start(self) -> NoReturn:
        print('Начало дефрагментации')
        self.prepare()
        key_path = Path(self.key_file)
        key_path.unlink(True)

        val_path = Path(self.value_file)
        val_path.unlink(True)

        temp_key = Path(self.key_file)
        temp_key.touch()
        temp_key.rename(self.key_file)

        temp_val = Path(self.value_file)
        temp_val.touch()
        temp_val.rename(self.value_file)

        for i in self.data:
            with open(temp_val, 'ab') as f:
                pos = f.tell()
                f.write(self.to_bytes(len(self.data[i]), VALUE_OFFSET_LEN))
                f.write(self.data[i])

            with open(temp_key, 'ab') as f:
                f.write(i)
                f.write(self.to_bytes(pos, KEY_OFFSET_LEN))
        print('Дефрагментация завершена')
