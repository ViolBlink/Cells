import numpy as np
import matplotlib.pyplot as plt
import lib
import json

""" Начало считывания данных """
fig1 = plt.figure(figsize=(8, 8),dpi=100)
ax1 = fig1.add_subplot(111)

with open("Parametres.json") as q:
    f = json.load(q)
Amaunt = int(f["GeneralParametrs"][0]["Count"])
""" Конец считывания данных """

squares = lib.Squares_Gen(Amaunt)


for sq in squares:
    sq.Print('r', ax1)


plt.show()