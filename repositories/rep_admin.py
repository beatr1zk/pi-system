from banco.db import conectar
from models.admin import Admin
from werkzeug.security import check_password_hash


def criar_tabela_admin():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin(
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(50) NOT NULL UNIQUE,
            senha VARCHAR(255) NOT NULL,
            ativo BOOLEAN DEFAULT TRUE
        )
    """)

    conexao.commit()

    cursor.close()
    conexao.close()


def criar_admin(admin):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO admin(
            usuario,
            senha
        )
        VALUES (%s, %s)
    """, (
        admin.usuario,
        admin.senha
    ))

    conexao.commit()

    admin.id = cursor.lastrowid

    cursor.close()
    conexao.close()

    return admin


def buscar_por_usuario(usuario):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, usuario, senha, ativo
        FROM admin
        WHERE usuario = %s
    """, (usuario,))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()


    if resultado is None:
        return None


    id_admin, usuario, senha, ativo = resultado


    admin = Admin.__new__(Admin)

    admin.id = id_admin
    admin.usuario = usuario
    admin.senha = senha
    admin.ativo = ativo


    return admin


def validar_senha(admin, senha_digitada):

    return check_password_hash(
        admin.senha,
        senha_digitada
    )