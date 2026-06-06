from dados import database
from datetime import datetime

class Manutencao_Controle:
    """Controller para fluxos de manutenção (CRUD + finalização)."""

    def __init__(self):
        database.iniciar_banco()

    def buscar_manutencao_por_id(self, manutencao_id):
        if isinstance(manutencao_id, str):
            manutencao_id = manutencao_id.strip()
        return database.buscar_manutencao_por_id(manutencao_id)

    def exibir_manutencao(self, manutencao):
        print(f"ID Manutenção: {manutencao.get('id_manutencao')}")
        print(f"Ativo ID: {manutencao.get('id_ativo')}")
        print(f"Categoria: {manutencao.get('categoria')}")
        print(f"Descrição: {manutencao.get('descricao')}")
        print(f"Data de Início: {manutencao.get('data')}")
        print(f"Data de Retorno: {manutencao.get('data_fim')}")
        print(f"Custo: R$ {manutencao.get('custo', 0):.2f}")
        print(f"Status: {manutencao.get('status')}")
        print("-" * 30)

    def criar_manutencao(self):
        print("\n--- NOVA MANUTENÇÃO ---")

        try:
            id_ativo = int(input("Digite o ID do ativo em manutenção: "))
        except ValueError:
            print("ID inválido, tente novamente.")
            return

        ativo = database.buscar_ativo_por_id(id_ativo)
        if not ativo:
            print("Ativo não encontrado!")
            return

        status = (ativo.get('status') or '').strip().lower()
        if status == 'alugado':
            print(f"Erro: O ativo {ativo.get('modelo')} está alugado e não pode entrar em manutenção.")
            return

        print(f"Ativo encontrado: {ativo.get('modelo')} ({ativo.get('placa')})")
        categoria = input("Categoria da manutenção (opcional; deixe em branco para inferir): ").strip()
        descricao = input("Serviço a ser realizado: ").strip()

        while True:
            d_ini = input("Data de Início (DD/MM/AAAA): ").strip()
            try:
                data_inicio = datetime.strptime(d_ini, "%d/%m/%Y").date()
                break
            except ValueError:
                print("Erro: Formato inválido! Use DD/MM/AAAA.")

        while True:
            d_fim = input("Data de Retorno (DD/MM/AAAA): ").strip()
            try:
                data_fim = datetime.strptime(d_fim, "%d/%m/%Y").date()
                if data_fim < data_inicio:
                    print("A data de retorno não pode ser anterior à data de início.")
                    continue
                break
            except ValueError:
                print("Erro: Formato inválido! Use DD/MM/AAAA.")

        while True:
            try:
                custo = float(input("Custo da manutenção: R$ "))
                if custo < 0:
                    print("Custo inválido!")
                    continue
                break
            except ValueError:
                print("Valor inválido, tente novamente.")

        database.inserir_manutencao(id_ativo, categoria, data_inicio, data_fim, descricao, custo)
        database.atualizar_ativo(id_ativo, {'status': 'Manutenção'})
        print("\nManutenção cadastrada com sucesso!")

    def listar_manutencao(self):
        manutencoes = database.listar_manutencoes()
        if not manutencoes:
            print("\nNenhuma manutenção cadastrada.")
            return

        print("\n--- LISTA DE MANUTENÇÕES ---")
        for m in manutencoes:
            ativo = database.buscar_ativo_por_id(m.get('id_ativo'))
            nome_ativo = (f"{ativo.get('modelo')} - {ativo.get('placa')} (ID {ativo.get('id_ativo')})"
                          if ativo else f"ID {m.get('id_ativo')} não encontrado")
            print(f"ID Manutenção: {m.get('id_manutencao')}")
            print(f"Ativo: {nome_ativo}")
            print(f"Categoria: {m.get('categoria')}")
            print(f"Descrição: {m.get('descricao')}")
            print(f"Data de Entrada: {m.get('data')}")
            print(f"Data de Retorno: {m.get('data_fim')}")
            print(f"Custo: R$ {m.get('custo', 0):.2f}")
            print("-" * 30)

    def finalizar_manutencao(self):
        ativas = database.listar_manutencoes_ativas()
        if not ativas:
            print("\nNenhuma manutenção ativa no momento.")
            return

        print("\n--- MANUTENÇÕES ATIVAS ---")
        for m in ativas:
            ativo = database.buscar_ativo_por_id(m.get('id_ativo'))
            nome_ativo = (f"{ativo.get('modelo')} ({ativo.get('placa')})"
                         if ativo else f"ID {m.get('id_ativo')}")
            print(f"ID: {m['id_manutencao']} | Ativo: {nome_ativo} | "
                  f"Descrição: {m['descricao']} | Retorno previsto: {m['data_fim']}")
        try:
            id_man = int(input("\nDigite o ID da manutenção para finalizar: "))
        except ValueError:
            print("ID inválido.")
            return

        ok = database.finalizar_manutencao(id_man)
        if ok:
            print(f"\nManutenção {id_man} finalizada! Ativo retornou para 'Disponível'.")
        else:
            print("Manutenção não encontrada.")

    def apagar_manutencao(self):
        print("--- EXCLUIR MANUTENÇÃO ---")
        try:
            id_manutencao = int(input("Digite o ID da manutenção a ser excluída: "))
        except ValueError:
            print("ID inválido, tente novamente.")
            return
        manutencao = database.buscar_manutencao_por_id(id_manutencao)
        if not manutencao:
            print("Manutenção não encontrada!")
            return
        database.apagar_manutencao(id_manutencao)
        print("Manutenção excluída com sucesso!")

    def editar_manutencao(self):
        print("--- EDITAR MANUTENÇÃO ---")
        try:
            id_manutencao = int(input("Digite o ID da manutenção a ser editada: "))
        except ValueError:
            print("ID inválido, tente novamente.")
            return
        manutencao = database.buscar_manutencao_por_id(id_manutencao)
        if not manutencao:
            print("Manutenção não encontrada!")
            return

        print(f"Manutenção atual: {manutencao}")
        descricao = input("Nova descrição (deixe em branco para manter): ").strip()
        custo_input = input("Novo custo (deixe em branco para manter): ").strip()

        updates = {}
        if descricao:
            updates['descricao'] = descricao
        if custo_input:
            try:
                custo = float(custo_input)
                if custo < 0:
                    print("Custo inválido!")
                    return
                updates['custo'] = custo
            except ValueError:
                print("Valor inválido, tente novamente.")
                return

        if updates:
            database.atualizar_manutencao(id_manutencao, updates)
            print("Manutenção atualizada com sucesso!")
        else:
            print("Nenhuma alteração feita.")
