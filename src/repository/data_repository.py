import sqlite3
from typing import Optional

from domain.contrato import Contrato
from domain.orcamento import Orcamento


class DataRepository:
    """Repository para persistência de dados usando SQLite."""

    def __init__(self, db_path: str = "data/orm.db"):
        self._db_path = db_path
        self._criar_tabelas()

    def _get_connection(self) -> sqlite3.Connection:
        """Retorna uma conexão com o banco."""
        import os

        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        return sqlite3.connect(self._db_path)

    def _criar_tabelas(self):
        """Cria as tabelas necessárias."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS orcamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_nome TEXT NOT NULL,
                    cliente_cpf TEXT,
                    cliente_telefone TEXT,
                    cliente_email TEXT,
                    cliente_possui_criancas INTEGER DEFAULT 0,
                    imovel_tipo TEXT NOT NULL,
                    imovel_endereco TEXT,
                    imovel_quartos INTEGER DEFAULT 1,
                    imovel_vagas INTEGER DEFAULT 0,
                    valor_aluguel_base REAL,
                    valor_quartos_extras REAL DEFAULT 0,
                    valor_vagas REAL DEFAULT 0,
                    valor_desconto REAL DEFAULT 0,
                    percentual_desconto REAL DEFAULT 0,
                    valor_aluguel_final REAL,
                    status TEXT DEFAULT 'RASCUNHO',
                    observacoes TEXT
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS contratos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    orcamento_id INTEGER NOT NULL,
                    quantidade_parcelas INTEGER NOT NULL,
                    valor_parcela REAL,
                    data_inicio TEXT,
                    data_fim TEXT,
                    status TEXT DEFAULT 'ATIVO',
                    FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id)
                )
            """
            )

            conn.commit()

    def salvar_orcamento(self, orcamento: Orcamento) -> int:
        """Salva um orçamento e retorna o ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO orcamentos (
                    cliente_nome, cliente_cpf, cliente_telefone, cliente_email,
                    cliente_possui_criancas, imovel_tipo, imovel_endereco,
                    imovel_quartos, imovel_vagas, valor_aluguel_base,
                    valor_quartos_extras, valor_vagas, valor_desconto,
                    percentual_desconto, valor_aluguel_final, status, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    orcamento.cliente.nome if orcamento.cliente else "",
                    orcamento.cliente.cpf if orcamento.cliente else "",
                    orcamento.cliente.telefone if orcamento.cliente else "",
                    orcamento.cliente.email if orcamento.cliente else "",
                    1
                    if orcamento.cliente and orcamento.cliente.possui_criancas
                    else 0,
                    orcamento.imovel.get_tipo() if orcamento.imovel else "",
                    orcamento.imovel.endereco if orcamento.imovel else "",
                    (
                        orcamento.imovel.quantidade_quartos
                        if orcamento.imovel
                        else 1
                    ),
                    (
                        orcamento.imovel.quantidade_vagas
                        if orcamento.imovel
                        else 0
                    ),
                    orcamento.valor_aluguel_base,
                    orcamento.valor_quartos_extras,
                    orcamento.valor_vagas,
                    orcamento.valor_desconto,
                    orcamento.percentual_desconto,
                    orcamento.valor_aluguel_final,
                    orcamento.status,
                    orcamento.observacoes,
                ),
            )

            conn.commit()
            return cursor.lastrowid

    def listar_orcamentos(self) -> list[dict]:
        """Lista todos os orçamentos."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orcamentos ORDER BY id DESC")
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, row)) for row in cursor.fetchall()]

    def obter_orcamento(self, orcamento_id: int) -> Optional[dict]:
        """Obtém um orçamento pelo ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM orcamentos WHERE id = ?", (orcamento_id,)
            )
            row = cursor.fetchone()
            if row:
                colunas = [desc[0] for desc in cursor.description]
                return dict(zip(colunas, row))
            return None

    def salvar_contrato(self, contrato: Contrato) -> int:
        """Salva um contrato e retorna o ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO contratos (
                    orcamento_id, quantidade_parcelas, valor_parcela,
                    data_inicio, data_fim, status
                ) VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    contrato.orcamento_id,
                    contrato.quantidade_parcelas,
                    contrato.valor_parcela,
                    str(contrato.data_inicio),
                    str(contrato.data_fim) if contrato.data_fim else None,
                    contrato.status,
                ),
            )

            conn.commit()
            return cursor.lastrowid

    def obter_contrato_por_orcamento(
        self, orcamento_id: int
    ) -> Optional[dict]:
        """Obtém o contrato de um orçamento."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM contratos WHERE orcamento_id = ? ORDER BY id DESC LIMIT 1",
                (orcamento_id,),
            )
            row = cursor.fetchone()
            if row:
                colunas = [desc[0] for desc in cursor.description]
                return dict(zip(colunas, row))
            return None
