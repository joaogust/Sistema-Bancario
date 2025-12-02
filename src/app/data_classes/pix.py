from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class PIX:
    """
    Representação em Python da tabela 'pix' do banco de dados.
    """
    valor: Decimal
    chave_destino: str
    tipo_chave: str = 'auto'