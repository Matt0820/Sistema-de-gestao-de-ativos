from dados import database
class Relatorios():
    def __init__(self):
        database.iniciar_banco()

    def _status_normalizado(self, status):
        return (status or '').strip().lower()

    def _exibir_ativo(self, ativo):
        print(f"ID: {ativo.get('id_ativo')}")
        print(f"Modelo: {ativo.get('modelo')}")
        print(f"Marca: {ativo.get('marca')}")
        print(f"Placa: {ativo.get('placa')}")
        print(f"Status: {ativo.get('status')}")
        print(f"Diária: R$ {ativo.get('diaria', 0):.2f}")
        print("-" * 30)

    def _exibir_cliente(self, cliente):
        print(f"ID: {cliente.get('id_cliente')}")
        print(f"Nome: {cliente.get('nome')}")
        print(f"Idade: {cliente.get('idade')}")
        print(f"CNH: {cliente.get('cnh')}")
        print("-" * 30)

    def relatorio_ativos_disponiveis(self):
        print("\n--- RELATÓRIO DE ATIVOS DISPONÍVEIS ---")
        lista_ativos = database.listar_ativos()
        ativos_disponiveis = [
            a for a in lista_ativos
            if self._status_normalizado(a.get('status')) == 'disponível'
        ]
        if not ativos_disponiveis:
            print("Nenhum ativo disponível no momento.")
            return
        for ativo in ativos_disponiveis:
            self._exibir_ativo(ativo)

    def relatorio_ativos_alugados(self):
        print("\n--- RELATÓRIO DE ATIVOS ALUGADOS ---")
        lista_ativos = database.listar_ativos()
        alugados = [
            a for a in lista_ativos
            if self._status_normalizado(a.get('status')) == 'alugado'
        ]
        if not alugados:
            print("Nenhum ativo alugado no momento.")
            return
        for ativo in alugados:
            self._exibir_ativo(ativo)

    def relatorio_clientes_ativos(self):
        print("\n--- RELATÓRIO DE CLIENTES ATIVOS ---")
        locacoes_ativas = database.listar_locacoes_ativas()
        if not locacoes_ativas:
            print("Não há clientes com locações ativas no momento.")
            return
        ids_vistos = set()
        for loc in locacoes_ativas:
            id_cliente = loc.get('id_cliente')
            if id_cliente in ids_vistos:
                continue
            ids_vistos.add(id_cliente)
            cliente = database.buscar_cliente_por_id(id_cliente)
            if cliente:
                self._exibir_cliente(cliente)

    def relatorio_manutencoes(self):          # <- self adicionado
        print("\n--- MANUTENÇÕES ATIVAS ---")
        ativas = database.listar_manutencoes_ativas()
        if not ativas:
            print("Nenhuma manutenção ativa.")
        else:
            for m in ativas:
                ativo = database.buscar_ativo_por_id(m.get('id_ativo'))
                nome_ativo = (f"{ativo.get('modelo')} ({ativo.get('placa')})"
                              if ativo else f"ID {m.get('id_ativo')}")
                print(f"ID: {m['id_manutencao']} | Ativo: {nome_ativo}")
                print(f"Categoria: {m.get('categoria')}")
                print(f"Descrição: {m['descricao']}")
                print(f"Entrada: {m['data']} | Retorno previsto: {m['data_fim']}")
                print(f"Custo: R$ {m['custo']:.2f}")
                print("-" * 30)

        print("\n--- MANUTENÇÕES FINALIZADAS ---")
        finalizadas = database.listar_manutencoes_finalizadas()
        if not finalizadas:
            print("Nenhuma manutenção finalizada.")
        else:
            for m in finalizadas:
                ativo = database.buscar_ativo_por_id(m.get('id_ativo'))
                nome_ativo = (f"{ativo.get('modelo')} ({ativo.get('placa')})"
                              if ativo else f"ID {m.get('id_ativo')}")
                print(f"ID: {m['id_manutencao']} | Ativo: {nome_ativo}")
                print(f"Categoria: {m.get('categoria')}")
                print(f"Descrição: {m['descricao']}")
                print(f"Entrada: {m['data']} | Retorno: {m['data_fim']}")
                print(f"Custo: R$ {m['custo']:.2f}")
                print("-" * 30)

    def relatorio_financeiro(self):
        print("\n--- RELATÓRIO FINANCEIRO ---")
        print("1. Mensal")
        print("2. Anual")
        tipo = input("Escolha o tipo: ").strip()

        if tipo not in ('1', '2'):
            print("Opção inválida.")
            return

        while True:
            try:
                ano = int(input("Ano (ex: 2025): "))
                break
            except ValueError:
                print("Ano inválido.")

        nomes_meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
                    'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']

        if tipo == '1':
            while True:
                try:
                    mes = int(input("Mês (1-12): "))
                    if 1 <= mes <= 12:
                        break
                    print("Mês inválido.")
                except ValueError:
                    print("Entrada inválida.")

            dados = database.relatorio_financeiro_mes(ano, mes)

            print(f"\n{'='*40}")
            print(f"  RELATÓRIO: {nomes_meses[mes-1]} / {ano}")
            print(f"{'='*40}")

            print("\n--- ENTRADAS (Locações)")
            if not dados['locacoes']:
                print("Nenhuma locação no período.")
            else:
                for l in dados['locacoes']:
                    print(f"  #{l['id_locacao']} {l['cliente']} | {l['ativo']} ({l['placa']}) "
                        f"| {l['data_ini']} → {l['data_fim']} | R$ {l['valor']:.2f} [{l['status']}]")

            print("\n--- SAÍDAS (Manutenções)")
            if not dados['manutencoes']:
                print("Nenhuma manutenção no período.")
            else:
                for m in dados['manutencoes']:
                    print(f"  #{m['id_manutencao']} {m['ativo']} ({m['placa']}) "
                        f"| {m['descricao']} | R$ {m['custo']:.2f} [{m['status']}]")

            print(f"\n{'='*40}")
            print(f"  Renda Bruta:   R$ {dados['entradas']:>10.2f}")
            print(f"  Custos:        R$ {dados['saidas']:>10.2f}")
            print(f"  Renda Líquida: R$ {dados['liquido']:>10.2f}")
            print(f"{'='*40}")

        else:
            dados = database.relatorio_financeiro_ano(ano)

            print(f"\n{'='*40}")
            print(f"  RELATÓRIO ANUAL: {ano}")
            print(f"{'='*40}")

            # Agrupa locações e manutenções por mês para exibir organizado
            for i, nome_mes in enumerate(nomes_meses, start=1):
                mes_str = f"{i:02d}"
                loc_mes  = [l for l in dados['locacoes']    if l['mes'] == mes_str]
                man_mes  = [m for m in dados['manutencoes'] if m['mes'] == mes_str]

                if not loc_mes and not man_mes:
                    continue

                total_entrada = sum(l['valor'] for l in loc_mes)
                total_saida   = sum(m['custo'] for m in man_mes)

                print(f"\n  ── {nome_mes} ──")

                if loc_mes:
                    print("  ENTRADAS:")
                    for l in loc_mes:
                        print(f"    #{l['id_locacao']} {l['cliente']} | {l['ativo']} ({l['placa']}) "
                            f"| {l['data_ini']} → {l['data_fim']} | R$ {l['valor']:.2f} [{l['status']}]")

                if man_mes:
                    print("  SAÍDAS:")
                    for m in man_mes:
                        print(f"    #{m['id_manutencao']} {m['ativo']} ({m['placa']}) "
                            f"| {m['descricao']} | R$ {m['custo']:.2f} [{m['status']}]")

                print(f"  Saldo do mês: R$ {total_entrada - total_saida:.2f}")

            print(f"\n{'='*40}")
            print(f"  TOTAL ANUAL")
            print(f"  Renda Bruta:   R$ {dados['entradas']:>10.2f}")
            print(f"  Custos:        R$ {dados['saidas']:>10.2f}")
            print(f"  Renda Líquida: R$ {dados['liquido']:>10.2f}")
            print(f"{'='*40}")