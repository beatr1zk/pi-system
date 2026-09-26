from banco.db import conectar
from models.lead import Lead

def criar_tabela_leads():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(150),
            telefone VARCHAR(20),
            servico VARCHAR(100) NOT NULL,
            mensagem TEXT,
            status_id INT,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            cliente_id INT NULL,

            FOREIGN KEY (status_id)
                REFERENCES status_leads(id),
            FOREIGN KEY (cliente_id)
                REFERENCES clientes(id)
        )"""
    )

    conexao.commit()
    cursor.close()
    conexao.close()

def criar_lead(lead):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO leads(nome, email, telefone, servico, mensagem, status_id, cliente_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (lead.nome, lead.email, lead.telefone, lead.servico, lead.mensagem, lead.status_id, lead.cliente_id
    ))

    conexao.commit()

    lead.id = cursor.lastrowid

    cursor.close()
    conexao.close()
    return lead

def listar_leads():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, email, telefone, servico, mensagem, status_id, data_cadastro, cliente_id
        FROM leads
    """)

    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    leads = []
    for id_lead, nome, email, telefone, servico, mensagem, status_id, data_cadastro, cliente_id in resultado:
        lead = Lead(nome, email, telefone, servico, mensagem, status_id, cliente_id)
        lead.id = id_lead
        lead.data_cadastro = data_cadastro
        leads.append(lead)
    return leads

def buscar_por_id(id_lead):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, email, telefone, servico, mensagem,
               status_id, data_cadastro, cliente_id
        FROM leads WHERE id = %s
    """, (id_lead,))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado is None:
        return None
    id_lead, nome, email, telefone, servico, mensagem, status_id, data_cadastro, cliente_id = resultado

    lead = Lead(nome, email, telefone, servico, mensagem, status_id, cliente_id)
    lead.id = id_lead
    lead.data_cadastro = data_cadastro
    return lead

def pesquisar_leads(termo):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, email, telefone, servico, mensagem,
               status_id, data_cadastro, cliente_id
        FROM leads
        WHERE nome LIKE %s
           OR email LIKE %s
           OR telefone LIKE %s
           OR servico LIKE %s
    """, ( f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%"
    ))

    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    leads = []

    for id_lead, nome, email, telefone, servico, mensagem, status_id, data_cadastro, cliente_id in resultado:
        lead = Lead(nome, email, telefone, servico, mensagem, status_id, cliente_id)
        lead.id = id_lead
        lead.data_cadastro = data_cadastro
        leads.append(lead)

    return leads

# def atualizar_lead(lead):
#     ...

# def excluir_lead(id_lead):
#     ...