from datetime import datetime, timedelta
from dados import database
class Locacao_Controle:

    def __init__(self, controle_cliente=None, controle_ativo=None):
        database.iniciar_banco()
        self.controle_cliente = controle_cliente
        self.controle_ativo = controle_ativo
    
    def buscar_locacao_por_id(self, id_locacao):
        if isinstance(id_locacao, str):
            id_locacao = id_locacao.strip()
        return database.buscar_locacao_por_id(id_locacao)

    def exibir_locacao(self, locacao):
        print(f"ID Locação: {locacao.get('id_locacao')}")
        print(f"Cliente ID: {locacao.get('id_cliente')}")
        print(f"Ativo ID: {locacao.get('id_ativo')}")
        print(f"Data Início: {locacao.get('data_ini')}")
        print(f"Duração: {locacao.get('duracao')}")
        print(f"Data Fim: {locacao.get('data_fim')}")
        print(f"Valor: R$ {locacao.get('valor', 0):.2f}")
        print(f"Status: {locacao.get('status')}")
        print("-" * 30)

    def realizar_locacao(self):
        print("\n--- NOVA LOCAÇÃO ---")
        cnh_busca = input("CNH do Cliente: ").strip()

        cliente = database.buscar_cliente_por_cnh(cnh_busca)
        if cliente is None:
            print("Erro: Cliente não encontrado!")
            return

        # Verifica se cliente já possui locação ativa
        for loc in database.listar_locacoes_ativas():
            if loc.get('id_cliente') == cliente.get('id_cliente'):
                print("Erro: Cliente já possui uma locação ativa!")
                return

        busca_ativo = input("Digite o 'ID' ou 'PLACA' do ativo para locação: ").strip()
        ativo = database.buscar_ativo_por_id_ou_placa(busca_ativo)
        if ativo is None:
            print("Erro: Ativo não encontrado.")
            return

        status = (ativo.get('status') or '').strip().lower()
        if status != 'disponível':
            print("Erro: Ativo não está disponível para locação.")
            return

        while True:
            duracao_input = input("Duração em Dias: ").strip()
            if duracao_input.isdigit() and int(duracao_input) > 0:
                duracao = int(duracao_input)
                break
            print("Duração inválida! Digite um número inteiro maior que zero.")

        while True:
            d_ini = input("Data de Início (DD/MM/AAAA): ").strip()
            try:
                data_inicio = datetime.strptime(d_ini, "%d/%m/%Y").date()
                break
            except ValueError:
                print("Erro: Formato inválido! Use DD/MM/AAAA.")

        valor = (ativo.get('diaria') or 0) * duracao
        data_fim = data_inicio + timedelta(days=duracao)

        database.cadastrar_locacao(
            cliente.get('id_cliente'),
            ativo.get('id_ativo'),
            data_inicio,
            duracao,
            data_fim,
            valor,
            'Ativa'
        )
        database.atualizar_ativo(ativo.get('id_ativo'), {'status': 'Alugado'})

        print("\nLocação realizada com sucesso!")
        print(f"Cliente: {cliente.get('nome')} | Veículo: {ativo.get('modelo')} ({ativo.get('placa')})")
        print(f"Período: {data_inicio} até {data_fim} | Valor Total: R$ {valor:.2f}")

    def finalizar_locacao(self):
        locacoes_ativas = database.listar_locacoes_completas()
        locacoes_ativas = [l for l in locacoes_ativas if (l.get('status') or '').lower() == 'ativa']

        if not locacoes_ativas:
            print("\nNenhuma locação ativa no momento.")
            return

        print("\n--- LOCAÇÕES ATIVAS ---")
        for l in locacoes_ativas:
            print(f"ID: {l['id_locacao']} | Cliente: {l['cliente']} | "
                  f"Veículo: {l['ativo']} ({l['placa']}) | Até: {l['data_fim']}")

        try:
            id_loc = int(input("\nDigite o ID da locação para finalizar: "))
        except ValueError:
            print("ID inválido.")
            return

        loc = database.buscar_locacao_por_id(id_loc)
        if loc is None:
            print("Locação não encontrada.")
            return
        if (loc.get('status') or '').lower() != 'ativa':
            print(f"Locação {id_loc} não está ativa.")
            return

        database.finalizar_locacao(id_loc)
        print("\nLocação encerrada com sucesso!")

    def listar_locacoes(self):
        locacoes = database.listar_locacoes_completas()

        if not locacoes:
            print("\nNenhuma locação cadastrada.")
            return

        print("\n=== LOCAÇÕES CADASTRADAS ===")
        for l in locacoes:
            print(f"ID Locação: {l['id_locacao']}")
            print(f"Cliente: {l['cliente']}")
            print(f"Veículo: {l['ativo']} ({l['placa']})")
            print(f"Período: {l['data_ini']} até {l['data_fim']}")
            print(f"Valor: R$ {l['valor']:.2f}")
            print(f"Status: {l['status']}")
            print("-" * 30)
