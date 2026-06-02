
def exibir_cronograma():

    ordens = carregar_ordens_compra()
    
    if not ordens:
        print("\n\033[33mNenhuma ordem de compra registrada ainda!\033[m")
        return
    

    matriz = {}
    componentes_ordenados = []
    
    for ordem in ordens:
        comp = ordem['componente']
        semana = ordem['semana']
        qtd = ordem['quantidade']
        
        if comp not in matriz:
            matriz[comp] = [0] * 8 
            componentes_ordenados.append(comp)
        

        matriz[comp][semana - 1] += qtd
    
    print("\n" + "="*100)
    print(" "*30 + "CRONOGRAMA DE COMPRAS")
    print("="*100)
    
    print(f"{"Componente":<20} | ", end="")
    for s in range(1, 9):
        print(f" Sem{s:>1} |", end="")
    print()
    print("-"*100)
    
    total_por_semana = [0] * 8
    
    for componente in sorted(componentes_ordenados):
        semanas = matriz[componente]
        print(f"{componente:<20} | ", end="")
        
        for idx, qtd in enumerate(semanas):
            if qtd > 0:
                print(f"{qtd:>5} |", end="")
                total_por_semana[idx] += qtd
            else:
                print(f"{"---":>5} |", end="")
        print()
    
    print("-"*100)
    print(f"{"TOTAL":<20} | ", end="")
    for qtd in total_por_semana:
        if qtd > 0:
            print(f"{qtd:>5} |", end="")
        else:
            print(f"{"---":>5} |", end="")
    print()
    
    print("="*100)
    print("\nLegenda: \"---\" = Sem necessidade de compra | Valores em unidades\n")


def carregar_ordens_compra():
    ARQUIVO_ESTOQUE = "estoque.txt"
    ordens = []
    
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        return ordens
    
    lendo_ordens = False
    for linha in linhas:
        linha = linha.strip()
        
        if linha == "===== ORDENS_COMPRA =====":
            lendo_ordens = True
            continue
        elif linha.startswith("====="):
            if lendo_ordens:
                break
        
        if lendo_ordens and linha:
            partes = linha.split("|")
            if len(partes) >= 3:
                ordens.append({
                    "componente": partes[0],
                    "quantidade": int(partes[1]),
                    "semana": int(partes[2])
                })
    
    return ordens


def exibir_grafico_semana(semana):
    ordens = carregar_ordens_compra()
    
    ordens_semana = [o for o in ordens if o['semana'] == semana]
    
    if not ordens_semana:
        print(f"\n\033[33mNenhuma compra programada para a Semana {semana}\033[m")
        return
    
    print(f"\n" + "="*60)
    print(f" "*15 + f"COMPRAS DA SEMANA {semana}")
    print("="*60)
    
    total = 0
    for ordem in ordens_semana:
        print(f"  • {ordem['componente']:<20} → {ordem['quantidade']:>5} unidades")
        total += ordem['quantidade']
    
    print("-"*60)
    print(f"Total de itens nesta semana: {total} unidades")
    print("="*60)


def exibir_resumo_compras():
    ordens = carregar_ordens_compra()
    
    if not ordens:
        print("\n\033[31mNenhuma ordem de compra registrada ainda!\033[m")
        return
    
    resumo = {}
    
    for ordem in ordens:
        comp = ordem['componente']
        qtd = ordem['quantidade']
        
        if comp not in resumo:
            resumo[comp] = {"total": 0, "semanas": []}
        
        resumo[comp]["total"] += qtd
        resumo[comp]["semanas"].append(ordem['semana'])
    
    print("\n" + "="*70)
    print(" "*20 + "RESUMO CONSOLIDADO DE COMPRAS")
    print("="*70)
    print(f"{'Componente':<20} | {'Total a Comprar':<18} | {'Semanas':<25}")
    print("-"*70)
    
    total_geral = 0
    
    for comp, dados in sorted(resumo.items()):
        semanas_str = ", ".join([f"Sem{s}" for s in sorted(set(dados['semanas']))])
        print(f"{comp:<20} | {str(dados['total']) + " un.":<17}  | {semanas_str:<25}")
        total_geral += dados['total']
    
    print("-"*70)
    print(f"{'TOTAL GERAL':<20} | {str(total_geral) + " un.":<17}  |")
    print("="*70)
