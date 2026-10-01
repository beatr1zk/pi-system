from flask import Blueprint, render_template, redirect, url_for, session, request


pagina_bp = Blueprint("pagina", __name__)


@pagina_bp.before_request
def exigir_login():
    """Páginas do admin: sem sessão, redireciona para a tela de login."""
    if request.endpoint == "pagina.login":
        return None
    if "id_admin" not in session:
        return redirect(url_for("pagina.login"))
    return None


@pagina_bp.route("/admin/login")
def login():
    if "id_admin" in session:
        return redirect(url_for("pagina.dashboard"))
    return render_template("admin/login.html")


@pagina_bp.route("/admin")
def admin():
    return redirect(url_for("pagina.dashboard"))


@pagina_bp.route("/admin/dashboard")
def dashboard():
    return render_template("admin/dashboard.html", titulo_pagina="Dashboard")


@pagina_bp.route("/admin/leads")
def leads():
    return render_template("admin/leads.html", titulo_pagina="Leads")


@pagina_bp.route("/admin/clientes")
def clientes():
    return render_template("admin/clientes.html", titulo_pagina="Clientes")

@pagina_bp.route("/admin/clientes/<int:id_cliente>")
def cliente(id_cliente):
    return render_template(
        "admin/cliente_detalhe.html",
        titulo_pagina="Cliente",
        id_cliente=id_cliente,
    )


@pagina_bp.route("/admin/projetos")
def projetos():
    return render_template("admin/projetos.html", titulo_pagina="Projetos")

@pagina_bp.route("/admin/projetos/<int:id_projeto>")
def projeto(id_projeto):
    return render_template(
        "admin/projeto_detalhe.html",
        titulo_pagina="Projeto",
        id_projeto=id_projeto,
    )


@pagina_bp.route("/admin/configuracoes")
def configuracoes():
    return render_template("admin/configuracoes.html", titulo_pagina="Configurações")