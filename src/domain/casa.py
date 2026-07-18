from dataclasses import dataclass
from typing import Optional

from .imovel import Imovel


@dataclass
class Casa(Imovel):
    """Representa uma Casa."""

    VALOR_BASE: float = 900.00
    VALOR_QUARTO_EXTRA: float = 250.00
    VALOR_VAGA: float = 300.00

    def _definir_valor_base(self) -> float:
        return self.VALOR_BASE

    def _valor_quarto_extra(self) -> float:
        return self.VALOR_QUARTO_EXTRA

    def pode_ter_quarto_extra(self) -> bool:
        return True

    def calcular_aluguel(self) -> float:
        """Calcula o aluguel: base + quartos extras + vagas."""
        base = self._valor_base
        quartos = self.calcular_quartos_extras()
        vagas = self.calcular_vagas()
        return base + quartos + vagas

    def calcular_vagas(self) -> float:
        """Calcula vagas: R$ 300,00 por vaga."""
        return self._quantidade_vagas * self.VALOR_VAGA

    def calcular_desconto(self, possui_criancas: bool) -> float:
        """Casa não possui desconto."""
        return 0.0
