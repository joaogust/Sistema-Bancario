from dataclasses import dataclass

@dataclass
class Telefone:
    """
    Representação em Python da tabela 'telefones' do banco de dados.
    """
    id: int
    numero: str
    tipo: str
    id_cliente: int