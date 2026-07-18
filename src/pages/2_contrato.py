import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.orcamento_service import OrcamentoService
from services.contrato_service import ContratoService
from repository.data_repository import DataRepository

st.set_page_config(page_title="Contrato", page_icon="📋", layout="wide")

st.title("📋 Calcular Parcelamento do Contrato")

st.markdown("---")

repository = DataRepository()
orcamento_service = OrcamentoService(repository)
contrato_service = ContratoService(repository)

st.subheader("Selecione o Orçamento")

orcamentos = orcamento_service.listar_orcamentos()

if not orcamentos:
    st.warning("Nenhum orçamento encontrado. Crie um orçamento primeiro na página **Orçamento**.")
else:
    opcoes = {f"#{o['id']} - {o['cliente_nome']} - {o['imovel_tipo']}": o for o in orcamentos}
    selecao = st.selectbox("Orçamentos", options=list(opcoes.keys()))

    if selecao:
        orcamento_data = opcoes[selecao]

        st.markdown("---")
        st.subheader("Dados do Orçamento")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Cliente", orcamento_data["cliente_nome"])
        with col2:
            st.metric("Tipo", orcamento_data["imovel_tipo"])
        with col3:
            st.metric("Valor Aluguel", f"R$ {orcamento_data['valor_aluguel_final']:.2f}")

        st.markdown("---")
        st.subheader("Definir Parcelamento")

        with st.form("contrato_form"):
            parcelas = st.slider(
                "Número de Parcelas",
                min_value=1,
                max_value=5,
                value=1,
            )

            valor_parcela = 2000.00 / parcelas
            st.info(f"💰 Valor de cada parcela: **R$ {valor_parcela:.2f}**")

            submitted = st.form_submit_button("📝 Salvar Contrato", type="primary")

        if submitted:
            try:
                contrato = contrato_service.criar_contrato(
                    orcamento_id=orcamento_data["id"],
                    quantidade_parcelas=parcelas,
                )

                contrato.orcamento_id = orcamento_data["id"]
                contrato_id = contrato_service.salvar_contrato(contrato)

                st.success(f"✅ Contrato #{contrato_id} salvo com sucesso!")

                st.markdown("---")
                st.subheader("📊 Resumo do Contrato")

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Valor Total", f"R$ {contrato.valor_total:.2f}")
                with col_b:
                    st.metric("Parcelas", f"{contrato.quantidade_parcelas}x")
                with col_c:
                    st.metric("Valor Parcela", f"R$ {contrato.valor_parcela:.2f}")

                st.markdown("---")
                st.subheader("📅 Composição Mensal")

                aluguel = orcamento_data["valor_aluguel_final"]
                total_mensal = aluguel + contrato.valor_parcela

                col_d, col_e = st.columns(2)
                with col_d:
                    st.metric("Aluguel Mensal", f"R$ {aluguel:.2f}")
                with col_e:
                    st.metric("Parcela Contrato", f"R$ {contrato.valor_parcela:.2f}")

                st.metric("💵 Total Mensal (primeiras parcelas)", f"R$ {total_mensal:.2f}")

                st.info(
                    f"📋 Contrato salvo com ID: **{contrato_id}**. "
                    f"Acesse a página de **Projeção** para exportar em CSV."
                )

            except Exception as e:
                st.error(f"Erro ao salvar contrato: {str(e)}")
