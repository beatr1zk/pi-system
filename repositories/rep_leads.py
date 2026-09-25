from banco.db import conectar

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
            status VARCHAR(30) DEFAULT 'novo',
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            cliente_id INT NULL,

            FOREIGN KEY (cliente_id)
                REFERENCES clientes(id)
        )"""
    )


    conexao.commit()
    cursor.close()
    conexao.close()