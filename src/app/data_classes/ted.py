from dataclasses import dataclass
from decimal import Decimal

@dataclass
class TED:
    """
    Representação em Python da tabela 'TED' do banco de dados.
    """
    valor: Decimal
    num_conta_destino: str
    agencia_destino: str
    tipo_conta_destino: str
    instituicao_destino: str
    nome_destino: str
    cpf_cnpj_destino: str