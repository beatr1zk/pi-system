from banco.db import conectar

def criar_tabela_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(150),
            telefone VARCHAR(20),
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
ON UPDATE CURRENT_TIMESTAMP,
            status VARCHAR(30) DEFAULT 'ativo'
        )"""
    )

    conexao.commit()
    cursor.close()
    conexao.close()