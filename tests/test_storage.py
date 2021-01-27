import json
from pathlib import Path
from unittest import TestCase

from kvstorage.defrag import Defragmentation
from kvstorage.path_manager import PathManager
from kvstorage.storage import Storage


class TestStorage(TestCase):

    def setUp(self):
        self.path_manager = PathManager()

        self.new_key_path = Path(__file__).parent.joinpath('test_key.bin')
        self.new_value_path = Path(__file__).parent.joinpath('test_value.bin')
        self.new_json_path = Path(__file__).parent.joinpath('test_config.json')

        self.path_manager.default_key_path = self.new_key_path
        self.path_manager.default_value_path = self.new_value_path
        self.path_manager.path_config = self.new_json_path
        self.path_manager.prepare()

        self.storage = Storage()

        # TODO В ТЕСТ ПРЕП
        self.right_key = (self.storage.get_hash('test') +
                          self.storage.to_bytes(0, 8))
        self.right_value = (self.storage.to_bytes(len('storage'), 4) +
                            'storage'.encode())

    def test_1_set_data_key(self):
        self.storage.set_data('test', 'storage')
        with open(self.storage.def_key_file, 'rb') as f:
            data = f.read(72)
        self.assertEqual(data, self.right_key)

    def test_2_set_data_value(self):
        with open(self.storage.def_value_file, 'rb') as f:
            data = f.read(4 + len('storage'))
        self.assertEqual(data, self.right_value)

    def test_3_get(self):
        data = self.storage.get('test')
        self.assertEqual(data, 'storage')

    def test_4_delete_key(self):
        self.new_key_path.unlink()
        self.new_value_path.unlink()
        self.storage.set_data('test', 'storage')
        self.storage.delete('test')
        with open(self.storage.def_key_file, 'rb') as f:
            data = f.read()
        self.assertEqual(data, b'')

    def test_5_delete_val(self):
        with open(self.storage.def_value_file, 'rb') as f:
            data = f.read()
        self.assertEqual(data, self.right_value)

    def test_6_defragmentation(self):
        d = Defragmentation(self.storage.def_key_file, self.storage.def_value_file)
        d.prepare()
        d.start()
        with open(self.storage.def_key_file, 'rb') as f:
            data1 = f.read()
        with open(self.storage.def_value_file, 'rb') as f:
            data2 = f.read()
        if data1 == self.right_key and data2 == self.right_value:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_7_add_path(self):
        self.path_manager.add_path('test', str(self.new_key_path),
                                   str(self.new_value_path))
        with open(self.new_json_path, 'r')as f:
            temp = json.load(f)
        # TODO В ТЕСТ ПРЕП
        data = {'key': str(self.new_key_path),
                'value': str(self.new_value_path)}
        self.assertEqual(temp['test'], data)

    def test_8_remove_path(self):
        self.path_manager.del_path('test')
        with open(self.new_json_path, 'r') as f:
            data = json.load(f)
            # TODO В ТЕСТ ПРЕП
        temp = {'default_path': {
            'key': str(self.new_key_path),
            'value': str(self.new_value_path)}}
        self.assertEqual(data, temp)

    def tearDown(self):
        self.new_key_path.unlink()
        self.new_value_path.unlink()
