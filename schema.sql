CREATE TABLE Profissao (
    id_profissao INT PRIMARY KEY,
    nome VARCHAR(20),
    CONSTRAINT pk_profissao PRIMARY KEY (id_profissao)
)

CREATE TABLE Telefone (
    id_telefone INT,
    numero VARCHAR(11),
    tipo VARCHAR(15),
    id_cliente INT,
    CONSTRAINT pk_telefone PRIMARY KEY (id_telefone),
    CONSTRAINT fk_telefone_cliente FOREIGN KEY REFERENCES Cliente(id_cliente),
    CONSTRAINT ck_tipo_telefone CHECK(tipo IN('residencial', 'celular'))
)

CREATE TABLE Endereco (
    id_endereco INT,
    rua VARCHAR(20),
    numero VARCHAR(10),
    bairro VARCHAR(20),
    cidade VARCHAR(20),
    estado VARCHAR(20),
    pais VARCHAR(20),
    cep VARCHAR(8),
    complemento VARCHAR(50),
    CONSTRAINT pk_endereco PRIMARY KEY (id_endereco)
)

CREATE TABLE Cliente (
    id_cliente INT,
    cpf VARCHAR(11),
    rg VARCHAR(9),
    nome VARCHAR(50),
    data_nascimento DATE,
    email VARCHAR(50),
    salario DECIMAL(10, 2),
    vl_patrimonio DECIMAL(12, 2),
    id_profissao INT,
    CONSTRAINT pk_cliente PRIMARY KEY (id_cliente),
    CONSTRAINT fk_cliente_profissao_id_profissao FOREIGN KEY REFERENCES Profissao(id_profissao)
)

CREATE TABLE Conta (
    id_conta INT,
    tipo VARCHAR(20),
    saldo DECIMAL(12, 2),
    data_hora_abertura TIMESTAMP,
    data_hora_fechadura TIMESTAMP,
    estado VARCHAR(20),
    id_cliente INT,
    CONSTRAINT pk_conta PRIMARY KEY (id_conta),
    CONSTRAINT fk_conta_cliente_id_cliente FOREIGN KEY REFERENCES Cliente(id_cliente),
    CONSTRAINT ck_estado_conta CHECK(estado IN('ativada', 'desativada'))
)

CREATE TABLE Chave_pix (
    id_chave_pix INT,
    chave VARCHAR(50),
    tipo VARCHAR(20),
    id_conta INT,
    CONSTRAINT pk_chave_pix PRIMARY KEY (id_chave_pix),
    CONSTRAINT fk_chave_pix_conta_id_conta FOREIGN KEY REFERENCES Conta(id_conta),
    CONSTRAINT ck_tipo_chave_pix CHECK(tipo IN('email', 'telefone', 'aleatoria'))
)

CREATE TABLE Pix (
    id_pix INT,
    tipo VARCHAR(20),
    chave_destino VARCHAR(50),
    CONSTRAINT pk_pix PRIMARY KEY (id_pix),
    CONSTRAINT ck_tipo_pix CHECK(tipo IN('email', 'telefone', 'aleatoria'))
)

CREATE TABLE Ted (
    id_ted INT,
    num_conta_destino VARCHAR(20),
    agencia_destino VARCHAR(20),
    tipo_conta_destino VARCHAR(20),
    instituicao_destino VARCHAR(30),
    nome_destino VARCHAR(50),
    cpf_cnpj_destino VARCHAR(14),
    CONSTRAINT (pk_ted) PRIMARY KEY (id_ted)
)

CREATE TABLE Movimentacao (
    id_movimentacao INT,
    data_hora TIMESTAMP,
    valor DECIMAL(12, 2),
    tipo VARCHAR(3),
    id_conta INT,
    id_ted INT,
    id_pix INT,
    CONSTRAINT pk_movimentacao PRIMARY KEY (id_movimentacao),
    CONSTRAINT fk_movimentacao_conta_id_conta FOREIGN KEY REFERENCES Conta(id_conta),
    CONSTRAINT fk_movimentacao_ted_id_ted FOREIGN KEY REFERENCES Ted(id_ted),
    CONSTRAINT fk_movimentacao_pix_id_pix FOREIGN KEY REFERENCES Pix(id_pix),
    CONSTRAINT ck_tipo_movimentacao CHECK(tipo IN('PIX', 'TED'))
)

CREATE TABLE Cliente_endereco (
    id_cliente INT NOT NULL,
    id_endereco INT NOT NULL,
    CONSTRAINT pk_cliente_endereco PRIMARY KEY (id_cliente, id_endereco),
    CONSTRAINT fk_cliente_endereco_cliente_id_cliente FOREIGN KEY REFERENCES Cliente(id_cliente),
    CONSTRAINT fk_cliente_endereco_endereco_id_endereco FOREIGN KEY REFERENCES Endereco(id_endereco)
)

CREATE TABLE Cliente_telefone (
    id_cliente INT NOT NULL,
    id_telefone INT NOT NULL,
    CONSTRAINT pk_cliente_telefone PRIMARY KEY (id_cliente, id_telefone),
    CONSTRAINT fk_cliente_telefone_cliente_id_cliente FOREIGN KEY REFERENCES Cliente(id_cliente),
    CONSTRAINT fk_cliente_telefone_telefone_id_telefone FOREIGN KEY REFERENCES Telefone(id_telefone)
)