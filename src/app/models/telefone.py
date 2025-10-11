class Telefone:
    def __init__(self, id: int, numero: int, id_cliente: int, tipo: str):
        self.id = id
        self.numero = numero
        self.id_cliente = id_cliente
        self.tipo = tipo

    def __str__(self):
        return f"id= {self.id}, numero= {self.numero}, id_cliente= {self.id_cliente}, tipo= {self.tipo}"