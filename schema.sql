CREATE TABLE Profissao (
    id_profissao INT PRIMARY KEY,
    nome VARCHAR(20)
)

CREATE TABLE Telefone (
    id_telefone INT PRIMARY KEY,
    numero VARCHAR(11),
    tipo CHECK('residencial', 'celular'),
    id_cliente INT,
    CONSTRAINT fk_cliente FOREIGN KEY REFERENCES Cliente(id_cliente),
)

CREATE TABLE Endereco (
    id_conta INT PRIMARY KEY
    rua VARCHAR(20),
    numero VARCHAR(10),
    bairro VARCHAR(20),
    cidade VARCHAR(20),
    estado VARCHAR(20),
    pais VARCHAR(20),
    cep VARCHAR(8),
    complemento VARCHAR(50)
)

CREATE TABLE Cliente (
    id_cliente INT PRIMARY KEY,
    cpf VARCHAR(11),
    rg VARCHAR(9),
    nome VARCHAR(50),
    data_nascimento DATE,
    email VARCHAR(50),
    salario DECIMAL(10, 2),
    vl_patrimonio DECIMAL(12, 2),
    id_profissao INT,
    CONSTRAINT fk_profissao FOREIGN KEY REFERENCES Profissao(id_profissao)
)

CREATE TABLE Conta (
    id_conta INT PRIMARY KEY,
    tipo VARCHAR(20),
    saldo DECIMAL(12, 2),
    data_hora_abertura TIMESTAMP,
    data_hora_fechadura TIMESTAMP,
    estado CHECK('ativada', 'desativada')
    id_cliente INT,
    CONSTRAINT fk_cliente FOREIGN KEY REFERENCES Cliente(id_cliente)
)

CREATE TABLE Chave_pix (
    id_chave_pix INT PRIMARY KEY,
    chave VARCHAR(50),
    tipo CHECK('email', 'telefone', 'aleatoria'),
    id_conta INT,
    CONSTRAINT fk_conta FOREIGN KEY REFERENCES Conta(id_conta)
)

CREATE TABLE Pix (
    id_pix INT PRIMARY KEY,
    tipo CHECK('email', 'telefone', 'aleatoria'),
    chave_destino VARCHAR(50)
)

CREATE TABLE Ted (
    id_ted INT PRIMARY KEY,
    num_conta_destino VARCHAR(20),
    agencia_destino VARCHAR(20),
    tipo_conta_destino VARCHAR(20),
    instituicao_destino VARCHAR(30),
    nome_destino VARCHAR(50),
    cpf_cnpj_destino VARCHAR(14)
)

CREATE TABLE Movimentacao (
    id_movimentacao INT PRIMARY KEY,
    data_hora TIMESTAMP,
    valor DECIMAL(12, 2),
    tipo CHECK('PIX', 'TED'),
    id_conta INT,
    id_ted INT,
    id_pix INT,
    CONSTRAINT fk_conta FOREIGN KEY REFERENCES Conta(id_conta),
    CONSTRAINT fk_ted FOREIGN KEY REFERENCES Ted(id_ted),
    CONSTRAINT fk_pix FOREIGN KEY REFERENCES Pix(id_pix)
)

CREATE TABLE Cliente_endereco (
    id_cliente INT NOT NULL,
    id_endereco INT NOT NULL,
    CONSTRAINT fk_cliente FOREIGN KEY REFERENCES Cliente(id_cliente),
    CONSTRAINT fk_endereco FOREIGN KEY REFERENCES Endereco(id_endereco),
    PRIMARY KEY (id_cliente, id_endereco)
)

CREATE TABLE Cliente_telefone (
    id_cliente INT NOT NULL,
    id_telefone INT NOT NULL,
    CONSTRAINT fk_cliente FOREIGN KEY REFERENCES Cliente(id_cliente),
    CONSTRAINT fk_telefone FOREIGN KEY REFERENCES Telefone(id_telefone),
    PRIMARY KEY (id_cliente, id_telefone)
)