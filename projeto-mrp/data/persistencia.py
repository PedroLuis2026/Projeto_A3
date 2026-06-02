
ARQUIVO_ESTOQUE = "estoque.txt"


def inicializar_arquivo():
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as f:
            pass  
    except FileNotFoundError:
        with open(ARQUIVO_ESTOQUE, 'w', encoding='utf-8') as f:
            f.write("===== COMPONENTES =====\n")
            f.write("Assento|20|1\n")
            f.write("Encosto|0|2\n")
            f.write("Eixo|10|1\n")
            f.write("Rodinhas|40|3\n\n")
            
            f.write("===== PRODUTOS =====\n")
            f.write("Cadeira|Assento:1,Encosto:1,Eixo:1,Rodinhas:5\n\n")
            
            f.write("===== HISTORICO_PEDIDOS =====\n\n")
            f.write("===== ORDENS_COMPRA =====\n\n")
            f.write("===== MOVIMENTACOES =====\n\n")


def carregar_componentes():
    componentes = {}
    
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        return componentes
    
    lendo_componentes = False
    for linha in linhas:
        linha = linha.strip()
        
        if linha == "===== COMPONENTES =====":
            lendo_componentes = True
            continue
        elif linha.startswith("====="):
            lendo_componentes = False
            continue
        
        if lendo_componentes and linha:
            partes = linha.split("|")
            if len(partes) >= 3:
                nome = partes[0]
                estoque = int(partes[1])
                lead_time = int(partes[2])
                componentes[nome] = {"estoque": estoque, "lead_time": lead_time}
    
    return componentes


def carregar_produtos():
    produtos = {}
    
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        return produtos
    
    lendo_produtos = False
    for linha in linhas:
        linha = linha.strip()
        
        if linha == "===== PRODUTOS =====":
            lendo_produtos = True
            continue
        elif linha.startswith("====="):
            lendo_produtos = False
            continue
        
        if lendo_produtos and linha:
            partes = linha.split("|")
            if len(partes) >= 2:
                nome_produto = partes[0]
                receita_str = partes[1]
                
                receita = {}
                for item in receita_str.split(","):
                    comp_qtd = item.split(":")
                    if len(comp_qtd) == 2:
                        comp = comp_qtd[0].strip()
                        qtd = int(comp_qtd[1])
                        receita[comp] = qtd
                
                produtos[nome_produto] = receita
    
    return produtos


def adicionar_componente(nome, estoque_inicial, lead_time):
    componentes = carregar_componentes()
    
    if nome in componentes:
        print(f"\033[31mComponente '{nome}' já existe!\033[m")
        return False
    
    componentes[nome] = {"estoque": estoque_inicial, "lead_time": lead_time}
    salvar_estoque(componentes)
    print(f"\033[32mComponente '{nome}' adicionado com sucesso!\033[m")
    return True


def adicionar_produto(nome, receita_dict):
    produtos = carregar_produtos()
    
    if nome in produtos:
        print(f"\033[33mProduto '{nome}' já existe!\033[m")
        return False
    
    
    componentes = carregar_componentes()
    for comp in receita_dict.keys():
        if comp not in componentes:
            print(f"\033[31mComponente '{comp}' não existe no estoque!\033[m")
            return False
    
    produtos[nome] = receita_dict
    
   
    with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    
    receita_str = ",".join([f"{comp}:{qtd}" for comp, qtd in receita_dict.items()])
    linha_novo_produto = f"{nome}|{receita_str}\n"
    
    
    conteudo = conteudo.replace(
        "===== PRODUTOS =====\n",
        f"===== PRODUTOS =====\n{linha_novo_produto}"
    )
    
    with open(ARQUIVO_ESTOQUE, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"\033[32m Produto '{nome}' adicionado com sucesso!\033[m")
    return True


def salvar_estoque(componentes):
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        return
    
    novas_linhas = []
    lendo_componentes = False
    
    for linha in linhas:
        if linha.strip() == "===== COMPONENTES =====":
            novas_linhas.append(linha)
            lendo_componentes = True
            for nome, dados in componentes.items():
                novas_linhas.append(f"{nome}|{dados['estoque']}|{dados['lead_time']}\n")
            novas_linhas.append("\n")
            continue
        
        if lendo_componentes and linha.strip().startswith("====="):
            lendo_componentes = False
        
        if not lendo_componentes:
            novas_linhas.append(linha)
    
    with open(ARQUIVO_ESTOQUE, 'w', encoding='utf-8') as f:
        f.writelines(novas_linhas)


def adicionar_pedido(produto, quantidade, semana):

    linha = f"{produto}|{quantidade}|{semana}\n"
    
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except FileNotFoundError:
        return
    
    conteudo = conteudo.replace(
        "===== HISTORICO_PEDIDOS =====\n",
        f"===== HISTORICO_PEDIDOS =====\n{linha}"
    )
    
    with open(ARQUIVO_ESTOQUE, 'w', encoding='utf-8') as f:
        f.write(conteudo)


def adicionar_ordem_compra(componente, quantidade, semana):

    linha = f"{componente}|{quantidade}|{semana}\n"
    
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except FileNotFoundError:
        return
    
    conteudo = conteudo.replace(
        "===== ORDENS_COMPRA =====\n",
        f"===== ORDENS_COMPRA =====\n{linha}"
    )
    
    with open(ARQUIVO_ESTOQUE, 'w', encoding='utf-8') as f:
        f.write(conteudo)


def adicionar_movimentacao(tipo, componente, quantidade, observacao):
    linha = f"{tipo}|{componente}|{quantidade}|{observacao}\n"
    
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except FileNotFoundError:
        return
    
    conteudo = conteudo.replace(
        "===== MOVIMENTACOES =====\n",
        f"===== MOVIMENTACOES =====\n{linha}"
    )
    
    with open(ARQUIVO_ESTOQUE, 'w', encoding='utf-8') as f:
        f.write(conteudo)


def exibir_historico():
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print("\033[33m Arquivo estoque.txt não encontrado!\033[m")
        return
    
    print("\n" + "="*70)
    print(" "*20 + "HISTÓRICO DE PEDIDOS")
    print("="*70)
    
    lendo_historico = False
    encontrou_dados = False
    
    for linha in linhas:
        linha = linha.strip()
        
        if linha == "===== HISTORICO_PEDIDOS =====":
            lendo_historico = True
            continue
        elif linha.startswith("====="):
            if lendo_historico:
                break
        
        if lendo_historico and linha:
            encontrou_dados = True
            partes = linha.split("|")
            print(f"Produto: {partes[0]:<12} Qtd: {partes[1]:>5} un.  Semana: {partes[2]}")
    
    if not encontrou_dados:
        print("Nenhum pedido registrado ainda.")
    
    print("="*70)


def exibir_movimentacoes():
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print("\033[31mArquivo estoque.txt não encontrado!\033[m")
        return
    
    print("\n" + "="*100)
    print(" "*30 + "HISTÓRICO DE MOVIMENTAÇÕES")
    print("="*100)
    print(f"{"Tipo":<8} | {"Componente":<15} | {"Qtd":<6} | Observação")
    print("-"*100)
    
    lendo_mov = False
    encontrou_dados = False
    
    for linha in linhas:
        linha = linha.strip()
        
        if linha == "===== MOVIMENTACOES =====":
            lendo_mov = True
            continue
        elif linha.startswith("====="):
            if lendo_mov:
                break
        
        if lendo_mov and linha:
            encontrou_dados = True
            partes = linha.split("|")
            print(f"{partes[0]:<8} | {partes[1]:<15} | {partes[2]:<6} | {partes[3]}")
    
    if not encontrou_dados:
        print("Nenhuma movimentação registrada ainda.")
    
    print("="*100)


def listar_componentes_estoque():
    componentes = carregar_componentes()
    
    if not componentes:
        print("Nenhum componente cadastrado.")
        return
    
    print("\n" + "="*60)
    print(" "*15 + "COMPONENTES DISPONÍVEIS")
    print("="*60)
    print(f"{'Nome':<20} | {'Estoque Atual':<15} | {'Lead Time':<12}")
    print("-"*60)
    
    for nome, dados in sorted(componentes.items()):
        print(f"{nome:<20} | {str(dados['estoque']) + " un.":<14}  | {str(dados['lead_time']) + " sem.":<10} ")
    
    print("="*60)


def listar_produtos():
    produtos = carregar_produtos()
    
    if not produtos:
        print("Nenhum produto cadastrado.")
        return
    
    print("\n" + "="*70)
    print(" "*20 + "PRODUTOS DISPONÍVEIS")
    print("="*70)
    
    for i, (nome, receita) in enumerate(sorted(produtos.items()), 1):
        print(f"\n{i}. {nome}")
        print("   Receita:")
        for comp, qtd in receita.items():
            print(f"      • {qtd} x {comp}")
    
    print("\n" + "="*70)
