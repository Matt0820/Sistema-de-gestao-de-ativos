from controle.ativo_controle import Ativo_Controle
from controle.cliente_controle import Cliente_Controle
from controle.locacao_controle import Locacao_Controle
from controle.manutencao_controle import Manutencao_Controle
from dados.relatorios import Relatorios

#funcao que exibe os submenus
def exibir_menu():
    print("\n" + "="*30)
    print("      SISTEMA DE LOCAÇÃO")
    print("="*30)
    print("1. Cadastros")
    print("2. Busca")
    print("3. Locações")
    print("4. Listagens")
    print("5. Relatórios")
    print("6. Editar")
    print("7. Excluir")
    print("8. Manutenção")
    print("0. Sair")
    print("="*30)

#funcao principal do sistema que controla o fluxo do programa e chama as funcoes de cada controle
def menu():
    ativo_controle = Ativo_Controle()
    controle_locacao = Locacao_Controle(controle_ativo=ativo_controle)
    controle_cliente = Cliente_Controle(controle_locacao)
    controle_locacao.controle_cliente = controle_cliente
    controle_manutencao = Manutencao_Controle()
    relatorios = Relatorios()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- CADASTROS ---")
            print("1. Cadastrar Ativo")
            print("2. Cadastrar Cliente")
            sub_opcao = input("Escolha uma opção: ").strip()
            if sub_opcao == "1":
                ativo_controle.cadastrar_ativo()
            elif sub_opcao == "2":
                controle_cliente.cadastrar_cliente()
            else:
                print("Opção inválida!")

        elif opcao == "2":
            print("\n--- BUSCA ---")
            print("1. Buscar Ativo")
            print("2. Buscar Cliente")
            print("3. Buscar Locação")
            print("4. Buscar Manutenção")
            sub_opcao = input("Escolha uma opção: ").strip()
           
            if sub_opcao == "1":
                busca = input("Digite o ID ou PLACA do ativo: ").strip()
                ativo = ativo_controle.buscar_ativo_por_id_ou_placa(busca)
                if ativo is None:
                    print("\nAtivo não encontrado.")
                else:
                    ativo_controle.exibir_ativo(ativo)
           
            elif sub_opcao == "2":
                busca = input("Digite o ID ou CNH do cliente: ").strip()
                cliente = controle_cliente.buscar_cliente_por_id_ou_cnh(busca)
                if cliente is None:
                    print("\nCliente não encontrado.")
                else:
                    controle_cliente.exibir_cliente(cliente)
            
            elif sub_opcao == "3":
                id_locacao = input("Digite o ID da locação: ").strip()
                locacao = controle_locacao.buscar_locacao_por_id(id_locacao)
                if locacao is None:
                    print("\nLocação não encontrada.")
                else:
                    controle_locacao.exibir_locacao(locacao)
            
            elif sub_opcao == "4":
                id_manutencao = input("Digite o ID da manutenção: ").strip()
                manutencao = controle_manutencao.buscar_manutencao_por_id(id_manutencao)
                if manutencao is None:
                    print("\nManutenção não encontrada.")
                else:
                    controle_manutencao.exibir_manutencao(manutencao)
            
            else:
                print("Opção inválida!")

        elif opcao == "3":
            print("\n--- LOCAÇÕES ---")
            print("1. Realizar Locação")
            print("2. Finalizar Locação")
            sub_opcao = input("Escolha uma opção: ").strip()
            if sub_opcao == "1":
                controle_locacao.realizar_locacao()
            elif sub_opcao == "2":
                controle_locacao.finalizar_locacao()
            else:
                print("Opção inválida!")

        elif opcao == "4":
            print("\n--- LISTAGENS ---")
            print("1. Listar Ativos")
            print("2. Listar Clientes")
            print("3. Listar Locações")
            print("4. Listar Manutenções")
            sub_opcao = input("Escolha uma opção: ").strip()
            if sub_opcao == "1":
                ativo_controle.listar_ativos()
            elif sub_opcao == "2":
                controle_cliente.listar_clientes()
            elif sub_opcao == "3":
                controle_locacao.listar_locacoes()
            elif sub_opcao == "4":
                controle_manutencao.listar_manutencao()
            else:
                print("Opção inválida!")

        elif opcao == "5":
            print("\n" + "="*10 + " RELATÓRIOS " + "="*10)
            print("1. Ativos Disponíveis")
            print("2. Clientes com Locação Ativa")
            print("3. Ativos Alugados")
            print("4. Manutenções")          
            print("5. Relatório Financeiro") 
            sub_opcao = input("Escolha uma opção: ").strip()
            if sub_opcao == "1":
                relatorios.relatorio_ativos_disponiveis()
            elif sub_opcao == "2":
                relatorios.relatorio_clientes_ativos()
            elif sub_opcao == "3":
                relatorios.relatorio_ativos_alugados()
            elif sub_opcao == "4":                          
                relatorios.relatorio_manutencoes()          
            elif sub_opcao == "5":                          
                relatorios.relatorio_financeiro()           
            else:
                print("Opção inválida!")
                
        elif opcao == "6":
            print("\n--- EDITAR ---")
            print("1. Editar Ativo")
            print("2. Editar Cliente")
            
            sub_opcao = input("Escolha uma opção: ").strip()
            if sub_opcao == "1":
                ativo_controle.editar_ativo()
            elif sub_opcao == "2":
                controle_cliente.editar_cliente()
            else:
                print("Opção inválida!")

        elif opcao == "7":
            print("\n--- EXCLUIR ---")
            print("1. Excluir Ativo")
            print("2. Excluir Cliente")
            print("3. Excluir manutencao")
            sub_opcao = input("Escolha uma opção: ").strip()
            if sub_opcao == "1":
                ativo_controle.apagar_ativo()
            elif sub_opcao == "2":
                controle_cliente.apagar_cliente()
            elif sub_opcao == "3":
                controle_manutencao.apagar_manutencao()
            else:
                print("Opção inválida!")

        elif opcao == "8":
            print("\n--- MANUTENÇÃO ---")
            print("1. Criar Manutenção")
            print("2. Listar Manutenções")
            print("3. Finalizar Manutenção")
            sub_opcao = input("Escolha uma opção: ").strip()
            if sub_opcao == "1":
                controle_manutencao.criar_manutencao()
            elif sub_opcao == "2":
                controle_manutencao.listar_manutencao()
            elif sub_opcao == "3":
                controle_manutencao.finalizar_manutencao()
            else:
                print("Opção inválida!")
        elif opcao == "0":
            print("Encerrando o sistema... Até logo!")
            break

        else:
            print("Opção inválida! Tente novamente.")

menu()