# Arquitetura de Software - Sistema de Orçamento R.M

## 1. Visão Geral

O sistema é desenvolvido em **Python** utilizando **Streamlit** para a interface web, seguindo uma arquitetura em **4 camadas** bem definidas.

## 2. Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                    │
│                      (Streamlit UI)                          │
│  • app.py - Página principal                                │
│  • pages/ - Páginas: Orçamento, Contrato, Projeção          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE SERVICES                        │
│                     (Lógica de Negócio)                      │
│  • orcamento_service.py - Criação e cálculo de orçamentos   │
│  • contrato_service.py - Parcelamento e projeção            │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE DOMÍNIO                         │
│                       (Modelo)                               │
│  • imovel.py - Classe abstrata                              │
│  • apartamento.py, casa.py, estudio.py - Subclasses         │
│  • cliente.py - Dados do cliente                            │
│  • orcamento.py - Orçamento de aluguel                      │
│  • contrato.py - Contrato imobiliário                       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE REPOSITORY                      │
│                     (Persistência)                           │
│  • data_repository.py - SQLite para persistência            │
└─────────────────────────────────────────────────────────────┘
```

## 3. Estrutura de Pastas

```
src/
├── app.py                      # Entry point Streamlit
├── requirements.txt            # Dependências
├── pages/
│   ├── 1_orcamento.py          # Página de orçamento
│   ├── 2_contrato.py           # Página de contrato
│   └── 3_projecao.py           # Página de projeção CSV
├── domain/
│   ├── __init__.py
│   ├── imovel.py               # Classe abstrata Imovel
│   ├── apartamento.py          # Subclasse Apartamento
│   ├── casa.py                 # Subclasse Casa
│   ├── estudio.py              # Subclasse Estudio
│   ├── cliente.py              # Entidade Cliente
│   ├── orcamento.py            # Entidade Orcamento
│   └── contrato.py             # Entidade Contrato
├── services/
│   ├── __init__.py
│   ├── orcamento_service.py    # Service de orçamentos
│   └── contrato_service.py     # Service de contratos
├── repository/
│   ├── __init__.py
│   └── data_repository.py      # Repository SQLite
└── data/                       # Dados persistentes
    └── orm.db                  # Banco SQLite
```

## 4. Classes e Responsabilidades

### 4.1. Camada de Domínio

| Classe | Tipo | Responsabilidade |
|--------|------|------------------|
| `Imovel` | Abstrata | Define contrato para cálculo de aluguel |
| `Apartamento` | Concreta | Implementa cálculo (R$ 700 + adicionais) |
| `Casa` | Concreta | Implementa cálculo (R$ 900 + adicionais) |
| `Estudio` | Concreta | Implementa cálculo (R$ 1.200 + progressivo) |
| `Cliente` | Entidade | Armazena dados e verifica elegibilidade |
| `Orcamento` | Entidade | Calcula valor final do aluguel |
| `Contrato` | Entidade | Gerencia parcelamento (1-5x) |

### 4.2. Camada de Services

| Service | Responsabilidade |
|---------|------------------|
| `OrcamentoService` | Criar imóvel, cliente e orçamento |
| `ContratoService` | Criar contrato, gerar projeção e exportar CSV |

### 4.3. Camada de Repository

| Repository | Responsabilidade |
|------------|------------------|
| `DataRepository` | CRUD de orçamentos e contratos (SQLite) |

## 5. Princípios POO Aplicados

### 5.1. Abstração
- Classe `Imovel` é abstrata, definindo contrato comum
- Usuário interage com interface simples (Streamlit)

### 5.2. Encapsulamento
- Atributos protegidos (prefixo `_`)
- Acesso através de properties
- Implementação interna oculta

### 5.3. Herança
- `Apartamento`, `Casa`, `Estudio` herdam de `Imovel`
- Reutilização de código e comportamento comum

### 5.4. Polimorfismo
- `calcular_aluguel()` e `calcular_vagas()` implementados diferentemente
- Cada imóvel possui regras específicas

## 6. Regras de Negócio Implementadas

| Regra | Classe | Método |
|-------|--------|--------|
| Valor base por tipo | Imovel | `__init__` |
| Quarto extra A (+200) | Apartamento | `calcular_quartos_extras()` |
| Quarto extra C (+250) | Casa | `calcular_quartos_extras()` |
| Vaga garagem (300) | Apartamento/Casa | `calcular_vagas()` |
| Vagas progressivas E | Estudio | `calcular_vagas()` |
| Desconto 5% | Apartamento | `calcular_desconto()` |
| Contrato 2000/parcelas | Contrato | `calcular_parcela()` |
| Projeção 12 meses | ContratoService | `gerar_projecao()` |

## 7. Como Executar

### 7.1. Instalar Dependências
```bash
cd src
pip install -r requirements.txt
```

### 7.2. Executar Aplicação
```bash
cd src
streamlit run app.py
```

### 7.3. Acessar
- URL: `http://localhost:8501`

## 8. Fluxo de Uso

1. **Orçamento**: Usuário preenche dados do cliente e imóvel → Sistema calcula valor
2. **Contrato**: Usuário seleciona orçamento e define parcelas → Sistema calcula parcela
3. **Projeção**: Usuário visualiza 12 meses → Pode exportar CSV

## 9. Persistência

- **Banco**: SQLite (local, sem servidor)
- **Arquivo**: `data/orm.db`
- **Tabelas**: `orcamentos`, `contratos`

## 10. Dependências

- `streamlit>=1.28.0` - Interface web
- `pandas>=2.0.0` - Manipulação de dados
- `sqlite3` - Persistência (biblioteca padrão Python)
