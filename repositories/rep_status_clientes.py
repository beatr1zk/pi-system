from banco.db import cursor_bd
from models.status_cliente import StatusCliente


def criar_tabela_status_clientes():
    with cursor_bd(commit=True) as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS status_clientes(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL UNIQUE
            )
        """)


def criar_status_cliente(status):
    with cursor_bd(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO status_clientes(nome) VALUES (%s)", (status.nome,)
        )
        status.id = cursor.lastrowid
    return status


def listar_status_clientes():
    with cursor_bd() as cursor:
        cursor.execute("SELECT id, nome FROM status_clientes")
        linhas = cursor.fetchall()

    lista = []
    for id_status, nome in linhas:
        status = StatusCliente(nome)
        status.id = id_status
        lista.append(status)
    return lista


def atualizar_status_cliente(status):
    with cursor_bd(commit=True) as cursor:
        cursor.execute(
            "UPDATE status_clientes SET nome = %s WHERE id = %s",
            (status.nome, status.id),
        )


def excluir_status_cliente(id_status):
    with cursor_bd(commit=True) as cursor:
        cursor.execute("DELETE FROM status_clientes WHERE id = %s", (id_status,))