from modelos.ativo import Ativo
from datetime import date
from banco.database import get_connection


class Ativo_Controle:

    def __init__(self):
        self.lista_ativos = []
        self._carregar_ativos()

    # ------------------------------------------------------------------ #
    #  Carregamento inicial do banco de dados                             #
    # ------------------------------------------------------------------ #

    def _carregar_ativos(self):
        """Lê todos os ativos do banco e reconstrói os objetos em memória."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ativos")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            # Cria o objeto sem passar pelo __init__ (que incrementaria o contador)
            ativo = object.__new__(Ativo)
            ativo.id_ativo          = row["id_ativo"]
            ativo.modelo            = row["modelo"]
            ativo.marca             = row["marca"]
            ativo.ano               = row["ano"]
            ativo.placa             = row["placa"]
            ativo.valor             = row["valor"]
            ativo.diaria            = row["diaria"]
            ativo.data_aquisicao    = date.fromisoformat(row["data_aquisicao"])
            ativo.status            = row["status"]
            ativo.depreciacao_final = row["depreciacao_final"]
            self.lista_ativos.append(ativo)

        # Sincroniza o contador de ID da classe com o maior ID persistido
        if self.lista_ativos:
            Ativo.contador_id = max(a.id_ativo for a in self.lista_ativos) + 1

    # ------------------------------------------------------------------ #
    #  Persistência individual                                            #
    # ------------------------------------------------------------------ #

    def _inserir_ativo_db(self, ativo):
        """Insere um novo ativo no banco e atualiza seu id_ativo."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ativos
                (modelo, marca, ano, placa, valor, diaria, data_aquisicao, status, depreciacao_final)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ativo.modelo,
            ativo.marca,
            ativo.ano,
            ativo.placa,
            ativo.valor,
            ativo.diaria,
            ativo.data_aquisicao.isoformat(),
            ativo.status,
            ativo.depreciacao_final,
        ))
        ativo.id_ativo = cursor.lastrowid   # sobrescreve com o ID real do banco
        Ativo.contador_id = ativo.id_ativo + 1
        conn.commit()
        conn.close()

    def _atualizar_ativo_db(self, ativo):
        """Atualiza todos os campos de um ativo existente no banco."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE ativos
            SET modelo=?, marca=?, ano=?, placa=?, valor=?, diaria=?,
                data_aquisicao=?, status=?, depreciacao_final=?
            WHERE id_ativo=?
        ''', (
            ativo.modelo,
            ativo.marca,
            ativo.ano,
            ativo.placa,
            ativo.valor,
            ativo.diaria,
            ativo.data_aquisicao.isoformat(),
            ativo.status,
            ativo.depreciacao_final,
            ativo.id_ativo,
        ))
        conn.commit()
        conn.close()

    def _deletar_ativo_db(self, id_ativo):
        """Remove um ativo do banco pelo seu ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ativos WHERE id_ativo=?", (id_ativo,))
        conn.commit()
        conn.close()

    # ------------------------------------------------------------------ #
    #  Helpers (sem alteração)                                            #
    # ------------------------------------------------------------------ #

    def status_normalizado(self, status):
        return status.strip().lower()

    def buscar_ativo_por_id_ou_placa(self, busca):
        busca = busca.strip().upper()
        for ativo in self.lista_ativos:
            if (busca.isdigit() and ativo.id_ativo == int(busca)) or ativo.placa == busca:
                return ativo
        return None

    def placa_ja_cadastrada(self, placa, id_ignorar=None):
        placa = placa.strip().upper()
        for ativo in self.lista_ativos:
            if ativo.placa == placa and ativo.id_ativo != id_ignorar:
                return True
        return False

    # ------------------------------------------------------------------ #
    #  CRUD                                                               #
    # ------------------------------------------------------------------ #

    def cadastrar_ativo(self):
        print("\n--- CADASTRO DE ATIVO ---")
        modelo = input("Modelo: ").strip()
        marca  = input("Marca: ").strip()

        while True:
            try:
                ano = int(input("Ano: "))
                break
            except ValueError:
                print("Erro: Ano deve ser um número inteiro!")

        while True:
            placa_input = input("Placa: ").strip().upper()
            if self.placa_ja_cadastrada(placa_input):
                print("Erro: Placa já cadastrada!")
            else:
                break

        while True:
            try:
                valor = float(input("Valor: "))
                break
            except ValueError:
                print("Erro: Valor deve ser um número!")

        while True:
            try:
                diaria = float(input("Valor da Diaria: "))
                break
            except ValueError:
                print("Erro: Valor da Diaria deve ser um número!")

        data = date.today()
        novo = Ativo(modelo, marca, ano, placa_input, valor, diaria, data)

        self._inserir_ativo_db(novo)        # ← persiste e corrige id_ativo
        self.lista_ativos.append(novo)
        print("\nAtivo cadastrado com sucesso!")

    def listar_ativos(self):
        if not self.lista_ativos:
            print("\nNenhum ativo cadastrado.")
            return
        print("\n--- LISTA DE ATIVOS ---")
        for ativo in self.lista_ativos:
            ativo.exibir_ativo()

    def editar_ativo(self):
        if not self.lista_ativos:
            print("Nenhum ativo cadastrado.")
            return

        id_editar        = input("Digite o 'ID' ou 'PLACA' do ativo para editar: ")
        ativo_encontrado = self.buscar_ativo_por_id_ou_placa(id_editar)

        if ativo_encontrado is None:
            print("\nAtivo não encontrado.")
            return

        if self.status_normalizado(ativo_encontrado.status) == "alugado":
            print(f"Erro: O ativo {ativo_encontrado.modelo} (ID: {ativo_encontrado.id_ativo}) "
                  f"está atualmente Alugado e não pode ser editado.")
            return

        print("\n--- Editar Ativo ---")
        print("Deixe em branco para manter o valor atual.")

        novo_modelo = input(f"Modelo ({ativo_encontrado.modelo}): ").strip()
        if novo_modelo:
            ativo_encontrado.modelo = novo_modelo

        nova_marca = input(f"Marca ({ativo_encontrado.marca}): ").strip()
        if nova_marca:
            ativo_encontrado.marca = nova_marca

        novo_ano = input(f"Ano ({ativo_encontrado.ano}): ").strip()
        if novo_ano:
            if novo_ano.isdigit():
                ativo_encontrado.ano = int(novo_ano)
            else:
                print("Ano inválido. Mantendo valor atual.")

        nova_placa = input(f"Placa ({ativo_encontrado.placa}): ").strip().upper()
        if nova_placa:
            if self.placa_ja_cadastrada(nova_placa, ativo_encontrado.id_ativo):
                print("Erro: Placa já cadastrada!")
                return
            ativo_encontrado.placa = nova_placa

        novo_valor = input(f"Valor ({ativo_encontrado.valor}): ").strip()
        if novo_valor:
            try:
                ativo_encontrado.valor = float(novo_valor)
            except ValueError:
                print("Valor inválido. Mantendo valor atual.")

        nova_diaria = input(f"Diária ({ativo_encontrado.diaria}): ").strip()
        if nova_diaria:
            try:
                ativo_encontrado.diaria = float(nova_diaria)
            except ValueError:
                print("Diária inválida. Mantendo valor atual.")

        ativo_encontrado.depreciacao_final = ativo_encontrado.calcular_depreciacao()

        self._atualizar_ativo_db(ativo_encontrado)  # ← persiste alterações
        print("\nAtivo atualizado com sucesso!")

    def apagar_ativo(self):
        if not self.lista_ativos:
            print("Nenhum ativo cadastrado.")
            return

        busca            = input("Digite o ID ou PLACA do ativo para apagar: ")
        ativo_encontrado = self.buscar_ativo_por_id_ou_placa(busca)

        if ativo_encontrado is None:
            print("\nAtivo não encontrado.")
            return

        if self.status_normalizado(ativo_encontrado.status) == "alugado":
            print(f"Erro: O ativo {ativo_encontrado.modelo} "
                  f"(ID: {ativo_encontrado.id_ativo}) está Alugado e não pode ser apagado.")
            return

        self._deletar_ativo_db(ativo_encontrado.id_ativo)  # ← remove do banco
        self.lista_ativos.remove(ativo_encontrado)
        print(f"\nAtivo {ativo_encontrado.modelo} "
              f"(ID: {ativo_encontrado.id_ativo}) apagado com sucesso!")

    # ------------------------------------------------------------------ #
    #  Relatórios                                                         #
    # ------------------------------------------------------------------ #

    def relatorio_ativos_disponiveis(self):
        print("\n--- RELATÓRIO DE ATIVOS DISPONÍVEIS ---")
        disponiveis = [a for a in self.lista_ativos
                       if self.status_normalizado(a.status) == "disponível"]
        if not disponiveis:
            print("Nenhum ativo Disponível no momento.")
            return
        for ativo in disponiveis:
            ativo.exibir_ativo()

    def relatorio_ativos_alugados(self):
        print("\n--- RELATÓRIO DE ATIVOS ALUGADOS ---")
        alugados = [a for a in self.lista_ativos
                    if self.status_normalizado(a.status) == "alugado"]
        if not alugados:
            print("Nenhum ativo Alugado no momento.")
            return
        for ativo in alugados:
            ativo.exibir_ativo()
