import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from domain.apartamento import Apartamento
from domain.casa import Casa
from domain.estudio import Estudio
from services.orcamento_service import OrcamentoService
from repository.data_repository import DataRepository

st.set_page_config(page_title="Orçamento", page_icon="📝", layout="wide")

st.title("📝 Gerar Orçamento de Aluguel")

st.markdown("---")

repository = DataRepository()
service = OrcamentoService(repository)

with st.form("orcamento_form"):
    st.subheader("Dados do Cliente")

    col1, col2 = st.columns(2)
    with col1:
        nome_cliente = st.text_input("Nome do Cliente *", placeholder="Maria Silva")
        cpf = st.text_input("CPF", placeholder="123.456.789-00")
    with col2:
        telefone = st.text_input("Telefone", placeholder="(11) 99999-1234")
        email = st.text_input("E-mail", placeholder="maria@email.com")

    possui_criancas = st.checkbox("Possui crianças?")

    st.markdown("---")
    st.subheader("Dados do Imóvel")

    col3, col4 = st.columns(2)
    with col3:
        tipo_imovel = st.selectbox(
            "Tipo de Imóvel *",
            options=["A - Apartamento", "C - Casa", "E - Estúdio"],
        )
        tipo_codigo = tipo_imovel.split(" - ")[0]

    with col4:
        endereco = st.text_input("Endereço", placeholder="Rua das Flores, 100")

    col5, col6 = st.columns(2)
    with col5:
        quartos = st.number_input(
            "Quantidade de Quartos",
            min_value=1,
            max_value=10,
            value=1,
            disabled=(tipo_codigo == "E"),
        )
    with col6:
        vagas = st.number_input(
            "Quantidade de Vagas",
            min_value=0,
            max_value=10,
            value=0,
        )

    st.markdown("---")

    submitted = st.form_submit_button("💰 Calcular Orçamento", type="primary")

if submitted:
    if not nome_cliente:
        st.error("Por favor, informe o nome do cliente.")
    elif not endereco:
        st.error("Por favor, informe o endereço do imóvel.")
    else:
        try:
            imovel = service.criar_imovel(
                tipo=tipo_codigo,
                endereco=endereco,
                quartos=quartos,
                vagas=vagas,
            )

            cliente = service.criar_cliente(
                nome=nome_cliente,
                cpf=cpf,
                telefone=telefone,
                email=email,
                possui_criancas=possui_criancas,
            )

            orcamento = service.criar_orcamento(cliente=cliente, imovel=imovel)

            orcamento_id = service.salvar_orcamento(orcamento)

            st.success(f"✅ Orçamento #{orcamento_id} gerado com sucesso!")

            st.markdown("---")
            st.subheader("📊 Resumo do Orçamento")

            resumo = orcamento.exibir_resumo()

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Valor Base", f"R$ {resumo['valor_base']:.2f}")
            with col_b:
                st.metric("Quartos Extras", f"R$ {resumo['quartos_extras']:.2f}")
            with col_c:
                st.metric("Vagas", f"R$ {resumo['vagas']:.2f}")

            col_d, col_e = st.columns(2)
            with col_d:
                if resumo["percentual_desconto"] > 0:
                    st.metric(
                        "Desconto",
                        f"-R$ {resumo['desconto']:.2f}",
                        f"-{resumo['percentual_desconto']:.0f}%",
                    )
                else:
                    st.metric("Desconto", "R$ 0,00", "Não aplicável")

            with col_e:
                st.metric(
                    "💰 Valor Final do Aluguel",
                    f"R$ {resumo['valor_final']:.2f}",
                )

            st.info(
                f"📋 Orçamento salvo com ID: **{orcamento_id}**. "
                f"Acesse a página de **Contrato** para definir o parcelamento."
            )

        except Exception as e:
            st.error(f"Erro ao calcular orçamento: {str(e)}")
