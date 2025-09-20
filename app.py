# src/app.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import matplotlib.pyplot as plt

from tabela import TabelaIntervaloClasse
from histogram import build_hist_data, plot_hist
from ogiva import ogiva_de_dados_brutos, ogiva_de_tabela_agrupada

# ---------------------------
# Estado global simples
# ---------------------------
ultimo_tabela = None
ultimo_intervalos = None

# ---------------------------
# Tema / Estilos
# ---------------------------
def configure_theme(root, dark=False):
    style = ttk.Style(root)
    # base
    style.theme_use("clam")

    if dark:
        bg      = "#121212"
        surface = "#1E1E1E"
        card    = "#232323"
        text    = "#EAEAEA"
        subtext = "#B5B5B5"
        accent  = "#3D7AFE"
        border  = "#333333"
        entrybg = "#2A2A2A"
    else:
        bg      = "#F6F7FB"
        surface = "#FFFFFF"
        card    = "#FFFFFF"
        text    = "#1C1C1C"
        subtext = "#666666"
        accent  = "#3D7AFE"
        border  = "#E5E7EB"
        entrybg = "#FFFFFF"

    root.configure(bg=bg)

    style.configure("Card.TFrame", background=card, borderwidth=1, relief="solid")
    style.map("Card.TFrame", background=[("active", card)])
    style.configure("Surface.TFrame", background=surface)
    style.configure("TLabel", background=card, foreground=text)
    style.configure("Muted.TLabel", background=card, foreground=subtext)
    style.configure("Title.TLabel", background=surface, foreground=text, font=("Segoe UI", 14, "bold"))
    style.configure("Header.TLabel", background=card, foreground=text, font=("Segoe UI", 12, "bold"))
    style.configure("Small.TLabel", background=card, foreground=subtext, font=("Segoe UI", 9))

    style.configure("TButton", font=("Segoe UI", 10), padding=8)
    style.map("TButton",
              background=[("!disabled", surface)],
              relief=[("pressed", "sunken")])

    style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=8)
    style.map("Accent.TButton",
              foreground=[("!disabled", "#FFFFFF")],
              background=[("!disabled", accent), ("active", "#2F63D6")])

    style.configure("TEntry", fieldbackground=entrybg, foreground=text, bordercolor=border)
    style.configure("TNotebook", background=surface)
    style.configure("TNotebook.Tab", padding=(16, 8), font=("Segoe UI", 10))

    # Treeview
    style.configure("Treeview",
                    background=card, fieldbackground=card, foreground=text,
                    bordercolor=border, borderwidth=1, rowheight=28, font=("Segoe UI", 10))
    style.map("Treeview", background=[("selected", accent)], foreground=[("selected", "#FFFFFF")])
    style.configure("Treeview.Heading",
                    background=surface, foreground=text, relief="flat",
                    font=("Segoe UI Semibold", 10))
    style.map("Treeview.Heading",
              background=[("active", surface)],
              relief=[("pressed", "groove")])

    # separadores
    style.configure("TSeparator", background=border)

    # status bar
    style.configure("Status.TLabel", background=surface if not dark else card, foreground=subtext, font=("Segoe UI", 9))


# ---------------------------
# Lógica de app
# ---------------------------
def parse_dados(texto):
    texto = texto.replace(",", " ")
    parts = [p for p in texto.split() if p.strip()]
    return [float(p) for p in parts]

def gerar_tabela():
    global ultimo_tabela, ultimo_intervalos
    txt = entrada_text.get("1.0", tk.END).strip()
    if not txt:
        messagebox.showinfo("Aviso", "Digite os dados (separados por espaço ou vírgula).")
        return
    try:
        dados = parse_dados(txt)
    except ValueError:
        messagebox.showerror("Erro", "Verifique: só números, separados por espaço/vírgula.")
        return

    t = TabelaIntervaloClasse()
    t.dados = dados
    t.definir_tipo_dados()
    est = t.calcular_estatisticas()
    intervs = t.gerar_intervalos()
    intervs = t.calcular_frequencias(intervs)

    ultimo_tabela = t
    ultimo_intervalos = intervs

    # Preenche Treeview
    for item in tabela_tree.get_children():
        tabela_tree.delete(item)

    n = len(dados)
    for i, I in enumerate(intervs, 1):
        rel_pct = 0.0 if n == 0 else (I["frequencia"] / n) * 100
        tabela_tree.insert("", "end", values=(
            i,
            I["intervalo"],
            f"{I['ponto_medio']:.2f}",
            I["frequencia"],
            I["frequencia_acumulada"],
            f"{rel_pct:.2f}%"
        ))

    # Stats
    stats_vars["n"].set(str(n))
    stats_vars["min"].set(f"{est['min']:.2f}")
    stats_vars["max"].set(f"{est['max']:.2f}")
    stats_vars["amp"].set(f"{est['amplitude']:.2f}")
    stats_vars["media"].set(f"{est['media']:.2f}")
    stats_vars["mediana"].set(f"{est['mediana']:.2f}")
    stats_vars["desvio"].set(f"{est['desvio_padrao']:.2f}")
    stats_vars["tipo"].set(t.tipo_dados)
    stats_vars["classes"].set(str(t.calcular_numero_classes()))

    status_var.set("Tabela gerada com sucesso. Dica: F5 abre histograma, F6 abre ogiva.")

def mostrar_histograma():
    if not (ultimo_tabela and ultimo_intervalos):
        messagebox.showinfo("Aviso", "Gere a tabela primeiro.")
        return
    t = ultimo_tabela
    intervs = ultimo_intervalos
    dados = t.dados

    if t.tipo_dados == "Contínuos":
        bins = [(I["limite_inferior"], I["limite_superior"]) for I in intervs]
        freq = [I["frequencia"] for I in intervs]
        dct = {"type": "continuous", "bins": bins, "freq": freq, "n": len(dados)}
    else:
        valores = [I["ponto_medio"] for I in intervs]
        freq = [I["frequencia"] for I in intervs]
        dct = {"type": "discrete", "values": valores, "freq": freq, "n": len(dados)}

    hist_data = build_hist_data(dct, use_density=False)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    plot_hist(ax, hist_data, title=f"Histograma ({t.tipo_dados})")
    fig.tight_layout()
    plt.show()

def mostrar_ogiva_tabela():
    if not (ultimo_tabela and ultimo_intervalos):
        messagebox.showinfo("Aviso", "Gere a tabela primeiro.")
        return
    intervs = [(I["limite_inferior"], I["limite_superior"]) for I in ultimo_intervalos]
    freq = [I["frequencia"] for I in ultimo_intervalos]
    ogiva_de_tabela_agrupada(intervs, freq, mostrar_percentual=True)

def mostrar_ogiva_brutos():
    if not ultimo_tabela:
        messagebox.showinfo("Aviso", "Gere a tabela primeiro (para capturar os dados).")
        return
    ogiva_de_dados_brutos(ultimo_tabela.dados, num_classes=None, mostrar_percentual=True)

def exportar_csv():
    if not ultimo_intervalos:
        messagebox.showinfo("Aviso", "Gere a tabela primeiro.")
        return
    caminho = filedialog.asksaveasfilename(defaultextension=".csv",
                                           filetypes=[("CSV", "*.csv")],
                                           title="Salvar tabela como CSV")
    if not caminho:
        return
    # Exporta colunas principais
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Classe", "Intervalo", "Ponto Médio", "Fi", "Fac", "Rel%"])
        n = len(ultimo_tabela.dados)
        for i, I in enumerate(ultimo_intervalos, 1):
            rel_pct = 0.0 if n == 0 else (I["frequencia"] / n) * 100
            w.writerow([i, I["intervalo"], f"{I['ponto_medio']:.4f}", I["frequencia"], I["frequencia_acumulada"], f"{rel_pct:.2f}"])
    messagebox.showinfo("Pronto", "CSV exportado com sucesso!")

def limpar():
    entrada_text.delete("1.0", tk.END)
    for item in tabela_tree.get_children():
        tabela_tree.delete(item)
    for k in stats_vars:
        stats_vars[k].set("--")
    status_var.set("Pronto.")

def toggle_theme():
    dark = theme_var.get()
    configure_theme(root, dark=dark)
    # re-aplica backgrounds específicos
    for frame in (header_frame, input_card, table_card, stats_card, footer_bar):
        frame.configure(style="Card.TFrame")
    header_frame.configure(style="Surface.TFrame")
    footer_bar.configure(style="Surface.TFrame")

# ---------------------------
# UI
# ---------------------------
root = tk.Tk()
root.title("📊 Estatística G2 — Tabela • Histograma • Ogiva")
root.geometry("1020x680")
root.minsize(900, 600)

# Tema inicial claro
configure_theme(root, dark=False)

# Header (título + toggle tema)
header_frame = ttk.Frame(root, style="Surface.TFrame", padding=(16, 12))
header_frame.pack(fill="x")

title_lbl = ttk.Label(header_frame, text="📊 Estatística G2", style="Title.TLabel")
subtitle_lbl = ttk.Label(header_frame, text="Tabela de frequências, histograma e ogiva", style="Small.TLabel")
title_lbl.grid(row=0, column=0, sticky="w")
subtitle_lbl.grid(row=1, column=0, sticky="w")

theme_var = tk.BooleanVar(value=False)
theme_chk = ttk.Checkbutton(header_frame, text="Modo escuro", command=toggle_theme, variable=theme_var)
theme_chk.grid(row=0, column=1, rowspan=2, sticky="e", padx=8)

header_frame.columnconfigure(0, weight=1)

# Área principal (grid 2 colunas)
main = ttk.Frame(root, style="Surface.TFrame", padding=(16, 8))
main.pack(fill="both", expand=True)
main.columnconfigure(0, weight=2, uniform="a")
main.columnconfigure(1, weight=1, uniform="a")
main.rowconfigure(1, weight=1)

# Card: Entrada + Ações
input_card = ttk.Frame(main, style="Card.TFrame", padding=12)
input_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))
ttk.Label(input_card, text="Entrada de dados", style="Header.TLabel").pack(anchor="w", pady=(0, 6))
ttk.Label(input_card, text="Separe valores por espaço ou vírgula (ex.: 10 20 30 40 50).", style="Small.TLabel").pack(anchor="w", pady=(0, 8))

entrada_text = tk.Text(input_card, height=4, wrap="word", font=("Cascadia Code", 11))
entrada_text.pack(fill="x", pady=(0, 8))

btn_row = ttk.Frame(input_card)
btn_row.pack(fill="x")
ttk.Button(btn_row, text="Gerar Tabela (Ctrl+Enter)", style="Accent.TButton", command=gerar_tabela).pack(side="left", padx=(0, 6))
ttk.Button(btn_row, text="Histograma (F5)", command=mostrar_histograma).pack(side="left", padx=6)
ttk.Button(btn_row, text="Ogiva (Tabela) (F6)", command=mostrar_ogiva_tabela).pack(side="left", padx=6)
ttk.Button(btn_row, text="Ogiva (Brutos)", command=mostrar_ogiva_brutos).pack(side="left", padx=6)
ttk.Button(btn_row, text="Exportar CSV", command=exportar_csv).pack(side="right", padx=(6, 0))
ttk.Button(btn_row, text="Limpar", command=limpar).pack(side="right", padx=6)

# Card: Tabela (Treeview)
table_card = ttk.Frame(main, style="Card.TFrame", padding=12)
table_card.grid(row=1, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))
ttk.Label(table_card, text="Tabela de distribuição de frequências", style="Header.TLabel").pack(anchor="w", pady=(0, 6))

cols = ("classe", "intervalo", "pm", "fi", "fac", "rel")
tabela_tree = ttk.Treeview(table_card, columns=cols, show="headings", selectmode="browse")
tabela_tree.heading("classe", text="Classe")
tabela_tree.heading("intervalo", text="Intervalo")
tabela_tree.heading("pm", text="Ponto Médio")
tabela_tree.heading("fi", text="Fi")
tabela_tree.heading("fac", text="Fac")
tabela_tree.heading("rel", text="Rel.%")

tabela_tree.column("classe", width=70, anchor="center")
tabela_tree.column("intervalo", width=200, anchor="w")
tabela_tree.column("pm", width=120, anchor="e")
tabela_tree.column("fi", width=80, anchor="center")
tabela_tree.column("fac", width=80, anchor="center")
tabela_tree.column("rel", width=80, anchor="e")

tabela_tree.pack(fill="both", expand=True)

# Card: Estatísticas (direita)
stats_card = ttk.Frame(main, style="Card.TFrame", padding=12)
stats_card.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(8, 0), pady=(0, 8))
ttk.Label(stats_card, text="Estatísticas", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

def add_stat(row, label):
    ttk.Label(stats_card, text=label + ":", style="TLabel").grid(row=row, column=0, sticky="w", pady=4)
    var = tk.StringVar(value="--")
    ttk.Label(stats_card, textvariable=var, style="TLabel").grid(row=row, column=1, sticky="e", pady=4)
    return var

stats_vars = {
    "n": add_stat(1, "n"),
    "min": add_stat(2, "min"),
    "max": add_stat(3, "max"),
    "amp": add_stat(4, "amplitude"),
    "media": add_stat(5, "média"),
    "mediana": add_stat(6, "mediana"),
    "desvio": add_stat(7, "desvio padrão"),
    "classes": add_stat(8, "nº classes"),
    "tipo": add_stat(9, "tipo"),
}

for i in range(10):
    stats_card.rowconfigure(i, weight=0)
stats_card.columnconfigure(0, weight=1)
stats_card.columnconfigure(1, weight=1)

# Footer / status bar
footer_bar = ttk.Frame(root, style="Surface.TFrame", padding=(16, 6))
footer_bar.pack(fill="x")
status_var = tk.StringVar(value="Pronto.")
status_lbl = ttk.Label(footer_bar, textvariable=status_var, style="Status.TLabel")
status_lbl.pack(side="left")

# Atalhos de teclado
def on_ctrl_enter(event):
    gerar_tabela()
def on_f5(event):
    mostrar_histograma()
def on_f6(event):
    mostrar_ogiva_tabela()

root.bind("<Control-Return>", on_ctrl_enter)
root.bind("<F5>", on_f5)
root.bind("<F6>", on_f6)

# Inicia
root.after(100, lambda: status_var.set("Digite dados e pressione Ctrl+Enter para gerar a tabela."))

root.mainloop()
