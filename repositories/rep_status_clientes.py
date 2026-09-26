from banco.db import conectar
from models.status_cliente import StatusCliente

def criar_tabela_status_clientes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status_clientes(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL UNIQUE
        )"""
    )

    conexao.commit()
    cursor.close()
    conexao.close()

def criar_status_cliente(status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO status_clientes(nome)
        VALUES (%s)
    """, (status.nome,))
    conexao.commit()

    status.id = cursor.lastrowid

    cursor.close()
    conexao.close()
    return status

def listar_status_clientes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome
        FROM status_clientes
    """)
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    status_clientes = []
    for id_status, nome in resultado:
        status = StatusCliente(nome)
        status.id = id_status
        status_clientes.append(status)
    return status_clientes

def buscar_por_id(id_status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome
        FROM status_clientes
        WHERE id = %s
    """, (id_status,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado is None:
        return None
    id_status, nome = resultado
    status = StatusCliente(nome)
    status.id = id_status
    return status

# def atualizar_status_cliente(status):
#     ...

# def excluir_status_cliente(id_status):
#     ...