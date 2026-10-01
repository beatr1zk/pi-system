import os
from dotenv import load_dotenv

load_dotenv()  # antes de qualquer import do projeto

from datetime import timedelta
from flask import Flask, render_template, jsonify
from mysql.connector import IntegrityError, DataError

from routes.prioridade_routes import prioridade_bp
from routes.categoria_routes import categoria_bp
from routes.cliente_routes import cliente_bp
from routes.contato_routes import contato_bp
from routes.projeto_routes import projeto_bp
from routes.pagina_routes import pagina_bp
from routes.status_routes import status_bp
from routes.login_routes import login_bp
from routes.lead_routes import lead_bp
from repositories import (
    rep_admin, rep_status_clientes, rep_status_leads, rep_status_projetos,
    rep_categorias, rep_prioridades_projeto, rep_clientes, rep_leads, rep_projetos,
)

app = Flask(__name__)

secret = os.getenv("SECRET_KEY")
if not secret:
    raise RuntimeError("SECRET_KEY não definida no .env")
app.secret_key = secret

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.getenv("FLASK_ENV") == "production"
app.permanent_session_lifetime = timedelta(hours=2)

# Corpo de requisição com no máximo 16 KB (protege o formulário público)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


@app.route("/")
def index():
    return render_template("index.html")


def inicializar_banco():
    rep_admin.criar_tabela_admin()
    rep_status_clientes.criar_tabela_status_clientes()
    rep_status_leads.criar_tabela_status_leads()
    rep_status_projetos.criar_tabela_status_projetos()
    rep_categorias.criar_tabela_categorias()
    rep_prioridades_projeto.criar_tabela_prioridades_projeto()
    rep_clientes.criar_tabela_clientes()
    rep_leads.criar_tabela_leads()
    rep_projetos.criar_tabela_projetos()


@app.errorhandler(IntegrityError)
def erro_integridade(e):
    return jsonify({"erro": "Operação viola uma regra de integridade (registro duplicado ou em uso)."}), 409


@app.errorhandler(DataError)
def erro_dados(e):
    return jsonify({"erro": "Dados inválidos."}), 400


@app.errorhandler(413)
def erro_tamanho(e):
    return jsonify({"erro": "Requisição grande demais."}), 413


@app.errorhandler(500)
def erro_interno(e):
    return jsonify({"erro": "Erro interno."}), 500


for bp in (prioridade_bp, categoria_bp, cliente_bp, contato_bp, projeto_bp,
           status_bp, pagina_bp, login_bp, lead_bp):
    app.register_blueprint(bp)

inicializar_banco()  # roda também com flask run / gunicorn

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")