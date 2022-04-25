from random import randint
import time

if __name__ == '__main__':
    pass

class Dot:
    # Координаты точки
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Сравнение двух объектов(точек)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Вывод координат в консоль
    def __repr__(self):
        return f"{self.x}, {self.y}"


# Определяем классы исключений

#Родительский класс для исключений
class BoardException(Exception):
    pass

#Задается исключение при попытке игрока выстрелить за доску
class BoardOutExeption(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

#Задается исключение для "забывчивых" игроков
class BoardUsedExeption(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"

#Исключение для размещения кораблей
class BoardWrongShipException(BoardException):
    pass

#Определяем класс корабля с параметрами: длина, точка носа корабля, ориентация  и кол-во жизни
class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    #Создаем пустой массив для кораблей, в которые попали. Проходим по всей длине корабля и записываем точки
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    #метод для проверки попадания в корабль
    def shooten(self, shot):
        return shot in self.dots

#Создается класс игрового поля
class Board():
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        #Количество пораженных кораблей будет хранится в данной переменной count (изначально равняется нулю)
        self.count = 0

        #Сетка для игрового поля
        self.field = [[" "] * size for _ in range(size)]

        #Список для занятых точек
        self.busy = []

        #Список кораблей (изначально пустой)
        self.ships = []

    #Метод добавления корабля
    def add_ship(self, ship):
        #В цикле проверим все точки корабля на то, чтобы они не выходили за игровое поле и не были заняты
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        #В цикле проходим по всем точкам корабля, обозначаем символом и заносим в список занятых точек
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        #Добавляем корабль в список кораблей и обводим корабль по контуру
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        #Список всех точек вокруг которой находится указатель. (0, 0) - текущая точка.
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        #Каждая точка корабля проходит через список near и исходная точка сдвигается на (dx, dy), проходя все точки, которые находятся возле корабля
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)


    #Вывод корабля на доску
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        #Если нужно скрывать символы на поле, то заменяем символы корабля на пустое поле
        if self.hid:
            res = res.replace("■", " ")
        return res

    #Проверяем, находится ли точка за пределами доски: координаты не должны быть в пределах от 0
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))


    def shot(self, d):
        #Если точка выходит за границы поля, то выбрасывается исключение
        if self.out(d):
            raise BoardOutExeption
        #Если точка занята, то выбрасывается исключение
        if d in self.busy:
            raise BoardUsedExeption
        #Если точка не была занята, то добавляем в список занятых точек
        self.busy.append(d)

        #Для каждого корабля в списке кораблей проверяем попадание точки. Если точка совпадает, то отнимаем жизнь и обозначаем символом X
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                #Если жизнь корабля равняется нулю, то добавляем в счет +1 убитый корабль
                if ship.lives == 0:
                    self.count += 1
                    #Контур корабля будет обозначен точками
                    self.contour(ship, verb=True)
                    print("Убит!")
                    #Возвращаем False, чтобы не делать дальше ход
                    return False
                else:
                    print("Ранен!")
                    # Возвращаем True, чтобы сделать еще ход
                    return True

        #Если корабль не был поражен, то выводим символ "." и сообщение
        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    # Перед началом игры нужно очистить список занятых кораблей, так как ранее в переменной хранились рандомно расставленные корабли,
    # а в течение игры будут храниться  точки, куда стреляет игрок
    def begin(self):
        self.busy = []

    #Сравниваем количество подбитых кораблей и кораблей на поле
    def defeat(self):
        return self.count == len(self.ships)

#Определим родительский класс игрока
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    #данный меттод должен быть у потомков класса
    def ask(self):
        raise NotImplementedError()

    #Метод в бесконечном цикле спрашивает пользователя точку для выстрела и стреляет
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

#Определим класс компьютера
class AI(Player):
    def ask(self):
        #Генерируем две точки от 0 до 5
        d = Dot(randint(0, 5), randint(0, 5))
        time.sleep(5)
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        time.sleep(2)
        return d

#Определяем класс пользователя
class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            #Проверяем, чтобы было введено только 2 координаты
            if len(cords) != 2:
                print("Введите только 2 координаты!")
                continue

            x, y = cords

            #Проверяем, что введенные координаты являются числами
            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue

            x, y = int(x), int(y)

            #Пользователю показывается точка с 1, а индексация начнается с нуля
            return Dot(x - 1, y - 1)

#Создаем класс игры и генерации досок
class Game:
    def __init__(self, size=6):
        #Список с длинами кораблей
        self.lens = [3, 2, 2, 1, 1, 1, 1]
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        #Создаем двух игроков
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    #Генерируем случайную доску
    # Пока доска пустая, пытаемся создать ее в цикле
    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def try_board(self):
        #Создаем доску
        board = Board(size=self.size)
        #Попытки, изначально установлено 0
        attempts = 0
        #Для всей длины корабля в цикле пытаемся поставить карабль, если попыток более 2000 - возвращаем None
        for l in self.lens:
            while True:
                attempts += 1
                if attempts > 20:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                #Если корабль установлен, то прекращаем цикл, если не установлен, то продалжаем цикл
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        #Подготавливаем доску к игре (очищается список из занятых кораблей)
        board.begin()
        return board

    #Приветствие пользователя и формат ввода
    def greet(self):
        print("-" * 25)
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-" * 25)
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    #Метод для отображения досок
    def print_boards(self):
        print("-" * 25)
        print("Доска пользователя:")
        print(self.us.board)
        print("-" * 25)
        print("Доска компьютера:")
        print(self.ai.board)

    #Создаем игровой цикл
    def loop(self):
        #Номер хода
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            #Если нужно повторить ход, то уменьшаем переменную на единицу
            if repeat:
                num -= 1

            #Если количество пораженных кораблей равно количеству кораблей на доске, то пользователь выиграл
            if self.ai.board.defeat():
                self.print_boards()
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.defeat():
                self.print_boards()
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    #Метод для запуска игры
    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()
