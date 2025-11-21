from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Conta:
    """
    Representação em Python da tabela 'contas' do banco de dados.
    Os nomes dos atributos DEVEM ser iguais aos nomes das colunas.
    """
    id: int
    agencia: str
    numero_conta: str
    tipo: str
    saldo: Decimal  # <-- O que queremos exibir
    data_hora_abertura: datetime
    estado: str
    id_cliente: int
    data_hora_fechamento: datetime | None = None # Opcional