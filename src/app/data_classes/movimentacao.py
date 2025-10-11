from dataclasses import dataclass
from datetime import datetime

@dataclass
class Movimentacao:
    id: int
    id_conta: int
    data_hora: datetime
    valor: float

@dataclass
class Pix(Movimentacao):
    chave_destino: str
    tipo_chave: str

@dataclass
class Ted(Movimentacao):
    cpf_cnpj_destino: str
    num_conta_destino: int
    agencia_destino: int
    tipo_conta_destino: str
    instituicao_destino: str
    nome_destino: str