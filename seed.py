from dotenv import load_dotenv

load_dotenv()  

import os
import getpass
import mysql.connector
from mysql.connector import IntegrityError

from banco.db import conectar
from models.admin import Admin
from repositories import (
    rep_admin, rep_status_clientes, rep_status_leads, rep_status_projetos,
    rep_categorias, rep_prioridades_projeto, rep_clientes, rep_leads, rep_projetos,
)


DADOS = {
    "status_clientes": ["Proposta enviada", "Ativo", "Inativo"],
    "status_leads": ["Novo", "Em contato", "Convertido", "Descartado"],
    "status_projetos": [
        "Aguardando aprovação", "Aguardando pagamento",
        "Em andamento", "Concluído", "Cancelado",
    ],
    "prioridades_projeto": ["Baixa", "Média", "Alta"],
    "categorias": ["Beleza", "Moda", "Tecnologia"],  
}


def criar_banco():
    nome_banco = os.getenv("DB_NAME")

    if not nome_banco:
        raise ValueError("DB_NAME não foi definido no arquivo .env.")

    if not nome_banco.replace("_", "").isalnum():
        raise ValueError("Nome do banco de dados inválido.")

    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    cursor = conexao.cursor()

    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{nome_banco}`")
        conexao.commit()
        print(f"Banco '{nome_banco}' verificado/criado.")
    finally:
        cursor.close()
        conexao.close()


def criar_tabelas():
    rep_admin.criar_tabela_admin()
    rep_status_clientes.criar_tabela_status_clientes()
    rep_status_leads.criar_tabela_status_leads()
    rep_status_projetos.criar_tabela_status_projetos()
    rep_categorias.criar_tabela_categorias()
    rep_prioridades_projeto.criar_tabela_prioridades_projeto()
    rep_clientes.criar_tabela_clientes()
    rep_leads.criar_tabela_leads()
    rep_projetos.criar_tabela_projetos()


def popular_tabela(tabela, nomes):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        for nome in nomes:
            cursor.execute(f"SELECT id FROM {tabela} WHERE nome = %s", (nome,))
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO {tabela}(nome) VALUES (%s)", (nome,))
                print(f"  + {tabela}: {nome}")
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()


def criar_admin_inicial():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT usuario FROM admin LIMIT 1")
    existente = cursor.fetchone()
    cursor.close()
    conexao.close()

    if existente:
        print(f"Já existe um admin ('{existente[0]}'). Nada foi alterado.")
        return

    usuario = input("Usuário do admin: ").strip()
    if not usuario or len(usuario) > 50:
        print("Usuário inválido (1 a 50 caracteres).")
        return

    senha = getpass.getpass("Senha: ")
    if senha != getpass.getpass("Confirme a senha: "):
        print("As senhas não conferem.")
        return
    if len(senha) < 10:
        print("Use pelo menos 10 caracteres.")
        return

    try:
        rep_admin.criar_admin(Admin(usuario, senha))
        print(f"Admin '{usuario}' criado.")
    except IntegrityError:
        print("Esse usuário já existe.")


if __name__ == "__main__":
    criar_banco()
    criar_tabelas()
    for tabela, nomes in DADOS.items():
        popular_tabela(tabela, nomes)
    criar_admin_inicial()