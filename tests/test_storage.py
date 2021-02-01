import json
from pathlib import Path
from unittest import TestCase

from kvstorage.defrag import Defragmentation
from kvstorage.path_manager import PathManager
from kvstorage.storage import Storage


class TestStorage(TestCase):

    def setUp(self):
        self.new_key_path = Path(__file__).parent.joinpath('test_key.bin')
        self.new_value_path = Path(__file__).parent.joinpath('test_value.bin')
        self.new_json_path = Path(__file__).parent.joinpath('test_config.json')

        self.storage = Storage(self.new_key_path,
                               self.new_value_path,
                               self.new_json_path)
        self.storage.prepare()

        self.key = self.storage.get_hash('key')
        self.key_offset = self.storage.to_bytes(0, 8)
        self.value_length = self.storage.to_bytes(len('value'), 4)
        self.value = 'value'.encode()

    def test_1_set_data_key(self):
        self.storage.set_data('key', 'value')
        with open(self.storage.def_key_file, 'rb') as f:
            data = f.read(72)
        self.assertEqual(data, self.key + self.key_offset)

    def test_2_set_data_value(self):
        self.storage.set_data('key', 'value')
        with open(self.storage.def_value_file, 'rb') as f:
            data = f.read()
        self.assertEqual(data, self.value_length + self.value)

    def test_3_get(self):
        self.storage.set_data('key', 'value')
        res = self.storage.get('key')
        self.assertEqual(res, 'value')

    def test_4_delete_key(self):
        self.storage.set_data('key', 'value')
        self.storage.delete('key')

        with open(self.storage.def_key_file, 'rb') as f:
            data = f.read()
        self.assertEqual(data, b'')

    def test_5_defragmentation(self):
        self.storage.set_data('key', 'value')
        self.storage.set_data('test', 'test')
        self.storage.set_data('test123', 'test_value')
        self.storage.delete('test')
        self.storage.delete('test123')
        d = Defragmentation(self.storage.def_key_file,
                            self.storage.def_value_file)
        d.start()
        with open(self.storage.def_key_file, 'rb') as f:
            a = f.read()
        self.assertEqual(a, self.key + self.key_offset)

    def test_7_add_path(self):
        path = PathManager()
        path.path_config = self.new_json_path
        path.add_path('test', str(self.new_key_path),
                      str(self.new_value_path))
        with open(path.path_config, 'r')as f:
            temp = json.load(f)
        data = {'key': str(self.new_key_path),
                'value': str(self.new_value_path)}
        self.assertEqual(temp['test'], data)

    def test_8_remove_path(self):
        path = PathManager()
        path.path_config = self.new_json_path
        path.del_path('test')
        with open(path.path_config, 'r') as f:
            data = json.load(f)
        temp = {'default_path': {
            'key': str(self.new_key_path),
            'value': str(self.new_value_path)}}
        self.assertEqual(data, temp)

    def tearDown(self):
        self.new_key_path.unlink()
        self.new_value_path.unlink()
