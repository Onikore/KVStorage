﻿## Локальное хранилище типа Ключ\Значение
***

#### Запуск программы:

    python -m main <команда>
    # Если Вы хотите вывести справку используйте python -m main -h

____

__Добавление данных в хранилище__

    python -m main set <ключ> <значение>
    Добавление пары <ключ, значение> в хранилище данных
    работает так же как обновление значения по ключу

____

__Удаление данных из хранилища__

    python -m main del <ключ>
    Удаление ячейки из вашего хранилища
    *Будьте осторожны когда будете выполнять операцию
    **вы можете потерять важные данные
    
____

__Просмотр данных хранилища__

    python -m main get <ключ>
    Получение значения ключа из хранилища

____

__Режим долгой сессии__
    
    python -m main long
    запуск продолжительной сессии в консоли
    
____

### Автор:
##### Гришин Дмитрий
