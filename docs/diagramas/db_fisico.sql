CREATE DATABASE avalia_projeto;
USE avalia_projeto;

-- ===========================
-- Seção de Criação de Tabelas
-- ===========================
CREATE TABLE perfil(
    id_perfil TINYINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome_perfil VARCHAR(25) NOT NULL UNIQUE
) ENGINE = InnoDB;

CREATE TABLE usuario(
    id_usuario INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(50) NOT NULL,
    login VARCHAR(30) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    fk_Perfil_Usuario TINYINT UNSIGNED NOT NULL,
    FOREIGN KEY(fk_Perfil_Usuario) REFERENCES perfil(id_perfil)
) ENGINE = InnoDB;

CREATE TABLE evento(
    id_evento INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome_evento VARCHAR(60) NOT NULL,
    data_inicio DATE NOT NULL,
    data_termino DATE,
    descricao_evento TEXT
) ENGINE = InnoDB;

CREATE TABLE avaliador(
    fk_Usuario INT UNSIGNED NOT NULL,
    fk_Evento INT UNSIGNED NOT NULL,
    PRIMARY KEY(fk_Usuario, fk_Evento),
    FOREIGN KEY(fk_Usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY(fk_Evento) REFERENCES evento(id_evento)
) ENGINE = InnoDB;

CREATE TABLE pergunta(
    id_pergunta INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    questao TEXT NOT NULL,
    peso TINYINT NOT NULL,
    fk_Evento_Pergunta INT UNSIGNED NOT NULL,
    FOREIGN KEY(fk_Evento_Pergunta) REFERENCES evento(id_evento)
) ENGINE = InnoDB;

CREATE TABLE grupo_pergunta(
    fk_Pergunta INT UNSIGNED NOT NULL,
    fk_Evento INT UNSIGNED NOT NULL,
    PRIMARY KEY(fk_Pergunta, fk_Evento),
    FOREIGN KEY(fk_Pergunta) REFERENCES pergunta(id_pergunta),
    FOREIGN KEY(fk_Evento) REFERENCES evento(id_evento)
)

CREATE TABLE projeto(
    id_projeto INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome_projeto VARCHAR(60) NOT NULL,
    integrantes TEXT NOT NULL,
    descricao_projeto TEXT,
    fk_Evento_Projeto INT UNSIGNED NOT NULL,
    FOREIGN KEY(fk_Evento_Projeto) REFERENCES evento(id_evento)
) ENGINE = InnoDB;

CREATE TABLE avaliacao(
    id_avaliacao INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nota TINYINT NOT NULL,
    fk_Projeto_Avaliacao INT UNSIGNED NOT NULL,
    FOREIGN KEY(fk_Projeto_Avaliacao) REFERENCES projeto(id_projeto)
) ENGINE = InnoDB;

CREATE TABLE avaliador_responsavel(
    fk_Usuario INT UNSIGNED NOT NULL,
    fk_Avaliacao INT UNSIGNED NOT NULL,
    PRIMARY KEY(fk_Usuario, fk_Avaliacao),
    FOREIGN KEY(fk_Usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY(fk_Avaliacao) REFERENCES avaliacao(id_avaliacao)
)

-- ==========================
-- Seção de Inserção de Dados
-- ==========================

-- Perfil
INSERT INTO perfil (nome_perfil) VALUES ('administrador');
INSERT INTO perfil (nome_perfil) VALUES ('avaliador');

-- Usuario
INSERT INTO usuario (nome_usuario, login, senha, fk_Perfil_Usuario)
VALUES ('ADM', 'admin', 'JDJiJDEyJGxzU0hYVS9KNy5pcUpOMG9nYXd6a3VOem5EUUJCQ1FVTDBRenJGN0Vhd3R2Yld4MEJFVlky', 1);
