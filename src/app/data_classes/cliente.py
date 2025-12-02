from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass
class Cliente:
    """
    Representação em Python da tabela 'clientes' do banco de dados.
    """
    id: int
    cpf: str
    rg: str
    nome: str
    data_nascimento: date 
    email: str
    salario: Decimal
    vl_patrimonio: Decimal
    id_profissao: int
    senha_hash: str