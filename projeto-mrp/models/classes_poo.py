
class Componente:
    
    def __init__(self, nome, estoque_inicial, lead_time):
        self.nome = nome
        self.estoque = estoque_inicial
        self.lead_time = lead_time
    
    def consumir(self, quantidade, motivo=""):
        if quantidade > self.estoque:
            print(f"\033[33m  ATENÇÃO: Estoque insuficiente de {self.nome}!\033[m")
            print(f"   Disponível: {self.estoque} | Necessário: {quantidade}")
            return False
        
        self.estoque -= quantidade
        return True
    
    def adicionar(self, quantidade):
        self.estoque += quantidade
        return True
    
    def __str__(self):
        return f"{self.nome}: {self.estoque} unidades (Lead Time: {self.lead_time} semanas)"
    
    def to_dict(self):
        return {
            "estoque": self.estoque,
            "lead_time": self.lead_time
        }


class ProdutoAcabado:
    
    def __init__(self, nome, receita_dict):
        self.nome = nome
        self.receita = receita_dict
    
    def listar_componentes(self):
        print(f"\n{'='*50}")
        print(f"BOM - {self.nome}")
        print(f"{'='*50}")
        for comp, qtd in self.receita.items():
            print(f"  {qtd}x {comp}")
        print(f"{'='*50}")
    
    def calcular_necessidade_total(self, quantidade_produzir):
        necessidades = {}
        for comp, qtd_unit in self.receita.items():
            necessidades[comp] = quantidade_produzir * qtd_unit
        return necessidades
    
    def __str__(self):
        componentes_str = ", ".join([f"{qtd}x {comp}" for comp, qtd in self.receita.items()])
        return f"{self.nome} ({componentes_str})"
