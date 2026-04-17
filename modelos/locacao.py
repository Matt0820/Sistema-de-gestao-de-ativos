#classe locação para armazenar os dados da locação
class Locacao:

    #contador de id para cada locação cadastrada
    contador_id_L = 0
    
    #metodo construtor para inicializar os atributos da locação
    def __init__(self, cliente_obj, ativo_obj, data_ini, duracao, data_fim, valor):
        
        # Gerador de ID automático para a locação
        self.id_locacao = Locacao.contador_id_L
        Locacao.contador_id_L += 1
        self.cliente = cliente_obj  # Objeto da classe Cliente
        self.ativo = ativo_obj      # Objeto da classe Ativo
        self.data_inicio = data_ini
        self.duracao = duracao
        self.data_fim = data_fim
        self.valor = valor
        self.status = "Ativa" #Locação: formatar pra "Ativa"
        self.ativo.status = "Alugado"

    #metodo para encerrar o contrato e liberar o veículo
    def finalizar(self):
        self.status = "Finalizada"
        self.ativo.status = "Disponível"

    #metodo para exibir os dados da locação de forma organizada
    def exibir_locacao(self):
        print(f"\nID Locação: {self.id_locacao} | Status: {self.status}")
        print(f"Cliente: {self.cliente.nome} (CNH: {self.cliente.cnh})")
        print(f"Veículo: {self.ativo.modelo} (Placa: {self.ativo.placa})")
        print(f"Duração: {self.duracao}")
        print(f"Período: {self.data_inicio} até {self.data_fim}")
        print(f"Valor Total: R$ {self.valor:.2f}")