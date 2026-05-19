from modelos.manutencao import Manutencao
from datetime import datetime
from dados import database

class Manutencao_Controle:
    def __init__(self, ativos):
        self.ativos = ativos
    
    
    def realizar_manutencao(self):
        print("\n--- NOVA MANUTENÇÃO ---")
        busca_ativo = input("Digite o 'ID' ou 'PLACA' do ativo para manutenção: ").strip().upper()
        ativo = database.buscar_ativo_por_id_ou_placa(busca_ativo)
        if ativo is None:
            print("Erro: Ativo não encontrado.")
            return
        if ativo.get('status') != "Disponível":
            print("Erro: Ativo não está disponível para manutenção.")
            return

        while True:
            d_realizacao = input("Digite a Data de Realização (DD/MM/AAAA): ").strip()
            try:
                data_realizacao = datetime.strptime(d_realizacao, "%d/%m/%Y").date()
                break
            except ValueError:
                print("Erro: Formato inválido! Por favor, use o formato DD/MM/AAAA.")

        while True:
            d_retorno = input("Digite a Previsão de Retorno (DD/MM/AAAA): ").strip()
            try:
                previsao_retorno = datetime.strptime(d_retorno, "%d/%m/%Y").date()
                break
            except ValueError:
                print("Erro: Formato inválido! Por favor, use o formato DD/MM/AAAA.")

        valor_input = input("Valor da Manutenção: ").strip()
        try:
            valor = float(valor_input)
        except ValueError:
            print("Valor inválido! Definindo valor como 0.")
            valor = 0.0

        id_manutencao = database.gerar_id_manutencao()

        manutencao = Manutencao(data_realizacao, previsao_retorno, id_manutencao, valor, 'Manutenção')
        manutencao.ativo_obj.marca = ativo.get('marca')
        manutencao.ativo_obj.modelo = ativo.get('modelo')
        manutencao.ativo_obj.placa = ativo.get('placa')

        database.cadastrar_manutencao(ativo.get('placa'), data_realizacao, previsao_retorno, id_manutencao, valor, 'Manutenção')
        database.atualizar_status_ativo(ativo.get('placa'), 'Em Manutenção')
        print("Manutenção cadastrada com sucesso!")
    
    def listar_manutencoes(self):
        manutencoes = database.listar_manutencoes()
        if not manutencoes:
            print("Nenhuma manutenção cadastrada.")
            return
        for m in manutencoes:
            print(f"ID: {m.get('id_manutencao')}, Ativo: {m.get('placa')}, Data Realização: {m.get('data_realizacao')}, Previsão Retorno: {m.get('previsao_retorno')}, Valor: {m.get('valor')}, Status: {m.get('status')}")
    
    def editar_manutencao(self):
        manutencoes = database.listar_manutencoes()
        if not manutencoes:
            print("Nenhuma manutenção cadastrada.")
            return
        id_busca = input("Digite o ID da manutenção que deseja editar: ").strip()
        manutencao = database.buscar_manutencao_por_id(id_busca)
        if manutencao is None:
            print("Erro: Manutenção não encontrada.")
            return
        
        print("Deixe o campo vazio para manter o valor atual.")
        d_realizacao = input(f"Data de Realização (atual: {manutencao.get('data_realizacao')}): ").strip()
        if d_realizacao:
            try:
                data_realizacao = datetime.strptime(d_realizacao, "%d/%m/%Y").date()
                manutencao['data_realizacao'] = data_realizacao
            except ValueError:
                print("Formato inválido! Mantendo data de realização atual.")

        d_retorno = input(f"Previsão de Retorno (atual: {manutencao.get('previsao_retorno')}): ").strip()
        if d_retorno:
            try:
                previsao_retorno = datetime.strptime(d_retorno, "%d/%m/%Y").date()
                manutencao['previsao_retorno'] = previsao_retorno
            except ValueError:
                print("Formato inválido! Mantendo previsão de retorno atual.")

        valor_input = input(f"Valor da Manutenção (atual: {manutencao.get('valor')}): ").strip()
        if valor_input:
            try:
                valor = float(valor_input)
                manutencao['valor'] = valor
            except ValueError:
                print("Valor inválido! Mantendo valor atual.")
        database.atualizar_manutencao(id_busca, manutencao)
        print("Manutenção atualizada com sucesso!")
    
    def finalizar_manutencao(self):
        manutencoes = database.listar_manutencoes()
        if not manutencoes:
            print("Nenhuma manutenção cadastrada.")
            return
        id_busca = input("Digite o ID da manutenção que deseja finalizar: ").strip()
        manutencao = database.buscar_manutencao_por_id(id_busca)
        if manutencao is None:
            print("Erro: Manutenção não encontrada.")
            return
        if (manutencao.get('status') or '').lower() in ('finalizada', 'finalizado'):
            print(f"Manutenção {id_busca} já está finalizada.")
            return
        
        database.finalizar_manutencao(id_busca)
        database.atualizar_status_ativo(manutencao.get('placa'), 'Disponível')
        print(f"Manutenção {id_busca} finalizada!")
        
        