from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass
class Cliente:
    id: int
    cpf: str
    rg: str
    nome: str
    data_nasc: date
    email: str
    salario: Decimal
    vl_patrimonio: Decimal
    id_profissao: int