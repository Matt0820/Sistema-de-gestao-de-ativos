#classe que cuida das manutencoes dos ativos
class Manutencao:
    #metodo construtor para inicializar os atributos da manutencao
    def __init__(self, id_manutencao, ativo, data_manutencao, data_fim, descricao, custo, categoria):
        self.id_manutencao = id_manutencao
        self.ativo = ativo
        self.data_manutencao = data_manutencao
        self.data_fim = data_fim
        self.descricao = descricao
        self.categoria = categoria
        self.custo = custo
        self.status = 'Em andamento' 
    
    #metodo para exibir os dados da manutencao de forma organizada
    def exibir_dados(self):
        print(f"ID da Manutenção: {self.id_manutencao}")
        print(f"Ativo: {self.ativo}")
        print(f"Data da Manutenção: {self.data_manutencao}")
        print(f"Data de Retorno: {self.data_fim}")
        print(f"Descrição: {self.descricao}")
        print(f"Categoria: {self.categoria}")
        print(f"Custo: {self.custo}")
        print(f"Status: {self.status}")