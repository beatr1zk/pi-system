from banco.db import conectar
from models.status_projeto import StatusProjeto

def criar_tabela_status_projetos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status_projetos(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL UNIQUE
        )"""
    )

    conexao.commit()
    cursor.close()
    conexao.close()

def criar_status_projeto(status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO status_projetos(nome)
        VALUES (%s)
    """, (status.nome,)
    )
    conexao.commit()

    status.id = cursor.lastrowid

    cursor.close()
    conexao.close()
    return status

def listar_status_projetos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome
        FROM status_projetos
    """)

    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    status_projetos = []
    for id_status, nome in resultado:
        status = StatusProjeto(nome)
        status.id = id_status
        status_projetos.append(status)
    return status_projetos

def atualizar_status_projeto(status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE status_projetos
        SET nome = %s
        WHERE id = %s
    """, (status.nome, status.id)
    )
    conexao.commit()

    cursor.close()
    conexao.close()

def excluir_status_projeto(id_status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        DELETE FROM status_projetos
        WHERE id = %s
    """, (id_status,)
    )
    conexao.commit()

    cursor.close()
    conexao.close()