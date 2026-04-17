#Importa a classe Locação e chama a lib "DataTime"
from modelos.locacao import Locacao
from datetime import datetime, timedelta


#Inicia a classe Controle_Locacao, onde serão implementados os métodos para realizar, finalizar e listar as locações
class Locacao_Controle:
    #Metodo construtor, onde temos a lista de locações
    def __init__(self, controle_cliente=None, controle_ativo=None):
        self.lista_locacoes = []
        self.controle_cliente = controle_cliente
        self.controle_ativo = controle_ativo

    #Metodo para realizar uma nova locação, onde o usuário irá informar a CNH do cliente, o ID ou placa do ativo, a duração e a data de início da locação
    def realizar_locacao(self):
        print("\n--- NOVA LOCAÇÃO ---")
        cnh_busca = input("CNH do Cliente: ").strip()

        #Verifica se o cliente ja tem uma locação ativa, para evitar que um cliente tenha mais de uma locação ao mesmo tempo
        for loc in self.lista_locacoes:
            if loc.cliente.cnh == cnh_busca and loc.status == "Ativa":
                print("Erro: Cliente já possui uma locação ativa!")
                return

        #Busca o cliente pela CNH
        cliente_alvo = self.controle_cliente.buscar_cliente_por_cnh(cnh_busca)

        if cliente_alvo is None:
            print("Erro: Cliente não encontrado!")
            return

        #Busca o ativo pela placa ou id
        busca_ativo = input("Digite o 'ID' ou 'PLACA' do ativo para locação: ").strip().upper()
        ativo_alvo = self.controle_ativo.buscar_ativo_por_id_ou_placa(busca_ativo)

        #se ele nao acha, ele retorna um erro
        if ativo_alvo is None:
            print("Erro: Ativo não encontrado.")
            return
        #se o ativo encontrado nao estiver disponivel, ele retorna um erro
        if ativo_alvo.status != "Disponível":
            print("Erro: Ativo não está disponível para locação.")
            return

        #Coleta dados e cria a locação
        while True:
            duracao_input = input("Duração em Dias: ").strip()
            if duracao_input.isdigit() and int(duracao_input) > 0:
                duracao = int(duracao_input)
                break
            print("Duração inválida! Digite um número inteiro maior que zero.")
            
        #Coleta a data de início da locação, e verifica se o formato é valido, caso contrário, ele retorna um erro
        while True:
            d_ini = input("Digite a Data de Inicio (DD/MM/AAAA): ").strip()
            try:
                data_inicio = datetime.strptime(d_ini, "%d/%m/%Y").date()
                break

            except ValueError:
                print("Erro: Formato inválido! Por favor, use o formato DD/MM/AAAA.")
                
        #Calcula o valor total da locação, multiplicando a diária do ativo pela duração, e calcula a data de fim da locação, somando a data de início com a duração em dias
        valor = ativo_alvo.diaria * duracao
        
        #Calcula a data de fim da locação, somando a data de início com a duração em dias
        data_fim = data_inicio + timedelta(days=duracao)

        #Cria a nova locação, adiciona na lista de locações e exibe uma mensagem de sucesso
        nova_loc = Locacao(cliente_alvo, ativo_alvo, data_inicio, duracao, data_fim, valor)
        
        #Atualiza o status do ativo para "Alugado"
        ativo_alvo.status = "Alugado"
        
        #Adiciona a nova locação na lista de locações
        self.lista_locacoes.append(nova_loc)
        
        #Exibe uma mensagem de sucesso
        print("Locação realizada com sucesso!")

    #Metodo para finalizar uma locação, onde o usuário irá informar o ID da locação, e o sistema irá verificar se a locação existe e se está ativa, caso contrário, ele retorna um erro
    def finalizar_locacao(self):
        #Verifica se existem locações registradas, se nao encontrar nenhuma, ele retorna um aviso
        if len(self.lista_locacoes) == 0:
            print("Nenhuma locação registrada.")
            return
        
        #Solicita o ID da locação para finalizar, e verifica se o ID é um número inteiro, caso contrário, ele retorna um erro
        try:
            id_loc = int(input("Digite o ID (Número) da locação para finalizar: "))
        except ValueError:
            print("ID inválido.")
            return

        #Percorre a lista de locações para encontrar a locação com o ID informado, e verifica se a locação está ativa, caso contrário, ele retorna um aviso, e se encontrar a locação, ele finaliza a locação, atualiza o status do ativo para "Disponível" e exibe uma mensagem de sucesso
        for loc in self.lista_locacoes:
            if loc.id_locacao == id_loc:
                if loc.status == "Finalizada":
                    print(f"Locação {id_loc} já está finalizada.")
                    return
                loc.finalizar()
                print(f"Locação {id_loc} encerrada!")
                return
        print("Locação não encontrada.")

    #Metodo para listar as locações, onde o sistema irá exibir todas as locações registradas, e se nao encontrar nenhuma, ele retorna um aviso
    def listar_locacoes(self):
        if len(self.lista_locacoes) == 0:
            print("Nenhuma locação registrada.")
            return

        print("\n--- LISTA DE LOCAÇÕES ---")
        for locacao in self.lista_locacoes:
            locacao.exibir_locacao()
