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
