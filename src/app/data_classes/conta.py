from dataclasses import dataclass
from datetime import date

@dataclass
class Conta:
    id: int
    tipo: str
    numero: int
    saldo: float
    data_hora_abertura: date
    data_hora_fechamento: date
    estado: str
    id_cliente: int