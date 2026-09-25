import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "~~Rotatoria@2026",
        database = "ifood2"
    )
    return conexao