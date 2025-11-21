from dataclasses import dataclass

@dataclass
class ChavePix:
    """
    Representação em Python da tabela 'chaves_pix' do banco de dados.
    """
    id: int
    chave: str
    tipo: str
    id_conta: int