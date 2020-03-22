def px_multiply(line, k, key='absolute'):
    """
    Функция изменяет числовые значения пискелов в строке line в k раз
    :param line: исходная строка
    :param k: множитель
    :param key: 'absolute' - абсолютное значение,
                'vw' - преобразовать px в % по ширине,
                'vh' - преобразовать px в % по высоте
    :return: измененная строка
    """
    screen_width = 1366
    screen_height = 768
    tmp_line = line
    l = len(tmp_line)
    values = []
    i = 0
    while i < l:
        s_int = ''
        a = tmp_line[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i < l:
                a = tmp_line[i]
            else:
                break
        i += 1
        if s_int != '':
            if i < l and tmp_line[i-1:i+1] == 'px':
                if key == 'absolute':
                    value = str(round(int(s_int)*k, 2))
                    line = line.replace(s_int, value)
                elif key == 'vw':
                    value = str(round(int(s_int)/screen_width, 3)) + 'vw'
                    line = line.replace(f'{s_int}px', value)
                elif key == 'vh':
                    value = str(round(int(s_int)/screen_height, 3)) + 'vh'
                    line = line.replace(f'{s_int}px', value)
    return line


def save_replaces(filename, *args):
    """
    Функция записывает в файл, какие свойства необходимо изменить по ширине, высоте или не изменять
    1-я строка - свойства, изменяемые по ширине
    2-я стркоа - свойства, изменяемые по высоте
    3-строка - неизменяемые свойства
    :param filename: файл для сохранения
    :param args: набор свойств для сохранения
    :return: None
    """
    with open(filename, 'w', encoding='UTF-8') as file:
        for i in args:
            for j in i:
                file.write(j + '&')
            file.write('\n')


def load_replaces(filename):
    """
    Функция считывает из файла, какие свойства необходимо изменить по ширине, высоте или не изменять
    1-я строка - свойства, изменяемые по ширине
    2-я стркоа - свойства, изменяемые по высоте
    3-строка - неизменяемые свойства
    :param filename: считываемый файл
    :return: w_r, h_r, n_r - свойства, необходимые изменить по ширине, высоте или не изменять соответственно
    """
    with open(filename, 'r', encoding='UTF-8') as file:
        w_r = set(file.readline().strip().split('&'))
        h_r = set(file.readline().strip().split('&'))
        n_r = set(file.readline().strip().split('&'))
    return w_r, h_r, n_r


if __name__ == '__main__':
    _input = 'small_resolution.css'
    _output = '4k.css'
    _output_rel = 'rel.css'
    _replaces_file = 'replaces.txt'
    width_new = 3840
    height_new = 2160
    width_old = 1366
    height_old = 768
    k_w = width_new / width_old
    k_h = height_new / height_old
    width_replaces, height_replaces, no_replaces = load_replaces(_replaces_file)
    with open(_output, 'w', encoding='UTF-8') as fout:
        with open(_input, 'r', encoding='UTF-8') as file:
            for line in file.readlines():
                if ':' in line:
                    header = line.split(':')[0].lstrip()
                    if header not in width_replaces and header not in height_replaces and \
                       header not in no_replaces:
                        print(header)
                        choice = input('Введите w для изменения ширины, y для изменения высоты,'
                                       'n - если не хотите изменять')
                        while choice not in 'whn':
                            choice = input('Введите w для изменения ширины, h для изменения высоты,'
                                           'n - если не хотите изменять')
                        if choice == 'w':
                            width_replaces.add(header)
                            new_line = px_multiply(line, k_w)
                        elif choice == 'h':
                            height_replaces.add(header)
                            new_line = px_multiply(line, k_h)
                        elif choice == 'n':
                            no_replaces.add(header)
                            new_line = line

                    else:
                        if header in width_replaces:
                            new_line = px_multiply(line, k_w)
                        elif header in height_replaces:
                            new_line = px_multiply(line, k_h)
                        else:
                            new_line = line

                else:
                    new_line = line
                fout.write(new_line)

    # save_replaces(_replaces_file, width_replaces, height_replaces, no_replaces)





