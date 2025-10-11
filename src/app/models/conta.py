from datetime import *

class Conta:
    def __init__(self, id: int, tipo: str, numero: int, saldo: float, data_hora_abertura: datetime, data_hora_fechamento: datetime, estado: str, id_cliente: int):
        self.id = id
        self.tipo = tipo
        self.numero = numero
        self.saldo = saldo
        self.data_hora_abertura = data_hora_abertura
        self.data_hora_fechamento = data_hora_fechamento
        self.estado = estado
        self.id_cliente = id_cliente

    def __str__(self):
        return f"id= {self.id}, tipo= {self.tipo}, numero= {self.numero}"