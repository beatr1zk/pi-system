from banco.db import conectar
from models.status_lead import StatusLead

def criar_tabela_status_leads():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status_leads(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL UNIQUE
        )"""
    )

    conexao.commit()
    cursor.close()
    conexao.close()

def criar_status_lead(status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO status_leads(nome)
        VALUES (%s)
    """, (status.nome,)
    )
    conexao.commit()
    status.id = cursor.lastrowid

    cursor.close()
    conexao.close()
    return status

def listar_status_leads():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome
        FROM status_leads
    """)
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    status_leads = []
    for id_status, nome in resultado:
        status = StatusLead(nome)
        status.id = id_status
        status_leads.append(status)
    return status_leads

def atualizar_status_lead(status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE status_leads
        SET nome = %s
        WHERE id = %s
    """, (status.nome, status.id)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

def excluir_status_lead(id_status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        DELETE FROM status_leads
        WHERE id = %s
    """, (id_status,)
    )
    conexao.commit()

    cursor.close()
    conexao.close()