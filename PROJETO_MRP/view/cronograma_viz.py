def carregar_ordens_compra():
    from data.save_point import arquivo

    ordens= []

    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        return ordens

    lendo_ordens = False
    for linha in linhas:
        linha = linha.strip()

        if linha == "===== ORDENS COMPRA =====":
            lendo_ordens = True
            continue
        elif linha.startswith("====="):
            if lendo_ordens:
                break
        
        if lendo_ordens and linha:
            partes = linha.split("|")
            ordens.append({
                'componente': partes[0],
                'quantidade': int(partes[1]),
                'semana': int(partes[2])
            })

    return ordens

def exibir_cronograma():
    ordens = carregar_ordens_compra()

    if not ordens:
        print("\033[31mNenhuma ordem de compra registrada ainda!\033[m")
        return 

    matriz = {}

    for ordem in ordens:
        comp = ordem['componente']
        semana = ordem['semana']
        qtd = ordem['quantidade']

        if comp not in matriz:
            matriz[comp] = [0] * 8

        matriz[comp][semana - 1] += qtd

    print("=" * 90)
    print("CRONOGRAMA DE COMPRAS".center(90))
    print("=" * 90)

    print(f"{"Componente":<15} | ", end="")
    for s in range(1, 9):
        print(f"Sem{s:>2} | ", end="")
    print()
    print("-" * 90) 

    for componente, semanas in sorted(matriz.items()):
        print(f"{componente:<15} | ", end="")
        for qtd in semanas:
            if qtd > 0:
                print(f"{qtd:>5} | ", end="")
            else:
                print(f"{"---":>5} | ", end="")
        print()
    
def exibir_grafico_semana(semana):
    ordens = carregar_ordens_compra()
    
    ordens_semana = [o for o in ordens if o['semana'] == semana]
    
    if not ordens_semana:
        print(f"\033[33mNenhuma compra programada para a Semana {semana}\033[m")
        return
    
    print(f"COMPRAS DA SEMANA {semana}")
    print("="*50)
    
    total = 0
    for ordem in ordens_semana:
        print(f"  • {ordem['componente']:<15} → {ordem['quantidade']:>5} unidades")
        total += ordem['quantidade']
    
    print("="*50)
    print(f"Total de itens: {total}")