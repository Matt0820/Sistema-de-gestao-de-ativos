#classe cliente para armazenar os dados do cliente
class Cliente:
    #metodo construtor para inicializar os atributos do cliente
    def __init__(self, id_cliente, nome, idade, cnh):
        self.id_cliente = id_cliente
        self.nome   = nome
        self.idade  = idade
        self.cnh    = cnh
        
    #metodo para exibir os dados do cliente de forma organizada    
    def exibir_cliente(self):
        print("\nDados do Cliente:")
        print(f"ID do cliente: {self.id_cliente}")
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"CNH: {self.cnh}")