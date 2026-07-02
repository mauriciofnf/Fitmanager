CREATE TABLE Personal (
	id_personal INT PRIMARY KEY,
	cref INT,
	nome_personal VARCHAR(50),
	telefone_personal INT,
	especialidade VARCHAR(50)
);

CREATE TABLE Aluno (
    id_aluno INT PRIMARY KEY,
	id_personal INT,
    nome VARCHAR(50),
    data_nascimento DATE,
	peso FLOAT,
	altura FLOAT,
	telefone INT,
	FOREIGN KEY (id_personal) REFERENCES Personal(id_personal)
);

CREATE TABLE Pagamento (
	id_pagamento INT PRIMARY KEY,
	id_aluno INT,
	data_pagamento DATE,
	status VARCHAR(50),
	valor INT,
	metodo VARCHAR(50),
	FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno)
);

CREATE TABLE Agenda (
	id_agenda INT PRIMARY KEY,
	id_aluno INT,
	data_agenda DATE,
	horario_agenda TIMESTAMP,
	status_agenda VARCHAR(50),
	FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno)
);

CREATE TABLE Endereco (
    id_endereco INT PRIMARY KEY,
    id_aluno INT,
    rua VARCHAR(100),
    numero INT,
    cidade VARCHAR(50),
    estado VARCHAR(2),
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno)
);

CREATE TABLE FichaTreino (
	id_ficha INT PRIMARY KEY,
	id_aluno INT,
	objetivo VARCHAR(50),
	data_inicio DATE,
	data_final DATE,
	observacoes_fichatreino VARCHAR(50),
	FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno)
);

CREATE TABLE Treino (
    id_treino INT PRIMARY KEY,
	id_ficha INT,
    nome_treino VARCHAR(50),
    duracao TIMESTAMP,
    tipo VARCHAR(50),
	FOREIGN KEY (id_ficha) REFERENCES FichaTreino(id_ficha)
);

CREATE TABLE Exercicio (
	id_exercicio INT PRIMARY KEY,
	nome_exercicio VARCHAR(50),
	grupo_muscular VARCHAR(50),
	descricao VARCHAR(200)
);

CREATE TABLE Treino_Exercicio (
	id_treino INT NOT NULL,
	id_exercicio INT NOT NULL,
	FOREIGN KEY (id_treino) REFERENCES Treino(id_treino),
	FOREIGN KEY (id_exercicio) REFERENCES Exercicio(id_exercicio)
);

CREATE TABLE Desempenho (
	id_desempenho INT PRIMARY KEY,
	id_treino INT,
	carga INT,
	reps INT,
	data_registro DATE,
	observacoes_desempenho VARCHAR(200),
	FOREIGN KEY (id_treino) REFERENCES Treino(id_treino)
);
