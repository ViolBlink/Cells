import numpy as np
import scipy.stats as sc
import matplotlib.pyplot as plt
# import Tlac/src/Square.py

""" Начало считывания данных """

fig1 = plt.figure(figsize=(8, 8),dpi=100)
ax1 = fig1.add_subplot(111)

fig2 = plt.figure(figsize=(8, 8),dpi=100)
ax2 = fig2.add_subplot(111)

# Считываем парамтры
f = open("Parametrs.txt")
f = f.read().split("\n")

Pre_f = f[:7]
f = f[7:]

Arr = []

for line in Pre_f:
    Arr.append(line.split(" ")[2])

a = float(Arr[0])  # Размер диогонали
x_min = float(Arr[1]) # Минимальное значение х для окна
y_min = float(Arr[3]) # Максимальное значение х для окна
x_max = float(Arr[2]) # Минимальное значение y для окна
y_max = float(Arr[4]) # Максимальное значение y для окна

mean = [float(Arr[5]), float(Arr[6])] # Матрица среднего

f1 = f[0].split(" ")
f2 = f[1].split(" ")

Cov = [[float(f1[0]), float(f1[1])], [float(f2[0]), float(f2[1])]] # Матрица ковариации

""" Конец считывания данных """

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

def leng(v1, v2):
    return np.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)

def Normal_Squares_Gen(len: int):

    squares = []
    i = 0

    while (i < len):
        x, y = np.random.multivariate_normal(mean, Cov).T
        v0 = np.array([[x], [y]])
        angle = np.random.rand() * 2 * np.pi

        flag = 1

        for square in squares:
            if leng(v0, square.centre) < 2 * a:
                flag = 0
                break
        
        if (flag == 1):
            ax2.plot(x, y, 'x')
            ax2.axis('equal')

            squares.append(Square(np.array([[x], [y]]), angle))
            i += 1

    return squares

def Cauchy_Squares_Gen(amaunt: int):
    squares = []
    i = 0

    while (i < amaunt):
        x, y = sc.cauchy.rvs(loc=0, scale=1), sc.cauchy.rvs(loc=0, scale=1)
        v0 = np.array([[x], [y]])
        angle = np.random.rand() * 2 * np.pi

        flag = 1

        for square in squares:
            if leng(v0, square.centre) < 2 * a:
                flag = 0
                break
        
        if (flag == 1):
            ax2.plot(x, y, 'x')
            ax2.axis('equal')

            squares.append(Square(np.array([[x], [y]]), angle))
            i += 1

    return squares


squares = Cauchy_Squares_Gen(100)

for sq in squares:
    sq.Print('r', ax1)


plt.show()