# src/ogiva.py
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple


def ogiva_de_tabela_agrupada(intervalos: List[Tuple[float, float]], frequencias: List[int], mostrar_percentual: bool = True):
    if len(intervalos) != len(frequencias):
        raise ValueError("intervalos e frequencias devem ter o mesmo comprimento.")
    if len(intervalos) == 0:
        raise ValueError("Tabela vazia.")

    upper_bounds = np.array([b for (a, b) in intervalos], dtype=float)
    freq = np.array(frequencias, dtype=float)
    n = freq.sum()
    cum_freq = np.cumsum(freq)

    if mostrar_percentual:
        yvals = cum_freq / n * 100.0
        ylabel = "Frequência acumulada (%)"
    else:
        yvals = cum_freq
        ylabel = "Frequência acumulada (absoluta)"

    lower_first = float(intervalos[0][0])
    x = np.concatenate(([lower_first], upper_bounds))
    y = np.concatenate(([0], yvals))

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker='o', linestyle='-', linewidth=2)
    plt.step(x, y, where='pre', alpha=0.3)
    plt.title("Ogiva (tabela agrupada)")
    plt.xlabel("Valor / Limite de classe")
    plt.ylabel(ylabel)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
