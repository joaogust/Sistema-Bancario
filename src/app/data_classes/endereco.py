from dataclasses import dataclass

@dataclass
class Endereco:
    id: int
    complemento: str
    rua: str
    numero: str
    cidade: str
    estado: str
    pais: str
    cep: str