# Modelagem Dinâmica - Sistema de Orçamento de Aluguel R.M

## 1. Visão Geral

Este documento apresenta a modelagem dinâmica do Sistema de Orçamento de Aluguel da Imobiliária R.M, demonstrando como o sistema atende aos requisitos funcionais através de uma **arquitetura em camadas**.

---

## 2. Arquitetura em Camadas

O sistema é estruturado em 4 camadas bem definidas, seguindo o princípio de **separação de responsabilidades**:

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                    │
│                        (Interface CLI)                       │
│  • Entrada de dados do usuário                               │
│  • Exibição de resultados                                    │
│  • Validação de entrada básica                               │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE CONTROLE                        │
│                      (Orcamento)                             │
│  • Orquestração dos cálculos                                 │
│  • Coordenação entre camadas                                 │
│  • Validação de regras de negócio                            │
└──────────────────────────────┬──────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                              ▼
┌───────────────────────────┐  ┌───────────────────────────┐
│    CAMADA DE NEGÓCIO      │  │    CAMADA DE DOMÍNIO       │
│   (Contrato, Projecao)    │  │  (Imovel, Cliente, etc.)   │
│ • Cálculo parcelamento    │  │ • Entidades de dados       │
│ • Geração projeção CSV    │  │ • Regras específicas       │
│ • Validações específicas  │  │ • Cálculos polimórficos    │
└───────────────────────────┘  └───────────────────────────┘
```

### 2.1. Camada de Apresentação (Interface)

**Responsabilidade**: Interface com o usuário final.

| Componente | Função |
|------------|--------|
| `Interface` | Recebe entradas do usuário via CLI |
| Validação | Valida formato dos dados antes de enviar |
| Exibição | Mostra resultados e mensagens de erro |

**Princípio POO aplicado**: *Abstração* - O usuário não precisa conhecer a complexidade interna dos cálculos.

---

### 2.2. Camada de Controle

**Responsabilidade**: Orquestrar as operações do sistema.

| Componente | Função |
|------------|--------|
| `Orcamento` | Coordena criação do orçamento |
| Validação | Verifica regras de negócio |
| Integração | Conecta camada de apresentação com negócio/domínio |

**Princípio POO aplicado**: *Encapsulamento* - A lógica de orquestração está isolada e protegida.

---

### 2.3. Camada de Negócio

**Responsabilidade**: Implementar regras de negócio específicas.

| Componente | Função |
|------------|--------|
| `Contrato` | Calcula parcelamento da taxa (R$ 2.000) |
| `ProjecaoMensal` | Gera projeção de 12 meses para CSV |

**Princípio POO aplicado**: *Herança* - Reutiliza dados do orçamento sem duplicação.

---

### 2.4. Camada de Domínio

**Responsabilidade**: Representar entidades de dados e cálculos específicos.

| Componente | Função |
|------------|--------|
| `Imovel` (abstrata) | Define contrato para cálculo de aluguel |
| `Apartamento` | Implementa cálculo específico (R$ 700 + adicionais) |
| `Casa` | Implementa cálculo específico (R$ 900 + adicionais) |
| `Estudio` | Implementa cálculo específico (R$ 1.200 + progressivo) |
| `Cliente` | Armazena dados e verifica elegibilidade |

**Princípio POO aplicado**: *Polimorfismo* - Cada tipo de imóvel calcula o aluguel de forma diferente.

---

## 3. Diagramas de Sequência

### 3.1. UC01: Gerar Orçamento de Aluguel

```
┌──────┐          ┌─────────┐          ┌──────┐          ┌──────┐
│ UI   │          │ Orcamento│          │ Imovel│          │Cliente│
└──┬───┘          └────┬─────┘          └──┬───┘          └──┬───┘
   │                   │                   │                   │
   │  1: Solicitar     │                   │                   │
   │  dados imóvel     │                   │                   │
   │──────────────────>│                   │                   │
   │                   │                   │                   │
   │                   │  2: Criar imóvel  │                   │
   │                   │──────────────────>│                   │
   │                   │                   │                   │
   │                   │  3: Criar cliente │                   │
   │                   │──────────────────────────────────────>│
   │                   │                   │                   │
   │                   │  4: Calcular      │                   │
   │                   │  aluguel          │                   │
   │                   │──────────────────>│                   │
   │                   │                   │                   │
   │                   │  5: Verificar     │                   │
   │                   │  desconto         │                   │
   │                   │──────────────────────────────────────>│
   │                   │                   │                   │
   │  6: Retornar      │                   │                   │
   │  orçamento        │                   │                   │
   │<──────────────────│                   │                   │
   │                   │                   │                   │
   │  7: Exibir        │                   │                   │
   │  resultado        │                   │                   │
   │───┐               │                   │                   │
   │<──┘               │                   │                   │
```

**Fluxo detalhado:**

| Etapa | Origem | Destino | Mensagem | Descrição |
|-------|--------|---------|----------|-----------|
| 1 | UI | Orcamento | `criar_orcamento()` | Usuário insere tipo, quartos, vagas, crianças |
| 2 | Orcamento | Imovel | `new(tipo, quartos, vagas)` | Cria instância do imóvel (polimórfico) |
| 3 | Orcamento | Cliente | `new(nome, possui_criancas)` | Cria instância do cliente |
| 4 | Orcamento | Imovel | `calcular_aluguel()` | Calcula valor (base + adicionais) |
| 5 | Orcamento | Cliente | `eh_elegivel_desconto()` | Verifica se aplica 5% |
| 6 | Orcamento | UI | `orcamento_completo` | Retorna valores calculados |
| 7 | UI | Usuário | `exibir_resumo()` | Mostra resultado formatado |

---

### 3.2. UC02: Calcular Parcelamento do Contrato

```
┌──────┐          ┌─────────┐          ┌─────────┐
│ UI   │          │ Orcamento│          │ Contrato │
└──┬───┘          └────┬─────┘          └────┬────┘
   │                   │                     │
   │  1: Definir       │                     │
   │  parcelas         │                     │
   │──────────────────>│                     │
   │                   │                     │
   │                   │  2: Criar contrato  │
   │                   │────────────────────>│
   │                   │                     │
   │                   │  3: Validar (1-5)   │
   │                   │                     │───┐
   │                   │                     │<──┘
   │                   │                     │
   │                   │  4: Calcular        │
   │                   │  parcela            │
   │                   │────────────────────>│
   │                   │                     │
   │  5: Retornar      │                     │
   │  valor parcela    │                     │
   │<──────────────────│                     │
   │                   │                     │
   │  6: Exibir        │                     │
   │  resultado        │                     │
   │───┐               │                     │
   │<──┘               │                     │
```

**Fluxo detalhado:**

| Etapa | Origem | Destino | Mensagem | Descrição |
|-------|--------|---------|----------|-----------|
| 1 | UI | Orcamento | `definir_parcelas(n)` | Usuário informa 1-5 parcelas |
| 2 | Orcamento | Contrato | `new(2000, parcelas)` | Cria contrato com valor fixo |
| 3 | Contrato | Contrato | `validar_parcelas()` | Verifica se 1 ≤ n ≤ 5 |
| 4 | Contrato | Contrato | `calcular_parcela()` | 2000 / número parcelas |
| 5 | Orcamento | UI | `valor_parcela` | Retorna valor calculado |
| 6 | UI | Usuário | `exibir_parcela()` | Mostra valor da parcela |

---

### 3.3. UC03: Exportar Orçamento em CSV

```
┌──────┐          ┌─────────┐          ┌──────────┐
│ UI   │          │ Orcamento│          │ProjecaoM │
└──┬───┘          └────┬─────┘          └────┬─────┘
   │                   │                     │
   │  1: Gerar         │                     │
   │  projeção         │                     │
   │──────────────────>│                     │
   │                   │                     │
   │                   │  2: Criar projeção  │
   │                   │────────────────────>│
   │                   │                     │
   │                   │  3: Gerar 12 meses  │
   │                   │                     │───┐
   │                   │                     │   │ Para cada mês:
   │                   │                     │   │ - aluguel
   │                   │                     │   │ - parcela (se ≤ n)
   │                   │                     │   │ - total
   │                   │                     │<──┘
   │                   │                     │
   │                   │  4: Exportar CSV    │
   │                   │────────────────────>│
   │                   │                     │
   │                   │  5: Arquivo criado  │
   │                   │<────────────────────│
   │                   │                     │
   │  6: Confirmar     │                     │
   │  exportação       │                     │
   │<──────────────────│                     │
   │                   │                     │
   │  7: Exibir        │                     │
   │  sucesso          │                     │
   │───┐               │                     │
   │<──┘               │                     │
```

**Fluxo detalhado:**

| Etapa | Origem | Destino | Mensagem | Descrição |
|-------|--------|---------|----------|-----------|
| 1 | UI | Orcamento | `gerar_projecao()` | Solicita geração do CSV |
| 2 | Orcamento | ProjecaoMensal | `new(orcamento, contrato)` | Cria projeção com dados |
| 3 | ProjecaoMensal | ProjecaoMensal | `gerar_projecao_12_meses()` | Monta array 12 meses |
| 4 | ProjecaoMensal | ProjecaoMensal | `exportar_csv()` | Grava arquivo .csv |
| 5 | ProjecaoMensal | Orcamento | `sucesso` | Confirma criação |
| 6 | Orcamento | UI | `caminho_arquivo` | Retorna localização |
| 7 | UI | Usuário | `mensagem_sucesso` | Confirma ao usuário |

---

## 4. Fluxos Alternativos

### 4.1. Entrada Inválida (Qualquer UC)

```
┌──────┐          ┌─────────┐
│ UI   │          │ Orcamento│
└──┬───┘          └────┬─────┘
   │                   │
   │  Dados inválidos  │
   │──────────────────>│
   │                   │
   │  Erro validação   │
   │<──────────────────│
   │                   │
   │  Exibir erro      │
   │───┐               │
   │<──┘               │
```

### 4.2. Orçamento Incompleto (UC03)

```
┌──────┐          ┌─────────┐
│ UI   │          │ Orcamento│
└──┬───┘          └────┬─────┘
   │                   │
   │  Gerar projeção   │
   │──────────────────>│
   │                   │
   │  Erro: incompleto │
   │<──────────────────│
   │                   │
   │  Retornar UC01    │
   │───┐               │
   │<──┘               │
```

---

## 5. Mapeamento de Requisitos Funcionais

| Requisito | UC | Camada Principal | Classes Envolvidas |
|-----------|-----|------------------|-------------------|
| Calcular aluguel base | UC01 | Domínio | Imovel, Apartamento, Casa, Estudio |
| Calcular quartos extras | UC01 | Domínio | Imovel (polimorfismo) |
| Calcular vagas garagem | UC01 | Domínio | Imovel (polimorfismo) |
| Aplicar desconto 5% | UC01 | Controle | Orcamento + Cliente |
| Parcelar contrato | UC02 | Negócio | Contrato |
| Gerar CSV 12 meses | UC03 | Negócio | ProjecaoMensal |
| Validar entradas | Todos | Apresentação | Interface |

---

## 6. Princípios POO na Arquitetura

### 6.1. Abstração
- **Interface CLI**: Usuário interage sem conhecer complexidade
- **Classe Imovel**: Define contrato comum para todos os tipos

### 6.2. Encapsulamento
- **Camada de Controle**: Lógica de orquestração protegida
- **Atributos protegidos**: Dados internos ocultos (prefixo `_`)

### 6.3. Herança
- **Domínio**: Apartamento, Casa, Estudio herdam de Imovel
- **Negócio**: ProjecaoMensal reutiliza dados de Orcamento

### 6.4. Polimorfismo
- **Cálculo de aluguel**: Cada imóvel implementa `calcular_aluguel()` diferentemente
- **Cálculo de vagas**: Cada imóvel implementa `calcular_vagas()` diferentemente

---

## 7. Arquivos Gerados

| Arquivo | Formato | Descrição |
|---------|---------|-----------|
| `diagrama-sequencia.puml` | PlantUML | Código fonte do diagrama |
| `modelagem-dinamica.md` | Markdown | Esta documentação |

### 7.1. Gerar Imagens

```bash
# Gerar PNG
java -jar ~/.local/bin/plantuml.jar -tpng diagrama-sequencia.puml

# Gerar SVG
java -jar ~/.local/bin/plantuml.jar -tsvg diagrama-sequencia.puml

# Gerar PDF
java -jar ~/.local/bin/plantuml.jar -tpdf diagrama-sequencia.puml
```

---

## 8. Referências

1. **Trabalho**: Algorithmic Thinking & Introduction to Object-Oriented Programming
2. **Modelagem Estática**: `../mod_estatic/diagrama-classes.puml`
3. **Regras de Negócio**: `../mod_estatic/modelagem-problema.md`
4. **Ferramenta**: PlantUML 1.2026.6
