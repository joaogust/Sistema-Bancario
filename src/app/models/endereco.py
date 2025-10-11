class Endereco:
    def __init__(self, id: int, complemento: str, rua: str, numero: str, bairro: str, cidade: str, estado: str, pais: str, cep: str):
        self.id = id
        self.complemento = complemento
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.pais = pais
        self.cep = cep

    def __str__(self):
        return f"id= {self.id}, rua= {self.rua}, numero= {self.numero}, bairro= {self.bairro}, cidade= {self.cidade}, estado= {self.estado}, pais= {self.pais}, cep= {self.cep}"