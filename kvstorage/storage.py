import hashlib
from pathlib import Path
from typing import NoReturn, Dict

from kvstorage import errors
from kvstorage.consts import KEY_BLOCK_LEN, \
    KEY_LEN, KEY_OFFSET_LEN, VALUE_OFFSET_LEN
from kvstorage.path_manager import PathManager


class Storage:
    def __init__(self, key_file: str, value_file: str):
        self.pm = PathManager()

        self.new_key_file = Path(key_file)
        self.new_value_file = Path(value_file)

        self.def_key_file = self.pm.default_key_path
        self.def_value_file = self.pm.default_value_path

        self.keys: Dict[bytes, int] = {}

    def prepare(self) -> NoReturn:
        self.pm.prepare()
        self.pm.set_defaults()

    def load(self) -> NoReturn:
        with self.def_key_file.open('rb') as f:
            while True:
                packet = f.read(KEY_BLOCK_LEN)
                key = packet[:KEY_LEN]
                offset = self.from_bytes(packet[KEY_LEN:])
                if key == b'':
                    break

                self.keys[key] = offset

    def defragmentation(self) -> NoReturn:
        from kvstorage.defrag import Defragmentation

        d = Defragmentation(self.def_key_file, self.def_value_file)
        d.start()

    def set_data(self, key: str, value: str) -> NoReturn:
        hashed_key = self.get_hash(key)

        if hashed_key not in self.keys:
            with open(self.def_value_file, 'ab') as f:
                pos = f.tell()
                f.write(self.to_bytes(len(value), VALUE_OFFSET_LEN))
                f.write(value.encode())
            with open(self.def_key_file, 'ab') as f:
                f.write(hashed_key)
                f.write(self.to_bytes(pos, KEY_OFFSET_LEN))

                self.keys[hashed_key] = pos
        else:
            self.delete(key)
            self.set_if_exists(key, value)

    def set_if_exists(self, key: str, value: str):
        hashed_key = self.get_hash(key)
        with open(self.def_value_file, 'rb+') as f:
            f.seek(self.keys[hashed_key])
            pos = f.tell()
            length = f.read(4)
            if len(value) < self.from_bytes(length):
                f.seek(-4, 1)
                f.write(self.to_bytes(len(value), VALUE_OFFSET_LEN))
                f.write(value.encode())
            else:
                f.seek(0, 2)
                pos = f.tell()
                f.write(self.to_bytes(len(value), VALUE_OFFSET_LEN))
                f.write(value.encode())
        with open(self.def_key_file, 'ab') as f:
            f.write(self.get_hash(key))
            f.write(self.to_bytes(pos, KEY_OFFSET_LEN))

        self.keys[hashed_key] = pos

    def get(self, find_key: str) -> NoReturn:
        find_key = self.get_hash(find_key)
        if find_key in self.keys:
            with open(self.def_value_file, 'rb') as f:
                f.seek(self.keys[find_key])
                length = f.read(VALUE_OFFSET_LEN)
                value = f.read(self.from_bytes(length))
                return value.decode()

    def delete(self, find_key: str) -> NoReturn:
        with open(self.def_key_file, 'rb+') as f:
            while True:
                start = f.tell()
                packet = f.read(KEY_BLOCK_LEN)
                key = packet[:KEY_LEN]

                if key == b'':
                    raise errors.KeyNotFoundError

                if key == self.get_hash(find_key):
                    f.seek(-KEY_BLOCK_LEN, 2)
                    end = f.tell()
                    temp = f.read(KEY_BLOCK_LEN)
                    f.seek(start)
                    f.write(temp)
                    f.truncate(end)
                    break

    def get_all(self):
        cases = []
        with self.def_value_file.open('rb') as f:
            while True:
                offset = f.read(VALUE_OFFSET_LEN)

                if offset == b'':
                    [print(x, end=' ') for x in cases]
                    break

                key = f.read(self.from_bytes(offset))
                cases.append(key.decode())

    def select_storage(self):
        res = self.pm.select_path()
        self.def_key_file = res[0]
        self.def_value_file = res[1]
        self.load()

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
