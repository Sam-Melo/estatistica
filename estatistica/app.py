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


    saida.delete("1.0", tk.END)
    saida.insert(tk.END, "=== TABELA DE FREQUÊNCIAS ===\n\n")
    for i, inter in enumerate(intervalos, 1):
        saida.insert(tk.END, f"{i}: {inter['intervalo']} -> Fi={inter['frequencia']}  Fac={inter['frequencia_acumulada']}\n Frac={inter['frequencia']}")

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

    tabela = ultimo_tabela
    intervalos = ultimo_intervalos
    dados = tabela.dados

    if tabela.tipo_dados == "Contínuos":
        bins = [(i['limite_inferior'], i['limite_superior']) for i in intervalos]
        freq = [i['frequencia'] for i in intervalos]
        data_dict = {"type": "continuous", "bins": bins, "freq": freq, "n": len(dados)}
    else:
        valores = [i['ponto_medio'] for i in intervalos]
        freq = [i['frequencia'] for i in intervalos]
        data_dict = {"type": "discrete", "values": valores, "freq": freq, "n": len(dados)}

    hist_data = build_hist_data(data_dict, use_density=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    plot_hist(ax, hist_data, title=f"Histograma ({tabela.tipo_dados})")
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
