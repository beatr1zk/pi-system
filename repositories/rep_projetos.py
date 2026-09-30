from contextlib import contextmanager

from banco.db import conectar
from models.projeto import Projeto

# Uma única lista de colunas e um único conversor: a ordem do SELECT
# e a montagem do Projeto ficam juntas, então a inversão não se repete.
COLUNAS = """id, cliente_id, categoria_id, nome, servico, escopo,
             url_proposta, data_pedido, data_entrega, data_conclusao,
             prioridade_id, status_id"""


@contextmanager
def _cursor(commit=False):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        yield cursor
        if commit:
            conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def _linha_para_projeto(linha):
    (id_projeto, cliente_id, categoria_id, nome, servico, escopo,
     url_proposta, data_pedido, data_entrega, data_conclusao,
     prioridade_id, status_id) = linha

    projeto = Projeto(
        cliente_id=cliente_id,
        categoria_id=categoria_id,
        nome=nome,
        escopo=escopo,
        servico=servico,
        data_pedido=data_pedido,
        data_entrega=data_entrega,
        data_conclusao=data_conclusao,
        prioridade_id=prioridade_id,
        status_id=status_id,
        url_proposta=url_proposta,
    )
    projeto.id = id_projeto
    return projeto


def criar_tabela_projetos():
    with _cursor(commit=True) as cursor:
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

                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (categoria_id) REFERENCES categorias(id),
                FOREIGN KEY (prioridade_id) REFERENCES prioridades_projeto(id),
                FOREIGN KEY (status_id) REFERENCES status_projetos(id)
            )
        """)


def criar_projeto(projeto):
    with _cursor(commit=True) as cursor:
        # COALESCE: se data_pedido vier None, vale o horário atual
        # (um NULL explícito ignoraria o DEFAULT da coluna).
        cursor.execute("""
            INSERT INTO projetos(
                cliente_id, categoria_id, nome, servico, escopo,
                url_proposta, data_pedido, data_entrega, data_conclusao,
                prioridade_id, status_id
            )
            VALUES (%s, %s, %s, %s, %s, %s,
                    COALESCE(%s, CURRENT_TIMESTAMP),
                    %s, %s, %s, %s)
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
        ))
        projeto.id = cursor.lastrowid
    return projeto


def listar_projetos():
    with _cursor() as cursor:
        cursor.execute(f"SELECT {COLUNAS} FROM projetos")
        linhas = cursor.fetchall()
    return [_linha_para_projeto(linha) for linha in linhas]


def buscar_por_id(id_projeto):
    with _cursor() as cursor:
        cursor.execute(
            f"SELECT {COLUNAS} FROM projetos WHERE id = %s", (id_projeto,)
        )
        linha = cursor.fetchone()
    return _linha_para_projeto(linha) if linha else None


def pesquisar_projetos(termo):
    padrao = f"%{termo}%"
    with _cursor() as cursor:
        cursor.execute(f"""
            SELECT {COLUNAS}
            FROM projetos
            WHERE nome LIKE %s OR servico LIKE %s OR escopo LIKE %s
        """, (padrao, padrao, padrao))
        linhas = cursor.fetchall()
    return [_linha_para_projeto(linha) for linha in linhas]


def atualizar_projeto(projeto):
    with _cursor(commit=True) as cursor:
        # COALESCE: data_pedido nula mantém o valor que já estava no banco.
        cursor.execute("""
            UPDATE projetos
            SET cliente_id = %s,
                categoria_id = %s,
                nome = %s,
                servico = %s,
                escopo = %s,
                url_proposta = %s,
                data_pedido = COALESCE(%s, data_pedido),
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
            projeto.id,
        ))


def excluir_projeto(id_projeto):
    with _cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM projetos WHERE id = %s", (id_projeto,))