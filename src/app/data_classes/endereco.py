from dataclasses import dataclass

@dataclass
class Endereco:
    """
    Representação em Python da tabela 'enderecos' do banco de dados.
    Os nomes dos atributos DEVEM ser iguais aos nomes das colunas.
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