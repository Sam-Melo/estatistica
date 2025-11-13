# src/app.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt

from tabela import TabelaIntervaloClasse
from histogram import plot_hist
from ogiva import ogiva_de_tabela_agrupada

ultimo_tabela = None
ultimo_intervalos = None


# ===================== FUNÇÕES ===============================

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

    # ================== EXIBIR TABELA =========================

    saida.delete("1.0", tk.END)
    saida.insert(tk.END, "=== TABELA DE FREQUÊNCIAS ===\n\n")

    saida.insert(tk.END, "Cls | Intervalo        | Fi | Fr(%) | Fac | Frac(%)\n")
    saida.insert(tk.END, "----------------------------------------------------\n")

    for i, inter in enumerate(intervalos, 1):

        li = inter.get("limite_inferior")
        ls = inter.get("limite_superior")
        intervalo_str = f"[{li} – {ls}]"

        fi = inter.get("frequencia", 0)
        fr = inter.get("frequencia_relativa", 0) * 100
        fac = inter.get("frequencia_acumulada", 0)
        frac = inter.get("frequencia_relativa_acumulada", 0) * 100

        saida.insert(
            tk.END,
            f"{i:<3} | {intervalo_str:<16} | {fi:<2} | {fr:>5.1f}% | {fac:<3} | {frac:>6.1f}%\n"
        )

    # ================== ESTATÍSTICAS ===========================

    saida.insert(tk.END, "\n=== ESTATÍSTICAS ===\n")
    saida.insert(tk.END, f"Total de dados (n): {len(tabela.dados)}\n")

    if "media" in estatisticas:
        saida.insert(tk.END, f"Média: {estatisticas['media']:.4f}\n")

    if "mediana" in estatisticas:
        saida.insert(tk.END, f"Mediana: {estatisticas['mediana']:.4f}\n")

    if "moda" in estatisticas and estatisticas["moda"] is not None:
        saida.insert(tk.END, f"Moda: {estatisticas['moda']}\n")

    if "variancia" in estatisticas:
        saida.insert(tk.END, f"Variância: {estatisticas['variancia']:.4f}\n")

    if "desvio_padrao" in estatisticas:
        saida.insert(tk.END, f"Desvio padrão: {estatisticas['desvio_padrao']:.4f}\n")

    if "cv" in estatisticas:
        saida.insert(tk.END, f"Coeficiente de variação: {estatisticas['cv']:.2f}%\n")

    if "amplitude_total" in estatisticas:
        saida.insert(tk.END, f"Amplitude total: {estatisticas['amplitude_total']}\n")

    saida.insert(tk.END, f"Tipo do conjunto: {tabela.tipo_dados}\n")


def mostrar_histograma():
    if not ultimo_intervalos:
        saida.insert(tk.END, "\n⚠️ Gere a tabela primeiro!\n")
        return

    plot_hist(ultimo_intervalos)


def mostrar_ogiva_tabela():
    if not ultimo_intervalos:
        saida.insert(tk.END, "\n⚠️ Gere a tabela primeiro!\n")
        return

    intervalos_xy = [(i['limite_inferior'], i['limite_superior']) for i in ultimo_intervalos]
    freq = [i["frequencia"] for i in ultimo_intervalos]

    ogiva_de_tabela_agrupada(intervalos_xy, freq, mostrar_percentual=True)


# ===================== INTERFACE (UI) ===============================

root = tk.Tk()
root.title("📊 Analisador Estatístico – Tabelas, Histogramas e Ogivas")
root.geometry("900x600")
root.configure(bg="#eef2f7")

# TEMA MODERNO
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=6, font=("Segoe UI", 10, "bold"))
style.configure("TLabel", background="#eef2f7", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

# CABEÇALHO
header = ttk.Label(root, text="Analisador Estatístico", style="Header.TLabel")
header.pack(pady=10)

# BLOCO DE ENTRADA
frame_input = ttk.Frame(root)
frame_input.pack(pady=5)

ttk.Label(frame_input, text="Insira os dados (separados por espaço):").pack(anchor="w")

entrada = scrolledtext.ScrolledText(frame_input, width=70, height=4, font=("Consolas", 10))
entrada.pack(pady=4)

# BOTÕES
frame_btn = ttk.Frame(root)
frame_btn.pack(pady=10)

ttk.Button(frame_btn, text="Gerar Tabela", command=gerar_tabela).grid(row=0, column=0, padx=8)
ttk.Button(frame_btn, text="Histograma", command=mostrar_histograma).grid(row=0, column=1, padx=8)
ttk.Button(frame_btn, text="Ogiva", command=mostrar_ogiva_tabela).grid(row=0, column=2, padx=8)

# ÁREA DE RESULTADO
saida = scrolledtext.ScrolledText(root, width=100, height=22, font=("Consolas", 10))
saida.pack(pady=10)

root.mainloop()
