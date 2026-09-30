from banco.db import conectar
from models.projeto import Projeto

def criar_tabela_projetos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projetos(
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT NOT NULL,
            categoria_id INT NOT NULL,
            nome VARCHAR(150) NOT NULL,
            servico VARCHAR(100),
            escopo TEXT,
            url_proposta VARCHAR(255),
            data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_entrega DATE,
            data_conclusao DATE,
            prioridade_id INT,
            status_id INT,

            FOREIGN KEY (cliente_id)
                REFERENCES clientes(id),
            FOREIGN KEY (categoria_id)
                REFERENCES categorias(id),
            FOREIGN KEY (prioridade_id)
                REFERENCES prioridades_projeto(id),
            FOREIGN KEY (status_id)
                REFERENCES status_projetos(id)
        )"""
    )
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_projeto(projeto):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO projetos(
            cliente_id,
            categoria_id,
            nome,
            servico,
            escopo,
            url_proposta,
            data_pedido,
            data_entrega,
            data_conclusao,
            prioridade_id,
            status_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
        (projeto.cliente_id,projeto.categoria_id,projeto.nome,projeto.servico,projeto.escopo,projeto.url_proposta,projeto.data_pedido,projeto.data_entrega,
        projeto.data_conclusao,projeto.prioridade_id,projeto.status_id)
    )
    conexao.commit()
    projeto.id = cursor.lastrowid

    cursor.close()
    conexao.close()
    return projeto

def listar_projetos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, cliente_id, categoria_id, nome, servico, escopo,
               url_proposta, data_pedido, data_entrega, data_conclusao,
               prioridade_id, status_id
        FROM projetos
    """)
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    projetos = []
    for id_projeto, cliente_id, categoria_id, nome, servico, escopo, url_proposta, data_pedido, data_entrega, data_conclusao, prioridade_id, status_id in resultado:
        projeto = Projeto(cliente_id, categoria_id, nome, servico, escopo, data_pedido, data_entrega, data_conclusao, prioridade_id, status_id, url_proposta)
        projeto.id = id_projeto
        projetos.append(projeto)
    return projetos

def buscar_por_id(id_projeto):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, cliente_id, categoria_id, nome, servico, escopo,
               url_proposta, data_pedido, data_entrega, data_conclusao,
               prioridade_id, status_id
        FROM projetos
        WHERE id = %s
    """, (id_projeto,)
    )
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado is None:
        return None
    id_projeto, cliente_id, categoria_id, nome, servico, escopo, url_proposta, data_pedido, data_entrega, data_conclusao, prioridade_id, status_id = resultado

    projeto = Projeto(cliente_id, categoria_id, nome, servico, escopo, data_pedido, data_entrega, data_conclusao, prioridade_id, status_id, url_proposta
    )
    projeto.id = id_projeto
    return projeto

def pesquisar_projetos(termo):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, cliente_id, categoria_id, nome, servico, escopo,
               url_proposta, data_pedido, data_entrega, data_conclusao,
               prioridade_id, status_id
        FROM projetos
        WHERE nome LIKE %s
           OR servico LIKE %s
           OR escopo LIKE %s
    """, (f"%{termo}%", f"%{termo}%", f"%{termo}%")
    )
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    projetos = []

    for id_projeto, cliente_id, categoria_id, nome, servico, escopo, url_proposta, data_pedido, data_entrega, data_conclusao, prioridade_id, status_id in resultado:
        projeto = Projeto(cliente_id, categoria_id, nome, servico, escopo, data_pedido, data_entrega, data_conclusao, prioridade_id, status_id, url_proposta)
        projeto.id = id_projeto
        projetos.append(projeto)

    return projetos

def atualizar_projeto(projeto):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE projetos
        SET cliente_id = %s,
            categoria_id = %s,
            nome = %s,
            servico = %s,
            escopo = %s,
            url_proposta = %s,
            data_pedido = %s,
            data_entrega = %s,
            data_conclusao = %s,
            prioridade_id = %s,
            status_id = %s
        WHERE id = %s
    """, (
        projeto.cliente_id,
        projeto.categoria_id,
        projeto.nome,
        projeto.servico,
        projeto.escopo,
        projeto.url_proposta,
        projeto.data_pedido,
        projeto.data_entrega,
        projeto.data_conclusao,
        projeto.prioridade_id,
        projeto.status_id,
        projeto.id
    ))

    conexao.commit()

    cursor.close()
    conexao.close()


def excluir_projeto(id_projeto):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM projetos
        WHERE id = %s
    """, (id_projeto,))

    conexao.commit()

    cursor.close()
    conexao.close()