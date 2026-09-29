from flask import Flask, render_template
from routes.cliente_routes import cliente_bp
from routes.pagina_routes import pagina_bp
from routes.lead_routes import lead_bp
from repositories import rep_status_clientes, rep_status_leads, rep_status_projetos, rep_categorias, rep_prioridades_projeto, rep_clientes, rep_leads, rep_projetos


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
app.register_blueprint(pagina_bp)
app.register_blueprint(lead_bp)


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)