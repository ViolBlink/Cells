import matplotlib.pyplot as plt
import lib
import json

""" Начало считывания данных """
fig1 = plt.figure(figsize=(8, 8),dpi=100)
ax1 = fig1.add_subplot(111)

""" Создание прототипа для картинки"""
fig = plt.figure(figsize=(8, 8),dpi=100)
ax = fig.add_subplot(111)
ax.set_title('After')
"""                                 """

with open("Parametres.json") as q:
    f = json.load(q)
Amount = int(f["GeneralParametrs"][0]["Count"])
""" Конец считывания данных """

lib.Squares_Gen(Amount, ax1)
lib.ShowSquare(ax1)
lib.Disp()

lib.ShowSquare(ax)

plt.show()