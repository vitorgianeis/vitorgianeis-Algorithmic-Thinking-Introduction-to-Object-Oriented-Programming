from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Contrato:
    """Representa um contrato imobiliário."""

    VALOR_TOTAL: float = 2000.00
    MAX_PARCELAS: int = 5
    MIN_PARCELAS: int = 1

    _orcamento_id: int = 0
    _quantidade_parcelas: int = 1
    _valor_parcela: float = 0.0
    _data_inicio: Optional[date] = None
    _data_fim: Optional[date] = None
    _status: str = "ATIVO"
    _id: Optional[int] = None

    def __post_init__(self):
        if self._data_inicio is None:
            self._data_inicio = date.today()
        self._calcular_parcela()

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def orcamento_id(self) -> int:
        return self._orcamento_id

    @orcamento_id.setter
    def orcamento_id(self, value: int):
        self._orcamento_id = value

    @property
    def quantidade_parcelas(self) -> int:
        return self._quantidade_parcelas

    @quantidade_parcelas.setter
    def quantidade_parcelas(self, value: int):
        if not self.validar_parcelas(value):
            raise ValueError(
                f"Quantidade de parcelas deve ser entre {self.MIN_PARCELAS} "
                f"e {self.MAX_PARCELAS}"
            )
        self._quantidade_parcelas = value
        self._calcular_parcela()

    @property
    def valor_parcela(self) -> float:
        return self._valor_parcela

    @property
    def valor_total(self) -> float:
        return self.VALOR_TOTAL

    @property
    def data_inicio(self) -> date:
        return self._data_inicio

    @property
    def data_fim(self) -> Optional[date]:
        return self._data_fim

    @data_fim.setter
    def data_fim(self, value: date):
        self._data_fim = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    def validar_parcelas(self, parcelas: int) -> bool:
        """Valida se a quantidade de parcelas é válida."""
        return self.MIN_PARCELAS <= parcelas <= self.MAX_PARCELAS

    def _calcular_parcela(self):
        """Calcula o valor de cada parcela."""
        self._valor_parcela = self.VALOR_TOTAL / self._quantidade_parcelas

    def calcular_parcela(self, parcelas: int) -> float:
        """Calcula o valor da parcela para a quantidade informada."""
        if not self.validar_parcelas(parcelas):
            raise ValueError(
                f"Quantidade de parcelas deve ser entre {self.MIN_PARCELAS} "
                f"e {self.MAX_PARCELAS}"
            )
        return self.VALOR_TOTAL / parcelas

    def finalizar(self):
        """Finaliza o contrato."""
        self._status = "FINALIZADO"
        self._data_fim = date.today()

    def cancelar(self):
        """Cancela o contrato."""
        self._status = "CANCELADO"
