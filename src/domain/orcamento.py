from dataclasses import dataclass
from typing import Optional

from .cliente import Cliente
from .imovel import Imovel


@dataclass
class Orcamento:
    """Representa um orçamento de aluguel."""

    _cliente: Optional[Cliente] = None
    _imovel: Optional[Imovel] = None
    _valor_aluguel_base: float = 0.0
    _valor_quartos_extras: float = 0.0
    _valor_vagas: float = 0.0
    _valor_desconto: float = 0.0
    _percentual_desconto: float = 0.0
    _valor_aluguel_final: float = 0.0
    _status: str = "RASCUNHO"
    _observacoes: str = ""
    _id: Optional[int] = None

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def cliente(self) -> Optional[Cliente]:
        return self._cliente

    @cliente.setter
    def cliente(self, value: Cliente):
        self._cliente = value

    @property
    def imovel(self) -> Optional[Imovel]:
        return self._imovel

    @imovel.setter
    def imovel(self, value: Imovel):
        self._imovel = value
        if value:
            self._valor_aluguel_base = value.valor_base

    @property
    def valor_aluguel_base(self) -> float:
        return self._valor_aluguel_base

    @property
    def valor_quartos_extras(self) -> float:
        return self._valor_quartos_extras

    @property
    def valor_vagas(self) -> float:
        return self._valor_vagas

    @property
    def valor_desconto(self) -> float:
        return self._valor_desconto

    @property
    def percentual_desconto(self) -> float:
        return self._percentual_desconto

    @property
    def valor_aluguel_final(self) -> float:
        return self._valor_aluguel_final

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    @property
    def observacoes(self) -> str:
        return self._observacoes

    @observacoes.setter
    def observacoes(self, value: str):
        self._observacoes = value

    def calcular_orcamento(self) -> float:
        """Calcula o valor total do orçamento."""
        if not self._imovel or not self._cliente:
            raise ValueError("Imóvel e cliente devem ser definidos")

        self._valor_quartos_extras = self._imovel.calcular_quartos_extras()
        self._valor_vagas = self._imovel.calcular_vagas()

        aluguel_com_adicionais = (
            self._valor_aluguel_base
            + self._valor_quartos_extras
            + self._valor_vagas
        )

        tipo_imovel = self._imovel.get_tipo()
        if self._cliente.eh_elegivel_desconto(tipo_imovel):
            self._percentual_desconto = 5.0
            self._valor_desconto = aluguel_com_adicionais * 0.05
        else:
            self._percentual_desconto = 0.0
            self._valor_desconto = 0.0

        self._valor_aluguel_final = aluguel_com_adicionais - self._valor_desconto
        self._status = "FINALIZADO"
        return self._valor_aluguel_final

    def exibir_resumo(self) -> dict:
        """Retorna um resumo do orçamento."""
        return {
            "imovel_tipo": self._imovel.get_tipo() if self._imovel else "",
            "endereco": self._imovel.endereco if self._imovel else "",
            "valor_base": self._valor_aluguel_base,
            "quartos_extras": self._valor_quartos_extras,
            "vagas": self._valor_vagas,
            "desconto": self._valor_desconto,
            "percentual_desconto": self._percentual_desconto,
            "valor_final": self._valor_aluguel_final,
            "cliente": self._cliente.nome if self._cliente else "",
            "possui_criancas": (
                self._cliente.possui_criancas if self._cliente else False
            ),
        }
