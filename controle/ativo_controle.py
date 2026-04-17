#importa a classe Ativo para manipular os dados dos ativos
from modelos.ativo import Ativo
#Importa o datetime
from datetime import date


#classe de controle de dados dos ativos, pois um unico controle unico é desnecessárimente extenso e pouluido.
class Ativo_Controle:

    #metodo construtor para inicializar a lista de ativos
    def __init__(self):
        self.lista_ativos = []

    #metodo auxiliar para padronizar comparações de status
    def status_normalizado(self, status):
        return status.strip().lower()

    #metodo para buscar um ativo pelo ID ou pela placa
    def buscar_ativo_por_id_ou_placa(self, busca):
        busca = busca.strip().upper()

        for ativo in self.lista_ativos:
            if (busca.isdigit() and ativo.id_ativo == int(busca)) or ativo.placa == busca:
                return ativo

        return None

    #metodo para verificar se uma placa já está cadastrada
    def placa_ja_cadastrada(self, placa, id_ignorar=None):
        placa = placa.strip().upper()

        for ativo in self.lista_ativos:
            if ativo.placa == placa and ativo.id_ativo != id_ignorar:
                return True

        return False

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

            if self.placa_ja_cadastrada(placa_input):
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
        novo = Ativo(modelo, marca, ano, placa_input, valor, diaria, data)

        #adiciona o novo ativo à lista de ativos do controle
        self.lista_ativos.append(novo)
        print("\nAtivo cadastrado com sucesso!")

    #metodo para listar todos os ativos cadastrados, exibindo seus dados de forma organizada
    def listar_ativos(self):
        #verifica se a lista de ativos está vazia, caso esteja, exibe uma mensagem informando que não há ativos cadastrados e retorna
        if len(self.lista_ativos) == 0:
            print("\nNenhum ativo cadastrado.")
            return

        #percorre a lista de ativos e chama o método exibir_ativo de cada objeto ativo para exibir seus dados
        print("\n--- LISTA DE ATIVOS ---")
        for ativo in self.lista_ativos:
            ativo.exibir_ativo()

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
        if self.status_normalizado(ativo_encontrado.status) == "alugado":
            print(f"Erro: O ativo {ativo_encontrado.modelo} (ID: {ativo_encontrado.id_ativo}) está atualmente Alugado e não pode ser editado.")
            return

        print("\n--- Editar Ativo ---")
        print("Deixe em branco para manter o valor atual.")

        #solicita os novos dados e mantém o atual caso fique em branco
        novo_modelo = input(f"Modelo ({ativo_encontrado.modelo}): ").strip()
        if novo_modelo:
            ativo_encontrado.modelo = novo_modelo

        nova_marca = input(f"Marca ({ativo_encontrado.marca}): ").strip()

        #se o usuário digitar uma nova marca, atualiza o atributo marca do ativo encontrado
        if nova_marca:
            ativo_encontrado.marca = nova_marca

        novo_ano = input(f"Ano ({ativo_encontrado.ano}): ").strip()

        #se o usuário digitar um novo ano, verifica se é um número inteiro e atualiza o atributo ano do ativo encontrado, caso contrário, exibe uma mensagem de erro e mantém o valor atual
        if novo_ano:
            if novo_ano.isdigit():
                ativo_encontrado.ano = int(novo_ano)
            else:
                print("Ano inválido. Mantendo valor atual.")

        nova_placa = input(f"Placa ({ativo_encontrado.placa}): ").strip().upper()

        #se o usuário digitar uma nova placa, verifica se já está cadastrada para outro ativo e, se não estiver, atualiza o atributo placa do ativo encontrado, caso contrário, exibe uma mensagem de erro e mantém o valor atual
        if nova_placa:
            if self.placa_ja_cadastrada(nova_placa, ativo_encontrado.id_ativo):
                print("Erro: Placa já cadastrada!")
                return

            ativo_encontrado.placa = nova_placa

        novo_valor = input(f"Valor ({ativo_encontrado.valor}): ").strip()

        #se o usuário digitar um novo valor, tenta converter para float e atualiza o atributo valor do ativo encontrado, caso contrário, exibe uma mensagem de erro e mantém o valor atual
        if novo_valor:
            try:
                ativo_encontrado.valor = float(novo_valor)
            except ValueError:
                print("Valor inválido. Mantendo valor atual.")

        nova_diaria = input(f"Diária ({ativo_encontrado.diaria}): ").strip()

        #se o usuário digitar uma nova diária, tenta converter para float e atualiza o atributo diaria do ativo encontrado, caso contrário, exibe uma mensagem de erro e mantém o valor atual
        if nova_diaria:
            try:
                ativo_encontrado.diaria = float(nova_diaria)
            except ValueError:
                print("Diária inválida. Mantendo valor atual.")

        #atualiza o valor depreciado após a edição
        ativo_encontrado.depreciacao_final = ativo_encontrado.calcular_depreciacao()
        print("\nAtivo atualizado com sucesso!")

    #metodo para apagar um ativo existente, solicitando ao usuário o ID ou a placa do ativo a ser apagado
    def apagar_ativo(self):

        #verifica se a lista de ativos está vazia, caso esteja, exibe uma mensagem informando que não há ativos cadastrados e retorna
        if len(self.lista_ativos) == 0:
            print("Nenhum ativo cadastrado.")
            return

        #solicita ao usuário o ID ou a placa do ativo a ser apagado
        busca = input("Digite o ID ou PLACA do ativo para apagar: ")
        ativo_encontrado = self.buscar_ativo_por_id_ou_placa(busca)

        #se nenhum ativo for encontrado com o ID ou placa fornecida, exibe uma mensagem informando que o ativo não foi encontrado e retorna
        if ativo_encontrado is None:
            print("\nAtivo não encontrado.")
            return

        #verifica se o ativo encontrado está atualmente alugado, caso esteja, exibe uma mensagem de erro informando que o ativo não pode ser apagado e retorna
        if self.status_normalizado(ativo_encontrado.status) == "alugado":
            print(
                f"Erro: O ativo {ativo_encontrado.modelo} "
                f"(ID: {ativo_encontrado.id_ativo}) está Alugado e não pode ser apagado."
            )
            return

        #remove o ativo encontrado da lista de ativos do controle e exibe uma mensagem informando que o ativo foi apagado com sucesso
        self.lista_ativos.remove(ativo_encontrado)
        print(
            f"\nAtivo {ativo_encontrado.modelo} "
            f"(ID: {ativo_encontrado.id_ativo}) apagado com sucesso!"
        )

    #metodo para gerar um relatório de ativos disponíveis, filtrando a lista de ativos para exibir apenas aqueles com status "Disponivel" e chamando o método exibir_ativo de cada um para mostrar seus dados
    def relatorio_ativos_disponiveis(self):

        print("\n--- RELATÓRIO DE ATIVOS DISPONÍVEIS ---")

        #filtra a lista de ativos para criar uma nova lista contendo apenas os ativos que estão com status disponível
        ativos_disponiveis = [
            ativo for ativo in self.lista_ativos
            if self.status_normalizado(ativo.status) == "disponível"
        ]

        #se a lista de ativos disponíveis estiver vazia, exibe uma mensagem informando que não há ativos disponíveis no momento e retorna
        if not ativos_disponiveis:
            print("Nenhum ativo Disponível no momento.")
            return

        #percorre a lista de ativos disponíveis e chama o método exibir_ativo de cada objeto ativo para exibir seus dados
        for ativo in ativos_disponiveis:
            ativo.exibir_ativo()

    #metodo para gerar um relatório de ativos alugados, filtrando a lista de ativos para exibir apenas aqueles com status "Alugado" e chamando o método exibir_ativo de cada um para mostrar seus dados
    def relatorio_ativos_alugados(self):
        print("\n--- RELATÓRIO DE ATIVOS ALUGADOS ---")

        #filtra a lista de ativos para criar uma nova lista contendo apenas os ativos que estão com status "Alugado", utilizando uma list comprehension para percorrer a lista de ativos e verificar o status de cada um
        alugados = [
            ativo for ativo in self.lista_ativos
            if self.status_normalizado(ativo.status) == "alugado"
        ]

        #se a lista de ativos alugados estiver vazia, exibe uma mensagem informando que não há ativos alugados no momento e retorna
        if not alugados:
            print("Nenhum ativo Alugado no momento.")
            return

        #percorre a lista de ativos alugados e chama o método exibir_ativo de cada objeto ativo para exibir seus dados
        for ativo in alugados:
            ativo.exibir_ativo()
