from dataclasses import dataclass
from typing import Optional

from .imovel import Imovel


@dataclass
class Estudio(Imovel):
    """Representa um Estúdio."""

    VALOR_BASE: float = 1200.00
    VALOR_VAGAS_PRIMEIRAS: float = 250.00
    VALOR_VAGA_ADICIONAL: float = 60.00
    LIMITE_VAGAS_BASE: int = 2

    def _definir_valor_base(self) -> float:
        return self.VALOR_BASE

    def _valor_quarto_extra(self) -> float:
        return 0.0

    def pode_ter_quarto_extra(self) -> bool:
        return False

    def calcular_aluguel(self) -> float:
        """Calcula o aluguel: base + vagas (progressivo)."""
        base = self._valor_base
        vagas = self.calcular_vagas()
        return base + vagas

    def calcular_vagas(self) -> float:
        """Calcula vagas: R$ 250 (2 primeiras) + R$ 60 (adicionais)."""
        if self._quantidade_vagas == 0:
            return 0.0
        if self._quantidade_vagas <= self.LIMITE_VAGAS_BASE:
            return self.VALOR_VAGAS_PRIMEIRAS
        vagas_adicionais = self._quantidade_vagas - self.LIMITE_VAGAS_BASE
        return self.VALOR_VAGAS_PRIMEIRAS + (
            vagas_adicionais * self.VALOR_VAGA_ADICIONAL
        )

    def calcular_desconto(self, possui_criancas: bool) -> float:
        """Estúdio não possui desconto."""
        return 0.0
