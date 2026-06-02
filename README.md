# 📋 Sistema Mini-MRP - Documentação Completa

## 🎯 Visão Geral

Sistema de **Planejamento e Controle da Produção (MRP)** desenvolvido em Python para gerenciar:
- **Explosão de BOM** (Bill of Materials)
- **Cálculo de Necessidades** (Bruta e Líquida)
- **Cronograma de Compras** com Lead Time
- **Persistência de Dados** em arquivo

## 📁 Estrutura de Arquivos

```
projeto-mrp/
├── main.py                 # Menu principal interativo
├── persistencia.py         # Gerenciamento do arquivo estoque.txt
├── motor_mrp.py            # Lógica de cálculo MRP
├── classes_poo.py          # Classes Componente e ProdutoAcabado
├── cronograma_viz.py       # Visualização de cronogramas
├── plano_mestre.py         # Processamento de pedidos
├── estoque.txt             # Arquivo de dados persistentes
└── README.md               # Este arquivo
```

## 🚀 Como Executar

### Requisitos
- Python 3.6 ou superior
- Sem dependências externas (apenas biblioteca padrão)

### Instalação e Execução

1. **Navegue até o diretório do projeto:**
```bash
cd projeto-mrp
```

2. **Execute o programa:**
```bash
python main.py
```

3. **O programa criará automaticamente o arquivo `estoque.txt` na primeira execução**

## 📊 Funcionalidades Principais

### 1. ➕ Novo Pedido de Produção
Cria um novo pedido que passa pelo motor MRP:
- Seleciona o produto
- Define quantidade e semana de entrega
- Calcula automaticamente as ordens de compra
- Atualiza o estoque
- Registra a movimentação

**Exemplo:**
```
Produto: Cadeira
Quantidade: 100 unidades
Semana de Entrega: 5
```

### 2. 📊 Ver Cronograma de Compras
Exibe uma matriz com:
- Componentes nas linhas
- Semanas (1-8) nas colunas
- Quantidades a comprar em cada semana

**Exemplo de saída:**
```
Componente       | Sem1 | Sem2 | Sem3 | Sem4 | Sem5 | Sem6 | Sem7 | Sem8
Rodinhas         | ---  |  460 | --- | --- | --- | --- | --- | ---
Encosto          | ---  | --- |  100 | --- | --- | --- | --- | ---
Assento          | ---  | --- | --- |   80 | --- | --- | --- | ---
Eixo             | ---  | --- | --- |   90 | --- | --- | --- | ---
```

### 3. 📦 Consultar Estoque Atual
Lista todos os componentes com:
- Nome do componente
- Quantidade em estoque
- Lead time (tempo de entrega)

### 4. 📋 Histórico de Pedidos
Mostra todos os pedidos realizados com:
- Produto
- Quantidade
- Semana de entrega

### 5. 📝 Histórico de Movimentações
Registro detalhado de:
- Consumos de estoque
- Entradas de componentes

### 6. ⚙️ Gerenciar Componentes e Produtos
**Adicionar Novo Componente:**
```
Nome: Roda Extra
Estoque inicial: 100 unidades
Lead time: 2 semanas
```

**Adicionar Novo Produto:**
```
Nome: Cadeira Premium
Componentes:
  - 1x Assento
  - 1x Encosto
  - 1x Eixo
  - 6x Rodinhas (em vez de 5)
```

### 7. 📌 Consultar Estoque de Produto
Analisa viabilidade de produção:
- Mostra componentes necessários
- Compara com estoque disponível
- Calcula quantas unidades são possíveis produzir

## 📄 Formato do Arquivo estoque.txt

### Seção COMPONENTES
```
===== COMPONENTES =====
Nome|EstoqueAtual|LeadTime
Assento|20|1
Rodinhas|40|3
```

### Seção PRODUTOS
```
===== PRODUTOS =====
NomeProduto|Componente1:Qtd1,Componente2:Qtd2
Cadeira|Assento:1,Encosto:1,Eixo:1,Rodinhas:5
```

### Seção HISTÓRICO DE PEDIDOS
```
===== HISTORICO_PEDIDOS =====
Produto|Quantidade|Semana
2024-04-27 14:30:22|Cadeira|100|5
```

### Seção ORDENS DE COMPRA
```
===== ORDENS_COMPRA =====
Componente|Quantidade|SemanaCompra
2024-04-27 14:30:22|Rodinhas|460|2
```

### Seção MOVIMENTAÇÕES
```
===== MOVIMENTACOES =====
Tipo|Componente|Quantidade|Observação
2024-04-27 14:30:22|CONSUMO|Assento|100|Pedido Cadeira 100un
```

## 🧮 Cálculos MRP Explicados

### Fórmula Básica:
```
Necessidade_Bruta = Demanda × Quantidade_na_Receita
Necessidade_Líquida = Necessidade_Bruta - Estoque_Atual
Semana_Compra = Semana_Entrega - Lead_Time
```

### Exemplo Prático:
```
Pedido: 100 Cadeiras para Semana 5

Para Rodinhas (5 por cadeira, Lead Time 3 semanas):
  Necessidade_Bruta = 100 × 5 = 500 unidades
  Estoque_Atual = 40 unidades
  Necessidade_Líquida = 500 - 40 = 460 unidades
  Semana_Compra = 5 - 3 = Semana 2

Conclusão: Comprar 460 rodinhas na Semana 2
```

## 🔧 Modificando o Sistema

### Adicionar Novo Componente via Menu
1. Vá para "Gerenciar Componentes e Produtos"
2. Escolha "Adicionar Novo Componente"
3. Preencha: nome, estoque inicial, lead time

### Adicionar Novo Produto via Menu
1. Vá para "Gerenciar Componentes e Produtos"
2. Escolha "Adicionar Novo Produto"
3. Selecione componentes e quantidades

### Modificar Estoque Manualmente
Edite o arquivo `estoque.txt` diretamente na seção `===== COMPONENTES =====`

## 🐛 Tratamento de Erros

O sistema valida:
- ✅ Semanas entre 1 e 8
- ✅ Quantidades positivas
- ✅ Componentes existentes em produtos
- ✅ Lead times muito longos (aviso)
- ✅ Arquivo não encontrado (recria automaticamente)

## 📊 Estrutura das Classes

### Classe Componente
```python
class Componente:
    def __init__(self, nome, estoque_inicial, lead_time)
    def consumir(quantidade, motivo)
    def adicionar(quantidade)
    def to_dict()
```

### Classe ProdutoAcabado
```python
class ProdutoAcabado:
    def __init__(self, nome, receita_dict)
    def listar_componentes()
    def calcular_necessidade_total(quantidade)
```

## 🎓 Exemplo Completo de Uso

### Cenário: Produzir 50 Cadeiras para Semana 6

1. **Inicie o programa:**
```bash
python main.py
```

2. **Escolha opção 1: Novo Pedido**
   - Produto: Cadeira
   - Quantidade: 50
   - Semana: 6

3. **Sistema calcula:**
   - Assento: 50 - 20 = 30 na Semana 5 (6-1)
   - Encosto: 50 - 0 = 50 na Semana 4 (6-2)
   - Eixo: 50 - 10 = 40 na Semana 5 (6-1)
   - Rodinhas: 250 - 40 = 210 na Semana 3 (6-3)

4. **Confirme o pedido** e o estoque será atualizado

5. **Veja o cronograma** (opção 2) com as compras planejadas

## 📝 Dicas de Uso

- **Backup:** Faça cópia do `estoque.txt` antes de testes grandes
- **Lead Time:** Cuidado com lead times muito longos em prazos curtos
- **Estoque Negativo:** O sistema permite (para simulações), mas avisa
- **Relatórios:** Use a opção de Histórico para auditar operações

## 🔍 Resolução de Problemas

### Arquivo estoque.txt não criado
- Certifique-se que tem permissão de escrita na pasta
- Verifique se o Python foi instalado corretamente

### Erro ao adicionar produto
- Verifique se todos os componentes existem
- Use a opção "Listar Componentes" primeiro

### Semana calculada fica negativa
- Lead time maior que a semana de entrega
- Mude a semana de entrega para mais tarde

## 📞 Suporte

Para dúvidas sobre o MRP, consulte a documentação original do projeto.

---

**Desenvolvido como projeto educacional de Planejamento e Controle da Produção** 🏭

Última atualização: 2026
