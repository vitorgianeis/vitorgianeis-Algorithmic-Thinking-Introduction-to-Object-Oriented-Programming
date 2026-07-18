from typing import Optional

from domain.apartamento import Apartamento
from domain.casa import Casa
from domain.cliente import Cliente
from domain.contrato import Contrato
from domain.estudio import Estudio
from domain.imovel import Imovel
from domain.orcamento import Orcamento
from repository.data_repository import DataRepository


class OrcamentoService:
    """Service para gerenciamento de orçamentos."""

    def __init__(self, repository: DataRepository):
        self._repository = repository

    def criar_imovel(
        self,
        tipo: str,
        endereco: str,
        quartos: int = 1,
        vagas: int = 0,
    ) -> Imovel:
        """Cria uma instância de imóvel conforme o tipo."""
        tipo = tipo.upper()
        if tipo == "A":
            imovel = Apartamento(
                _endereco=endereco,
                _quantidade_quartos=quartos,
                _quantidade_vagas=vagas,
            )
        elif tipo == "C":
            imovel = Casa(
                _endereco=endereco,
                _quantidade_quartos=quartos,
                _quantidade_vagas=vagas,
            )
        elif tipo == "E":
            imovel = Estudio(
                _endereco=endereco,
                _quantidade_quartos=1,
                _quantidade_vagas=vagas,
            )
        else:
            raise ValueError(f"Tipo de imóvel inválido: {tipo}")
        return imovel

    def criar_cliente(
        self,
        nome: str,
        cpf: str = "",
        telefone: str = "",
        email: str = "",
        possui_criancas: bool = False,
    ) -> Cliente:
        """Cria uma instância de cliente."""
        return Cliente(
            _nome=nome,
            _cpf=cpf,
            _telefone=telefone,
            _email=email,
            _possui_criancas=possui_criancas,
        )

    def criar_orcamento(
        self,
        cliente: Cliente,
        imovel: Imovel,
    ) -> Orcamento:
        """Cria e calcula um orçamento."""
        orcamento = Orcamento(_cliente=cliente, _imovel=imovel)
        orcamento.calcular_orcamento()
        return orcamento

    def salvar_orcamento(self, orcamento: Orcamento) -> int:
        """Salva o orçamento no repositório."""
        return self._repository.salvar_orcamento(orcamento)

    def listar_orcamentos(self) -> list[dict]:
        """Lista todos os orçamentos."""
        return self._repository.listar_orcamentos()

    def obter_orcamento(self, orcamento_id: int) -> Optional[Orcamento]:
        """Obtém um orçamento pelo ID."""
        return self._repository.obter_orcamento(orcamento_id)
