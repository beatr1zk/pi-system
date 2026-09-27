from banco.db import conectar
from models.prioridade_projeto import PrioridadeProjeto

def criar_tabela_prioridades_projeto():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prioridades_projeto(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL UNIQUE
        )"""
    )
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_prioridade_projeto(prioridade):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO prioridades_projeto(nome)
        VALUES (%s)
    """, (prioridade.nome,)
    )
    conexao.commit()

    prioridade.id = cursor.lastrowid

    cursor.close()
    conexao.close()
    return prioridade

def listar_prioridades_projeto():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome
        FROM prioridades_projeto
    """)
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    prioridades = []
    for id_prioridade, nome in resultado:
        prioridade = PrioridadeProjeto(nome)
        prioridade.id = id_prioridade
        prioridades.append(prioridade)
    return prioridades

def atualizar_prioridade_projeto(prioridade):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE prioridades_projeto
        SET nome = %s
        WHERE id = %s
    """, (prioridade.nome, prioridade.id)
    )
    conexao.commit()

    cursor.close()
    conexao.close()

def excluir_prioridade_projeto(id_prioridade):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        DELETE FROM prioridades_projeto
        WHERE id = %s
    """, (id_prioridade,)
    )
    conexao.commit()

    cursor.close()
    conexao.close()