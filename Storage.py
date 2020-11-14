import hashlib
import os

class Storage:
    def __init__(self, key_file, value_file):
        self.key_file = key_file
        self.value_file = value_file

    @staticmethod
    def get_hash(x):
        hash_object = hashlib.sha256(x.encode())
        return bytes(hash_object.hexdigest(), encoding='utf-8')

    @staticmethod
    def to_bytes(value, length):
        return int.to_bytes(value, length, byteorder='big')

    @staticmethod
    def from_bytes(value):
        return int.from_bytes(value, byteorder='big')

    def _check_file_size(self):
        return True if os.path.getsize(self.value_file) == 0 else False

    def setup_first_run(self, key, value):
        with open(self.value_file, 'wb') as f:
            f.write(self.to_bytes(len(value), 4))
            f.write(bytes(value, encoding='utf-8'))

        with open(self.key_file, 'wb') as f:
            f.write(self.get_hash(key))
            f.write(self.to_bytes(0, 8))

    def check_state(self, key, value):
        if self._check_file_size():
            self.setup_first_run(key, value)
        else:
            self.set_data(key, value)

    def _check_key_exists(self, key):
        with open(self.key_file, 'rb') as f:
            status = ('OK', 'BAD_KEY')
            while True:
                packet = f.read(72)
                hash_key, offset = packet[:64], self.from_bytes(packet[64:])
                if hash_key == self.get_hash(key):
                    print('Обнаружено совпадение ключей')
                    return status[1]
                if hash_key == b'' and offset == 0:
                    return status[0]

    # TODO НЕПОНЯТНО ПОЧЕМУ ОНО НЕ РАБОТаЕТ ПОЧИНИТЬ
    def set_data(self, key, value):
        if self._check_key_exists(key) == 'OK':
            with open(self.key_file, 'rb') as f:
                f.seek(-72, 2)
                packet = f.read(72)
                offset = self.from_bytes(packet[64:])
            #     тут вроде ок

            with open(self.value_file, 'rb+') as f:
                f.seek(offset)
                length = self.from_bytes(f.read(4))
                f.seek(4 + length)
                pos = f.tell()

                f.write(self.to_bytes(len(value), 4))
                f.write(bytes(value, encoding='utf-8'))

            with open(self.key_file, 'ab') as f:
                f.write(self.get_hash(key))
                f.write(self.to_bytes(pos, 8))
    #             тут все ок

    def get(self, find_key):
        with open(self.key_file, 'rb') as f:
            while True:
                packet = f.read(72)
                key, offset = packet[:64], self.from_bytes(packet[64:])
                if key == self.get_hash(find_key):
                    print(f'ключ нашелся {key}')
                    with open(self.value_file, 'rb') as a:
                        a.seek(offset)
                        length = self.from_bytes(a.read(4))
                        value = a.read(length)
                        print(f'    значение {value}')
                        break
                if key == b'' and offset == 0:
                    print('КЛЮЧА НЕТ')
                    break

    def delete(self, key):
        pass  # сделать позже


storage = Storage('keys.bin', 'values.bin')
storage.check_state('python', 'tasks')
storage.check_state('python1', 'privett')
storage.check_state('python2', 'zdarova')
# storage.get('python')
