

arquivo = "estoque.txt"

def iniciar_arquivo():
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            pass
    except FileNotFoundError:
        with open(arquivo, 'w', ecoding='utf-8') as f:
            
            f.write("=== COMPONENTES ===\n")
            f.write("Assento|20un|1sem\n")
            f.write("Encosto|0un|2sem\n")
            f.write("Eixo|10un|1sem\n")
            f.write("Rodinhas|40un|3sem\n\n")
            
            f.write("=== PRODUTOS ===\n")
            f.write("Cadeira|Assento:1un,Encosto:1,Eixo:1,Rodinhas:5\n\n")

            f.write("=== HISTORICO PEDIDOS ===\n")
            f.write("=== ORDENS COMPRA ===\n")
            f.write("=== MOVIMENTAÇÕES ===\n")

def carregar_componentes():
    
    componentes = {}
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    lendo_linhas = False
    for linha in linhas:
        linha = linha.strip()

        if linha == "=== COMPONENTES ===":
            lendo_linhas = True
            continue
        elif linha.startswith("==="):
            lendo_linhas = False
            continue
        if lendo_linhas and linha:
            partes = linha.split("|")
            nome = partes[0]
            estoque = int(partes[1].replace("un", "").strip())
            lead_time = int(partes[2].replace("sem", "").strip())
            componentes[nome] = {"estoque": estoque, "lead_time": lead_time}
    
    return componentes  
        

