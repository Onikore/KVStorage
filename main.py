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


# def get():
#     pass
#
#
# def delete():
#     pass

def get_hash(x):
    hash_object = hashlib.sha256(x.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


def set_key(a):
    with open('values.bin', 'rb') as f:
        offset = int.from_bytes(f.read(4), byteorder='big')
        print(offset)
        val = f.read(offset)
        print(val)
    with open('keys.bin', 'wb') as f:
        f.write(a)
        f.write(int.to_bytes(offset, 8, byteorder='big'))


def set_value(b):
    with open('values.bin', 'wb') as f:
        f.write(int.to_bytes(len(b), 4, byteorder='big'))
        f.write(bytes(b, encoding='utf-8'))
        f.close()


# ЗНАЧЕНИЕ -
# 4 БАЙТА ДЛИНЫ ЗНАЧЕНИЯ
# + N БАЙТ ЗНАЧЕНИЯ

def get_values():
    key = get_hash(input())
    value = input()
    # print(value)

    set_value(value)
    set_key(bytes(key, encoding='utf-8'))


get_values()
