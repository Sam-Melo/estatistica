import math

class TabelaIntervaloClasse:
    def __init__(self):
        self.dados = []
        self.tipo_dados = None
        self.casas_decimais = 2  # valor padrão

    def entrada_dados(self):
        """Solicita entrada de dados do usuário"""
        print("=== ENTRADA DE DADOS ===")
        print("Digite os dados separados por vírgula, espaço ou ambos:")
        entrada = input("Dados: ").replace(",", " ")

        valores = [x.strip() for x in entrada.split() if x.strip()]
        try:
            self.dados = [float(x) for x in valores]
        except ValueError:
            print("❌ Erro: certifique-se de digitar apenas números válidos.")
            self.dados = []
            return

        self.definir_tipo_dados()

        print(f"\nDados recebidos: {self.dados}")
        print(f"Tipo de dados: {self.tipo_dados}")
        print(f"Quantidade: {len(self.dados)}")

        try:
            casas = input("\nQuantas casas decimais deseja exibir? (padrão = 2): ")
            self.casas_decimais = int(casas) if casas.strip() else 2
        except ValueError:
            print("Valor inválido! Usando 2 casas decimais.")
            self.casas_decimais = 2

    def definir_tipo_dados(self):
        decimais = any(x != int(x) for x in self.dados)
        self.tipo_dados = "Contínuos" if decimais else "Discretos"

    def calcular_estatisticas(self):
        min_val = min(self.dados)
        max_val = max(self.dados)
        amplitude_total = max_val - min_val
        k = round(1 + 3.322 * math.log10(len(self.dados)))
        amplitude_classe = amplitude_total / k

        return {
            'min': min_val,
            'max': max_val,
            'amplitude_total': amplitude_total,
            'k': k,
            'amplitude_classe': amplitude_classe
        }

    def gerar_intervalos(self):
        min_val = min(self.dados)
        max_val = max(self.dados)
        n_dados = len(self.dados)

        # Número de classes (Sturges)
        k = round(1 + 3.322 * math.log10(n_dados))
        amplitude_classe = (max_val - min_val) / k

        fator = 10 ** self.casas_decimais
        amplitude_classe = math.ceil(amplitude_classe * fator) / fator

        intervalos = []
        limite_inferior = min_val

        for i in range(k):
            limite_superior = limite_inferior + amplitude_classe

            if i == k - 1:
                limite_superior = max_val

            formato = f"{{:.{self.casas_decimais}f}}"

            if self.tipo_dados == "Discretos":
                intervalo_str = f"{int(limite_inferior)} |-| {int(math.ceil(limite_superior))}" if i == k - 1 \
                    else f"{int(limite_inferior)} |- {int(math.floor(limite_superior))}"
            else:
                intervalo_str = f"{formato.format(limite_inferior)} |-| {formato.format(limite_superior)}" if i == k - 1 \
                    else f"{formato.format(limite_inferior)} |- {formato.format(limite_superior)}"

            intervalos.append({
                'intervalo': intervalo_str,
                'limite_inferior': limite_inferior,
                'limite_superior': limite_superior,
                'frequencia': 0,
                'frequencia_acumulada': 0,
                'eh_ultima_classe': (i == k - 1),
                'frequencia_relativa': 0,
                'frequencia_relativa_acumulada': 0,
                'frequencia_percentual': 0,
                'frequencia_percentual_acumulada': 0
            })
            limite_inferior = limite_superior

        return intervalos

    def calcular_frequencias(self, intervalos):
        n_total = len(self.dados)

        for dado in self.dados:
            for intervalo in intervalos:
                if self.tipo_dados == "Discretos":
                    if intervalo['limite_inferior'] <= dado <= intervalo['limite_superior']:
                        intervalo['frequencia'] += 1
                        break
                else:
                    if intervalo['eh_ultima_classe']:
                        if intervalo['limite_inferior'] <= dado <= intervalo['limite_superior']:
                            intervalo['frequencia'] += 1
                            break
                    elif intervalo['limite_inferior'] <= dado < intervalo['limite_superior']:
                        intervalo['frequencia'] += 1
                        break

        freq_acum = freq_rel_acum = freq_perc_acum = 0
        for intervalo in intervalos:
            freq_acum += intervalo['frequencia']
            intervalo['frequencia_acumulada'] = freq_acum

            intervalo['frequencia_relativa'] = intervalo['frequencia'] / n_total
            freq_rel_acum += intervalo['frequencia_relativa']
            intervalo['frequencia_relativa_acumulada'] = freq_rel_acum

            intervalo['frequencia_percentual'] = round(intervalo['frequencia_relativa'] * 100, 2)
            freq_perc_acum += intervalo['frequencia_percentual']
            intervalo['frequencia_percentual_acumulada'] = round(freq_perc_acum, 2)

        return intervalos

    def exibir_tabela(self, intervalos, estatisticas):
        dec = self.casas_decimais
        formato = f"{{:.{dec}f}}"

        print("\n" + "=" * 110)
        print("TABELA DE DISTRIBUIÇÃO DE FREQUÊNCIAS COMPLETA")
        print("=" * 110)
        print(f"{'Classe':<6} {'Intervalo':<20} {'Fi':<6} {'Fac':<8} {'Fr':<10} {'Frac':<10} {'F%':<10} {'Fac%':<10}")
        print("-" * 110)

        for i, intervalo in enumerate(intervalos, 1):
            casas_fr = 2 if self.tipo_dados == "Discretos" else dec
            f_percent = f"{intervalo['frequencia_percentual']:.2f}%"
            fac_percent = f"{intervalo['frequencia_percentual_acumulada']:.2f}%"

            print(f"{i:<6} {intervalo['intervalo']:<20} "
                  f"{intervalo['frequencia']:<6} "
                  f"{intervalo['frequencia_acumulada']:<8} "
                  f"{intervalo['frequencia_relativa']:<10.{casas_fr}f} "
                  f"{intervalo['frequencia_relativa_acumulada']:<10.{casas_fr}f} "
                  f"{f_percent:<10} "
                  f"{fac_percent:<10}")

        print("-" * 110)
        total = len(self.dados)
        print(f"{'Total':<6} {'':<20} "
              f"{total:<6} "
              f"{total:<8} "
              f"{1.0:<10.2f} "
              f"{1.0:<10.2f} "
              f"{'100.0%':<10} "
              f"{'100.0%':<10}")

        print("\n" + "=" * 60)
        print("ESTATÍSTICAS DESCRITIVAS:")
        print("=" * 60)
        print(f"Quantidade de dados: {len(self.dados)}")
        print(f"Valor mínimo: {formato.format(estatisticas['min'])}")
        print(f"Valor máximo: {formato.format(estatisticas['max'])}")
        print(f"Amplitude total: {formato.format(estatisticas['amplitude_total'])}")
        print(f"Número de classes (Sturges): {estatisticas['k']}")

        # 🔹 Exibe a fórmula detalhada da amplitude de classe
        print("\nAmplitude de Classe (A):")
        print(f"A = (maior - menor) / K")
        print(f"A = ({formato.format(estatisticas['max'])} - {formato.format(estatisticas['min'])}) / {estatisticas['k']} "
              f"= {formato.format(estatisticas['amplitude_classe'])}")

        print(f"\nTipo de dados: {self.tipo_dados}")

    def gerar_e_exibir_tabela(self):
        if not self.dados:
            print("Nenhum dado foi inserido!")
            return
        estatisticas = self.calcular_estatisticas()
        intervalos = self.gerar_intervalos()
        intervalos_com_freq = self.calcular_frequencias(intervalos)
        self.exibir_tabela(intervalos_com_freq, estatisticas)


def main():
    print("SOFTWARE PARA TABELA DE INTERVALO DE CLASSE")
    print("Desenvolvido em Python - Dados Quantitativos\n")

    tabela = TabelaIntervaloClasse()

    while True:
        print("\nMenu:")
        print("1. Inserir dados")
        print("2. Gerar tabela")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            tabela.entrada_dados()
        elif opcao == '2':
            tabela.gerar_e_exibir_tabela()
        elif opcao == '3':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
