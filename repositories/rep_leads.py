from banco.db import cursor_bd
from models.lead import Lead

COLUNAS = """id, nome, email, telefone, servico, mensagem,
             status_id, data_cadastro, cliente_id"""


def _linha_para_lead(linha):
    (id_lead, nome, email, telefone, servico, mensagem,
     status_id, data_cadastro, cliente_id) = linha
    lead = Lead(nome, email, telefone, servico, mensagem, status_id, cliente_id)
    lead.id = id_lead
    lead.data_cadastro = data_cadastro
    return lead


def criar_tabela_leads():
    with cursor_bd(commit=True) as cursor:
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

                FOREIGN KEY (status_id) REFERENCES status_leads(id),
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        """)


def criar_lead(lead):
    with cursor_bd(commit=True) as cursor:
        # COALESCE: status_id nulo vira 1 ("Novo")
        cursor.execute("""
            INSERT INTO leads(nome, email, telefone, servico, mensagem,
                              status_id, cliente_id)
            VALUES (%s, %s, %s, %s, %s, COALESCE(%s, 1), %s)
        """, (lead.nome, lead.email, lead.telefone, lead.servico,
              lead.mensagem, lead.status_id, lead.cliente_id))
        lead.id = cursor.lastrowid
    return lead


def listar_leads():
    with cursor_bd() as cursor:
        cursor.execute(f"SELECT {COLUNAS} FROM leads")
        linhas = cursor.fetchall()
    return [_linha_para_lead(l) for l in linhas]


def buscar_por_id(id_lead):
    with cursor_bd() as cursor:
        cursor.execute(f"SELECT {COLUNAS} FROM leads WHERE id = %s", (id_lead,))
        linha = cursor.fetchone()
    return _linha_para_lead(linha) if linha else None


def pesquisar_leads(termo):
    padrao = f"%{termo}%"
    with cursor_bd() as cursor:
        cursor.execute(f"""
            SELECT {COLUNAS} FROM leads
            WHERE nome LIKE %s OR email LIKE %s OR telefone LIKE %s OR servico LIKE %s
        """, (padrao, padrao, padrao, padrao))
        linhas = cursor.fetchall()
    return [_linha_para_lead(l) for l in linhas]


def atualizar_lead(lead):
    with cursor_bd(commit=True) as cursor:
        cursor.execute("""
            UPDATE leads
            SET nome = %s, email = %s, telefone = %s, servico = %s,
                mensagem = %s, status_id = %s, cliente_id = %s
            WHERE id = %s
        """, (lead.nome, lead.email, lead.telefone, lead.servico,
              lead.mensagem, lead.status_id, lead.cliente_id, lead.id))


def converter_lead(id_lead, cliente):
    """Cria o cliente, vincula ao lead e marca o lead como 'Convertido',
    tudo em uma transação só. Lança ValueError se o lead já foi convertido."""
    with cursor_bd(commit=True) as cursor:
        cursor.execute("""
            INSERT INTO clientes(nome, email, telefone, cpf, detalhes)
            VALUES (%s, %s, %s, %s, %s)
        """, (cliente.nome, cliente.email, cliente.telefone,
              cliente._cpf, cliente.detalhes))
        cliente.id = cursor.lastrowid

        cursor.execute(
            "SELECT id FROM status_leads WHERE nome = %s LIMIT 1", ("Convertido",)
        )
        linha = cursor.fetchone()
        status_convertido = linha[0] if linha else None

        # "AND cliente_id IS NULL" impede conversão dupla, mesmo com dois cliques
        cursor.execute("""
            UPDATE leads
            SET cliente_id = %s, status_id = COALESCE(%s, status_id)
            WHERE id = %s AND cliente_id IS NULL
        """, (cliente.id, status_convertido, id_lead))
        if cursor.rowcount == 0:
            raise ValueError("Este lead já foi convertido.")  # desfaz o INSERT
    return cliente


def excluir_lead(id_lead):
    with cursor_bd(commit=True) as cursor:
        cursor.execute("DELETE FROM leads WHERE id = %s", (id_lead,))