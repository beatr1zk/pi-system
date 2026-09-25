from banco.db import conectar

def criar_tabela_projetos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projetos(
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT NOT NULL,
            categoria_id INT NOT NULL,

            nome VARCHAR(150) NOT NULL,
            escopo TEXT,

            data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_entrega DATE,

            prioridade VARCHAR(20) DEFAULT 'media',
            status VARCHAR(30) DEFAULT 'aguardando_pagamento',

            FOREIGN KEY (cliente_id)
                REFERENCES clientes(id),
            FOREIGN KEY (categoria_id)
                REFERENCES categorias(id)
        )"""
    )

    conexao.commit()
    cursor.close()
    conexao.close()