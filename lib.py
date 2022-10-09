import numpy as np
import matplotlib.pyplot as plt
import json

fig = plt.figure(figsize=(8, 8),dpi=100)
ax = fig.add_subplot(111)

# Считываем парамтры
with open("Parametres.json") as q:
    f = json.load(q)

file_Gen = f["GeneralParametrs"]
file_Normal = f["Normal"]

a = float(file_Gen[0]["a"])  # Размер диогонали
x_min = float(file_Gen[0]["x_min"]) # Минимальное значение х для окна
y_min = float(file_Gen[0]["y_min"]) # Максимальное значение х для окна
y_max = float(file_Gen[0]["y_max"]) # Максимальное значение y для окна
x_max = float(file_Gen[0]["x_max"]) # Минимальное значение y для окна
Nx = file_Gen[0]["Nx"] # Число центров по x
Ny = file_Gen[0]["Ny"] # Число центров по y

mean = [float(file_Normal[0]["x0"]), float(file_Normal[0]["y0"])] # Матрица среднего

f = file_Normal[0]["Cov"].split("\n")
f1 = f[0].split(" ")
f2 = f[1].split(" ")

Cov = [[float(f1[0]), float(f1[1])], [float(f2[0]), float(f2[1])]] # Матрица ковариации


Field = [[0] * Nx for _ in range(Ny)] # Поля для заполнения притяжения

hx = float(x_max - x_min)/Nx
hy = float(y_max - y_min)/Ny

X = np.linspace(x_min, x_max, Nx)
Y = np.linspace(y_min, y_max, Ny)

def AddCentres(ax):

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


    return np.array([[vx], [vy]]), [ix, iy]
    
def leng(v1, v2):
    """Функция, возвращающая длину между двумя векторами"""
    return np.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)

def Grav():
    """"Функция, которая по заданому полю расположений возвращает графф смещений"""
    fil = [[0] * Nx for _ in range(Ny)]
    
    for x in range(Nx):
        for y in range(Ny):
            pos = [x, y] # Рассматриваеммая точка
            Position = [-1, -1]


            if(Field[x][y]):

                Pre_Possible_positions = [Move([x, y], [1, 0]), Move([x, y], [0, 1]), # Смещаемся в четыре стороны и создаем массив
                Move([x, y], [-1, 0]), Move([x, y], [0, -1])]                         # в котором хранятся возможные точки

                Possible_positions = []                                                             # Создаем массив фактических точек для смещения

                for Tile in Pre_Possible_positions:                                                    # Заполняем массив
                    if(Tile != [-1, -1]):
                        Possible_positions.append(Tile)
                                                                                                    # Находим ближайшую точку для смещения
                l = 0

                for Tile in Possible_positions:
                    if(Tile == Possible_positions[0]):
                        l = leng(pos, Tile)
                        Position = Tile
                    else:
                        if(leng(pos, Tile) < l):
                            l = leng(pos, Tile)
                            Position = Tile

            fil[x][y] = Position                                                                    # Создаем графф смещений
    return fil

def Move(start, direction):
    """Возвращает ближайшую от start точку в направлении, указаным direction"""
    x = start[0] + direction[0]
    y = start[1] + direction[1]

    while((x < Nx) and (x >= 0) and (y < Ny) and (y > 0)):
        if((Field[x][y] != 0) and (np.abs(start[0] - x) > 1) and (np.abs(start[0] - y) > 1)): 
            return [x, y]
        x = x + direction[0]
        y = y + direction[1]
    return [-1, -1]

def GTD(Graph, pos):
    """Обходит граф"""
    
    if(pos == Graph[Graph[pos[0], pos[1]][0], Graph[pos[0], pos[1]][1]]):
        return 

    else:
        GTD(Graph, Graph[pos[0], pos[1]])

def Squares_Gen(len: int):

    squares = []
    i = 0

    while (i < len):
        x, y = np.random.multivariate_normal(mean, Cov).T
        v0, n = Closest(x, y)
        # v0 = [[x], [y]]
        angle = np.pi/4
        
        if(Field[n[1]][n[0]] == 0):
            flag = 1
            Field[n[1]][n[0]] = 1

        else: 
            flag = 0
        
        if (flag == 1):
            ax.plot(v0[0][0], v0[1][0], 'x', color='r')
            ax.axis('equal')

            squares.append(Square(np.array([[v0[0][0]], [v0[1][0]]]), angle))
            i += 1

    return squares
class Square:
    def __init__(self, v0, angle: float) -> None:
        Rotate = np.array([[0, 1], 
                            [-1, 0]])
        self.points = [np.array([[0], [0]])] * 4

        self.points[0] = np.array([[a*np.cos(angle)], [a*np.sin(angle)]])

        self.points[1] = Rotate.dot(self.points[0])
        self.points[2] = Rotate.dot(self.points[1])
        self.points[3] = Rotate.dot(self.points[2])

        self.centre = v0

        for v in self.points:
            v += v0
        pass

    def Print(self, col, axe):
        for i in range(4):
            x1, y1 = [self.points[i][0][0], self.points[(i + 1) % 4][0][0]], [self.points[i][1][0], self.points[(i + 1) % 4][1][0]]
            axe.plot(x1, y1, color=col)
        pass