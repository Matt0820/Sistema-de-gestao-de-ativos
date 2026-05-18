#importa a classe Ativo para manipular os dados dos ativos
from modelos.ativo import Ativo
#Importa o datetime
from datetime import date

from dados import database

#classe de controle de dados dos ativos, pois um unico controle unico é desnecessárimente extenso e pouluido.
class Ativo_Controle:

    #metodo construtor para inicializar a lista de ativos
    def __init__(self):
        database.iniciar_banco()
        self.lista_ativos = database.listar_ativos()

    #metodo auxiliar para padronizar comparações de status
    def status_normalizado(self, status):
        return status.strip().lower()

    #metodo para buscar um ativo pelo ID ou pela placa
    def buscar_ativo_por_id_ou_placa(self, busca):
        busca = busca.strip().upper()
        return database.buscar_ativo_por_id_ou_placa(busca)

    #metodo para cadastrar um novo ativo, solicitando os dados ao usuário
    def cadastrar_ativo(self):
        print("\n--- CADASTRO DE ATIVO ---")
        modelo = input("Modelo: ").strip()
        marca = input("Marca: ").strip()

        #input do ano
        while True:
            try:
                ano = int(input("Ano: "))
                break
            except ValueError:
                print("Erro: Ano deve ser um número inteiro!")

        while True:
            #a placa é recebida no input e convertida para maiuscula para padronização
            placa_input = input("Placa: ").strip().upper()

            if database.verificar_placa_existente(placa_input):
                print("Erro: Placa já cadastrada!")
            else:
                break

        while True:
            #o valor é recebido como string e convertido para float, caso o usuário digite um valor inválido, exibe uma mensagem de erro e solicita novamente
            try:
                valor = float(input("Valor: "))
                break
            except ValueError:
                print("Erro: Valor deve ser um número!")

        while True:
            #a diaria é recebida como string e convertida para float, caso o usuário digite um valor inválido, exibe uma mensagem de erro e solicita novamente
            try:
                diaria = float(input("Valor da Diaria: "))
                break
            except ValueError:
                print("Erro: Valor da Diaria deve ser um número!")

        data = date.today()

        #cria um objeto ativo com os dados da classe Ativo
        # calcula depreciação se necessário usando a classe Ativo
        try:
            novo_obj = Ativo(modelo, marca, ano, placa_input, valor, diaria, data)
            depreciacao = getattr(novo_obj, 'calcular_depreciacao', lambda: None)()
        except Exception:
            depreciacao = None

        database.cadastrar_ativo(modelo, marca, ano, placa_input, valor, diaria, data, status="Disponível", depreciacao=depreciacao)
        self.lista_ativos = database.listar_ativos()
        print("\nAtivo cadastrado com sucesso!")

    #metodo para listar todos os ativos cadastrados, exibindo seus dados de forma organizada
    def listar_ativos(self):
        lista_ativos = database.listar_ativos()
        #verifica se a lista de ativos está vazia, caso esteja, exibe uma mensagem informando que não há ativos cadastrados e retorna
        if len(lista_ativos) == 0:
            print("\nNenhum ativo cadastrado.")
            return

        #percorre a lista de ativos e chama o método exibir_ativo de cada objeto ativo para exibir seus dados
        print("\n--- LISTA DE ATIVOS ---\n")
        for ativo in lista_ativos:
            print(f"ID: {ativo.get('id')}")
            print(f"Modelo: {ativo.get('modelo')}")
            print(f"Marca: {ativo.get('marca')}")
            print(f"Ano: {ativo.get('ano')}")
            print(f"Placa: {ativo.get('placa')}")
            print(f"Valor: {ativo.get('valor')}")
            print(f"Diária: {ativo.get('diaria')}")
            print(f"Data: {ativo.get('data')}")
            print(f"Status: {ativo.get('status')}")
            print(f"Depreciação: {ativo.get('depreciacao')}")
            print("-" * 30)

    #metodo para editar os dados de um ativo existente, solicitando ao usuário o ID ou a placa do ativo a ser editado e os novos dados
    def editar_ativo(self):
        #verifica se a lista de ativos está vazia, caso esteja, exibe uma mensagem informando que não há ativos cadastrados e retorna
        if len(self.lista_ativos) == 0:
            print("Nenhum ativo cadastrado.")
            return

        #solicita ao usuário o ID ou a placa do ativo a ser editado
        id_editar = input("Digite o 'ID' ou 'PLACA' do ativo para editar: ")
        ativo_encontrado = self.buscar_ativo_por_id_ou_placa(id_editar)

        #se nenhum ativo for encontrado com o ID ou placa fornecida, exibe uma mensagem informando que o ativo não foi encontrado e retorna
        if ativo_encontrado is None:
            print("\nAtivo não encontrado.")
            return

        #verifica se o ativo encontrado está atualmente alugado
        if self.status_normalizado(ativo_encontrado.get('status')) == "alugado":
            print(f"Erro: O ativo {ativo_encontrado.get('modelo')} (ID: {ativo_encontrado.get('id')}) está atualmente Alugado e não pode ser editado.")
            return

        print("\n--- Editar Ativo ---")
        print("Deixe em branco para manter o valor atual.")

        #solicita os novos dados e mantém o atual caso fique em branco
        # coleta novos valores (deixa em branco para manter)
        novo_modelo = input(f"Modelo ({ativo_encontrado.get('modelo')}): ").strip()
        nova_marca = input(f"Marca ({ativo_encontrado.get('marca')}): ").strip()
        novo_ano = input(f"Ano ({ativo_encontrado.get('ano')}): ").strip()
        nova_placa = input(f"Placa ({ativo_encontrado.get('placa')}): ").strip().upper()
        novo_valor = input(f"Valor ({ativo_encontrado.get('valor')}): ").strip()
        nova_diaria = input(f"Diária ({ativo_encontrado.get('diaria')}): ").strip()

        dados_atualizados = {}
        if novo_modelo:
            dados_atualizados['modelo'] = novo_modelo
        if nova_marca:
            dados_atualizados['marca'] = nova_marca
        if novo_ano:
            if novo_ano.isdigit():
                dados_atualizados['ano'] = int(novo_ano)
            else:
                print("Ano inválido. Mantendo valor atual.")
        if nova_placa:
            if database.verificar_placa_existente(nova_placa, ativo_encontrado.get('id')):
                print("Erro: Placa já cadastrada!")
                return
            dados_atualizados['placa'] = nova_placa
        if novo_valor:
            try:
                dados_atualizados['valor'] = float(novo_valor)
            except ValueError:
                print("Valor inválido. Mantendo valor atual.")
        if nova_diaria:
            try:
                dados_atualizados['diaria'] = float(nova_diaria)
            except ValueError:
                print("Diária inválida. Mantendo valor atual.")

        # recalcula depreciação se necessário
        try:
            modelo_final = dados_atualizados.get('modelo', ativo_encontrado.get('modelo'))
            marca_final = dados_atualizados.get('marca', ativo_encontrado.get('marca'))
            ano_final = dados_atualizados.get('ano', ativo_encontrado.get('ano'))
            placa_final = dados_atualizados.get('placa', ativo_encontrado.get('placa'))
            valor_final = dados_atualizados.get('valor', ativo_encontrado.get('valor'))
            diaria_final = dados_atualizados.get('diaria', ativo_encontrado.get('diaria'))
            data_final = ativo_encontrado.get('data')
            temp_obj = Ativo(modelo_final, marca_final, ano_final, placa_final, valor_final, diaria_final, data_final)
            dados_atualizados['depreciacao'] = getattr(temp_obj, 'calcular_depreciacao', lambda: None)()
        except Exception:
            pass

        # persiste alterações
        database.atualizar_ativo(ativo_encontrado.get('id'), dados_atualizados)
        self.lista_ativos = database.listar_ativos()
        print("\nAtivo atualizado com sucesso!")

    #metodo para apagar um ativo existente, solicitando ao usuário o ID ou a placa do ativo a ser apagado
    def apagar_ativo(self):
        lista_ativos = database.listar_ativos()
        #verifica se a lista de ativos está vazia, caso esteja, exibe uma mensagem informando que não há ativos cadastrados e retorna
        if len(lista_ativos) == 0:
            print("Nenhum ativo cadastrado.")
            return

        #solicita ao usuário o ID ou a placa do ativo a ser apagado
        busca = input("Digite o ID ou PLACA do ativo para apagar: ")
        ativo_encontrado = database.buscar_ativo_por_id_ou_placa(busca)

        #se nenhum ativo for encontrado com o ID ou placa fornecida, exibe uma mensagem informando que o ativo não foi encontrado e retorna
        if ativo_encontrado is None:
            print("\nAtivo não encontrado.")
            return

        #verifica se o ativo encontrado está atualmente alugado, caso esteja, exibe uma mensagem de erro informando que o ativo não pode ser apagado e retorna
        if self.status_normalizado(ativo_encontrado.get('status')) == "alugado":
            print(f"Erro: O ativo {ativo_encontrado.get('modelo')} (ID: {ativo_encontrado.get('id')}) está Alugado e não pode ser apagado.")
            return

        database.apagar_ativo(ativo_encontrado.get('id'))
        self.lista_ativos = database.listar_ativos()
        print(f"\nAtivo {ativo_encontrado.get('modelo')} (ID: {ativo_encontrado.get('id')}) apagado com sucesso!")

    #metodo para gerar um relatório de ativos disponíveis, filtrando a lista de ativos para exibir apenas aqueles com status "Disponivel" e chamando o método exibir_ativo de cada um para mostrar seus dados
    def relatorio_ativos_disponiveis(self):

        print("\n--- RELATÓRIO DE ATIVOS DISPONÍVEIS ---")

        #filtra a lista de ativos para criar uma nova lista contendo apenas os ativos que estão com status disponível
        self.lista_ativos = database.listar_ativos()
        ativos_disponiveis = [
            ativo for ativo in self.lista_ativos
            if self.status_normalizado(ativo.get('status')) == "disponível"
        ]

        #se a lista de ativos disponíveis estiver vazia, exibe uma mensagem informando que não há ativos disponíveis no momento e retorna
        if not ativos_disponiveis:
            print("Nenhum ativo Disponível no momento.")
            return

        #percorre a lista de ativos disponíveis e chama o método exibir_ativo de cada objeto ativo para exibir seus dados
        for ativo in ativos_disponiveis:
            print(f"ID: {ativo.get('id')}")
            print(f"Modelo: {ativo.get('modelo')}")
            print(f"Marca: {ativo.get('marca')}")
            print(f"Placa: {ativo.get('placa')}")
            print(f"Status: {ativo.get('status')}")
            print("-" * 30)

    #metodo para gerar um relatório de ativos alugados, filtrando a lista de ativos para exibir apenas aqueles com status "Alugado" e chamando o método exibir_ativo de cada um para mostrar seus dados
    def relatorio_ativos_alugados(self):
        print("\n--- RELATÓRIO DE ATIVOS ALUGADOS ---")

        #filtra a lista de ativos para criar uma nova lista contendo apenas os ativos que estão com status "Alugado", utilizando uma list comprehension para percorrer a lista de ativos e verificar o status de cada um
        self.lista_ativos = database.listar_ativos()
        alugados = [
            ativo for ativo in self.lista_ativos
            if self.status_normalizado(ativo.get('status')) == "alugado"
        ]

        #se a lista de ativos alugados estiver vazia, exibe uma mensagem informando que não há ativos alugados no momento e retorna
        if not alugados:
            print("Nenhum ativo Alugado no momento.")
            return

        #percorre a lista de ativos alugados e chama o método exibir_ativo de cada objeto ativo para exibir seus dados
        for ativo in alugados:
            print(f"ID: {ativo.get('id')}")
            print(f"Modelo: {ativo.get('modelo')}")
            print(f"Marca: {ativo.get('marca')}")
            print(f"Placa: {ativo.get('placa')}")
            print(f"Status: {ativo.get('status')}")
            print("-" * 30)
