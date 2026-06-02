from dados import database
from datetime import datetime

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except Exception:
    class _C: pass
    Fore = _C()
    Fore.CYAN = ""
    Fore.RED = ""
    Fore.GREEN = ""
    Fore.YELLOW = ""
    Style = _C()
    Style.RESET_ALL = ""


class Manutencao_Controle:
    """Controller para fluxos de manutenção (CRUD + finalização)."""

    def __init__(self):
        database.iniciar_banco()

    def buscar_manutencao_por_id(self, manutencao_id):
        if isinstance(manutencao_id, str):
            manutencao_id = manutencao_id.strip()
        return database.buscar_manutencao_por_id(manutencao_id)

    def exibir_manutencao(self, manutencao):
        print(Fore.CYAN + f"ID Manutenção: {manutencao.get('id_manutencao')}" + Style.RESET_ALL)
        print(f"Ativo ID: {manutencao.get('id_ativo')}")
        print(f"Categoria: {manutencao.get('categoria')}")
        print(f"Descrição: {manutencao.get('descricao')}")
        print(f"Data de Início: {manutencao.get('data')}")
        print(f"Data de Retorno: {manutencao.get('data_fim')}")
        print(f"Custo: R$ {manutencao.get('custo', 0):.2f}")
        print(f"Status: {manutencao.get('status')}")
        print("-" * 30)

    def criar_manutencao(self):
        print(Fore.CYAN + "\n--- NOVA MANUTENÇÃO ---" + Style.RESET_ALL)

        try:
            id_ativo = int(input("Digite o ID do ativo em manutenção: "))
        except ValueError:
            print(Fore.RED + "ID inválido, tente novamente." + Style.RESET_ALL)
            return

        ativo = database.buscar_ativo_por_id(id_ativo)
        if not ativo:
            print(Fore.RED + "Ativo não encontrado!" + Style.RESET_ALL)
            return

        status = (ativo.get('status') or '').strip().lower()
        if status == 'alugado':
            print(Fore.RED + f"Erro: O ativo {ativo.get('modelo')} está alugado e não pode entrar em manutenção." + Style.RESET_ALL)
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
        print(Fore.GREEN + "\nManutenção cadastrada com sucesso!" + Style.RESET_ALL)

    def listar_manutencao(self):
        manutencoes = database.listar_manutencoes()
        if not manutencoes:
            print(Fore.YELLOW + "\nNenhuma manutenção cadastrada." + Style.RESET_ALL)
            return

        print(Fore.CYAN + "\n--- LISTA DE MANUTENÇÕES ---" + Style.RESET_ALL)
        for m in manutencoes:
            ativo = database.buscar_ativo_por_id(m.get('id_ativo'))
            nome_ativo = (f"{ativo.get('modelo')} - {ativo.get('placa')} (ID {ativo.get('id_ativo')})"
                          if ativo else f"ID {m.get('id_ativo')} não encontrado")
            print(Fore.CYAN + f"ID Manutenção: {m.get('id_manutencao')}" + Style.RESET_ALL)
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
            print(Fore.YELLOW + "\nNenhuma manutenção ativa no momento." + Style.RESET_ALL)
            return

        print(Fore.CYAN + "\n--- MANUTENÇÕES ATIVAS ---" + Style.RESET_ALL)
        for m in ativas:
            ativo = database.buscar_ativo_por_id(m.get('id_ativo'))
            nome_ativo = (f"{ativo.get('modelo')} ({ativo.get('placa')})"
                         if ativo else f"ID {m.get('id_ativo')}")
            print(f"ID: {m['id_manutencao']} | Ativo: {nome_ativo} | "
                  f"Descrição: {m['descricao']} | Retorno previsto: {m['data_fim']}")
        try:
            id_man = int(input("\nDigite o ID da manutenção para finalizar: "))
        except ValueError:
            print(Fore.RED + "ID inválido." + Style.RESET_ALL)
            return

        ok = database.finalizar_manutencao(id_man)
        if ok:
            print(Fore.GREEN + f"\nManutenção {id_man} finalizada! Ativo retornou para 'Disponível'." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Manutenção não encontrada." + Style.RESET_ALL)

    def apagar_manutencao(self):
        print(Fore.CYAN + "--- EXCLUIR MANUTENÇÃO ---" + Style.RESET_ALL)
        try:
            id_manutencao = int(input("Digite o ID da manutenção a ser excluída: "))
        except ValueError:
            print(Fore.RED + "ID inválido, tente novamente." + Style.RESET_ALL)
            return
        manutencao = database.buscar_manutencao_por_id(id_manutencao)
        if not manutencao:
            print(Fore.RED + "Manutenção não encontrada!" + Style.RESET_ALL)
            return
        database.apagar_manutencao(id_manutencao)
        print(Fore.GREEN + "Manutenção excluída com sucesso!" + Style.RESET_ALL)

    def editar_manutencao(self):
        print(Fore.CYAN + "--- EDITAR MANUTENÇÃO ---" + Style.RESET_ALL)
        try:
            id_manutencao = int(input("Digite o ID da manutenção a ser editada: "))
        except ValueError:
            print(Fore.RED + "ID inválido, tente novamente." + Style.RESET_ALL)
            return
        manutencao = database.buscar_manutencao_por_id(id_manutencao)
        if not manutencao:
            print(Fore.RED + "Manutenção não encontrada!" + Style.RESET_ALL)
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
            print(Fore.GREEN + "Manutenção atualizada com sucesso!" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Nenhuma alteração feita." + Style.RESET_ALL)
