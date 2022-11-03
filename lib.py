import numpy as np
import matplotlib.pyplot as plt
import json

""" Считывание параметров   """
with open("Parametres.json") as FileOfParametrs:
    Parametrs = json.load(FileOfParametrs)

# Общие параметры
Gen_Param = Parametrs["GeneralParametrs"]
# Параметры распределения
Normal_Param = Parametrs["Normal"]

a = float(Gen_Param[0]["a"])                                                             # Размер диогонали
x_min = float(Gen_Param[0]["x_min"])                                                     # Минимальное значение х для окна
y_min = float(Gen_Param[0]["y_min"])                                                     # Максимальное значение х для окна
y_max = float(Gen_Param[0]["y_max"])                                                     # Максимальное значение y для окна
x_max = float(Gen_Param[0]["x_max"])                                                     # Минимальное значение y для окна
Nx = Gen_Param[0]["Nx"]                                                                  # Число центров по x
Ny = Gen_Param[0]["Ny"]                                                                  # Число центров по y

mean = [float(Normal_Param[0]["x0"]), float(Normal_Param[0]["y0"])]                      # Матрица среднего

f = Normal_Param[0]["Cov"].split("\n")
f1 = f[0].split(" ")
f2 = f[1].split(" ")

Cov = [[float(f1[0]), float(f1[1])], [float(f2[0]), float(f2[1])]]                      # Матрица ковариации


Field = [[0] * Nx for _ in range(Ny)]                                                   # Поля для заполнения притяжения
Squares = []                                                                            # Массив, в котором хранится центр и угол
IndOfSquares = []                                                                       # Массив, в котором хранятся индексы ячейки

hx = float(x_max - x_min)/Nx
hy = float(y_max - y_min)/Ny

X = np.linspace(x_min, x_max, Nx)
Y = np.linspace(y_min, y_max, Ny)
""" Конец считывания параметров """

def AddCentres(ax):
    """ Функция, которая рисует центры ячеек """
    X = np.linspace(x_min, x_max, Nx)
    Y = np.linspace(y_min, y_max, Ny)

    for x in X:
        for y in Y:
            ax.plot(x, y, 'o', color='b')
    ax.axis('equal')

def Closest(x, y):
    """Функция, находящая ближайшую ячейку для точки (x, y), возвращает центр и индексы ячейки"""

    vx = X[0]
    vy = Y[0]
    ix = 0
    iy = 0

    for fx in X:
        if (np.abs(x - fx) < np.abs(x - vx)):
            vx = fx
            ix += 1

    for fy in Y:
        if (np.abs(y - fy) < np.abs(y - vy)):
            vy = fy
            iy += 1

    return [ix, iy]

def leng(v1, v2):
    """Функция, возвращающая длину разности двух векторов"""
    return np.sqrt((X[v1[0]] - Y[v2[0]]) ** 2 + (X[v1[1]] - Y[v2[1]]) ** 2)

def Norm(v):
    return np.sqrt(v[0][0] ** 2 + v[1][0] ** 2)

def Squares_Gen(len: int, ax):
    """Функция, которая генерирует len квадратов"""
    #   Вроде можно убрать, но надо будет проверить
    i = 1

    while (i <= len):
        x, y = np.random.multivariate_normal(mean, Cov).T
        n = Closest(x, y)
        angle = np.pi/4
        
        if(Field[n[1]][n[0]] == 0):
            flag = 1
            Field[n[1]][n[0]] = i                                                       # В поле, где есть квадрат пишется
                                                                                        # номер квадрата +1

        else: 
            flag = 0
        
        if (flag == 1):
            ax.plot(X[n[0]], Y[n[1]], 'x', color='r')
            ax.axis('equal')

            Squares.append([[n[0], n[1]], angle, 0, []])
            IndOfSquares.append([[n[0]], [n[1]]])
            i += 1

def PaintSquare(ind, angle, col, ax):
    """Функция, которая рисует квадрат с центрм r0, углом поворота angle"""
    Rotate = np.array([[0, 1], 
                    [-1, 0]])

    points = [np.array([[0], [0]])] * 4

    points[0] = np.array([[a*np.cos(angle)], [a*np.sin(angle)]])
    points[1] = Rotate.dot(points[0])
    points[2] = Rotate.dot(points[1])
    points[3] = Rotate.dot(points[2])

    r0 = [[X[ind[0]]], [Y[ind[1]]]]
    for point in points:
        point += r0
    
    for i in range(4):
            x1, y1 = [points[i][0][0], points[(i + 1) % 4][0][0]], [points[i][1][0], points[(i + 1) % 4][1][0]]
            ax.plot(x1, y1, color=col)

def ShowSquare(ax):

    for square in Squares:
        PaintSquare(square[0], square[1], 'r', ax)

def Move(start, direction):
    """Возвращает ближайшую от start точку в направлении, указаным direction"""
    x = start[0][0] + direction[0][0]
    y = start[1][0] + direction[1][0]

    while((x < Nx) and (x >= 0) and (y < Ny) and (y > 0)):
        if((Field[x][y] != 0) and ((np.abs(start[0][0] - x) > 1) or (np.abs(start[1][0] - y) > 1))): 
            return Field[x][y]
        x = x + direction[0][0]
        y = y + direction[1][0]
    return 0

def Displase():
    """Функция, находящая смещение для квадратов"""
    ind = 1
    for i in range(len(Squares)):

        square = Squares[i]
        ind_of_square = IndOfSquares[i]
        # Текущее положение в виде столбца #

        # Пока без проверки на 0 и нахождения минимального #
        Pre_Possible_positions = [Move(ind_of_square, [[0], [1]]), Move(ind_of_square, [[1], [0]]),
        Move(ind_of_square, [[0], [-1]]), Move(ind_of_square, [[-1], [0]])]
        
        Possible_positions = []                                                          # Создаем массив фактических точек для смещения

        for Index_Of_Tile in Pre_Possible_positions:                                     # Заполняем массив
            if(Index_Of_Tile != 0):
                Possible_positions.append(Index_Of_Tile)

        for Index_Of_Tile in Possible_positions:
            if(Index_Of_Tile == Possible_positions[0]):
                square[2] = Index_Of_Tile
                continue
            
            if(leng(square[0], Squares[Index_Of_Tile - 1][0]) < leng(square[0], Squares[square[2] - 1][0])):
                square[2] = Index_Of_Tile
        
        # Squares[square[2]][4].append(ind)
        ind += 1 
    pass
    # Копия массива квадратов
    
    

    pass

def Disp():
    Displase()

    for sq in Squares:
        if(sq[2] != 0):
            dis_x = Squares[sq[2] - 1][0] - sq[0][0][0]
            dis_y = Squares[sq[2] - 1][0][1][0] - sq[0][1][0]

            dis = [[dis_x], [dis_y]]

            n_dis = dis/Norm(dis)

            dis[0][0] = dis[0][0] - n_dis[0][0]
            dis[1][0] = dis[1][0] - n_dis[1][0]

            closest = Closest(dis[0][0], dis[1][0])

            sq[0][0] = X[closest[0]]
            sq[1][0] = Y[closest[1]]
