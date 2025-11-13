# src/app.py
import tkinter as tk
from tkinter import scrolledtext, messagebox
import matplotlib.pyplot as plt
from tabela import TabelaIntervaloClasse
from histogram import build_hist_data, plot_hist
from ogiva import ogiva_de_dados_brutos, ogiva_de_tabela_agrupada

ultimo_tabela = None
ultimo_intervalos = None

def gerar_tabela():
    global ultimo_tabela, ultimo_intervalos
    texto = entrada.get("1.0", tk.END).strip()
    if not texto:
        saida.delete("1.0", tk.END)
        saida.insert(tk.END, "Digite os dados!\n")
        return
    try:
        dados = [float(x) for x in texto.replace(",", " ").split()]
    except ValueError:
        messagebox.showerror("Erro", "Insira apenas números válidos.")
        return

    tabela = TabelaIntervaloClasse()
    tabela.dados = dados
    tabela.definir_tipo_dados()
    estatisticas = tabela.calcular_estatisticas()
    intervalos = tabela.gerar_intervalos()
    intervalos = tabela.calcular_frequencias(intervalos)

    ultimo_tabela = tabela
    ultimo_intervalos = intervalos

    # mostra um resumo
    saida.delete("1.0", tk.END)
    saida.insert(tk.END, "=== TABELA DE FREQUÊNCIAS ===\n\n")
    for i, inter in enumerate(intervalos, 1):
        saida.insert(tk.END, f"{i}: {inter['intervalo']} -> Fi={inter['frequencia']}  Fac={inter['frequencia_acumulada']}\n")

    saida.insert(tk.END, "\n=== ESTATÍSTICAS ===\n")
    saida.insert(tk.END, f"n = {len(tabela.dados)}\n")
    saida.insert(tk.END, f"Média = {estatisticas['media']:.2f}\n")
    saida.insert(tk.END, f"Mediana = {estatisticas['mediana']:.2f}\n")
    saida.insert(tk.END, f"Desvio padrão = {estatisticas['desvio_padrao']:.2f}\n")
    saida.insert(tk.END, f"Tipo = {tabela.tipo_dados}\n")

def mostrar_histograma():
    if not (ultimo_tabela and ultimo_intervalos):
        saida.insert(tk.END, "\n⚠️ Gere a tabela primeiro!\n")
        return

    # Construir limites reais
    limites = []
    frequencias = []
    labels = []

    for inter in ultimo_intervalos:
        li = inter["limite_inferior"]
        ls = inter["limite_superior"]
        limites.append(li)
        frequencias.append(inter["frequencia"])
        labels.append(f"[{li} – {ls}]")

    limites.append(ultimo_intervalos[-1]["limite_superior"])

    # Largura real de cada classe
    larguras = [
        limites[i+1] - limites[i]
        for i in range(len(limites) - 1)
    ]

    fig, ax = plt.subplots(figsize=(9, 4))

    # Barras grudadas (histograma contínuo)
    ax.bar(
        limites[:-1],
        frequencias,
        width=larguras,
        align="edge",
        edgecolor="black",
        alpha=0.7
    )

    # Labels do eixo X no formato [a – b]
    ax.set_xticks(limites[:-1])
    ax.set_xticklabels(labels, rotation=45, ha="right")

    ax.set_title("Histograma (contínuos)")
    ax.set_xlabel("Blocos (Classes)")
    ax.set_ylabel("Frequência Absoluta")

    plt.tight_layout()
    plt.show()

def mostrar_ogiva_tabela():
    if not (ultimo_tabela and ultimo_intervalos):
        saida.insert(tk.END, "\n⚠️ Gere a tabela primeiro!\n")
        return
    # usa os limites superiores da tabela agrupada
    intervalos_xy = [(i['limite_inferior'], i['limite_superior']) for i in ultimo_intervalos]
    freq = [i['frequencia'] for i in ultimo_intervalos]
    ogiva_de_tabela_agrupada(intervalos_xy, freq, mostrar_percentual=True)

def mostrar_ogiva_brutos():
    if not ultimo_tabela:
        saida.insert(tk.END, "\n⚠️ Gere a tabela primeiro (para eu pegar os dados)!\n")
        return
    ogiva_de_dados_brutos(ultimo_tabela.dados, num_classes=None, mostrar_percentual=True)

# --------- UI ---------
root = tk.Tk()
root.title("Tabela de Frequência | Histograma | Ogiva")

tk.Label(root, text="Digite os dados (separados por espaço ou vírgula):").pack()
entrada = scrolledtext.ScrolledText(root, width=60, height=3)
entrada.pack()

frame_btn = tk.Frame(root)
frame_btn.pack(pady=6)

tk.Button(frame_btn, text="Gerar Tabela", command=gerar_tabela).grid(row=0, column=0, padx=4)
tk.Button(frame_btn, text="Histograma", command=mostrar_histograma).grid(row=0, column=1, padx=4)
tk.Button(frame_btn, text="Ogiva (tabela)", command=mostrar_ogiva_tabela).grid(row=0, column=2, padx=4)
tk.Button(frame_btn, text="Ogiva (brutos)", command=mostrar_ogiva_brutos).grid(row=0, column=3, padx=4)

saida = scrolledtext.ScrolledText(root, width=90, height=20)
saida.pack()

root.mainloop()
