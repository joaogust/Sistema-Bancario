from datetime import *

class Movimentacao:
    def __init__(self, id: int, id_conta: int, data_hora: datetime, valor: float):
        self.id = id
        self.id_conta = id_conta
        self.data_hora = data_hora
        self.valor = valor

    def __str__(self):
        return f"id= {self.id}, id_conta= {self.id_conta}, data_hora= {self.data_hora}, valor= {self.valor}"