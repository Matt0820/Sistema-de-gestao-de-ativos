#importa datetime pra calcular a depreciação
from datetime import datetime


#classe principal do ativo
class Ativo:
    #contador de id para cada ativo cadastrado
    contador_id = 0

    #metodo construtor para inicializar os atributos do ativo
    def __init__(self, modelo, marca, ano, placa, valor, diaria, data_aquisicao):

        self.id_ativo = Ativo.contador_id
        Ativo.contador_id += 1
        self.modelo = modelo
        self.marca = marca
        self.ano = ano
        self.placa = placa
        self.valor = valor
        self.diaria = diaria
        self.data_aquisicao = data_aquisicao
        self.status = "Disponível"
        self.depreciacao_final = self.calcular_depreciacao()

    #metodo para calcular a depreciação do ativo com base no tempo de uso
    def calcular_depreciacao(self):
        data_atual = datetime.now().date()
        tempo_uso = (data_atual - self.data_aquisicao).days / 365
        taxa_depreciacao = 0.20

        for i in range(1, 6):
            if tempo_uso < i:
                valor_depreciado = self.valor * (1 - taxa_depreciacao * i)
                return max(valor_depreciado, 0)

        return 0

    #metodo para exibir os dados do ativo de forma organizada
    def exibir_ativo(self):
        print(f"\n--- Dados do Ativo [{self.id_ativo}] ---")
        print(f"ID do ativo: {self.id_ativo}")
        print(f"Modelo/Marca: {self.modelo} / {self.marca}")
        print(f"Ano: {self.ano} | Placa: {self.placa}")
        print(f"Data de Aquisição: {self.data_aquisicao}")
        print(f"Valor Original: R$ {self.valor:.2f}")
        print(f"Valor Atual (Depreciado): R$ {self.depreciacao_final:.2f}")
        print(f"Valor da Diaria: R$ {self.diaria:.2f}")
        print(f"Status: {self.status}")
