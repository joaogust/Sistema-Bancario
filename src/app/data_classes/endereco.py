from dataclasses import dataclass

@dataclass
class Endereco:
    """
    Representação em Python da tabela 'enderecos' do banco de dados.
    """
    id: int
    rua: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    id_cliente: int
    complemento: str | None = None