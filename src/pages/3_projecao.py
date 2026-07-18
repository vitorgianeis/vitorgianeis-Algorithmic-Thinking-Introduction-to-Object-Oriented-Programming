import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.orcamento_service import OrcamentoService
from services.contrato_service import ContratoService
from repository.data_repository import DataRepository

st.set_page_config(page_title="Projeção", page_icon="📊", layout="wide")

st.title("📊 Projeção de 12 Meses")

st.markdown("---")

repository = DataRepository()
orcamento_service = OrcamentoService(repository)
contrato_service = ContratoService(repository)

st.subheader("Selecione o Orçamento")

orcamentos = orcamento_service.listar_orcamentos()

if not orcamentos:
    st.warning("Nenhum orçamento encontrado.")
else:
    opcoes = {f"#{o['id']} - {o['cliente_nome']}": o for o in orcamentos}
    selecao = st.selectbox("Orçamentos", options=list(opcoes.keys()))

    if selecao:
        orcamento_data = opcoes[selecao]

        contrato_data = contrato_service.obter_contrato_por_orcamento(
            orcamento_data["id"]
        )

        if not contrato_data:
            st.warning(
                "Contrato não encontrado para este orçamento. "
                "Crie um contrato na página **Contrato**."
            )
        else:
            from domain.contrato import Contrato
            from domain.orcamento import Orcamento
            from domain.cliente import Cliente

            cliente = Cliente(
                _nome=orcamento_data["cliente_nome"],
                _possui_criancas=bool(orcamento_data["cliente_possui_criancas"]),
            )

            orcamento = Orcamento(
                _cliente=cliente,
                _valor_aluguel_final=orcamento_data["valor_aluguel_final"],
            )

            contrato = Contrato(
                _orcamento_id=orcamento_data["id"],
                _quantidade_parcelas=contrato_data["quantidade_parcelas"],
                _valor_parcela=contrato_data["valor_parcela"],
            )

            projecao = contrato_service.gerar_projecao(orcamento, contrato)

            st.markdown("---")
            st.subheader("📋 Resumo")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Cliente", orcamento_data["cliente_nome"])
            with col2:
                st.metric("Valor Aluguel", f"R$ {orcamento_data['valor_aluguel_final']:.2f}")
            with col3:
                st.metric("Parcelas", f"{contrato.quantidade_parcelas}x R$ {contrato.valor_parcela:.2f}")

            st.markdown("---")
            st.subheader("📅 Projeção Mensal (12 meses)")

            import pandas as pd

            df = pd.DataFrame(projecao)
            df["aluguel"] = df["aluguel"].apply(lambda x: f"R$ {x:.2f}")
            df["parcela_contrato"] = df["parcela_contrato"].apply(
                lambda x: f"R$ {x:.2f}"
            )
            df["total_mes"] = df["total_mes"].apply(lambda x: f"R$ {x:.2f}")
            df = df.rename(
                columns={
                    "mes": "Mês",
                    "aluguel": "Aluguel",
                    "parcela_contrato": "Parcela Contrato",
                    "total_mes": "Total Mês",
                }
            )

            st.dataframe(df, use_container_width=True, hide_index=True)

            total_geral = sum(p["total_mes"] for p in projecao)
            total_aluguel = sum(p["aluguel"] for p in projecao)
            total_contrato = sum(p["parcela_contrato"] for p in projecao)

            st.markdown("---")
            st.subheader("💰 Totais")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Total Aluguel (12 meses)", f"R$ {total_aluguel:.2f}")
            with col_b:
                st.metric("Total Contrato", f"R$ {total_contrato:.2f}")
            with col_c:
                st.metric("Total Geral", f"R$ {total_geral:.2f}")

            st.markdown("---")
            st.subheader("📥 Exportar CSV")

            if st.button("📥 Gerar Arquivo CSV", type="primary"):
                try:
                    nome_arquivo = f"projecao_{orcamento_data['id']}_{orcamento_data['cliente_nome'].replace(' ', '_')}.csv"
                    caminho = contrato_service.exportar_csv(projecao, nome_arquivo)

                    with open(caminho, "r") as f:
                        csv_content = f.read()

                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv_content,
                        file_name=nome_arquivo,
                        mime="text/csv",
                    )

                    st.success(f"✅ Arquivo CSV gerado: {caminho}")

                except Exception as e:
                    st.error(f"Erro ao gerar CSV: {str(e)}")
