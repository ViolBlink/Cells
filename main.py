import numpy as np
import matplotlib.pyplot as plt
import lib
import json

""" Начало считывания данных """
fig1 = plt.figure(figsize=(8, 8),dpi=100)
ax1 = fig1.add_subplot(111)

fig2 = plt.figure(figsize=(8, 8),dpi=100)
ax2 = fig2.add_subplot(111)

# Считываем парамтры распределения
with open("Parametres.json") as q:
    f = json.load(q)

a = float(f["GeneralParametrs"][0]["a"])
mean = [float(f["Normal"][0]["x0"]), float(f["Normal"][0]["y0"])] # Матрица среднего

f = f["Normal"][0]["Cov"].split("\n")
f1 = f[0].split(" ")
f2 = f[1].split(" ")

Cov = [[float(f1[0]), float(f1[1])], [float(f2[0]), float(f2[1])]] # Матрица ковариации

""" Конец считывания данных """


def Squares_Gen(len: int):

    squares = []
    i = 0

    while (i < len):
        x, y = np.random.multivariate_normal(mean, Cov).T
        v0 = lib.Closest(x, y)
        angle = np.random.rand() * 2 * np.pi
        
        flag = 1

        for square in squares:
            if lib.leng(v0, square.centre) < 2 * a:
                flag = 0
                break
        
        if (flag == 1):
            ax2.plot(v0[0][0], v0[1][0], 'x', color='r')
            ax2.axis('equal')

            squares.append(lib.Square(np.array([[v0[0][0]], [v0[1][0]]]), angle))
            i += 1

    return squares


lib.AddCentres(ax2)
squares = Squares_Gen(5)


for sq in squares:
    sq.Print('r', ax1)


plt.show()