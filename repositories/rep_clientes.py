from banco.db import cursor_bd
from models.cliente import Cliente

COLUNAS = """id, nome, email, telefone, cpf, detalhes,
             data_cadastro, data_atualizacao, status_id"""


def _linha_para_cliente(linha):
    (id_cliente, nome, email, telefone, cpf, detalhes,
     data_cadastro, data_atualizacao, status_id) = linha
    cliente = Cliente(nome, email, telefone, cpf, detalhes, status_id)
    cliente.id = id_cliente
    cliente.data_cadastro = data_cadastro
    cliente.data_atualizacao = data_atualizacao
    return cliente


def criar_tabela_clientes():
    with cursor_bd(commit=True) as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL,
                telefone VARCHAR(20),
                cpf VARCHAR(14),
                detalhes TEXT,
                data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,
                status_id INT DEFAULT 1,

                FOREIGN KEY (status_id) REFERENCES status_clientes(id)
            )
        """)


def criar_cliente(cliente):
    with cursor_bd(commit=True) as cursor:
        # COALESCE: status_id nulo vira 1 (um NULL explícito ignoraria o DEFAULT)
        cursor.execute("""
            INSERT INTO clientes(nome, email, telefone, cpf, detalhes, status_id)
            VALUES (%s, %s, %s, %s, %s, COALESCE(%s, 1))
        """, (cliente.nome, cliente.email, cliente.telefone,
              cliente._cpf, cliente.detalhes, cliente.status_id))
        cliente.id = cursor.lastrowid
    return cliente


def listar_clientes():
    with cursor_bd() as cursor:
        cursor.execute(f"SELECT {COLUNAS} FROM clientes")
        linhas = cursor.fetchall()
    return [_linha_para_cliente(l) for l in linhas]


def buscar_por_id(id_cliente):
    with cursor_bd() as cursor:
        cursor.execute(f"SELECT {COLUNAS} FROM clientes WHERE id = %s", (id_cliente,))
        linha = cursor.fetchone()
    return _linha_para_cliente(linha) if linha else None


def pesquisar_clientes(termo):
    padrao = f"%{termo}%"
    with cursor_bd() as cursor:
        cursor.execute(f"""
            SELECT {COLUNAS} FROM clientes
            WHERE nome LIKE %s OR email LIKE %s OR telefone LIKE %s OR cpf LIKE %s
        """, (padrao, padrao, padrao, padrao))
        linhas = cursor.fetchall()
    return [_linha_para_cliente(l) for l in linhas]


def atualizar_cliente(cliente):
    with cursor_bd(commit=True) as cursor:
        cursor.execute("""
            UPDATE clientes
            SET nome = %s, email = %s, telefone = %s,
                cpf = %s, detalhes = %s, status_id = %s
            WHERE id = %s
        """, (cliente.nome, cliente.email, cliente.telefone,
              cliente._cpf, cliente.detalhes, cliente.status_id, cliente.id))


def excluir_cliente(id_cliente):
    with cursor_bd(commit=True) as cursor:
        cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))