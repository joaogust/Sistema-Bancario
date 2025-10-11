from datetime import *

class Chave_pix:
    def __init__(self, id: int, chave: str, tipo: str, id_conta: int):
        self.id = id
        self.chave = chave
        self.tipo = tipo
        self.id_conta = id_conta

    def __str__(self):
        return f"id= {self.id}, chave= {self.chave}, tipo= {self.tipo}, id_conta= {self.id_conta}"