import numpy as np
import matplotlib.pyplot as plt
import json

# Считываем парамтры
with open("Parametres.json") as q:
    f = json.load(q)

f = f["GeneralParametrs"]

a = float(f[0]["a"])  # Размер диогонали
x_min = float(f[0]["x_min"]) # Минимальное значение х для окна
y_min = float(f[0]["y_min"]) # Максимальное значение х для окна
y_max = float(f[0]["y_max"]) # Максимальное значение y для окна
x_max = float(f[0]["x_max"]) # Минимальное значение y для окна
Nx = f[0]["Nx"] # Число центров по x
Ny = f[0]["Ny"] # Число центров по y

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

    vx = X[0]
    vy = Y[0]

    for fx in X:
        if (np.abs(x - fx) < np.abs(x - vx)):
            vx = fx

    for fy in Y:
        if (np.abs(y - fy) < np.abs(y - vy)):
            vy = fy

    return np.array([[vx], [vy]])

def leng(v1, v2):
    return np.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)

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

    def Print(self, col, ax):
        for i in range(4):
            x1, y1 = [self.points[i][0][0], self.points[(i + 1) % 4][0][0]], [self.points[i][1][0], self.points[(i + 1) % 4][1][0]]
            ax.plot(x1, y1, color=col)
        pass