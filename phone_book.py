"""
    Создать телефонный справочник с возможностью импорта и экспорта данных в формате .txt.
    Фамилия, имя, отчество, номер телефона - данные, которые должны находиться в файле.
    1. Программа должна выводить данные.
    2. Программа должна сохранять данные в текстовом файле.
    3. Пользователь может ввести одну из характеристик для поиска
        определенной записи(Например имя или фамилию человека).
    4. Использование функций. Ваша программа не должна быть линейной.

    Дополнить телефонный справочник возможностью изменения и удаления данных.
    Пользователь также может ввести имя или фамилию, и Вы должны реализовать
    функционал для изменения и удаления данных.

    Дополнить справочник возможностью копирования данных из одного файла в другой.
    Пользователь вводит номер строки, которую необходимо перенести из одного файла в другой.
"""

# Глобальные переменные
path = "phone_book.txt"  # Путь к файлу с телефонным справочником.
data = {}  # Хранит данные в памяти.
saved = True  # Флаг, показывающий, что данные сохранены в файл

# Формат хранения данных в файле - csv, разделитель ";". Три поля: "ФИО", "телефон", "примечания".


def load():
    """Загружает данные из файла"""
    with open(path, 'r', encoding="utf-8") as data_file:
        read_data = [line.rstrip().split(';') for line in data_file]
        # Если в записи не три поля - считаем ее некорректной и игнорируем.
        # filter не использован для информирования пользователя о пропущенных строках.
        n = 1
        temp_data = []
        for rec in read_data:
            if len(rec) == 3:
                temp_data.append(rec)
            else:
                print(f'Строка № {n} имеет некорректный формат, пропущена.')
            n += 1
    count = [i + 1 for i in range(len(temp_data))]
    global data
    data = dict(zip(count, temp_data))
    print('Данные загружены.')
    global saved
    saved = True


def save():
    """Сохраняет данные в файл"""
    data_to_write = [';'.join(s) + '\n' for s in data.values()]
    with open(path, 'w', encoding='utf-8') as data_file:
        data_file.writelines(data_to_write)
    print('Данные сохранены')
    global saved
    saved = True


def set_filename():
    """Устанавливает имя файла для сохранения/загрузки данных"""
    global path
    path = input('Введите имя файла для хранения данных: ')
    global saved
    saved = False
    print('Имя файла обновлено')


def show_records(sublist):
    """
    Выводит на экран записи из переданного словаря
    :param sublist: словарь с записями для вывода
    """
    for k, v in sublist.items():
        print(f"№ {k}: {v[0]} - {v[1]}  # {v[2]}")


def show_phone_book():
    """Выводит на экран весь справочник"""
    show_records(data)


def find():
    """Ищет записи по вхождению в ФИО, выводит их на экран"""
    str_to_find = input('Введите подстроку для поиска в ФИО: ').lower()
    show_records(dict(filter(lambda item: str_to_find in item[1][0].lower(), data.items())))


def add():
    """Добавляет новую запись в справочник"""
    print('Добавление новой записи')
    fio = input('Введите ФИО: ')
    tel = input('Введите номер телефона: ')
    comment = input('Введите комментарий: ')
    global data
    n = max(data.keys()) + 1
    data[n] = [fio, tel, comment]
    print('Запись добавлена')
    show_records({n: data[n]})
    global saved
    saved = False


def select_record():
    """
    Запрашивает у пользователя номер записи для обработки.
    :return: Номер записи, либо "0" - отмена ввода.
    """
    while True:
        try:
            n = int(input('Введите номер записи для изменения или 0 для отмены: '))
            if n == 0 or n in data:
                return n
            else:
                print('Записи с таким номером нет, попробуйте еще раз')
        except ValueError:
            print('Некорректный ввод, попробуйте еще раз')


def change():
    """Изменяет существующую запись"""
    global data
    n = select_record()
    if n == 0:
        return
    show_records({n: data[n]})
    fio = input('Введите новое ФИО. Пустая строка - оставить без изменений: ')
    tel = input('Введите новый номер телефона. Пустая строка - оставить без изменений: ')
    comment = input('Введите новый комментарий. Пустая строка - оставить без изменений: ')
    if fio == '':
        fio = data[n][0]
    if tel == '':
        tel = data[n][1]
    if comment == '':
        comment = data[n][2]
    data[n] = [fio, tel, comment]
    print('Запись обновлена')
    show_records({n: data[n]})
    global saved
    saved = False


def delete():
    """Удаляет запись из справочника"""
    global data
    n = select_record()
    if n == 0:
        return
    data.pop(n)
    print(f'Запись № {n} удалена')
    global saved
    saved = False


def exit_program():
    if saved:
        print('Выход')
        exit(0)
    print('Данные не сохранены')
    print('"Y" - сохранить и выйти')
    print('"N" - выйти без сохранения')
    print('Любой другой ввод - отмена')
    choice = input('Ваш выбор: ').upper()
    if choice == 'Y':
        save()
        exit(0)
    elif choice == 'N':
        exit(0)
    # Иначе - возвращаемся в меню


def err():
    print('Неверный выбор, повторите ввод.')


def menu():
    while True:
        print()
        print('Выберите пункт меню:')
        print('   1: Загрузить данные из файла')
        print('   2: Сохранить данные в файл')
        print('   3: Изменить имя файла для хранения данных')
        print('   4: Показать справочник')
        print('   5: Поиск по ФИО')
        print('   6: Добавить')
        print('   7: Изменить')
        print('   8: Удалить')
        print('   0: Выход')
        switch = {
            '1': load,
            '2': save,
            '3': set_filename,
            '4': show_phone_book,
            '5': find,
            '6': add,
            '7': change,
            '8': delete,
            '0': exit_program
        }
        switch.get(input(), err)()  # Выбираем метод из словаря и запускаем его.


# Запуск программы
menu()
