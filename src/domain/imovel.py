from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Imovel(ABC):
    """Classe abstrata que representa um imóvel."""

    _id: Optional[int] = None
    _endereco: str = ""
    _quantidade_quartos: int = 1
    _quantidade_vagas: int = 0

    def __post_init__(self):
        self._valor_base = self._definir_valor_base()

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def endereco(self) -> str:
        return self._endereco

    @endereco.setter
    def endereco(self, value: str):
        self._endereco = value

    @property
    def quantidade_quartos(self) -> int:
        return self._quantidade_quartos

    @quantidade_quartos.setter
    def quantidade_quartos(self, value: int):
        if value < 1:
            raise ValueError("Quantidade de quartos deve ser pelo menos 1")
        self._quantidade_quartos = value

    @property
    def quantidade_vagas(self) -> int:
        return self._quantidade_vagas

    @quantidade_vagas.setter
    def quantidade_vagas(self, value: int):
        if value < 0:
            raise ValueError("Quantidade de vagas não pode ser negativa")
        self._quantidade_vagas = value

    @property
    def valor_base(self) -> float:
        return self._valor_base

    @abstractmethod
    def _definir_valor_base(self) -> float:
        """Define o valor base do aluguel conforme o tipo de imóvel."""
        pass

    @abstractmethod
    def calcular_aluguel(self) -> float:
        """Calcula o valor total do aluguel."""
        pass

    @abstractmethod
    def calcular_vagas(self) -> float:
        """Calcula o valor das vagas de garagem."""
        pass

    @abstractmethod
    def pode_ter_quarto_extra(self) -> bool:
        """Verifica se o imóvel pode ter quarto extra."""
        pass

    def calcular_quartos_extras(self) -> float:
        """Calcula o valor dos quartos extras."""
        if not self.pode_ter_quarto_extra():
            return 0.0
        quartos_extras = self._quantidade_quartos - 1
        if quartos_extras <= 0:
            return 0.0
        return quartos_extras * self._valor_quarto_extra()

    @abstractmethod
    def _valor_quarto_extra(self) -> float:
        """Retorna o valor de cada quarto extra."""
        pass

    def get_tipo(self) -> str:
        """Retorna o tipo do imóvel."""
        return self.__class__.__name__
