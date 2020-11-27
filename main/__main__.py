import argparse

from main.storage import Storage


def long_session():
    print('Начало сессии')
    print('===================================')
    while True:
        x = input()
        if x == 'set':
            storage.set_data(input('Введите ключ: '),
                             input('Введите значение: '))
        elif x == 'get':
            storage.get(input('Ключ: '))
        elif x == 'del':
            storage.delete(input('Ключ: '))
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

    long_parser = subparsers.add_parser('long', help='сессия в консоли')
    long_parser.set_defaults(command="long")

    del_parser = subparsers.add_parser('del', help='Удаление значения')
    del_parser.add_argument('key', help='Ключ', type=str)
    del_parser.set_defaults(command="del")
    args = parser.parse_args()

    storage = Storage('keys.bin', 'values.bin')
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
    except KeyError:
        exit("Был введен неверный ключ")
