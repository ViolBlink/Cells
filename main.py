import numpy as np
import matplotlib.pyplot as plt

""" Начало считывания данных """

fig = plt.figure(figsize=(8, 8),dpi=100)
ax = fig.add_subplot(111)

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

Cov = [[float(f[0][0]), float(f[0][2])], [float(f[1][0]), float(f[1][2])]] # Матрица ковариации

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

        for v in self.points:
            v += v0
        pass

    def Print(self, col, ax):
        for i in range(4):
            x1, y1 = [self.points[i][0][0], self.points[(i + 1) % 4][0][0]], [self.points[i][1][0], self.points[(i + 1) % 4][1][0]]
            ax.plot(x1, y1, color=col)
        pass

def Generation():
    x, y = np.random.multivariate_normal(mean, Cov).T
    angle = np.random.rand() * 2 * np.pi

    return Square(np.array(x, y), angle)

squares = []
for i in range(100):
    squares.append(Generation())

for sq in squares:
    sq.Print('r', ax)

plt.show()