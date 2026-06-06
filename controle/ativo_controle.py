from modelos.ativo import Ativo
from datetime import date
from dados import database
import re
class Ativo_Controle:

    def __init__(self):
        database.iniciar_banco()

    def _status_normalizado(self, status):
        return (status or '').strip().lower()

    def _ativo_disponivel(self, ativo):
        """Retorna True somente se o ativo estiver com status 'Disponível'."""
        return self._status_normalizado(ativo.get('status')) == 'disponível'

    def buscar_ativo_por_id_ou_placa(self, busca):
        return database.buscar_ativo_por_id_ou_placa(busca.strip())
    
    def validar_placa(self, placa):
    # Padrão Mercosul (AAA0A00) e Padrão Antigo (AAA-0000)
        padrao = r"^[A-Z]{3}\d{1}[A-Z]{1}\d{2}$|^[A-Z]{3}[0-9]{4}$"
        if re.match(padrao, placa.upper()):
            return True
        return False


    def cadastrar_ativo(self):
        print("\n--- CADASTRO DE ATIVO ---")
        modelo = input("Modelo: ").strip()
        marca = input("Marca: ").strip()

        while True:
            try:
                ano = int(input("Ano: "))
                if ano < 1900 or ano > date.today().year:
                    print("Ano inválido!")
                    continue
                break
            except ValueError:
                print("Erro: Ano deve ser um número inteiro!")

        while True:
            placa_input = input("Placa: ").strip().upper()
            if not self.validar_placa(placa_input):
                print("Erro: Placa inválida! Use o formato AAA-0000 ou AAA0A00.")
                continue
            if database.verificar_placa_existente(placa_input):
                print("Erro: Placa já cadastrada!")
            else:
                break

        while True:
            try:
                valor = float(input("Valor: "))
                if valor <= 0:
                    print("Valor inválido!")
                    continue
                break
            except ValueError:
                print("Erro: Valor deve ser um número!")

        while True:
            try:
                diaria = float(input("Valor da Diaria: "))
                if diaria <= 0:
                    print("Valor da diária inválido!")
                    continue
                break
            except ValueError:
                print("Erro: Valor da Diaria deve ser um número!")

        data = date.today()

        try:
            novo_obj = Ativo(modelo, marca, ano, placa_input, valor, diaria, data)
            depreciacao = novo_obj.calcular_depreciacao()
        except Exception:
            depreciacao = None

        database.cadastrar_ativo(modelo, marca, ano, placa_input, valor, diaria, data,
                                 status="Disponível", depreciacao=depreciacao)
        print("\nAtivo cadastrado com sucesso!")

    def listar_ativos(self):
        lista_ativos = database.listar_ativos()
        if not lista_ativos:
            print("\nNenhum ativo cadastrado.")
            return

        print("\n--- LISTA DE ATIVOS ---\n")
        for ativo in lista_ativos:
            self.exibir_ativo(ativo)

            
    def exibir_ativo(self, ativo):
        print(f"ID: {ativo.get('id_ativo')}")
        print(f"Modelo: {ativo.get('modelo')}")
        print(f"Marca: {ativo.get('marca')}")
        print(f"Ano: {ativo.get('ano')}")
        print(f"Placa: {ativo.get('placa')}")
        print(f"Valor: R$ {ativo.get('valor'):.2f}")
        print(f"Diária: R$ {ativo.get('diaria'):.2f}")
        print(f"Data de Cadastro: {ativo.get('data')}")
        print(f"Status: {ativo.get('status')}")
        if ativo.get('depreciacao') is not None:
            print(f"Depreciação Acumulada: R$ {ativo.get('depreciacao'):.2f}")
        print("-" * 30)

    def editar_ativo(self):
        if not database.listar_ativos():
            print("\nNenhum ativo cadastrado.")
            return

        id_editar = input("Digite o 'ID' ou 'PLACA' do ativo para editar: ").strip()
        ativo_encontrado = self.buscar_ativo_por_id_ou_placa(id_editar)

        if ativo_encontrado is None:
            print("\nAtivo não encontrado.")
            return

        status = self._status_normalizado(ativo_encontrado.get('status'))
        if status in ('alugado', 'manutenção'):
            print(f"Erro: O ativo {ativo_encontrado.get('modelo')} "
                  f"(ID: {ativo_encontrado.get('id_ativo')}) não pode ser editado pois está indisponível.")
            return

        print("\n--- Editar Ativo ---")
        print("Deixe em branco para manter o valor atual.")

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
            if novo_ano.isdigit() and 1900 <= int(novo_ano) <= date.today().year:
                dados_atualizados['ano'] = int(novo_ano)
            else:
                print("Ano inválido. Mantendo valor atual.")
        if nova_placa:
            if database.verificar_placa_existente(nova_placa, ativo_encontrado.get('id_ativo')):
                print("Erro: Placa já cadastrada!")
                return
            dados_atualizados['placa'] = nova_placa
        if novo_valor:
            try:
                v = float(novo_valor)
                if v > 0:
                    dados_atualizados['valor'] = v
                else:
                    print("Valor inválido. Mantendo valor atual.")
            except ValueError:
                print("Valor inválido. Mantendo valor atual.")
        if nova_diaria:
            try:
                d = float(nova_diaria)
                if d > 0:
                    dados_atualizados['diaria'] = d
                else:
                    print("Diária inválida. Mantendo valor atual.")
            except ValueError:
                print("Diária inválida. Mantendo valor atual.")

        if not dados_atualizados:
            print("\nNenhuma alteração informada.")
            return

        # Recalcula depreciação com os valores finais
        try:
            modelo_final  = dados_atualizados.get('modelo',  ativo_encontrado.get('modelo'))
            marca_final   = dados_atualizados.get('marca',   ativo_encontrado.get('marca'))
            ano_final     = dados_atualizados.get('ano',     ativo_encontrado.get('ano'))
            placa_final   = dados_atualizados.get('placa',   ativo_encontrado.get('placa'))
            valor_final   = dados_atualizados.get('valor',   ativo_encontrado.get('valor'))
            diaria_final  = dados_atualizados.get('diaria',  ativo_encontrado.get('diaria'))
            data_final    = ativo_encontrado.get('data')
            temp_obj = Ativo(modelo_final, marca_final, ano_final, placa_final,
                             valor_final, diaria_final, data_final)
            dados_atualizados['depreciacao'] = temp_obj.calcular_depreciacao()
        except Exception:
            pass

        database.atualizar_ativo(ativo_encontrado.get('id_ativo'), dados_atualizados)
        print("\nAtivo atualizado com sucesso!")

    def apagar_ativo(self):
        if not database.listar_ativos():
            print("Nenhum ativo cadastrado.")
            return

        busca = input("Digite o ID ou PLACA do ativo para apagar: ").strip()
        ativo_encontrado = self.buscar_ativo_por_id_ou_placa(busca)

        if ativo_encontrado is None:
            print("\nAtivo não encontrado.")
            return

        status = self._status_normalizado(ativo_encontrado.get('status'))
        if status in ('alugado', 'manutenção'):
            print(f"Erro: O ativo {ativo_encontrado.get('modelo')} "
                  f"(ID: {ativo_encontrado.get('id_ativo')}) está indisponível e não pode ser apagado.")
            return

        database.apagar_ativo(ativo_encontrado.get('id_ativo'))
        print(f"\nAtivo {ativo_encontrado.get('modelo')} "
              f"(ID: {ativo_encontrado.get('id_ativo')}) apagado com sucesso!")