#importa a classe cliente para criar objetos cliente
from modelos.cliente import Cliente


#classe de controle de dados dos clientes, pois um unico controle unico é desnecessárimente extenso e pouluido.
class Cliente_Controle:

    #metodo construtor para inicializar a lista de clientes
    def __init__(self, controle_locacao):
        self.lista_clientes = []
        self.controle_locacao = controle_locacao

    #metodo para buscar cliente pela CNH
    def buscar_cliente_por_cnh(self, cnh):
        cnh = cnh.strip()
        for cliente in self.lista_clientes:
            if cliente.cnh == cnh:
                return cliente
        return None

    #metodo para verificar se a CNH já está cadastrada
    def cnh_ja_cadastrada(self, cnh):
        cnh = cnh.strip()
        for cliente in self.lista_clientes:
            if cliente.cnh == cnh:
                return True
        return False

    #metodo para verificar se o cliente possui locação ativa
    def cliente_possui_locacao_ativa(self, cnh):
        for locacao in self.controle_locacao.lista_locacoes:
            if locacao.cliente.cnh == cnh and locacao.status == "Ativa":
                return True
        return False

    #metodo para cadastrar um novo cliente, solicitando os dados ao usuário
    def cadastrar_cliente(self):
        print("\n--- CADASTRO DE CLIENTE ---")

        # Validar o nome, garantindo que seja composto apenas por letras e espaços
        while True:
            nome = input("Nome: ").strip()
            if nome.replace(" ", "").isalpha():
                break
            print("Nome inválido! Use apenas letras.")

        # Validar a idade, garantindo que seja um número inteiro e maior ou igual a 18
        while True:
            try:
                idade = int(input("Idade: "))
                if idade >= 18:
                    break
                print("Idade inválida! O cliente deve ser maior de idade.")
            except ValueError:
                print("A idade precisa ser um numero.")

        # Validar a CNH, garantindo que seja composta por 9 dígitos numéricos e que seja única na lista de clientes
        while True:
            cnh = input("CNH: ").strip()

            if len(cnh) != 9 or not cnh.isdigit():
                print("A CNH está inválida. Tente novamente.")
                continue

            if self.cnh_ja_cadastrada(cnh):
                print("Erro: CNH já cadastrada!")
            else:
                break

        # Se a CNH for válida e única, criar um novo objeto Cliente e adicioná-lo à lista de clientes
        novo_cliente = Cliente(nome, idade, cnh)
        self.lista_clientes.append(novo_cliente)
        print("\nCliente cadastrado com sucesso!")

    #metodo para listar os clientes cadastrados, exibindo seus dados
    def listar_clientes(self):
        if len(self.lista_clientes) == 0:
            print("\nNenhum cliente cadastrado.")
            return

        print("\n--- LISTA DE CLIENTES ---")
        for cliente in self.lista_clientes:
            cliente.exibir_cliente()

    #metodo para editar os dados de um cliente
    def editar_cliente(self):
        if len(self.lista_clientes) == 0:
            print("\nNenhum cliente cadastrado.")
            return

        cnh_busca = input("Digite a CNH do cliente para editar: ").strip()
        cliente = self.buscar_cliente_por_cnh(cnh_busca)

        if cliente is None:
            print("\nCliente não encontrado.")
            return

        if self.cliente_possui_locacao_ativa(cliente.cnh):
            print(f"Erro: O cliente {cliente.nome} (CNH: {cliente.cnh}) está com uma locação ativa e não pode ser editado.")
            return

        print("\n--- EDITAR CLIENTE ---")
        print("Deixe em branco para manter o valor atual.")

        # Validar o nome, garantindo que seja composto apenas por letras e espaços
        while True:
            nome = input(f"Novo Nome ({cliente.nome}): ").strip()
            if nome == "":
                nome = cliente.nome
                break

            if nome.replace(" ", "").isalpha():
                break

            print("Nome inválido! Use apenas letras.")

        # Validar a idade, garantindo que seja um número inteiro e maior ou igual a 18
        while True:
            idade_input = input(f"Nova Idade ({cliente.idade}): ").strip()

            if idade_input == "":
                idade = cliente.idade
                break

            if idade_input.isdigit() and int(idade_input) >= 18:
                idade = int(idade_input)
                break

            print("Idade inválida!")

        # Atualizar os dados do cliente com os novos valores
        cliente.nome = nome
        cliente.idade = idade
        print("\nCliente atualizado com sucesso!")

    #apagar cliente
    def apagar_cliente(self):
        if len(self.lista_clientes) == 0:
            print("\nNenhum cliente cadastrado.")
            return

        cnh_apagar = input("Digite a CNH do cliente para apagar: ").strip()
        cliente = self.buscar_cliente_por_cnh(cnh_apagar)

        if cliente is None:
            print("\nCliente não encontrado.")
            return

        if self.cliente_possui_locacao_ativa(cliente.cnh):
            print(f"Erro: O cliente {cliente.nome} (CNH: {cliente.cnh}) está com uma locação ativa e não pode ser apagado.")
            return

        self.lista_clientes.remove(cliente)
        print(f"\nCliente com CNH {cnh_apagar} apagado com sucesso!")

    #metodo para buscar um cliente cadastrado
    def buscar_cliente(self):
        if len(self.lista_clientes) == 0:
            print("\nNenhum cliente cadastrado.")
            return

        cnh_cliente = input("\nDigite a CNH do cliente: ").strip()
        cliente = self.buscar_cliente_por_cnh(cnh_cliente)

        if cliente is None:
            print("\nCliente não encontrado.")
            return

        cliente.exibir_cliente()

    def relatorio_clientes_ativos(self):
        print("\n--- RELATÓRIO DE CLIENTES ATIVOS ---")

        clientes_ativos = []

        # percorre todas as locações
        for locacao in self.controle_locacao.lista_locacoes:
            if locacao.status == "Ativa" and locacao.cliente not in clientes_ativos:
                clientes_ativos.append(locacao.cliente)

        if not clientes_ativos:
            print("Não há clientes com locações ativas no momento.")
            return

        for cliente in clientes_ativos:
            cliente.exibir_cliente()
