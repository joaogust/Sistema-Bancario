from dataclasses import dataclass
from datetime import date

@dataclass
class Cliente:
    id: int
    rg: int
    cpf: int
    nome: str
    data_nasc: date
    email: str
    salario: float
    vl_patrimonio: float
    id_profissao: int