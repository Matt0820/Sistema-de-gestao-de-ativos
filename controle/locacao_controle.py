#Importa a classe Locação e chama a lib "DataTime"
from datetime import datetime, timedelta
from dados import database


class Locacao_Controle:
    #comentario do mateus: a variavel ja e declarada dentro do metodo, nao existe necessidade de colocar um =None :)
    def __init__(self, controle_cliente, controle_ativo):
        database.iniciar_banco()
        self.controle_cliente = controle_cliente
        self.controle_ativo = controle_ativo

    def realizar_locacao(self):
        print("\n--- NOVA LOCAÇÃO ---")
        cnh_busca = input("CNH do Cliente: ").strip()

        # verifica cliente
        cliente = database.buscar_cliente_por_cnh(cnh_busca)
        if cliente is None:
            print("Erro: Cliente não encontrado!")
            return

        # verifica se cliente já tem locação ativa
        if database.listar_locacoes_ativas():
            for l in database.listar_locacoes_ativas():
                if l.get('cliente_obj') == cnh_busca:
                    print("Erro: Cliente já possui uma locação ativa!")
                    return

        # busca ativo
        busca_ativo = input("Digite o 'ID' ou 'PLACA' do ativo para locação: ").strip().upper()
        ativo = database.buscar_ativo_por_id_ou_placa(busca_ativo)
        if ativo is None:
            print("Erro: Ativo não encontrado.")
            return
        if ativo.get('status') != "Disponível":
            print("Erro: Ativo não está disponível para locação.")
            return

        # coleta duração e datas
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

        valor = (ativo.get('diaria') or 0) * duracao
        data_fim = data_inicio + timedelta(days=duracao)

        # cadastra locação no banco; armazenamos cliente_obj como CNH e ativo_obj como placa
        database.cadastrar_locacao(cliente.get('cnh'), ativo.get('placa'), data_inicio, f"{duracao} dias", data_fim, valor, 'Ativa')

        # atualiza status do ativo
        database.atualizar_ativo(ativo.get('id'), {'status': 'Alugado'})

        print("Locação realizada com sucesso!")

    def finalizar_locacao(self):
        locacoes = database.listar_locacoes()
        if not locacoes:
            print("Nenhuma locação registrada.")
            return

        try:
            id_loc = int(input("Digite o ID (Número) da locação para finalizar: "))
        except ValueError:
            print("ID inválido.")
            return

        loc = database.buscar_locacao_por_id(id_loc)
        if loc is None:
            print("Locação não encontrada.")
            return
        if (loc.get('status') or '').lower() in ('finalizada', 'finalizado'):
            print(f"Locação {id_loc} já está finalizada.")
            return

        database.finalizar_locacao(id_loc)
        print(f"Locação {id_loc} encerrada!")

    def listar_locacoes(self):
        locacoes = database.listar_locacoes()
        if not locacoes:
            print("Nenhuma locação registrada.")
            return

        print("\n--- LISTA DE LOCAÇÕES ---")
        for l in locacoes:
            print(f"ID Locação: {l.get('id_transacao_mensal')} | Status: {l.get('status')}")
            print(f"Cliente: {l.get('cliente_obj')}")
            print(f"Veículo (placa): {l.get('ativo_obj')}")
            print(f"Duração: {l.get('duracao')}")
            print(f"Período: {l.get('data_ini')} até {l.get('data_fim')}")
            print(f"Valor Total: R$ {l.get('valor')}")
            print("-" * 30)
