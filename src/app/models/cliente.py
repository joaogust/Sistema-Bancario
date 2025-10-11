from datetime import *

class Cliente:
    def __init__(self, id: int, rg: int, cpf: int, nome: str, data_nasc: date, email: str, salario: float, vl_patrimonio: float, id_profissao: int):
        self.id = id
        self.rg = rg
        self.cpf = cpf
        self.nome = nome
        self.data_nasc = data_nasc
        self.email = email
        self.salario = salario
        self.vl_patrimonio = vl_patrimonio
        self.id_profissao = id_profissao

    def __str__(self):
        return f"id= {self.id}, nome= {self.nome}"