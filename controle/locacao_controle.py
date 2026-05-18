from modelos.locacao import Locacao
from datetime import datetime, timedelta, date
from banco.database import get_connection


class Locacao_Controle:

    def __init__(self, controle_cliente=None, controle_ativo=None):
        self.lista_locacoes    = []
        self.controle_cliente  = controle_cliente
        self.controle_ativo    = controle_ativo
        # Nota: carregar_locacoes() é chamado de main.py após todos os
        # controles estarem prontos, para garantir que clientes e ativos
        # já estejam carregados antes de reconstruir as locações.

    # ------------------------------------------------------------------ #
    #  Carregamento inicial do banco de dados                             #
    # ------------------------------------------------------------------ #

    def carregar_locacoes(self):
        """
        Lê todas as locações do banco e reconstrói os objetos em memória.
        Deve ser chamado após controle_cliente e controle_ativo estarem
        totalmente inicializados.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM locacoes")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            cliente = self.controle_cliente.buscar_cliente_por_cnh(row["cnh_cliente"])
            ativo   = self.controle_ativo.buscar_ativo_por_id_ou_placa(str(row["id_ativo"]))

            if cliente is None or ativo is None:
                # Registo órfão — ignora (integridade referencial protege no banco)
                continue

            # Constrói o objeto sem chamar __init__ (que alteraria status do ativo)
            locacao = object.__new__(Locacao)
            locacao.id_locacao  = row["id_locacao"]
            locacao.cliente     = cliente
            locacao.ativo       = ativo
            locacao.data_inicio = date.fromisoformat(row["data_inicio"])
            locacao.duracao     = row["duracao"]
            locacao.data_fim    = date.fromisoformat(row["data_fim"])
            locacao.valor       = row["valor"]
            locacao.status      = row["status"]
            self.lista_locacoes.append(locacao)

        # Sincroniza o contador de ID com o maior ID persistido
        if self.lista_locacoes:
            Locacao.contador_id_L = max(l.id_locacao for l in self.lista_locacoes) + 1

    # ------------------------------------------------------------------ #
    #  Persistência individual                                            #
    # ------------------------------------------------------------------ #

    def _inserir_locacao_db(self, locacao):
        """Insere uma nova locação no banco e atualiza seu id_locacao."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO locacoes
                (cnh_cliente, id_ativo, data_inicio, duracao, data_fim, valor, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            locacao.cliente.cnh,
            locacao.ativo.id_ativo,
            locacao.data_inicio.isoformat(),
            locacao.duracao,
            locacao.data_fim.isoformat(),
            locacao.valor,
            locacao.status,
        ))
        locacao.id_locacao = cursor.lastrowid
        Locacao.contador_id_L = locacao.id_locacao + 1
        conn.commit()
        conn.close()

    def _atualizar_status_locacao_db(self, id_locacao, novo_status):
        """Atualiza apenas o status de uma locação."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE locacoes SET status=? WHERE id_locacao=?",
            (novo_status, id_locacao),
        )
        conn.commit()
        conn.close()

    def _atualizar_status_ativo_db(self, id_ativo, novo_status):
        """Atualiza o status de um ativo (chamado ao alugar/devolver)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE ativos SET status=? WHERE id_ativo=?",
            (novo_status, id_ativo),
        )
        conn.commit()
        conn.close()

    # ------------------------------------------------------------------ #
    #  Operações (sem alteração na lógica de negócio)                    #
    # ------------------------------------------------------------------ #

    def realizar_locacao(self):
        print("\n--- NOVA LOCAÇÃO ---")
        cnh_busca = input("CNH do Cliente: ").strip()

        for loc in self.lista_locacoes:
            if loc.cliente.cnh == cnh_busca and loc.status == "Ativa":
                print("Erro: Cliente já possui uma locação ativa!")
                return

        cliente_alvo = self.controle_cliente.buscar_cliente_por_cnh(cnh_busca)
        if cliente_alvo is None:
            print("Erro: Cliente não encontrado!")
            return

        busca_ativo = input("Digite o 'ID' ou 'PLACA' do ativo para locação: ").strip().upper()
        ativo_alvo  = self.controle_ativo.buscar_ativo_por_id_ou_placa(busca_ativo)

        if ativo_alvo is None:
            print("Erro: Ativo não encontrado.")
            return
        if ativo_alvo.status != "Disponível":
            print("Erro: Ativo não está disponível para locação.")
            return

        while True:
            duracao_input = input("Duração em Dias: ").strip()
            if duracao_input.isdigit() and int(duracao_input) > 0:
                duracao = int(duracao_input)
                break
            print("Duração inválida! Digite um número inteiro maior que zero.")

        while True:
            d_ini = input("Digite a Data de Inicio (DD/MM/AAAA): ").strip()
            try:
                data_inicio = datetime.strptime(d_ini, "%d/%m/%Y").date()
                break
            except ValueError:
                print("Erro: Formato inválido! Por favor, use o formato DD/MM/AAAA.")

        valor    = ativo_alvo.diaria * duracao
        data_fim = data_inicio + timedelta(days=duracao)

        nova_loc = Locacao(cliente_alvo, ativo_alvo, data_inicio, duracao, data_fim, valor)

        # Persiste locação e status do ativo
        self._inserir_locacao_db(nova_loc)
        self._atualizar_status_ativo_db(ativo_alvo.id_ativo, "Alugado")

        self.lista_locacoes.append(nova_loc)
        print("Locação realizada com sucesso!")

    def finalizar_locacao(self):
        if not self.lista_locacoes:
            print("Nenhuma locação registrada.")
            return

        try:
            id_loc = int(input("Digite o ID (Número) da locação para finalizar: "))
        except ValueError:
            print("ID inválido.")
            return

        for loc in self.lista_locacoes:
            if loc.id_locacao == id_loc:
                if loc.status == "Finalizada":
                    print(f"Locação {id_loc} já está finalizada.")
                    return
                loc.finalizar()   # atualiza objetos em memória

                # Persiste os dois status alterados
                self._atualizar_status_locacao_db(id_loc, "Finalizada")
                self._atualizar_status_ativo_db(loc.ativo.id_ativo, "Disponível")

                print(f"Locação {id_loc} encerrada!")
                return

        print("Locação não encontrada.")

    def listar_locacoes(self):
        if not self.lista_locacoes:
            print("Nenhuma locação registrada.")
            return
        print("\n--- LISTA DE LOCAÇÕES ---")
        for locacao in self.lista_locacoes:
            locacao.exibir_locacao()
