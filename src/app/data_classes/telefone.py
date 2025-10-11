from dataclasses import dataclass\

@dataclass
class Telefone:
    id: int
    numero: int
    tipo: str
    id_cliente: int