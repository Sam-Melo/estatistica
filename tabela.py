import math

class TabelaIntervaloClasse:
    def __init__(self):
        self.dados = []
        self.tipo_dados = None
        
    def entrada_dados(self):
        """Solicita entrada de dados do usuário"""
        print("=== ENTRADA DE DADOS ===")
        print("Digite os dados separados por vírgula ou espaço:")
        entrada = input("Dados: ")
        
        # Processa a entrada
        if ',' in entrada:
            self.dados = [float(x.strip()) for x in entrada.split(',') if x.strip()]
        else:
            self.dados = [float(x.strip()) for x in entrada.split() if x.strip()]
        
        # Determina se os dados são discretos ou contínuos
        self.definir_tipo_dados()
        
        print(f"Dados recebidos: {self.dados}")
        print(f"Tipo de dados: {self.tipo_dados}")
        print(f"Quantidade: {len(self.dados)}")
    
    def definir_tipo_dados(self):
        """Define se os dados são discretos ou contínuos"""
        # Verifica se há casas decimais
        decimais = any(x != int(x) for x in self.dados)
        self.tipo_dados = "Contínuos" if decimais else "Discretos"
    
    def calcular_estatisticas(self):
        """Calcula estatísticas básicas"""
        min_val = min(self.dados)
        max_val = max(self.dados)
        amplitude = max_val - min_val
        
        # Média
        media = sum(self.dados) / len(self.dados)
        
        # Mediana
        sorted_dados = sorted(self.dados)
        n = len(sorted_dados)
        if n % 2 == 0:
            mediana = (sorted_dados[n//2 - 1] + sorted_dados[n//2]) / 2
        else:
            mediana = sorted_dados[n//2]
        
        # Desvio padrão
        variancia = sum((x - media) ** 2 for x in self.dados) / len(self.dados)
        desvio_padrao = math.sqrt(variancia)
        
        return {
            'min': min_val,
            'max': max_val,
            'amplitude': amplitude,
            'media': media,
            'mediana': mediana,
            'desvio_padrao': desvio_padrao
        }
    
    def calcular_numero_classes(self):
        """Calcula o número ideal de classes usando a regra de Sturges"""
        n = len(self.dados)
        k = 1 + 3.3 * math.log10(n)
        return round(k)
    
    def gerar_intervalos(self):
        """Gera os intervalos de classe"""
        min_val = min(self.dados)
        max_val = max(self.dados)
        amplitude_total = max_val - min_val
        n_classes = self.calcular_numero_classes()
        
        # Ajusta a amplitude para ter intervalos "bonitos"
        amplitude_classe = amplitude_total / n_classes
        amplitude_classe = math.ceil(amplitude_classe * 10) / 10  # Arredonda para cima
        
        # Gera os intervalos
        intervalos = []
        limite_inferior = min_val
        
        for i in range(n_classes):
            # Para a última classe, garantir que inclua o valor máximo
            if i == n_classes - 1:
                limite_superior = max_val
            else:
                limite_superior = limite_inferior + amplitude_classe
            
            if self.tipo_dados == "Discretos":
                # Para dados discretos
                if i == n_classes - 1:
                    # Última classe: inclui ambos os limites [a |-| b]
                    intervalo_str = f"{int(limite_inferior)} |-| {int(limite_superior)}"
                else:
                    # Demais classes: inclui apenas limite inferior [a |- b)
                    intervalo_str = f"{int(limite_inferior)} |- {int(limite_superior)}"
            else:
                # Para dados contínuos
                if i == n_classes - 1:
                    # Última classe: inclui ambos os limites [a |-| b]
                    intervalo_str = f"{limite_inferior:.2f} |-| {limite_superior:.2f}"
                else:
                    # Demais classes: inclui apenas limite inferior [a |- b)
                    intervalo_str = f"{limite_inferior:.2f} |- {limite_superior:.2f}"
            
            intervalos.append({
                'intervalo': intervalo_str,
                'limite_inferior': limite_inferior,
                'limite_superior': limite_superior,
                'frequencia': 0,
                'frequencia_acumulada': 0,
                'ponto_medio': (limite_inferior + limite_superior) / 2,
                'eh_ultima_classe': (i == n_classes - 1),  # Flag para identificar última classe
                'frequencia_relativa': 0,
                'frequencia_relativa_acumulada': 0,
                'frequencia_percentual': 0,
                'frequencia_percentual_acumulada': 0
            })
            
            limite_inferior = limite_superior
        
        return intervalos
    
    def calcular_frequencias(self, intervalos):
        """Calcula todas as frequências para cada intervalo"""
        n_total = len(self.dados)
        
        # Calcula frequência absoluta
        for dado in self.dados:
            for intervalo in intervalos:
                if intervalo['eh_ultima_classe']:
                    # Última classe: inclui ambos os limites [a |-| b]
                    if intervalo['limite_inferior'] <= dado <= intervalo['limite_superior']:
                        intervalo['frequencia'] += 1
                        break
                else:
                    # Demais classes: inclui apenas limite inferior [a |- b)
                    if intervalo['limite_inferior'] <= dado < intervalo['limite_superior']:
                        intervalo['frequencia'] += 1
                        break
        
        # Calcula frequências acumuladas e relativas
        freq_acumulada = 0
        freq_relativa_acumulada = 0
        freq_percentual_acumulada = 0
        
        for intervalo in intervalos:
            # Frequência absoluta acumulada
            freq_acumulada += intervalo['frequencia']
            intervalo['frequencia_acumulada'] = freq_acumulada
            
            # Frequência relativa
            intervalo['frequencia_relativa'] = intervalo['frequencia'] / n_total
            
            # Frequência relativa acumulada
            freq_relativa_acumulada += intervalo['frequencia_relativa']
            intervalo['frequencia_relativa_acumulada'] = freq_relativa_acumulada
            
            # Frequência relativa percentual
            intervalo['frequencia_percentual'] = intervalo['frequencia_relativa'] * 100
            
            # Frequência relativa percentual acumulada
            freq_percentual_acumulada += intervalo['frequencia_percentual']
            intervalo['frequencia_percentual_acumulada'] = freq_percentual_acumulada
        
        return intervalos
    
    def exibir_tabela(self, intervalos_com_freq, estatisticas):
        """Exibe a tabela formatada com todas as frequências"""
        print("\n" + "="*120)
        print("TABELA DE DISTRIBUIÇÃO DE FREQUÊNCIAS COMPLETA")
        print("="*120)
        
        print(f"{'Classe':<6} {'Intervalo':<20} {'Fi':<6} {'Fac':<6} {'Fr':<8} {'Frac':<8} {'F%':<8} {'F%ac':<8} {'Ponto Médio':<12}")
        print("-"*120)
        
        for i, intervalo in enumerate(intervalos_com_freq, 1):
            print(f"{i:<6} {intervalo['intervalo']:<20} "
                  f"{intervalo['frequencia']:<6} "
                  f"{intervalo['frequencia_acumulada']:<6} "
                  f"{intervalo['frequencia_relativa']:<8.4f} "
                  f"{intervalo['frequencia_relativa_acumulada']:<8.4f} "
                  f"{intervalo['frequencia_percentual']:<8.2f}% "
                  f"{intervalo['frequencia_percentual_acumulada']:<8.2f}% "
                  f"{intervalo['ponto_medio']:<12.2f}")
        
        # Linha de total
        print("-"*120)
        total_fi = len(self.dados)
        total_fac = total_fi
        total_fr = 1.0
        total_frac = 1.0
        total_fp = 100.0
        total_fpac = 100.0
        
        print(f"{'Total':<6} {'':<20} "
              f"{total_fi:<6} "
              f"{total_fac:<6} "
              f"{total_fr:<8.4f} "
              f"{total_frac:<8.4f} "
              f"{total_fp:<8.2f}% "
              f"{total_fpac:<8.2f}% "
              f"{'':<12}")
        
        print("\nLEGENDA:")
        print("Fi  = Frequência Absoluta")
        print("Fac = Frequência Absoluta Acumulada")
        print("Fr  = Frequência Relativa")
        print("Frac = Frequência Relativa Acumulada")
        print("F%  = Frequência Relativa Percentual")
        print("F%ac = Frequência Relativa Percentual Acumulada")
        print("\nNOTAÇÃO DOS INTERVALOS:")
        print("a |- b  = Inclui 'a' mas não inclui 'b'")
        print("a |-| b = Inclui ambos 'a' e 'b'")
        
        print("\n" + "="*60)
        print("ESTATÍSTICAS DESCRITIVAS:")
        print("="*60)
        print(f"Quantidade de dados: {len(self.dados)}")
        print(f"Valor mínimo: {estatisticas['min']:.2f}")
        print(f"Valor máximo: {estatisticas['max']:.2f}")
        print(f"Amplitude total: {estatisticas['amplitude']:.2f}")
        print(f"Desvio padrão: {estatisticas['desvio_padrao']:.2f}")
        print(f"Número de classes: {self.calcular_numero_classes()}")
        print(f"Tipo de dados: {self.tipo_dados}")
    
    def gerar_e_exibir_tabela(self):
        """Gera e exibe a tabela completa"""
        if not self.dados:
            print("Nenhum dado foi inserido!")
            return
        
        estatisticas = self.calcular_estatisticas()
        intervalos = self.gerar_intervalos()
        intervalos_com_freq = self.calcular_frequencias(intervalos)
        
        self.exibir_tabela(intervalos_com_freq, estatisticas)

# Função principal
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
            if tabela.dados:
                tabela.gerar_e_exibir_tabela()
            else:
                print("Por favor, insira dados primeiro!")
        elif opcao == '3':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()