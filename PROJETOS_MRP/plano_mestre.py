import os

def separação():
    print("=" * 50)

def menu_principal(lista):
    os.system("clear" if os.name != "nt" else "cls")
    separação()
    print("SISTEMA MRP".center(50))
    separação()
    print(f"{lista[0]} - Novo Pedido de Produção")
    print(f"{lista[1]} - Ver Cronograma de Compras")
    print(f"{lista[2]} - Consultar Estoque Atual")         
    print(f"{lista[3]} - Histórico de Pedidos")         
    print(f"{lista[4]} - Histórico de Movimentações")         
    print(f"{lista[5]} - Sair")
    print("=" * 50)
    while True:
        try:
            opçao = input("Digite a sua opção: ")
            if opçao not in ["1","2","3","4","5","6"] or not opçao:
                print("OPÇÃO INEXISTENTE!")
                continue
        except KeyboardInterrupt:
            print("ERRO, NÃO INTERROMPA FORÇADAMENTE O PROGRAMA!")
            continue
        break
    return opçao

def criar_pedido(produtos): 
    separação()
    print("NOVO PEDIDO DE PRODUÇÃO".center(50))
    separação()
    print("PRODUTOS DISPONIVEIS".center(50))
    for i , produto in enumerate(produtos.keys(), 1):
        print(f"\033[34m{i}: {produto}\033[m")
    while True:
        escolha_produto = input("Nome do Produto: ").title().strip()
        if escolha_produto not in produtos:
            print("\033[31mPRODUTO NÃO ENCONTRADO!\033[m")
            continue
        break
    while True:
        try:
            quantidade = int(input("Quantidade: "))
            if quantidade <= 0:
                print("\033[31mDIGITE UM NÚMERO VÁLIDO!\033[m")
                continue
        except (ValueError,KeyboardInterrupt):
            print("\033[31mDIGITE UM NÚMERO VÁLIDO!\033[m")
            continue
        break
    while True:
        try:
            semana = int(input("Semana de entrega(1-8): "))
            if semana < 1 or semana > 8:
                print("\033[33mA SEMANA DEVE ESTAR ENTRE 1 E 8!\033[m")
                continue
        except (ValueError,KeyboardInterrupt):
            print("\033[31mDIGITE UM NÚMERO VÁLIDO!\033[m")
            continue
        break
    return {'produto': escolha_produto, 'quantidade': quantidade, 'semana': semana}
    
