from pathlib import Path
from unittest import TestCase

from kvstorage.defrag import Defragmentation
from kvstorage.storage import Storage


class TestStorage(TestCase):

    def setUp(self):
        self.keys_bin = 'test_keys.bin'
        self.values_bin = 'test_values.bin'
        self.storage = Storage(self.keys_bin, self.values_bin)

        self.right_key = (self.storage.get_hash('test') +
                          self.storage.to_bytes(0, 8))
        self.right_value = (self.storage.to_bytes(len('storage'), 4) +
                            'storage'.encode())

        self.storage.set_data('test', 'storage')

    def test_1_set_data_key(self):
        with open(self.storage.def_key_file, 'rb') as f:
            data = f.read(72)
        self.assertEqual(data, self.right_key)

    def test_2_set_data_value(self):
        with open(self.storage.def_value_file, 'rb') as f:
            data = f.read(4 + len('storage'))
        self.assertEqual(data, self.right_value)

    def test_3_get(self):
        data = self.storage.get('test')
        self.assertEqual(data, 'значение: storage')

    def test_4_delete_key(self):
        self.storage.delete('test')
        with open(self.storage.def_key_file, 'rb') as f:
            data = f.read()
        self.assertEqual(data, b'')

    def test_5_delete_val(self):
        with open(self.storage.def_value_file, 'rb') as f:
            data = f.read()
        self.assertEqual(data, self.right_value)

    def test_6_defragmentation(self):
        d = Defragmentation(self.keys_bin, self.values_bin)
        d.start()
        with open(self.storage.def_key_file, 'rb') as f:
            data1 = f.read()
        with open(self.storage.def_value_file, 'rb') as f:
            data2 = f.read()
        if data1 == self.right_key and data2 == self.right_value:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def tearDown(self):
        Path(self.keys_bin).unlink()
        Path(self.values_bin).unlink()
