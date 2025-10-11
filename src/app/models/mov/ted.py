from src.app.models.mov.movimentacao import Movimentacao
from datetime import *


class Ted(Movimentacao):
    def __init__(self, id: int, id_conta: int, data_hora: datetime, valor: float, cpf_cnpj_destino: str, num_conta_destino: int, agencia_destino: int, tipo_conta_destino: str, instituicao_destino: str, nome_destino: str):
        super().__init__(id, id_conta, data_hora, valor)
        self.cpf_cnpj_destino = cpf_cnpj_destino
        self.num_conta_destino = num_conta_destino
        self.agencia_destino = agencia_destino
        self.tipo_conta_destino = tipo_conta_destino
        self.instituicao_destino = instituicao_destino
        self.nome_destino = nome_destino

