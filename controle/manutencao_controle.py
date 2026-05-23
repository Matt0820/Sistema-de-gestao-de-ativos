from dados import database
from datetime import datetime
class Manutencao_Controle:
    def __init__(self):
        database.iniciar_banco()
        self.manutencoes = database.listar_manutencoes()
    
    def criar_manutencao(self):
        #pega o id do ativo por id e ve se ele de fato existe
        try:
            id_ativo = int(input("Digite o id do ativo em manutencao: "))
            ativo = database.buscar_ativo_por_id(id_ativo)
            if not ativo:
                print("Ativo nao encontrado!")
                return
            else:
                print("Ativo encontrado, redirecionando para o proximo passo")
                descricao = input("Qual é o serviço realizado? ").strip()
                while True:
                    d_ini = input("Digite a Data de Inicio (DD/MM/AAAA): ").strip()
                    try:
                        data_inicio = datetime.strptime(d_ini, "%d/%m/%Y").date()
                        break
                    except ValueError:
                        print("Erro: Formato inválido! Por favor, use o formato DD/MM/AAAA.")
                while True:
                    d_fim = input("Digite a Data de Retorno (DD/MM/AAAA): ").strip()
                    try:
                        data_fim = datetime.strptime(d_fim, "%d/%m/%Y").date()
                        if data_fim < data_inicio:
                            print("Invalido, a data de retorno nao pode ser menor que a data de inicio")
                            return
                        else:
                            break
                    except ValueError:
                        print("Erro: Formato inválido! Por favor, use o formato DD/MM/AAAA.")      
                try:
                    custo = float(input("Qual o valor da manutencao: "))
                except ValueError:
                    print("Valor invalido, tente novamente")
                    return 
                database.inserir_manutencao(id_ativo,data_inicio, data_fim,descricao,custo)
                print("Manutencao cadastrada com sucesso!")
        except ValueError:
            print("id invalido, tente novamente")
            return
    def listar_manutencao(self):
        manutencao = database.listar_manutencoes()
        if not manutencao:
            print("Nao existem manutencoes ativas no momento")
        else:
            for i in manutencao:
                print(f"id da manutencao: {i.get('id_ativo')}")
                print(f"descricao da manutencao: {i.get('descricao')}")
                print(f"Data da entrada: {i.get('data')}")
                print(f"Data de Retorno: {i.get('data_fim')}")
                ativo_id = i.get('ativo_id')
                ativo = database.buscar_ativo_por_id(ativo_id)
                if ativo:
                    print(f"Ativo associado: {ativo.get('modelo')} - {ativo.get('placa')} (id {ativo.get('id')})")
                else:
                    print(f"Ativo associado: id {ativo_id} nao encontrado")
                print(f"Pagamento: {i.get('custo')}")
        #teste isso mateus!
        