
from engine.motor_calculos import *
from data.persistencia import *
from view.cronograma_viz import *


def criar_pedido(produtos):

    print("\n" + "="*70)
    print(" "*15 + "NOVO PEDIDO DE PRODUÇÃO")
    print("="*70)
    
    if not produtos:
        print("\033[31mNenhum produto cadastrado no sistema!\033[m")
        return None
    
    print("\nProdutos disponíveis:")
    lista_produtos = sorted(produtos.keys())
    for i, produto in enumerate(lista_produtos, 1):
        print(f"  {i}. {produto}")
    
    print()
    opcao = input("Escolha o número do produto (ou 0 para cancelar): ").strip()
    
    if opcao == "0":
        return None
    
    try:
        idx = int(opcao) - 1
        if idx < 0 or idx >= len(lista_produtos):
            print("\033[31mOpção inválida!\033[m")
            return None
        produto = lista_produtos[idx]
    except ValueError:
        print("\033[31mDigite um número válido!\033[m")
        return None
    
    try:
        quantidade = int(input("\nQuantidade a produzir: "))
        if quantidade <= 0:
            print("\033[31mQuantidade deve ser positiva!\033[m")
            return None
    except ValueError:
        print("\033[31mDigite um número válido!\033[m")
        return None
    
    try:
        semana = int(input("Semana de entrega (1-8): "))
        if semana < 1 or semana > 8:
            print("\033[33mSemana deve estar entre 1 e 8!\033[m")
            return None
    except ValueError:
        print("\033[31mDigite um número válido!\033[m")
        return None
    
    return {"produto": produto, "quantidade": quantidade, "semana": semana}


def processar_pedido(componentes, produtos):
    pedido = criar_pedido(produtos)
    
    if not pedido:
        print("\n\033[31mPedido cancelado!\033[m")
        return False
    
    receita = produtos[pedido["produto"]]
    eh_viavel, problemas = validar_viabilidade(
        receita, 
        pedido["quantidade"], 
        pedido["semana"],
        componentes
    )
    
    if not eh_viavel:
        print("\n\033[33mATENÇÃO: Pedido não é viável!\033[m")
        for problema in problemas:
            print(f"  • {problema}")
        return False
    
    ordens = calcular_mrp(
        receita, 
        pedido["quantidade"], 
        pedido["semana"],
        componentes
    )
    
    exibir_resumo_pedido(pedido, ordens)
    
    print()
    confirmacao = input("Confirmar pedido? (s/n): ").lower().strip()
    
    if confirmacao != 's':
        print("\n\033[31mPedido cancelado!\033[m")
        return False
    
    if processar_confirmacao_pedido(pedido, ordens, componentes):
        print("\n\033[32mPedido confirmado e salvo com sucesso!\033[m")
        
        print("\nExibindo cronograma atualizado...\n")
        exibir_cronograma()
        
        return True
    else:
        print("\n\033[31mErro ao processar pedido!\033[m")
        return False


def exibir_resumo_pedido(pedido, ordens):
    print("\n" + "="*75)
    print("RESUMO DO PEDIDO".center(75))
    print("="*75)
    print(f"Produto: {pedido['produto']}")
    print(f"Quantidade: {pedido['quantidade']} unidades")
    print(f"Entrega: Semana {pedido['semana']}")
    print("\nORDENS DE COMPRA GERADAS:")
    print("-"*75)
    print(f"{"Componente":<20} | {"Nec.Bruta":<12} | {"Estoque":<10} | {"Nec.Líquida":<12} | "
          f"{"Semana":<8}")
    print("-"*75)
    
    total_itens = 0
    
    for ordem in ordens:
        if ordem['necessidade'] > 0:
            print(f"{ordem['nome']:<20} | {str(ordem['necessidade_bruta']) + " un.":<12} | "
                  f"{str(ordem['estoque_atual']) + " un.":<10} | {str(ordem['necessidade']) + " un.":<12} | "
                  f"{str(ordem['semana_compra']) + " sem.":<6}")
            total_itens += ordem['necessidade']
        else:
            print(f"{ordem['nome']:<20} | {ordem['necessidade_bruta']:>10} un. | "
                  f"{ordem['estoque_atual']:>8} un. | {'(Em estoque)':<10} | {'---':>6}")
    
    print("-"*75)
    print(f"Total de itens a comprar: {total_itens} unidades")
    print("="*75)


def processar_confirmacao_pedido(pedido, ordens, componentes):
  
    try:

        adicionar_pedido(
            pedido['produto'], 
            pedido['quantidade'], 
            pedido['semana']
        )
        
        for ordem in ordens:
            if ordem['necessidade'] > 0:
                adicionar_ordem_compra(
                    ordem['nome'], 
                    ordem['necessidade'], 
                    ordem['semana_compra']
                )
                
                componentes[ordem['nome']]['estoque'] -= ordem['necessidade_bruta']
                
                adicionar_movimentacao(
                    "CONSUMO",
                    ordem['nome'],
                    ordem['necessidade_bruta'],
                    f"Pedido {pedido['produto']} {pedido['quantidade']}un - Entrega Sem{pedido['semana']}"
                )
        
        salvar_estoque(componentes)
        
        return True
    
    except Exception as e:
        print(f"\n\033[31mErro ao processar pedido: {e}\033[m")
        return False


def consultar_estoque_produto(produto, componentes, produtos):
    if produto not in produtos:
        print(f"\033[33mProduto '{produto}' não existe!\033[m")
        return
    
    receita = produtos[produto]
    
    print("\n" + "="*70)
    print(f"ANÁLISE DE ESTOQUE - {produto}")
    print("="*70)
    
    for comp, qtd_unit in receita.items():
        if comp in componentes:
            estoque = componentes[comp]['estoque']
            unidades_possiveis = estoque // qtd_unit if qtd_unit > 0 else 0
            
            print(f"\n{comp}:")
            print(f"  Necessário por unidade: {qtd_unit}")
            print(f"  Estoque disponível: {estoque}")
            print(f"  Quantidade de '{produto}' possível: {unidades_possiveis} un.")
        else:
            print(f"\n\033[33m{comp}: COMPONENTE NÃO ENCONTRADO NO ESTOQUE\033[m")
    
    print("\n" + "="*70)
