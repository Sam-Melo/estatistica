# src/main.py
import matplotlib.pyplot as plt
from histograma import build_hist_data, plot_hist

def fake_continuous():
    return {"type":"continuous","bins":[(0,10),(10,30),(30,40)],"freq":[2,6,2],"n":10}

def fake_discrete():
    return {"type":"discrete","values":[1,2,4],"freq":[1,3,2],"n":6}

if __name__ == "__main__":
    # Contínua (densidade)
    fig1, ax1 = plt.subplots()
    h1 = build_hist_data(fake_continuous(), use_density=True)
    plot_hist(ax1, h1, "Histograma Contínuo")
    plt.tight_layout()
    fig1.savefig("outputs/cont_hist.png", dpi=300)

    # Discreta (freq relativa)
    fig2, ax2 = plt.subplots()
    h2 = build_hist_data(fake_discrete(), use_density=True)
    plot_hist(ax2, h2, "Histograma Discreto")
    plt.tight_layout()
    fig2.savefig("outputs/disc_hist.png", dpi=300)
