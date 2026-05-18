from modelos.cliente import Cliente
from banco.database import get_connection


class Cliente_Controle:

    def __init__(self, controle_locacao):
        self.lista_clientes    = []
        self.controle_locacao  = controle_locacao
        self._carregar_clientes()

    # ------------------------------------------------------------------ #
    #  Carregamento inicial do banco de dados                             #
    # ------------------------------------------------------------------ #

    def _carregar_clientes(self):
        """Lê todos os clientes do banco e reconstrói os objetos em memória."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            cliente = Cliente(row["nome"], row["idade"], row["cnh"])
            self.lista_clientes.append(cliente)

    # ------------------------------------------------------------------ #
    #  Persistência individual                                            #
    # ------------------------------------------------------------------ #

    def _inserir_cliente_db(self, cliente):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (cnh, nome, idade) VALUES (?, ?, ?)",
            (cliente.cnh, cliente.nome, cliente.idade),
        )
        conn.commit()
        conn.close()

    def _atualizar_cliente_db(self, cliente):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clientes SET nome=?, idade=? WHERE cnh=?",
            (cliente.nome, cliente.idade, cliente.cnh),
        )
        conn.commit()
        conn.close()

    def _deletar_cliente_db(self, cnh):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE cnh=?", (cnh,))
        conn.commit()
        conn.close()

    # ------------------------------------------------------------------ #
    #  Helpers (sem alteração)                                            #
    # ------------------------------------------------------------------ #

    def buscar_cliente_por_cnh(self, cnh):
        cnh = cnh.strip()
        for cliente in self.lista_clientes:
            if cliente.cnh == cnh:
                return cliente
        return None

    def cnh_ja_cadastrada(self, cnh):
        return self.buscar_cliente_por_cnh(cnh) is not None

    def cliente_possui_locacao_ativa(self, cnh):
        for locacao in self.controle_locacao.lista_locacoes:
            if locacao.cliente.cnh == cnh and locacao.status == "Ativa":
                return True
        return False

    # ------------------------------------------------------------------ #
    #  CRUD                                                               #
    # ------------------------------------------------------------------ #

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
                print("A idade precisa ser um número.")

        while True:
            cnh = input("CNH: ").strip()
            if len(cnh) != 9 or not cnh.isdigit():
                print("A CNH está inválida. Tente novamente.")
                continue
            if self.cnh_ja_cadastrada(cnh):
                print("Erro: CNH já cadastrada!")
            else:
                break

        novo_cliente = Cliente(nome, idade, cnh)
        self._inserir_cliente_db(novo_cliente)   # ← persiste
        self.lista_clientes.append(novo_cliente)
        print("\nCliente cadastrado com sucesso!")

    def listar_clientes(self):
        if not self.lista_clientes:
            print("\nNenhum cliente cadastrado.")
            return
        print("\n--- LISTA DE CLIENTES ---")
        for cliente in self.lista_clientes:
            cliente.exibir_cliente()

    def editar_cliente(self):
        if not self.lista_clientes:
            print("\nNenhum cliente cadastrado.")
            return

        cnh_busca = input("Digite a CNH do cliente para editar: ").strip()
        cliente   = self.buscar_cliente_por_cnh(cnh_busca)

        if cliente is None:
            print("\nCliente não encontrado.")
            return

        if self.cliente_possui_locacao_ativa(cliente.cnh):
            print(f"Erro: O cliente {cliente.nome} (CNH: {cliente.cnh}) "
                  f"está com uma locação ativa e não pode ser editado.")
            return

        print("\n--- EDITAR CLIENTE ---")
        print("Deixe em branco para manter o valor atual.")

        while True:
            nome = input(f"Novo Nome ({cliente.nome}): ").strip()
            if nome == "":
                nome = cliente.nome
                break
            if nome.replace(" ", "").isalpha():
                break
            print("Nome inválido! Use apenas letras.")

        while True:
            idade_input = input(f"Nova Idade ({cliente.idade}): ").strip()
            if idade_input == "":
                idade = cliente.idade
                break
            if idade_input.isdigit() and int(idade_input) >= 18:
                idade = int(idade_input)
                break
            print("Idade inválida!")

        cliente.nome  = nome
        cliente.idade = idade
        self._atualizar_cliente_db(cliente)   # ← persiste alterações
        print("\nCliente atualizado com sucesso!")

    def apagar_cliente(self):
        if not self.lista_clientes:
            print("\nNenhum cliente cadastrado.")
            return

        cnh_apagar = input("Digite a CNH do cliente para apagar: ").strip()
        cliente    = self.buscar_cliente_por_cnh(cnh_apagar)

        if cliente is None:
            print("\nCliente não encontrado.")
            return

        if self.cliente_possui_locacao_ativa(cliente.cnh):
            print(f"Erro: O cliente {cliente.nome} (CNH: {cliente.cnh}) "
                  f"está com uma locação ativa e não pode ser apagado.")
            return

        self._deletar_cliente_db(cnh_apagar)    # ← remove do banco
        self.lista_clientes.remove(cliente)
        print(f"\nCliente com CNH {cnh_apagar} apagado com sucesso!")

    def buscar_cliente(self):
        if not self.lista_clientes:
            print("\nNenhum cliente cadastrado.")
            return

        cnh_cliente = input("\nDigite a CNH do cliente: ").strip()
        cliente     = self.buscar_cliente_por_cnh(cnh_cliente)

        if cliente is None:
            print("\nCliente não encontrado.")
            return

        cliente.exibir_cliente()

    def relatorio_clientes_ativos(self):
        print("\n--- RELATÓRIO DE CLIENTES ATIVOS ---")
        clientes_ativos = []
        for locacao in self.controle_locacao.lista_locacoes:
            if locacao.status == "Ativa" and locacao.cliente not in clientes_ativos:
                clientes_ativos.append(locacao.cliente)

        if not clientes_ativos:
            print("Não há clientes com locações ativas no momento.")
            return

        for cliente in clientes_ativos:
            cliente.exibir_cliente()
