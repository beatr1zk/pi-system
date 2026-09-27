from flask import Flask, render_template
from routes.cliente_routes import cliente_bp
from repositories import rep_status_clientes
from repositories import rep_status_leads
from repositories import rep_status_projetos
from repositories import rep_categorias
from repositories import rep_prioridades_projeto
from repositories import rep_clientes
from repositories import rep_leads
from repositories import rep_projetos


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def inicializar_banco():
    rep_status_clientes.criar_tabela_status_clientes()
    rep_status_leads.criar_tabela_status_leads()
    rep_status_projetos.criar_tabela_status_projetos()
    rep_categorias.criar_tabela_categorias()
    rep_prioridades_projeto.criar_tabela_prioridades_projeto()

    rep_clientes.criar_tabela_clientes()
    rep_leads.criar_tabela_leads()
    rep_projetos.criar_tabela_projetos()


app.register_blueprint(cliente_bp)


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)