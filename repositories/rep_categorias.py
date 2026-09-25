from banco.db import conectar

def criar_tabela_categorias():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL UNIQUE,
            descricao VARCHAR(255)
        )"""
    )

    conexao.commit()
    cursor.close()
    conexao.close()