import argparse

from kvstorage.path_manager import PathManager
from kvstorage.storage import Storage


def long_session():
    print('''Возможные команды:
    set - Ввод данных в хранилище
    get - Получение данных из хранилища
    del - Удаление данных из хранилища
    all - Получение всех значений из хранилища
    chp - Смена хранилища
    stp - Добавление хранилища
    dlp - Удаление хранилища
    defrag - Дефрагментации хранилища
    exit - Выход из программы\n''')
    print('Начало сессии')
    print('===================================')
    while True:
        x = input()
        if x == 'set':
            storage.set_data(input('Введите ключ: '),
                             input('Введите значение: '))
        elif x == 'get':
            print(storage.get(input('Ключ: ')))
        elif x == 'del':
            storage.delete(input('Ключ: '))
        elif x == 'all':
            storage.get_all()
        elif x == 'chp':
            storage.select_storage()
        elif x == 'stp':
            path_manager.add_path(input('Название места: '),
                                  input('Путь до ключа: '),
                                  input('Путь до значения: '))
        elif x == 'dlp':
            path_manager.del_path(input('Название места: '))
        elif x == 'defrag':
            storage.defragmentation()
        elif x == 'exit':
            print('===================================')
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KV-storage')
    parser.set_defaults(command='zero_args')

    subparsers = parser.add_subparsers()

    set_parser = subparsers.add_parser('set', help='Добавление данных')
    set_parser.add_argument('key', help='Ключ', type=str)
    set_parser.add_argument('value', help='Значение', type=str)
    set_parser.set_defaults(command="set")

    get_parser = subparsers.add_parser('get', help='Получение значения')
    get_parser.add_argument('key', help='Ключ', type=str)
    get_parser.set_defaults(command="get")

    long_parser = subparsers.add_parser('long', help='Долгая сессия')
    long_parser.set_defaults(command="long")

    get_all_parser = subparsers.add_parser('all', help='получение '
                                                       'все значений')
    get_all_parser.set_defaults(command="all")

    defrag_parser = subparsers.add_parser('defrag', help='Дефрагментации '
                                                         'хранилища')
    defrag_parser.set_defaults(command="defrag")

    del_parser = subparsers.add_parser('del', help='Удаление значения')
    del_parser.add_argument('key', help='Ключ', type=str)
    del_parser.set_defaults(command="del")
    args = parser.parse_args()

    storage = Storage('keys.bin', 'values.bin')
    path_manager = PathManager()
    command = args.command
    try:
        if command == 'set':
            storage.set_data(args.key, args.value)
        elif command == 'get':
            storage.get(args.key)
        elif command == 'del':
            storage.delete(args.key)
        elif command == 'long':
            long_session()
        elif command == 'defrag':
            storage.defragmentation()
        elif command == 'all':
            storage.get_all()
    except KeyError:
        exit("Был введен неверный ключ")
