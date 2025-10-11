from src.app.models.mov.movimentacao import Movimentacao
from datetime import *


class Pix(Movimentacao):
    def __init__(self, id: int, id_conta: int, data_hora: datetime, valor: float, chave_destino: str, tipo_chave: str):
        super().__init__(id, id_conta, data_hora, valor)
        self.chave_destino = chave_destino
        self.tipo_chave = tipo_chave
