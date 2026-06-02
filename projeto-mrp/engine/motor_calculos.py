
def calcular_mrp(receita, demanda, semana_entrega, componentes):

    resultado = []
    
    for nome_componente, qtd_receita in receita.items():
        if nome_componente not in componentes:
            print(f"\033[33mAVISO: Componente '{nome_componente}' não encontrado no estoque!\033[m")
            continue
        
        dados_comp = componentes[nome_componente]
        
        nec_bruta = demanda * qtd_receita
        
    
        estoque_atual = dados_comp['estoque']
        nec_liquida = max(0, nec_bruta - estoque_atual)
        

        semana_compra = semana_entrega - dados_comp['lead_time']

        if semana_compra < 1:
            semana_compra = 1
            print(f"\033[33mAVISO: Lead time do {nome_componente} é muito longo!\033[m")
        
        resultado.append({
            "nome": nome_componente,
            "necessidade_bruta": nec_bruta,
            "necessidade": nec_liquida,
            "semana_compra": semana_compra,
            "estoque_atual": estoque_atual,
            "lead_time": dados_comp['lead_time']
        })
    
    return resultado


def validar_viabilidade(receita, demanda, semana_entrega, componentes):
    problemas = []
    
    for nome_componente, qtd_receita in receita.items():
        if nome_componente not in componentes:
            problemas.append(f"Componente '{nome_componente}' não existe no estoque")
            continue
        
        dados_comp = componentes[nome_componente]
        semana_necessaria = semana_entrega - dados_comp['lead_time']
        
        if semana_necessaria < 1:
            problemas.append(
                f"Lead time do {nome_componente} ({dados_comp['lead_time']} sem.) "
                f"é incompatível com semana de entrega {semana_entrega}"
            )
    
    return (len(problemas) == 0, problemas)


def gerar_relatorio_mrp(resultado):
    print("\n" + "="*100)
    print("RELATÓRIO DETALHADO DO CÁLCULO MRP")
    print("="*100)
    print(f"{'Componente':<20} | {'Nec.Bruta':<12} | {'Estoque':<10} | {'Nec.Líquida':<12} | "
          f"{'Lead Time':<10} | {'Semana Compra':<13}")
    print("-"*100)
    
    for ordem in resultado:
        print(f"{ordem['nome']:<20} | {ordem['necessidade_bruta']:>10} un. | "
              f"{ordem['estoque_atual']:>8} un. | {ordem['necessidade']:>10} un. | "
              f"{ordem['lead_time']:>8} sem. | {ordem['semana_compra']:>11}")
    
    print("="*100)
