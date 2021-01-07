import json
from pathlib import Path
from typing import Dict, NoReturn

from kvstorage import errors


class PathManager:
    def __init__(self):
        self.default_key_path = Path(__file__).parent.parent.joinpath('key.bin')
        self.default_value_path = Path(__file__).parent.parent.joinpath('value.bin')
        self.path_config = Path(__file__).parent.parent.joinpath('path_config.json')

    def prepare(self) -> NoReturn:
        if not self.default_key_path.exists():
            self.default_key_path.touch()
        if not self.default_value_path.exists():
            self.default_value_path.touch()
        if not self.path_config.exists():
            self.path_config.touch()

    def add_path(self, place: str, key_path: str, value_path: str) -> NoReturn:
        data: Dict[str, Dict[str, str]] = {
            place: {
                'key': key_path,
                'value': value_path
            }
        }

        if not self.path_config.stat().st_size:
            self.set_defaults()

        with open(self.path_config, 'r') as f:
            temp = json.load(f)
        with open(self.path_config, 'w') as f:
            temp.update(data)
            json.dump(temp, f)

    def del_path(self, place: str) -> NoReturn:
        with open(self.path_config, 'r') as f:
            temp = json.load(f)
        del temp[place]
        with open(self.path_config, 'w') as f:
            json.dump(temp, f)

    def set_defaults(self) -> NoReturn:
        data: Dict[str, Dict[str, str]] = {
            'default_path': {
                'key': str(self.default_key_path),
                'value': str(self.default_value_path)
            }
        }
        with open(self.path_config, 'w') as f:
            json.dump(data, f)

    def select_path(self) -> NoReturn:
        mas = []
        with open(self.path_config, 'r') as f:
            temp = json.load(f)
        print('Доступные хранилища:')
        for i, v in enumerate(temp):
            print(f'{i}: {v}')
            mas.append(v)
        value = int(input("Выберите место хранения файлов: "))
        mas_len = len(mas) - 1

        if value > mas_len:
            raise errors.ListLengthError(mas_len)
        if value < 0:
            raise errors.NegativeLengthError(mas_len)

        return temp[mas[value]]['key'], temp[mas[value]]['value']
