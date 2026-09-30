import os
import mysql.connector
from contextlib import contextmanager


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

@contextmanager
def cursor_bd(commit=False):
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