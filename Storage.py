import hashlib
import os


# KEYS.BIN

# КЛЮЧ -
# 64 БАЙТА +
# 8 БАЙТ ОТСТУПОВ
#
# VALUES.BIN

# ЗНАЧЕНИЕ -
# 4 БАЙТА ДЛИНЫ ЗНАЧЕНИЯ
# + N БАЙТ ЗНАЧЕНИЯ

class Storage:
    def __init__(self, key_file, value_file):
        self.key_file = key_file
        self.value_file = value_file
        self.first_run = self._check_file_size(self.value_file)

    def get_hash(self, x):
        hash_object = hashlib.sha256(x.encode())
        return hash_object.hexdigest()

    # TODO починить проверку
    def _check_file_exists(self):
        if not os.path.exists(self.key_file):
            open(self.key_file)
        if not os.path.exists(self.value_file):
            open(self.value_file)

    def _check_file_size(self, file):
        return True if os.path.getsize(file) == 0 else False

    def setup_first_run(self, key, value):
        with open(self.value_file, 'wb') as f:
            f.write(int.to_bytes(len(value), 4, byteorder='big'))
            f.write(bytes(value, encoding='utf-8'))

        with open(self.key_file, 'wb') as f:
            f.write(bytes(self.get_hash(key), encoding='utf-8'))
            f.write(int.to_bytes(0, 8, byteorder='big'))

    def set_data(self, key, value):
        if self.first_run:
            self.setup_first_run(key, value)

    def get(self, find_key):
        with open(self.key_file, 'rb') as f:
            while True:
                packet = f.read(72)
                key, offset = packet[:64], int.from_bytes(packet[64:], byteorder='big')
                hash_key = bytes(self.get_hash(find_key), encoding='utf-8')
                if key == hash_key:
                    print(f'ключ нашелся {key}')
                    break
        with open(self.value_file, 'rb') as f:
            f.seek(offset)
            length = int.from_bytes(f.read(4), byteorder='big')
            value = f.read(length)
            print(f'    значение {value}')

    def delete(self, key):
        pass  # сделать позже


storage = Storage('keys.bin', 'values.bin')
# storage.set_data('2', '3')
storage.get('2')
# storage.set_data('asd', 'dsa')
# storage.get('asd')
