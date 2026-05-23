class Manutencao:
    def __init__(self, id_manutencao, ativo, data_manutencao, data_fim, descricao, custo):
        self.id_manutencao = id_manutencao
        self.ativo = ativo
        self.data_manutencao = data_manutencao
        self.data_fim = data_fim
        self.descricao = descricao
        self.custo = custo
        self.status = 'Em andamento'  # Status inicial da manutenção
    
    def exibir_dados(self):
        print(f"ID da Manutenção: {self.id_manutencao}")
        print(f"Ativo: {self.ativo}")
        print(f"Data da Manutenção: {self.data_manutencao}")
        print(f"Data de Retorno: {self.data_fim}")
        print(f"Descrição: {self.descricao}")
        print(f"Custo: {self.custo}")
        print(f"Status: {self.status}")