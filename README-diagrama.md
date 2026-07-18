# Diagrama de Classes - Sistema de Orçamento R.M

## Visão Geral

Este diagrama apresenta a modelagem estática do Sistema de Orçamento de Aluguel da Imobiliária R.M, utilizando os princípios de Programação Orientada a Objetos (POO).

## Arquivos Gerados

| Arquivo | Formato | Tamanho | Uso |
|---------|---------|---------|-----|
| `diagrama-classes.puml` | PlantUML | 7 KB | Código fonte do diagrama |
| `diagrama-classes.png` | PNG | 237 KB | Imagem para documentação |
| `diagrama-classes.svg` | SVG | 45 KB | Imagem vetorial (web) |
| `diagrama-classes.pdf` | PDF | 9 KB | Documento para impressão |

## Estrutura do Diagrama

### 1. Pacote: Modelo de Domínio

Contém as classes relacionadas aos imóveis:

```
┌─────────────────────────────────────────────────────────────┐
│                     Calculavel (Interface)                   │
│                     + calcular(): float                     │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ implementa
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Imovel (Classe Abstrata)                  │
│  - id: int                                                  │
│  - tipo: str                                                │
│  - valor_base: float                                        │
│  - quantidade_quartos: int                                  │
│  - quantidade_vagas: int                                    │
│  + calcular_aluguel(): float {abstract}                     │
│  + calcular_vagas(): float {abstract}                       │
│  + pode_ter_quarto_extra(): bool {abstract}                 │
└─────────────────────────────────────────────────────────────┘
              ▲               ▲               ▲
              │               │               │
     ┌────────┴──────┐ ┌─────┴──────┐ ┌──────┴───────┐
     │               │ │            │ │              │
┌────┴─────┐   ┌─────┴────┐  ┌─────┴────┐
│Apartamento│   │   Casa   │  │ Estudio  │
│ R$ 700   │   │  R$ 900  │  │ R$ 1200  │
└──────────┘   └──────────┘  └──────────┘
```

### 2. Pacote: Entidades de Negócio

Contém as classes de orçamento e contrato:

```
┌──────────────┐      ┌──────────────┐
│   Cliente    │      │  Orcamento   │
├──────────────┤      ├──────────────┤
│ - id         │◄─────│ - cliente    │
│ - nome       │  1   │ - imovel     │
│ - criancas   │      │ - desconto   │
└──────────────┘      │ - parcelas   │
                      └──────┬───────┘
                             │ 1
                             ▼
                      ┌──────────────┐
                      │   Contrato   │
                      ├──────────────┤
                      │ - valor      │
                      │ - parcelas   │
                      └──────┬───────┘
                             │ 1
                             ▼
                      ┌──────────────┐
                      │ProjecaoMensal│
                      ├──────────────┤
                      │ - meses[]    │
                      │ + csv()      │
                      └──────────────┘
```

## Classes Implementadas

### 1. Imovel (Abstrata)
- **Atributos**: id, tipo, valor_base, quantidade_quartos, quantidade_vagas
- **Métodos abstratos**: calcular_aluguel(), calcular_vagas(), pode_ter_quarto_extra()
- **Função**: Base para todos os tipos de imóveis

### 2. Apartamento
- **Herda de**: Imovel
- **Valor base**: R$ 700,00
- **Quarto extra**: +R$ 200,00
- **Vaga garagem**: R$ 300,00
- **Desconto**: 5% (se sem crianças)

### 3. Casa
- **Herda de**: Imovel
- **Valor base**: R$ 900,00
- **Quarto extra**: +R$ 250,00
- **Vaga garagem**: R$ 300,00
- **Desconto**: Não aplicável

### 4. Estudio
- **Herda de**: Imovel
- **Valor base**: R$ 1.200,00
- **Quarto extra**: Não permitido
- **Vagas**: R$ 250 (2 primeiras) + R$ 60 (adicionais)
- **Desconto**: Não aplicável

### 5. Cliente
- **Atributos**: id, nome, possui_criancas
- **Método**: eh_elegivel_desconto()
- **Função**: Armazena dados do cliente

### 6. Orcamento
- **Atributos**: id, cliente, imovel, parcelas, valores calculados
- **Métodos**: calcular_orcamento(), exibir_resumo()
- **Função**: Central do sistema, orquestra cálculos

### 7. Contrato
- **Constantes**: VALOR_TOTAL = 2000, MAX_PARCELAS = 5
- **Métodos**: validar_parcelas(), calcular_parcela()
- **Função**: Gerencia parcelamento da taxa

### 8. ProjecaoMensal
- **Atributos**: orcamento, contrato, meses[]
- **Métodos**: gerar_projecao(), exportar_csv()
- **Função**: Gera projeção de 12 meses para CSV

## Relacionamentos

| Relacionamento | Tipo | Cardinalidade | Descrição |
|----------------|------|---------------|-----------|
| Imovel → Apartamento | Herança | - | Apartamento é um tipo de Imovel |
| Imovel → Casa | Herança | - | Casa é um tipo de Imovel |
| Imovel → Estudio | Herança | - | Estudio é um tipo de Imovel |
| Imovel → Calculavel | Implementação | - | Imovel implementa Calculavel |
| Orcamento → Cliente | Associação | 1:1 | Orcamento usa Cliente |
| Orcamento → Imovel | Associação | 1:1 | Orcamento referencia Imovel |
| Contrato → Orcamento | Composição | 1:1 | Contrato é composto por Orcamento |
| ProjecaoMensal → Orcamento | Composição | 1:1 | Usa dados do Orcamento |
| ProjecaoMensal → Contrato | Composição | 1:1 | Usa dados do Contrato |

## Princípios POO Aplicados

### 1. Abstração
- Classe `Imovel` é abstrata, definindo contrato para subclasses
- Interface `Calculavel` define método comum para cálculos

### 2. Encapsulamento
- Atributos são protegidos (prefixo `_`)
- Acesso através de métodos getter
- Implementação interna oculta

### 3. Herança
- `Apartamento`, `Casa` e `Estudio` herdam de `Imovel`
- Reutilização de código e comportamento comum

### 4. Polimorfismo
- Métodos abstratos implementados de forma diferente em cada subclasse
- `calcular_aluguel()` e `calcular_vagas()` têm comportamento específico

## Regras de Negócio Implementadas

| Regra | Classe | Método |
|-------|--------|--------|
| Valor base por tipo | Imovel | __init__ |
| Quarto extra A (+200) | Apartamento | calcular_aluguel() |
| Quarto extra C (+250) | Casa | calcular_aluguel() |
| Vaga garagem (300) | Apartamento/Casa | calcular_vagas() |
| Vagas progressivas E | Estudio | calcular_vagas() |
| Desconto 5% | Apartamento | calcular_desconto() |
| Contrato 2000/parcelas | Contrato | calcular_parcela() |
| Projeção 12 meses | ProjecaoMensal | gerar_projecao() |

## Como Visualizar

### Opção 1: Abrir imagem PNG
```bash
# No Linux
xdg-open diagrama-classes.png

# No macOS
open diagrama-classes.png

# No Windows
start diagrama-classes.png
```

### Opção 2: Abrir SVG no navegador
```bash
# Qualquer sistema
xdg-open diagrama-classes.svg  # Linux
open diagrama-classes.svg      # macOS
start diagrama-classes.svg     # Windows
```

### Opção 3: Editar código fonte
```bash
# Abrir em editor de texto
code diagrama-classes.puml  # VS Code
vim diagrama-classes.puml   # Vim
```

## Regenerar Diagrama

Se precisar modificar o diagrama:

```bash
# Gerar todos os formatos
java -jar ~/.local/bin/plantuml.jar -tpng diagrama-classes.puml
java -jar ~/.local/bin/plantuml.jar -tsvg diagrama-classes.puml
java -jar ~/.local/bin/plantuml.jar -tpdf diagrama-classes.puml

# Ou usar o alias (se configurado)
plantuml diagrama-classes.puml
```

## Referências

- **Trabalho**: Algorithmic Thinking & Introduction to Object-Oriented Programming
- **Modelagem**: modelagem-problema.md
- **Ferramenta**: PlantUML 1.2026.6
