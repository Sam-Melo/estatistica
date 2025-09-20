# src/histogram.py
def build_hist_data(data, use_density=True):
    """
    data (dict) nos formatos:
      Contínua:
        {"type":"continuous","bins":[(lo,hi),...],"freq":[...],"n":N}
      Discreta:
        {"type":"discrete","values":[...],"freq":[...],"n":N}
    Retorna um dicionário pronto pro plot.
    """
    t = data.get("type")
    if t == "continuous":
        bins = data["bins"]
        freq = data["freq"]
        n = data["n"]
        edges = [bins[0][0]] + [b[1] for b in bins]           # [l0,u0,u1,...]
        widths = [hi - lo for (lo, hi) in bins]
        if use_density:
            heights = [fi / (n * w) for fi, w in zip(freq, widths)]
        else:
            heights = list(freq)
        return {"type":"continuous","edges":edges,"heights":heights}
    elif t == "discrete":
        values = data["values"]
        freq = data["freq"]
        n = data["n"]
        # largura padrão simples: 0.8 entre vizinhos (ou 1.0 se não der)
        if len(values) > 1:
            gaps = [values[i+1]-values[i] for i in range(len(values)-1)]
            min_gap = min(gaps) if len(gaps)>0 else 1.0
        else:
            min_gap = 1.0
        width = 0.8 * (min_gap if min_gap>0 else 1.0)
        heights = [fi/n for fi in freq]  # freq relativa pra ficar básico
        return {"type":"discrete","x":values,"width":width,"heights":heights}
    else:
        raise ValueError("type deve ser 'continuous' ou 'discrete'.")

def plot_hist(ax, hist_data, title=""):
    """
    Plota em um eixo matplotlib.
    - Contínua: retângulos por classe.
    - Discreta: barras centradas em cada valor.
    """
    from matplotlib.patches import Rectangle

    if hist_data["type"] == "continuous":
        edges = hist_data["edges"]
        heights = hist_data["heights"]
        for i, h in enumerate(heights):
            x0, x1 = edges[i], edges[i+1]
            ax.add_patch(Rectangle((x0, 0), x1-x0, h, fill=False))
        ax.set_xlim(edges[0], edges[-1])
        ax.set_ylabel("Densidade/Freq.")
    else:
        x = hist_data["x"]
        w = hist_data["width"]
        h = hist_data["heights"]
        lefts = [xi - w/2 for xi in x]
        ax.bar(lefts, h, width=w, align="edge")
        ax.set_ylabel("Frequência relativa")

    ax.set_xlabel("Valores")
    if title:
        ax.set_title(title)
    ax.set_ylim(bottom=0)
    ax.grid(True, linestyle="--", alpha=0.4)