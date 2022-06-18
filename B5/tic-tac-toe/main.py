def show_field(f):
    print("  0 1 2")
    for row in range(len(f)):
        print(str(row), ' '.join(f[row]))


def make_move(f, user):
    def check_cords(f):
        while True:
            cords = input("Введите координаты: ").split()
            if len(cords) != 2:
                print("Введите 2 координаты: ")
                continue
            if not (cords[0].isdigit() and cords[1].isdigit()):
                print("Введите числовые координаты: ")
                continue
            _x, _y = map(int, cords)
            if not (0 <= _x < 3 and 0 <= _y < 3):
                print("Выход из диапазона!Введите координаты: ")
                continue
            if f[_x][_y] != '-':
                print("Клетка занята!Введите координаты: ")
                continue
            break
        return _x, _y

    x, y = check_cords(f)
    f[x][y] = user
    show_field(f)
    return x, y


def is_victor(f, user):
    f_list = []
    for row in f:
        f_list += row
    win_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    indices = set([i for i, x in enumerate(f_list) if x == user])
    for p in win_positions:
        if len(indices.intersection(set(p))) == 3:
            return True
    return False


def start_game(f):
    count = 0
    show_field(field)
    while True:
        if count % 2 == 0:
            user = 'x'
        else:
            user = 'o'

        if count < 9:
            make_move(field, user)
            count += 1
            if count >= 5 and is_victor(field, user):
                print(f"Выиграл {user}")
                break
        elif count == 9:
            print("Ничья!")
            break


field = [['-'] * 3 for _ in range(3)]
start_game(field)
