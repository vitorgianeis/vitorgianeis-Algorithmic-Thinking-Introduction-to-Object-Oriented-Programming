from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Cliente:
    """Representa um cliente da imobiliária."""

    _nome: str = ""
    _cpf: str = ""
    _telefone: str = ""
    _email: str = ""
    _possui_criancas: bool = False
    _id: Optional[int] = None

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, value: str):
        if not value:
            raise ValueError("Nome não pode ser vazio")
        self._nome = value

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, value: str):
        self._cpf = value

    @property
    def telefone(self) -> str:
        return self._telefone

    @telefone.setter
    def telefone(self, value: str):
        self._telefone = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value

    @property
    def possui_criancas(self) -> bool:
        return self._possui_criancas

    @possui_criancas.setter
    def possui_criancas(self, value: bool):
        self._possui_criancas = value

    def eh_elegivel_desconto(self, tipo_imovel: str) -> bool:
        """Verifica se o cliente é elegível para desconto."""
        return tipo_imovel == "Apartamento" and not self._possui_criancas
