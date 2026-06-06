from dados import database
import re
class Cliente_Controle:

    def __init__(self, controle_locacao=None):
        database.iniciar_banco()
        self.controle_locacao = controle_locacao
        
    def buscar_cliente_por_id_ou_cnh(self, cnh):
        return database.buscar_cliente_por_id_ou_cnh(cnh.strip())

    def buscar_cliente_por_cnh(self, cnh):
        return database.buscar_cliente_por_cnh(cnh.strip())

    def cnh_ja_cadastrada(self, cnh):
        return database.verificar_cnh_existente(cnh.strip())

    def cliente_possui_locacao_ativa(self, cliente):
        """Verifica se um cliente (dict) possui alguma locação ativa pelo id_cliente."""
        locacoes_ativas = database.listar_locacoes_ativas()
        for loc in locacoes_ativas:
            if loc.get('id_cliente') == cliente.get('id_cliente'):
                return True
        return False

    def exibir_cliente(self, cliente):
        print(f"ID: {cliente.get('id_cliente')}")
        print(f"Nome: {cliente.get('nome')}")
        print(f"Idade: {cliente.get('idade')}")
        print(f"CNH: {cliente.get('cnh')}")
        print("-" * 30)

    def cadastrar_cliente(self):
        print("\n--- CADASTRO DE CLIENTE ---")

        while True:
            nome = input("Nome: ").strip()
            if re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", nome) and nome.strip():
                break
            print("Nome inválido! Use apenas letras.")

        while True:
            try:
                idade = int(input("Idade: "))
                if idade >= 18:
                    break
                print("Idade inválida! O cliente deve ser maior de idade.")
            except ValueError:
                print("A idade precisa ser um número.")

        while True:
            cnh = input("CNH: ").strip()
            if len(cnh) != 11 or not cnh.isdigit():
                print("CNH inválida! Deve conter exatamente 11 dígitos numéricos.")
                continue
            if self.cnh_ja_cadastrada(cnh):
                print("Erro: CNH já cadastrada!")
            else:
                break

        database.cadastrar_cliente(nome, idade, cnh)
        print("\nCliente cadastrado com sucesso!")

    def listar_clientes(self):
        clientes = database.listar_clientes()
        if not clientes:
            print("\nNenhum cliente cadastrado.")
            return

        print("\n--- LISTA DE CLIENTES ---")
        for c in clientes:
            self.exibir_cliente(c)

    def editar_cliente(self):
        if not database.listar_clientes():
            print("\nNenhum cliente cadastrado.")
            return

        cnh_busca = input("Digite a CNH do cliente para editar: ").strip()
        cliente = self.buscar_cliente_por_cnh(cnh_busca)
        if cliente is None:
            print("\nCliente não encontrado.")
            return

        if self.cliente_possui_locacao_ativa(cliente):
            print(f"Erro: O cliente {cliente.get('nome')} (CNH: {cliente.get('cnh')}) "
                f"está com uma locação ativa e não pode ser editado.")
            return

        print("\n--- EDITAR CLIENTE ---")
        print("Deixe em branco para manter o valor atual.")

        nome = input(f"Novo Nome ({cliente.get('nome')}): ").strip()
        idade_input = input(f"Nova Idade ({cliente.get('idade')}): ").strip()

        dados = {}
        if nome:
            if re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", nome):
                dados['nome'] = nome
            else:
                print("Nome inválido! Mantendo valor atual.")
        if idade_input:
            if idade_input.isdigit() and int(idade_input) >= 18:
                dados['idade'] = int(idade_input)
            else:
                print("Idade inválida! Mantendo valor atual.")

        if dados:
            database.atualizar_cliente(cliente.get('id_cliente'), dados)
            print("\nCliente atualizado com sucesso!")
        else:
            print("Nenhuma alteração informada.")

    def apagar_cliente(self):
        if not database.listar_clientes():
            print("\nNenhum cliente cadastrado.")
            return

        busca = input("Digite a CNH ou ID do cliente para apagar: ").strip()
        cliente = self.buscar_cliente_por_id_ou_cnh(busca)

        if cliente is None:
            print("\nCliente não encontrado.")
            return

        if self.cliente_possui_locacao_ativa(cliente):
            print(f"Erro: O cliente {cliente.get('nome')} (CNH: {cliente.get('cnh')}) "
                f"está com uma locação ativa e não pode ser apagado." )
            return

        database.apagar_cliente(cliente.get('id_cliente'))
        print(f"\nCliente {cliente.get('nome')} (ID: {cliente.get('id_cliente')}) apagado com sucesso!")

    def buscar_cliente(self):
        if not database.listar_clientes():
            print("\nNenhum cliente cadastrado.")
            return

        cnh_cliente = input("\nDigite a CNH do cliente: ").strip()
        cliente = self.buscar_cliente_por_cnh(cnh_cliente)
        if cliente is None:
            print("\nCliente não encontrado.")
            return

        self.exibir_cliente(cliente)