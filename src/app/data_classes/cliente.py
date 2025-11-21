from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass
class Cliente:
    """
    Representação em Python da tabela 'clientes' do banco de dados.
    Os nomes dos atributos DEVEM ser iguais aos nomes das colunas.
    """
    id: int
    cpf: str
    rg: str
    nome: str
    data_nascimento: date  # <-- Esta era a linha que faltava
    email: str
    salario: Decimal
    vl_patrimonio: Decimal
    id_profissao: int
    senha_hash: str
    
    # Você pode adicionar métodos aqui se precisar,
    # mas para o erro, apenas os atributos acima são necessários.