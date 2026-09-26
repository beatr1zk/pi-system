from banco.db import conectar
from models.cliente import Cliente

def criar_tabela_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL,
            telefone VARCHAR(20),
            cpf VARCHAR(14),
            servico VARCHAR(100),
            detalhes TEXT,
            url_proposta VARCHAR(255),
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,
            status_id INT,
            
            FOREIGN KEY (status_id) REFERENCES status_clientes(id)
        )"""
    )

    conexao.commit()
    cursor.close()
    conexao.close()

def criar_cliente(cliente):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO clientes(nome, email, telefone, cpf, servico, detalhes, url_proposta, status_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
        (cliente.nome, cliente.email, cliente.telefone, cliente._cpf, cliente.servico, cliente.detalhes, 
        cliente.url_proposta, cliente.status_id
    ))
    conexao.commit()
    cliente.id = cursor.lastrowid

    cursor.close()
    conexao.close()
    return cliente

def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, email, telefone, cpf, servico, detalhes,
               url_proposta, data_cadastro, data_atualizacao, status_id
        FROM clientes
    """)
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    clientes = []
    for id_cliente, nome, email, telefone, cpf, servico, detalhes, url_proposta, data_cadastro, data_atualizacao, status_id in resultado:
        cliente = Cliente(nome, email, telefone, cpf, servico, detalhes, url_proposta, status_id)
        cliente.id = id_cliente
        cliente.data_cadastro = data_cadastro
        cliente.data_atualizacao = data_atualizacao
        clientes.append(cliente)
    return clientes

def buscar_por_id(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, email, telefone, cpf, servico, detalhes,
               url_proposta, data_cadastro, data_atualizacao, status_id
        FROM clientes
        WHERE id = %s
    """, (id_cliente,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado is None:
        return None
    id_cliente, nome, email, telefone, cpf, servico, detalhes, url_proposta, data_cadastro, data_atualizacao, status_id = resultado

    cliente = Cliente(nome, email, telefone, cpf, servico, detalhes, url_proposta, status_id)
    cliente.id = id_cliente
    cliente.data_cadastro = data_cadastro
    cliente.data_atualizacao = data_atualizacao
    return cliente

def pesquisar_clientes(termo):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, email, telefone, cpf, servico, detalhes, url_proposta, data_cadastro, data_atualizacao, status_id
        FROM clientes WHERE nome LIKE %s
           OR email LIKE %s
           OR telefone LIKE %s
           OR cpf LIKE %s
    """, 
    (f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%")
    )
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    clientes = []
    for id_cliente, nome, email, telefone, cpf, servico, detalhes, url_proposta, data_cadastro, data_atualizacao, status_id in resultado:
        cliente = Cliente(nome, email, telefone, cpf, servico, detalhes, url_proposta, status_id)
        cliente.id = id_cliente
        cliente.data_cadastro = data_cadastro
        cliente.data_atualizacao = data_atualizacao
        clientes.append(cliente)
    return clientes

# def atualizar_cliente(cliente):
#     ...

# def excluir_cliente(id_cliente):
#     ...