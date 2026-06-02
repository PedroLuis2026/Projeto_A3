
from data.persistencia import *
from plano_mestre import *
from view.cronograma_viz import *


def limpar_tela():
    print("\n" * 2)


def exibir_menu_principal():
    print("\n" + "="*70)
    print(" "*15 + "SISTEMA MRP - CONTROLE DE PRODUÇÃO")
    print("="*70)
    print("\n1.  Novo Pedido de Produção")
    print("2.  Ver Cronograma de Compras")
    print("3.  Consultar Estoque Atual")
    print("4.  Histórico de Pedidos")
    print("5.  Histórico de Movimentações")
    print("6.  Gerenciar Componentes e Produtos")
    print("7.  Consultar Estoque de Produto")
    print("8.  Resumo de Compras")
    print("9.  Sair")
    print("\n" + "="*70)


def menu_gerenciamento():
    while True:
        print("\n" + "="*70)
        print(" "*20 + "GERENCIAMENTO")
        print("="*70)
        print("\n1.  Adicionar Novo Componente")
        print("2.  Adicionar Novo Produto")
        print("3.  Listar Componentes")
        print("4.  Listar Produtos")
        print("5.  Voltar ao Menu Principal")
        print("\n" + "="*70)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            adicionar_componente_novo()
        elif opcao == "2":
            adicionar_produto_novo()
        elif opcao == "3":
            listar_componentes_estoque()
            input("\nPressione ENTER para continuar...")
        elif opcao == "4":
            listar_produtos()
            input("\nPressione ENTER para continuar...")
        elif opcao == "5":
            break
        else:
            print("\n\033[31mOpção inválida!\033[m")


def adicionar_componente_novo():
    print("\n" + "="*70)
    print(" "*15 + "ADICIONAR NOVO COMPONENTE")
    print("="*70)
    
    try:
        nome = input("\nNome do componente: ").strip().title().replace(" De ", " de ").replace(" Da ", " da ").replace(" Do ", " do ")
        
        if not nome:
            print("\033[31mNome não pode estar vazio!\033[m")
            return
        
        estoque = int(input("Estoque inicial (unidades): "))
        if estoque < 0:
            print("\033[31mEstoque não pode ser negativo!\033[m")
            return
        
        lead_time = int(input("Lead time (semanas): "))
        if lead_time <= 0:
            print("\033[31mLead time deve ser positivo!\033[m")
            return
        
        if adicionar_componente(nome, estoque, lead_time):
            print("\033[32mComponente adicionado com sucesso!\033[m")
        
        input("\nPressione ENTER para continuar...")
    
    except ValueError:
        print("\n\033[31mDigite valores válidos!\033[m")
        input("\nPressione ENTER para continuar...")
    except Exception as e:
        print(f"\n\033[31mErro: {e}\033[m")
        input("\nPressione ENTER para continuar...")


def adicionar_produto_novo():
    print("\n" + "="*70)
    print(" "*15 + "ADICIONAR NOVO PRODUTO")
    print("="*70)
    
    try:
        componentes_disponiveis = carregar_componentes()
        
        if not componentes_disponiveis:
            print("\n\033[31mNenhum componente cadastrado!\033[m")
            input("\nPressione ENTER para continuar...")
            return
        
        nome_produto = input("\nNome do produto: ").strip().title().replace(" De ", " de ").replace(" Da ", " da ").replace(" Do ", " do ")
        
        if not nome_produto:
            print("\033[31mNome não pode estar vazio!\033[m")
            return
        
        print("\nComponentes disponíveis:")
        lista_componentes = sorted(componentes_disponiveis.keys())
        for i, comp in enumerate(lista_componentes, 1):
            print(f"  {i}. {comp}")
        
        receita = {}
        adicionar_mais = True
        
        while adicionar_mais:
            print()
            opcao = input("Escolha o número do componente (ou 0 para terminar): ").strip()
            
            if opcao == "0":
                if not receita:
                    print("\033[31mO produto deve ter pelo menos um componente!\033[m")
                    continue
                adicionar_mais = False
            else:
                try:
                    idx = int(opcao) - 1
                    if idx < 0 or idx >= len(lista_componentes):
                        print("\033[31mOpção inválida!\033[m")
                        continue
                    
                    comp = lista_componentes[idx]
                    
                    if comp in receita:
                        print(f"\033[33m{comp} já foi adicionado!\033[m")
                        continue
                    
                    qtd = int(input(f"Quantidade de '{comp}' por unidade: "))
                    
                    if qtd <= 0:
                        print("\033[31mQuantidade deve ser positiva!\033[m")
                        continue
                    
                    receita[comp] = qtd
                    print(f"\033[32m{qtd}x {comp} adicionado à receita\033[m")
                
                except ValueError:
                    print("\033[31mDigite um número válido!\033[m")
        
        if adicionar_produto(nome_produto, receita):
            print("\n\033[32mProduto adicionado com sucesso!\033[m")
        
        input("\nPressione ENTER para continuar...")
    
    except Exception as e:
        print(f"\n\033[31mErro: {e}\033[m")
        input("\nPressione ENTER para continuar...")


def main():
    inicializar_arquivo()
    
    print("\n" + "="*70)
    print(" "*15 + "BEM-VINDO AO SISTEMA MRP!")
    print("="*70)
    print("\nCarregando dados do sistema...")
    
    while True:
        try:
            componentes = carregar_componentes()
            produtos = carregar_produtos()
            
            exibir_menu_principal()
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                if not produtos:
                    print("\n\033[31mNenhum produto cadastrado! Adicione um produto no menu Gerenciar.\033[m")
                    input("\nPressione ENTER para continuar...")
                else:
                    processar_pedido(componentes, produtos)
                    input("\nPressione ENTER para continuar...")
            
            elif opcao == "2":
                exibir_cronograma()
                input("\nPressione ENTER para continuar...")
            
            elif opcao == "3":
                listar_componentes_estoque()
                input("\nPressione ENTER para continuar...")
            
            elif opcao == "4":
                exibir_historico()
                input("\nPressione ENTER para continuar...")
            
            elif opcao == "5":
                exibir_movimentacoes()
                input("\nPressione ENTER para continuar...")
            
            elif opcao == "6":
                menu_gerenciamento()
            
            elif opcao == "7":
                if not produtos:
                    print("\n\033[31mNenhum produto cadastrado!\033[m")
                    input("\nPressione ENTER para continuar...")
                else:
                    listar_produtos()
                    print()
                    produto = input("Digite o nome do produto: ").strip().title().replace(" De ", " de ").replace(" Da ", " da ").replace(" Do ", " do ")
                    consultar_estoque_produto(produto, componentes, produtos)
                    input("\nPressione ENTER para continuar...")
            
            elif opcao == "8":
                exibir_resumo_compras()
                input("\nPressione ENTER para continuar...")
            
            elif opcao == "9":
                print("\n" + "="*70)
                print("Obrigado por usar o Sistema MRP!")
                print("="*70 + "\n")
                break
            
            else:
                print("\n\033[31mOpção inválida!\033[m")
                input("\nPressione ENTER para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("Sistema interrompido pelo usuário.")
            print("="*70 + "\n")
            break
        
        except Exception as e:
            print(f"\n\033[31mErro inesperado: {e}\033[m")
            input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
