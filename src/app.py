import streamlit as st

st.set_page_config(
    page_title="Sistema de Orçamento R.M",
    page_icon="🏠",
    layout="wide",
)

st.title("🏠 Sistema de Orçamento de Aluguel R.M")
st.markdown("---")

st.markdown("""
## Bem-vindo ao Sistema da Imobiliária R.M

Este sistema permite gerenciar orçamentos de aluguel de imóveis.

### Funcionalidades

- **📝 Gerar Orçamento**: Calcule o valor do aluguel para apartamentos, casas ou estúdios
- **📋 Contratos**: Gerencie o parcelamento da taxa de contrato
- **📊 Projeções**: Visualize a projeção de 12 meses e exporte em CSV

### Como Utilizar

1. Acesse o menu lateral para navegar entre as páginas
2. Comece gerando um orçamento na página **Orçamento**
3. Após o orçamento, defina o parcelamento na página **Contrato**
4. Visualize e exporte a projeção na página **Projeção**

---

### Arquitetura do Sistema

```
┌─────────────────────────────────────┐
│     INTERFACE (Streamlit)           │
└──────────────────┬──────────────────┘
                   ▼
┌─────────────────────────────────────┐
│     SERVICES (Negócio)              │
└──────────────────┬──────────────────┘
                   ▼
┌─────────────────────────────────────┐
│     DOMÍNIO (Modelo)                │
└──────────────────┬──────────────────┘
                   ▼
┌─────────────────────────────────────┐
│     REPOSITORY (Dados)              │
└─────────────────────────────────────┘
```
""")
