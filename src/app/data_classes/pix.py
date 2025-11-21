from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class PIX:
    valor: Decimal
    chave_destino: str
    tipo_chave: str = 'auto'  # Agora é detectado automaticamente