from dataclasses import dataclass

@dataclass
class Ted:
    id: int
    num_conta_destino: int
    agencia_destino: int
    tipo_conta_destino: str
    instituicao_destino: str
    nome_destino: str
    cpf_cnpj_destino: int