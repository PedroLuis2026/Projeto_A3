from data.save_point import salvar_estoque, adicionar_movimentacao

class Componente:
    def __init__(self, nome, estoque_inicial, lead_time):
        self.nome = nome
        self.estoque = estoque_inicial
        self.lead_time = lead_time
    
    def consumir(self, quantidade, motivo=""):
        if quantidade > self.estoque:
            print(f"\033[33mATENÇÃO\033[m: Estoque insuficiente de {self.nome}")
            print(f" Dísponível: \033[32m{self.estoque}\033[m | Necessário: \033[33m{quantidade}\033[m")
            return False

        self.estoque -= quantidade
    
        adicionar_movimentacao("CONSUMO", self.nome, quantidade, motivo)
        
        return True
    
    def adicionar(self, quantidade, motivo="Entrada manual"):
        self.estoque += quantidade
        adicionar_movimentacao("ENTRADA", self.nome, quantidade, motivo)
    
    def __str__(self):
        return f"{self.nome}: {self.estoque} unidades (LT: {self.lead_time} sem.)"
    
    def to_dict(self):
        return {
            'estoque': self.estoque, 
            'lead_time': self.lead_time
        }
    
class ProdutoAcabado():
    def __init__(self, nome, receita_dict):
        self.nome = nome
        self.receita = receita_dict
    
    def listar_ordens(self):
        print(f"\nBOM - {self.nome}")
        print("-" * 40)
        for comp, quant in self.receita.items():
            print(f"  - {quant} x {comp}")
        print("-" * 40)
    
    def calcular_necessidade_t(self, quantidade_produzir):
        necessidades = {}
        for comp, quant_un in self.receita.items():
            necessidades[comp] = quantidade_produzir * quant_un
        return necessidades

    
def carregar_comp_objetos():
    from data.save_point import carregar_componentes

    dados = carregar_componentes()
    objetos = {}

    for nome, info in dados.items():
        objetos[nome] = Componente(nome, info['estoque'], info['lead_time'])
    
    return objetos

def salvar_comp_objetos(componentes_obj):
    dados_dict = {}
    for nome, obj in componentes_obj.items():
        dados_dict[nome] = obj.to_dict()
    salvar_estoque(dados_dict)
