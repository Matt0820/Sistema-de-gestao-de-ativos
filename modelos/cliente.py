#classe cliente para armazenar os dados do cliente
class Cliente:

    #metodo construtor para inicializar os atributos do cliente
    def __init__(self, nome, idade, cnh):
        self.nome   = nome
        self.idade  = idade
        self.cnh    = cnh
        
    #metodo para exibir os dados do cliente de forma organizada    
    def exibir_cliente(self):
        print("\nDados do Cliente:")
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"CNH: {self.cnh}")