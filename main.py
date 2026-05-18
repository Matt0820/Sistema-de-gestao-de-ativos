from banco.database import inicializar_banco
from controle.ativo_controle import Ativo_Controle
from controle.cliente_controle import Cliente_Controle
from controle.locacao_controle import Locacao_Controle


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
    print("0. Sair")
    print("="*30)


def menu():
    # 1. Inicializa o banco (cria tabelas se não existirem)
    inicializar_banco()

    # 2. Inicializa os controles — ordem importa para o carregamento do banco
    ativo_controle   = Ativo_Controle()                          # carrega ativos do DB
    controle_locacao = Locacao_Controle(None, ativo_controle)    # sem cliente ainda
    controle_cliente = Cliente_Controle(controle_locacao)        # carrega clientes do DB
    controle_locacao.controle_cliente = controle_cliente         # injeta referência

    # 3. Agora que clientes e ativos estão prontos, carrega as locações
    controle_locacao.carregar_locacoes()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n--- CADASTROS ---")
            print("1. Cadastrar Ativo")
            print("2. Cadastrar Cliente")
            sub_opcao = input("Escolha uma opção: ")
            if sub_opcao == "1":
                ativo_controle.cadastrar_ativo()
            elif sub_opcao == "2":
                controle_cliente.cadastrar_cliente()
            else:
                print("Opção inválida! Retornando ao menu principal.")

        elif opcao == "2":
            print("\n--- BUSCA ---")
            print("1. Buscar Ativo")
            print("2. Buscar Cliente")
            sub_opcao = input("Escolha uma opção: ")
            if sub_opcao == "1":
                busca = input("Digite o ID ou PLACA do ativo: ")
                ativo = ativo_controle.buscar_ativo_por_id_ou_placa(busca)
                if ativo is None:
                    print("\nAtivo não encontrado.")
                else:
                    ativo.exibir_ativo()
            elif sub_opcao == "2":
                controle_cliente.buscar_cliente()
            else:
                print("Opção inválida! Retornando ao menu principal.")

        elif opcao == "3":
            print("\n--- LOCAÇÕES ---")
            print("1. Realizar Locação")
            print("2. Finalizar Locação")
            sub_opcao = input("Escolha uma opção: ")
            if sub_opcao == "1":
                controle_locacao.realizar_locacao()
            elif sub_opcao == "2":
                controle_locacao.finalizar_locacao()
            else:
                print("Opção inválida! Retornando ao menu principal.")

        elif opcao == "4":
            print("\n--- LISTAGENS ---")
            print("1. Listar Ativos")
            print("2. Listar Clientes")
            print("3. Listar Locações")
            sub_opcao = input("Escolha uma opção: ")
            if sub_opcao == "1":
                ativo_controle.listar_ativos()
            elif sub_opcao == "2":
                controle_cliente.listar_clientes()
            elif sub_opcao == "3":
                controle_locacao.listar_locacoes()
            else:
                print("Opção inválida! Retornando ao menu principal.")

        elif opcao == "5":
            print("\n" + "="*10 + "RELATORIOS" + "="*10)
            print("1. Relatório de Ativos Disponiveis")
            print("2. Relatório de Clientes Ativos")
            print("3. Relatório de Ativos Alugados")
            sub_opcao = input("Escolha uma opção: ")
            if sub_opcao == "1":
                ativo_controle.relatorio_ativos_disponiveis()
            elif sub_opcao == "2":
                controle_cliente.relatorio_clientes_ativos()
            elif sub_opcao == "3":
                ativo_controle.relatorio_ativos_alugados()
            else:
                print("Opção inválida! Retornando ao menu principal.")

        elif opcao == "6":
            print("\n--- EDITAR ---")
            print("1. Editar Ativo")
            print("2. Editar Cliente")
            sub_opcao = input("Escolha uma opção: ")
            if sub_opcao == "1":
                ativo_controle.editar_ativo()
            elif sub_opcao == "2":
                controle_cliente.editar_cliente()
            else:
                print("Opção inválida! Retornando ao menu principal.")

        elif opcao == "7":
            print("\n--- EXCLUIR ---")
            print("1. Excluir Ativo")
            print("2. Excluir Cliente")
            sub_opcao = input("Escolha uma opção: ")
            if sub_opcao == "1":
                ativo_controle.apagar_ativo()
            elif sub_opcao == "2":
                controle_cliente.apagar_cliente()
            else:
                print("Opção inválida! Retornando ao menu principal.")

        elif opcao == "0":
            print("Encerrando o sistema... Até logo!")
            break

        else:
            print("Opção inválida! Tente novamente.")


menu()
