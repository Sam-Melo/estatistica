# histogram.py

from matplotlib.patches import Rectangle

# =====================================================================
#  CONSTRUÇÃO DOS DADOS DO HISTOGRAMA
# =====================================================================

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

    # ------------------------------------------------------------------
    # HISTOGRAMA CONTÍNUO (com classes)
    # ------------------------------------------------------------------
    if t == "continuous":
        bins = data["bins"]
        freq = data["freq"]     # pode ser Fi ou Fac, você escolhe no app.py
        n = data["n"]

        # edges = [l0, u0, u1, ...]
        edges = [bins[0][0]] + [b[1] for b in bins]
        widths = [hi - lo for (lo, hi) in bins]

        if use_density:
            heights = [fi / (n * w) for fi, w in zip(freq, widths)]
        else:
            heights = list(freq)   # usa a frequência que veio (ex.: Fac)

        return {
            "type": "continuous",
            "edges": edges,
            "heights": heights,
        }

    # ------------------------------------------------------------------
    # HISTOGRAMA DISCRETO (barras individuais)
    # ------------------------------------------------------------------
    elif t == "discrete":
        values = data["values"]
        freq = data["freq"]  # frequência absoluta
        n = data["n"]

        # largura = menor distância entre valores -> barras coladas
        if len(values) > 1:
            gaps = [values[i+1] - values[i] for i in range(len(values) - 1)]
            min_gap = min(gaps) if gaps else 1.0
        else:
            min_gap = 1.0

        width = (min_gap if min_gap > 0 else 1.0)  # *** SEM 0.8, para colar ***

        return {
            "type": "discrete",
            "x": values,
            "width": width,
            "heights": list(freq),
        }

    else:
        raise ValueError("type deve ser 'continuous' ou 'discrete'.")


# =====================================================================
#  PLOTAGEM DO HISTOGRAMA
# =====================================================================

def plot_hist(ax, hist_data, title=""):
    """
    - Contínua: barras coladas por classe (usando amplitude de classe no eixo X).
    - Discreta: barras coladas em cada valor.
    """

    # ------------------------------------------------------------------
    # PLOT CONTÍNUO
    # ------------------------------------------------------------------
    if hist_data["type"] == "continuous":
        edges = hist_data["edges"]
        heights = hist_data["heights"]

        mids = []
        labels = []

        for i, h in enumerate(heights):
            x0, x1 = edges[i], edges[i+1]
            width = x1 - x0

            # barra colada sem borda
            ax.add_patch(
                Rectangle(
                    (x0, 0),
                    width,
                    h,
                    edgecolor=None,
                    linewidth=0,
                    fill=True,
                    alpha=0.7,
                )
            )

            # meio do intervalo
            mids.append((x0 + x1) / 2)
            labels.append(f"{x0:.1f}-{x1:.1f}")

        ax.set_xlim(edges[0], edges[-1])
        ax.set_ylim(bottom=0)

        ax.set_ylabel("Frequência absoluta acumulada")
        ax.set_xlabel("Amplitude / Intervalo de classe")
        ax.set_xticks(mids)
        ax.set_xticklabels(labels, rotation=45, ha="right")

    # ------------------------------------------------------------------
    # PLOT DISCRETO
    # ------------------------------------------------------------------
    else:  # discrete
        x = hist_data["x"]
        w = hist_data["width"]
        h = hist_data["heights"]

        # left = centro - metade da largura
        lefts = [xi - w / 2 for xi in x]

        # barras encostadas (width = min_gap lá em cima)
        ax.bar(lefts, h, width=w, align="edge")

        # limites horizontais justos nas barras
        ax.set_xlim(min(x) - w / 2, max(x) + w / 2)
        ax.set_ylim(bottom=0)

        ax.set_ylabel("Frequência absoluta")
        ax.set_xlabel("Valores")

    if title:
        ax.set_title(title)

    ax.grid(True, linestyle="--", alpha=0.4)
