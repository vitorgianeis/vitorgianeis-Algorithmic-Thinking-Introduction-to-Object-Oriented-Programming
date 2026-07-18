# Modelagem do Problema - Sistema de Orçamento de Aluguel R.M

## 1. Contexto do Negócio

### 1.1. Descrição da Empresa
A **Imobiliária R.M** é uma empresa especializada na locação de imóveis residenciais, operando com três tipos de propriedades:
- Apartamentos
- Casas
- Estúdios

### 1.2. Problema Identificado
Atualmente, a imobiliária R.M realiza o cálculo de orçamentos de aluguel de forma manual, o que gera:
- **Ineficiência**: Tempo excessivo para preparar orçamentos
- **Erros de cálculo**: Possibilidade de equívocos nas regras de acréscimos e descontos
- **Falta de padronização**: Cálculos podem variar entre atendentes
- **Dificuldade de projeção**: Não há visão clara do custo total ao longo do tempo

### 1.3. Solução Proposta
Desenvolver uma aplicação digital que automatize a geração de orçamentos de aluguel, aplicando automaticamente as regras de negócio da empresa e gerando projeções financeiras para os clientes.

---

## 2. Objetivo do Sistema

### 2.1. Objetivo Principal
Automatizar e padronizar a geração de orçamentos de locação para a imobiliária R.M, eliminando processos manuais e erros de cálculo.

### 2.2. Objetivos Específicos
1. **Calcular automaticamente** o valor do aluguel mensal conforme o tipo de imóvel
2. **Aplicar regras de acréscimos** por quartos extras e vagas de garagem
3. **Aplicar descontos** conforme elegibilidade do cliente
4. **Calcular parcelamento** do contrato imobiliário
5. **Gerar arquivo CSV** com projeção de 12 parcelas
6. **Apresentar resultados** de forma clara e detalhada

---

## 3. Regras de Negócio

### 3.1. Tipos de Imóvel e Valores Base

| Tipo de Imóvel | Valor Base (1 Quarto) | Quarto Extra |
|----------------|----------------------|--------------|
| Apartamento | R$ 700,00 | +R$ 200,00 |
| Casa | R$ 900,00 | +R$ 250,00 |
| Estúdio | R$ 1.200,00 | Não disponível |

**Observação**: O estúdio possui apenas 1 quarto, não sendo permitido acréscimo de quartos extras.

### 3.2. Regras de Vagas

#### 3.2.1. Garagem (Apartamento e Casa)
- **Valor por vaga**: R$ 300,00
- **Cálculo**: Quantidade de vagas × R$ 300,00

#### 3.2.2. Estacionamento (Estúdio)
- **Primeiras 2 vagas**: R$ 250,00 (pacote)
- **Vagas adicionais**: R$ 60,00 cada

**Exemplos de cálculo para Estúdio:**
| Vagas | Cálculo | Valor Total |
|-------|---------|-------------|
| 1 | R$ 250,00 | R$ 250,00 |
| 2 | R$ 250,00 | R$ 250,00 |
| 3 | R$ 250,00 + R$ 60,00 | R$ 310,00 |
| 4 | R$ 250,00 + R$ 60,00 × 2 | R$ 370,00 |

### 3.3. Regras de Desconto

#### 3.3.1. Desconto por Ausência de Crianças
- **Percentual**: 5% sobre o valor do aluguel
- **Elegibilidade**: Apenas para Apartamentos
- **Condição**: Cliente não possui crianças

**Fórmula**: `desconto = valor_aluguel × 0.05`

**Observação**: O desconto não se aplica a Casas ou Estúdios.

### 3.4. Regras de Contrato

#### 3.4.1. Valor do Contrato
- **Valor fixo**: R$ 2.000,00
- **Natureza**: Taxa administrativa única

#### 3.4.2. Parcelamento
- **Máximo de parcelas**: 5
- **Mínimo de parcelas**: 1
- **Cálculo**: `parcela = R$ 2.000,00 / número de parcelas`

**Exemplos de parcelamento:**
| Parcelas | Cálculo | Valor da Parcela |
|----------|---------|------------------|
| 1 | R$ 2.000,00 / 1 | R$ 2.000,00 |
| 2 | R$ 2.000,00 / 2 | R$ 1.000,00 |
| 3 | R$ 2.000,00 / 3 | R$ 666,67 |
| 4 | R$ 2.000,00 / 4 | R$ 500,00 |
| 5 | R$ 2.000,00 / 5 | R$ 400,00 |

### 3.5. Composição do Valor Mensal Total

O valor mensal total pago pelo cliente é composto por:

```
Valor Mensal Total = Valor do Aluguel + Parcela do Contrato
```

**Onde:**
- `Valor do Aluguel` = Base + Adicionais - Desconto
- `Parcela do Contrato` = R$ 2.000,00 / número de parcelas (quando aplicável)

---

## 4. Casos de Uso

### 4.1. UC01: Gerar Orçamento de Aluguel

| Campo | Descrição |
|-------|-----------|
| **ID** | UC01 |
| **Nome** | Gerar Orçamento de Aluguel |
| **Ator** | Administrador da Imobiliária |
| **Objetivo** | Calcular o valor mensal de aluguel para um cliente |
| **Pré-condição** | Sistema acessível, dados do imóvel disponíveis |
| **Pós-condição** | Orçamento gerado com valor mensal calculado |

**Fluxo Principal:**
1. Administrador seleciona o tipo de imóvel (A/C/E)
2. Sistema exibe valor base do aluguel
3. Administrador informa quantidade de quartos (se aplicável)
4. Sistema calcula acréscimo de quarto extra (se houver)
5. Administrador informa quantidade de vagas
6. Sistema calcula valor das vagas conforme regra do imóvel
7. Sistema verifica elegibilidade para desconto
8. Sistema aplica desconto (se elegível)
9. Sistema calcula valor mensal total do aluguel
10. Sistema exibe orçamento detalhado

**Fluxos Alternativos:**
- **6a.** Se estúdio e vagas > 2: Aplica regra progressiva de vagas
- **7a.** Se não for apartamento: Não aplicar desconto
- **7b.** Se for apartamento mas possui crianças: Não aplicar desconto

### 4.2. UC02: Calcular Parcelamento do Contrato

| Campo | Descrição |
|-------|-----------|
| **ID** | UC02 |
| **Nome** | Calcular Parcelamento do Contrato |
| **Ator** | Administrador da Imobiliária |
| **Objetivo** | Dividir a taxa de contrato em parcelas |
| **Pré-condição** | Orçamento de aluguel gerado (UC01) |
| **Pós-condição** | Valor da parcela do contrato calculado |

**Fluxo Principal:**
1. Sistema solicita número de parcelas desejado (1-5)
2. Administrador informa quantidade de parcelas
3. Sistema valida se parcelas está entre 1 e 5
4. Sistema calcula valor da parcela: R$ 2.000,00 / parcelas
5. Sistema exibe valor da parcela do contrato

**Fluxos Alternativos:**
- **3a.** Se parcelas > 5: Exibir mensagem de erro e solicitar nova entrada
- **3b.** Se parcelas < 1: Exibir mensagem de erro e solicitar nova entrada

### 4.3. UC03: Exportar Orçamento em CSV

| Campo | Descrição |
|-------|-----------|
| **ID** | UC03 |
| **Nome** | Exportar Orçamento em CSV |
| **Ator** | Administrador da Imobiliária |
| **Objetivo** | Gerar arquivo com projeção de 12 parcelas |
| **Pré-condição** | Orçamento completo gerado (UC01 + UC02) |
| **Pós-condição** | Arquivo .csv criado com sucesso |

**Fluxo Principal:**
1. Sistema verifica se orçamento está completo
2. Sistema solicita confirmação para gerar arquivo
3. Administrador confirma geração
4. Sistema cria arquivo .csv com 12 linhas (meses 1-12)
5. Para cada mês, sistema inclui:
   - Número do mês
   - Valor do aluguel
   - Valor da parcela do contrato (se aplicável)
   - Valor total do mês
6. Sistema confirma criação do arquivo

**Fluxos Alternativos:**
- **1a.** Se orçamento incompleto: Exibir mensagem e retornar ao UC01
- **5a.** Se mês > número de parcelas: Valor da parcela = R$ 0,00

---

## 5. Exemplos Numéricos Detalhados

### 5.1. Exemplo 1: Apartamento Simples

**Dados de entrada:**
- Tipo: Apartamento
- Quartos: 1
- Vagas: 0
- Possui crianças: Sim
- Parcelas contrato: 3

**Cálculos:**
| Etapa | Operação | Valor |
|-------|----------|-------|
| Base | R$ 700,00 | R$ 700,00 |
| Quarto extra | +R$ 0,00 (1 quarto) | R$ 700,00 |
| Vagas | +R$ 0,00 (0 vagas) | R$ 700,00 |
| Desconto | -R$ 0,00 (possui crianças) | R$ 700,00 |
| **Aluguel Final** | | **R$ 700,00** |
| Parcela contrato | R$ 2.000,00 / 3 | R$ 666,67 |
| **Mensal Total** | R$ 700,00 + R$ 666,67 | **R$ 1.366,67** |

### 5.2. Exemplo 2: Apartamento com Desconto

**Dados de entrada:**
- Tipo: Apartamento
- Quartos: 2
- Vagas: 1
- Possui crianças: Não
- Parcelas contrato: 5

**Cálculos:**
| Etapa | Operação | Valor |
|-------|----------|-------|
| Base | R$ 700,00 | R$ 700,00 |
| Quarto extra | +R$ 200,00 | R$ 900,00 |
| Vagas | +R$ 300,00 (1 × R$ 300) | R$ 1.200,00 |
| Desconto 5% | -R$ 60,00 (R$ 1.200 × 0,05) | R$ 1.140,00 |
| **Aluguel Final** | | **R$ 1.140,00** |
| Parcela contrato | R$ 2.000,00 / 5 | R$ 400,00 |
| **Mensal Total** | R$ 1.140,00 + R$ 400,00 | **R$ 1.540,00** |

### 5.3. Exemplo 3: Casa Completa

**Dados de entrada:**
- Tipo: Casa
- Quartos: 2
- Vagas: 2
- Possui crianças: Sim
- Parcelas contrato: 4

**Cálculos:**
| Etapa | Operação | Valor |
|-------|----------|-------|
| Base | R$ 900,00 | R$ 900,00 |
| Quarto extra | +R$ 250,00 | R$ 1.150,00 |
| Vagas | +R$ 600,00 (2 × R$ 300) | R$ 1.750,00 |
| Desconto | -R$ 0,00 (não é apartamento) | R$ 1.750,00 |
| **Aluguel Final** | | **R$ 1.750,00** |
| Parcela contrato | R$ 2.000,00 / 4 | R$ 500,00 |
| **Mensal Total** | R$ 1.750,00 + R$ 500,00 | **R$ 2.250,00** |

### 5.4. Exemplo 4: Estúdio com Vagas

**Dados de entrada:**
- Tipo: Estúdio
- Vagas: 4
- Parcelas contrato: 2

**Cálculos:**
| Etapa | Operação | Valor |
|-------|----------|-------|
| Base | R$ 1.200,00 | R$ 1.200,00 |
| Quarto extra | - | R$ 1.200,00 |
| Vagas (2 primeiras) | R$ 250,00 | R$ 1.450,00 |
| Vagas (2 adicionais) | 2 × R$ 60,00 = R$ 120,00 | R$ 1.570,00 |
| Desconto | -R$ 0,00 (não é apartamento) | R$ 1.570,00 |
| **Aluguel Final** | | **R$ 1.570,00** |
| Parcela contrato | R$ 2.000,00 / 2 | R$ 1.000,00 |
| **Mensal Total** | R$ 1.570,00 + R$ 1.000,00 | **R$ 2.570,00** |

---

## 6. Restrições do Projeto

### 6.1. Restrições Técnicas
1. **Linguagem obrigatória**: Python
2. **Paradigma obrigatório**: Programação Orientada a Objetos (POO)
3. **Execução**: Aplicação deve ser executável em qualquer ambiente com Python

### 6.2. Restrições de Entrega
1. **Fluxograma**: Documento teórico em PDF
2. **Código-fonte**: Arquivos .py com estrutura POO
3. **Vídeo pitch**: Máximo 4 minutos, publicado em plataforma online
4. **Repositório**: Código publicado no GitHub

### 6.3. Restrições de Negócio
1. **Valores fixos**: Todos os valores são pré-definidos conforme regras da R.M
2. **Parcelas máximas**: Contrato limitado a 5 parcelas
3. **Desconto exclusivo**: Apenas para apartamentos sem crianças

---

## 7. Premissas

### 7.1. Premissas de Negócio
1. O valor do contrato (R$ 2.000,00) é uma taxa administrativa fixa
2. Todos os imóveis seguem as mesmas regras de cálculo
3. O desconto de 5% é aplicado apenas uma vez sobre o valor do aluguel
4. A projeção CSV siempre terá 12 meses, independente do parcelamento

### 7.2. Premissas Técnicas
1. O usuário possui Python instalado em sua máquina
2. O sistema será utilizado em ambiente local (Desktop)
3. A saída será no terminal (CLI) ou interface gráfica simples

### 7.3. Premissas de Uso
1. O administrador da imobiliária é o usuário principal
2. O sistema será utilizado para novos orçamentos (não histórico)
3. Cada execução gera um único orçamento

---

## 8. Critérios de Sucesso

### 8.1. Critérios Funcionais
1. ✅ Sistema calcula corretamente o aluguel para os 3 tipos de imóvel
2. ✅ Sistema aplica acréscimos de quartos conforme regra
3. ✅ Sistema calcula vagas corretamente (regra fixa e progressiva)
4. ✅ Sistema aplica desconto de 5% quando elegível
5. ✅ Sistema calcula parcelamento do contrato (1-5 parcelas)
6. ✅ Sistema gera arquivo CSV com 12 parcelas
7. ✅ Sistema exibe resultados detalhados

### 8.2. Critérios de Qualidade
1. ✅ Código utiliza princípios de POO
2. ✅ Código é legível e organizado
3. ✅ Cálculos são precisos (2 casas decimais)
4. ✅ Sistema trata entradas inválidas
5. ✅ Fluxograma está claro e completo

### 8.3. Critérios de Entrega
1. ✅ Fluxograma entregue em PDF
2. ✅ Código-fonte entregue em pasta compactada
3. ✅ Repositório GitHub público
4. ✅ Vídeo pitch com até 4 minutos
5. ✅ Demonstração funcional do sistema

---

## 9. Glossário

| Termo | Definição |
|-------|-----------|
| **Aluguel** | Valor mensal pago pelo locatário pelo uso do imóvel |
| **Contrato** | Taxa administrativa fixa de R$ 2.000,00 |
| **Orçamento** | Projeção financeira do custo mensal do aluguel |
| **Parcela** | Divisão do valor do contrato ao longo do tempo |
| **Vaga** | Espaço de estacionamento associado ao imóvel |
| **Desconto** | Redução percentual aplicada ao valor do aluguel |

---

## 10. Referências

1. Trabalho: Algorithmic Thinking & Introduction to Object-Oriented Programming
2. Regras de negócio: Imobiliária R.M
3. Documentação oficial Python: https://www.python.org/doc/
