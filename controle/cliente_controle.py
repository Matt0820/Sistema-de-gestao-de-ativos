#importa a classe cliente para criar objetos cliente
from dados import database


#classe de controle de dados dos clientes, ajustada para usar o banco de dados e dicts
class Cliente_Controle:

    def __init__(self, controle_locacao=None):
        database.iniciar_banco()
        self.controle_locacao = controle_locacao

    def buscar_cliente_por_cnh(self, cnh):
        cnh = cnh.strip()
        return database.buscar_cliente_por_cnh(cnh)

    def cnh_ja_cadastrada(self, cnh):
        cnh = cnh.strip()
        return database.verificar_cnh_existente(cnh)

    def cliente_possui_locacao_ativa(self, cnh):
        ativos = database.listar_locacoes_ativas()
        for loc in ativos:
            if loc.get('cliente_obj') == cnh:
                return True
        return False

    def cadastrar_cliente(self):
        print("\n--- CADASTRO DE CLIENTE ---")

        while True:
            nome = input("Nome: ").strip()
            if nome.replace(" ", "").isalpha():
                break
            print("Nome inválido! Use apenas letras.")

        while True:
            try:
                idade = int(input("Idade: "))
                if idade >= 18:
                    break
                print("Idade inválida! O cliente deve ser maior de idade.")
            except ValueError:
                print("A idade precisa ser um numero.")

        while True:
            cnh = input("CNH: ").strip()
            if len(cnh) != 9 or not cnh.isdigit():
                print("A CNH está inválida. Tente novamente.")
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
            print(f"ID: {c.get('id_transacao_mensal')}")
            print(f"Nome: {c.get('nome')}")
            print(f"Idade: {c.get('idade')}")
            print(f"CNH: {c.get('cnh')}")
            print("-" * 30)

    def editar_cliente(self):
        clientes = database.listar_clientes()
        if not clientes:
            print("\nNenhum cliente cadastrado.")
            return

        cnh_busca = input("Digite a CNH do cliente para editar: ").strip()
        cliente = self.buscar_cliente_por_cnh(cnh_busca)
        if cliente is None:
            print("\nCliente não encontrado.")
            return

        if self.cliente_possui_locacao_ativa(cliente.get('cnh')):
            print(f"Erro: O cliente {cliente.get('nome')} (CNH: {cliente.get('cnh')}) está com uma locação ativa e não pode ser editado.")
            return

        print("\n--- EDITAR CLIENTE ---")
        print("Deixe em branco para manter o valor atual.")

        nome = input(f"Novo Nome ({cliente.get('nome')}): ").strip()
        idade_input = input(f"Nova Idade ({cliente.get('idade')}): ").strip()

        dados = {}
        if nome:
            if nome.replace(" ", "").isalpha():
                dados['nome'] = nome
            else:
                print("Nome inválido! Mantendo valor atual.")
        if idade_input:
            if idade_input.isdigit() and int(idade_input) >= 18:
                dados['idade'] = int(idade_input)
            else:
                print("Idade inválida! Mantendo valor atual.")

        if dados:
            database.atualizar_cliente(cliente.get('id_transacao_mensal'), dados)
            print("\nCliente atualizado com sucesso!")
        else:
            print("Nenhuma alteração informada.")

    def apagar_cliente(self):
        clientes = database.listar_clientes()
        if not clientes:
            print("\nNenhum cliente cadastrado.")
            return

        cnh_apagar = input("Digite a CNH do cliente para apagar: ").strip()
        cliente = self.buscar_cliente_por_cnh(cnh_apagar)
        if cliente is None:
            print("\nCliente não encontrado.")
            return

        if self.cliente_possui_locacao_ativa(cliente.get('cnh')):
            print(f"Erro: O cliente {cliente.get('nome')} (CNH: {cliente.get('cnh')}) está com uma locação ativa e não pode ser apagado.")
            return

        database.apagar_cliente(cliente.get('id_transacao_mensal'))
        print(f"\nCliente com CNH {cnh_apagar} apagado com sucesso!")

    def buscar_cliente(self):
        clientes = database.listar_clientes()
        if not clientes:
            print("\nNenhum cliente cadastrado.")
            return

        cnh_cliente = input("\nDigite a CNH do cliente: ").strip()
        cliente = self.buscar_cliente_por_cnh(cnh_cliente)
        if cliente is None:
            print("\nCliente não encontrado.")
            return

        print(f"\nID: {cliente.get('id_transacao_mensal')}")
        print(f"Nome: {cliente.get('nome')}")
        print(f"Idade: {cliente.get('idade')}")
        print(f"CNH: {cliente.get('cnh')}")

    def relatorio_clientes_ativos(self):
        print("\n--- RELATÓRIO DE CLIENTES ATIVOS ---")

        locacoes_ativas = database.listar_locacoes_ativas()
        clientes_ativos = []
        for loc in locacoes_ativas:
            cnh = loc.get('cliente_obj')
            if cnh and cnh not in clientes_ativos:
                clientes_ativos.append(cnh)

        if not clientes_ativos:
            print("Não há clientes com locações ativas no momento.")
            return

        for cnh in clientes_ativos:
            cliente = database.buscar_cliente_por_cnh(cnh)
            if cliente:
                print(f"ID: {cliente.get('id_transacao_mensal')}")
                print(f"Nome: {cliente.get('nome')}")
                print(f"CNH: {cliente.get('cnh')}")
                print("-" * 30)
