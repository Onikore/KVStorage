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

    def _check_file_exists(self):
        if not os.path.exists(self.key_file):
            open(self.key_file)
        if not os.path.exists(self.value_file):
            open(self.value_file)

    def _check_file_size(self, file):
        return True if os.path.getsize(file) == 0 else False

    def setup_first_run(self, key, value):
        print(f'zaebic {key} {value}')

    def set_data(self, key, value):
        if self.first_run:
            self.setup_first_run(key, value)

    def get(self, key):
        pass  # сделать позже

    def delete(self, key):
        pass  # сделать позже


storage = Storage('keys.bin', 'values.bin')
storage.set_data(2, 3)
