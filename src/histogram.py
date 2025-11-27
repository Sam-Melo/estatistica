import matplotlib.pyplot as plt

def build_hist_data(intervalos):
    """
    Constrói os limites de classe e labels no formato [a – b].
    """
    limites = []
    frequencias = []
    labels = []

    for inter in intervalos:
        li = inter['limite_inferior']
        ls = inter['limite_superior']

        limites.append(li)
        frequencias.append(inter['frequencia'])
        labels.append(f"[{li} – {ls}]")

    # último limite superior
    limites.append(intervalos[-1]['limite_superior'])

    return limites, frequencias, labels


def plot_hist(intervalos, title="Histograma (contínuos)"):
    limites, frequencias, labels = build_hist_data(intervalos)

    # larguras das barras
    larguras = [
        limites[i+1] - limites[i]
        for i in range(len(limites)-1)
    ]

    fig, ax = plt.subplots(figsize=(10, 4))

    # barras grudadas com amplitude real
    ax.bar(
        limites[:-1],
        frequencias,
        width=larguras,
        align="edge",
        edgecolor="black",
        alpha=0.7
    )

    # rótulos das classes (ESTE É O QUE VOCÊ QUER)
    ax.set_xticks(limites[:-1])
    ax.set_xticklabels(labels, rotation=45, ha="right")

    ax.set_xlabel("Blocos (Classes)")
    ax.set_ylabel("Frequência Absoluta")
    ax.set_title(title)

    plt.tight_layout()
    plt.show()
