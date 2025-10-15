from dataclasses import dataclass
from datetime import datetime

@dataclass
class Movimentacao:
    id: int
    id_conta: int
    data_hora: datetime
    valor: float
    tipo: str
    id_pix: int
    id_ted: int