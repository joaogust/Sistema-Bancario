from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass
class Cliente:
    id: int
    rg: int
    cpf: int
    nome: str
    data_nasc: date
    email: str
    salario: Decimal
    vl_patrimonio: Decimal
    id_profissao: int