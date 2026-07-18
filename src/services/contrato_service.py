from typing import Optional

from domain.contrato import Contrato
from domain.orcamento import Orcamento
from repository.data_repository import DataRepository


class ContratoService:
    """Service para gerenciamento de contratos."""

    def __init__(self, repository: DataRepository):
        self._repository = repository

    def criar_contrato(
        self,
        orcamento_id: int,
        quantidade_parcelas: int,
    ) -> Contrato:
        """Cria um contrato para o orçamento."""
        contrato = Contrato(
            _orcamento_id=orcamento_id,
            _quantidade_parcelas=quantidade_parcelas,
        )
        return contrato

    def salvar_contrato(self, contrato: Contrato) -> int:
        """Salva o contrato no repositório."""
        return self._repository.salvar_contrato(contrato)

    def obter_contrato_por_orcamento(
        self, orcamento_id: int
    ) -> Optional[Contrato]:
        """Obtém o contrato de um orçamento."""
        return self._repository.obter_contrato_por_orcamento(orcamento_id)

    def calcular_parcela(self, parcelas: int) -> float:
        """Calcula o valor da parcela sem criar contrato."""
        contrato = Contrato()
        return contrato.calcular_parcela(parcelas)

    def gerar_projecao(
        self, orcamento: Orcamento, contrato: Contrato
    ) -> list[dict]:
        """Gera projeção de 12 meses."""
        projecao = []
        for mes in range(1, 13):
            parcela = (
                contrato.valor_parcela if mes <= contrato.quantidade_parcelas
                else 0.0
            )
            total = orcamento.valor_aluguel_final + parcela
            projecao.append(
                {
                    "mes": mes,
                    "aluguel": orcamento.valor_aluguel_final,
                    "parcela_contrato": parcela,
                    "total_mes": total,
                }
            )
        return projecao

    def exportar_csv(
        self,
        projecao: list[dict],
        nome_arquivo: str,
    ) -> str:
        """Exporta a projeção para CSV."""
        import csv
        import os

        os.makedirs("data", exist_ok=True)
        caminho = os.path.join("data", nome_arquivo)

        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            writer = csv.DictWriter(
                arquivo,
                fieldnames=["mes", "aluguel", "parcela_contrato", "total_mes"],
            )
            writer.writeheader()
            writer.writerows(projecao)

        return caminho
