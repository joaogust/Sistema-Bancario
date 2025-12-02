from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Movimentacao:
    """
    Representação em Python da tabela 'movimentacoes'.
    """
    id: int
    valor: Decimal
    data_hora: datetime
    tipo: str
    id_conta: int
    chave_destino: str | None = None
    num_conta_destino: str | None = None
    agencia_destino: str | None = None
    tipo_conta_destino: str | None = None
    instituicao_destino: str | None = None
    nome_destino: str | None = None
    cpf_cnpj_destino: str | None = None