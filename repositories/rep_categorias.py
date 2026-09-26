from banco.db import conectar
from models.categoria import Categoria

def criar_tabela_categorias():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL UNIQUE
        )"""
    )
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_categoria(categoria):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO categorias(nome)
        VALUES (%s)
    """, (categoria.nome,))
    conexao.commit()
    categoria.id = cursor.lastrowid
    
    cursor.close()
    conexao.close()
    return categoria


def listar_categorias():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome
        FROM categorias
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()

    categorias = []
    for id_categoria, nome in resultado:
        categoria = Categoria(nome)
        categoria.id = id_categoria
        categorias.append(categoria)
    return categorias


def buscar_por_id(id_categoria):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome
        FROM categorias
        WHERE id = %s
    """, (id_categoria,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    if resultado is None:
        return None
    id_categoria, nome = resultado


    categoria = Categoria(nome)
    categoria.id = id_categoria
    return categoria



# def atualizar_categoria(categoria):
# ...

# def excluir_categoria(id_categoria):
#     ...