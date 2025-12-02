from dataclasses import dataclass
from datetime import date

@dataclass
class Profissao:
    """
    Representação em Python da tabela 'profissao' do banco de dados.
    """
    id: int
    nome: str
