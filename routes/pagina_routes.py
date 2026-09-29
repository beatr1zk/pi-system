from flask import Blueprint, render_template, redirect, url_for


pagina_bp = Blueprint("pagina", __name__)


@pagina_bp.route("/admin")
def admin():
    return redirect(url_for("pagina.dashboard"))


@pagina_bp.route("/admin/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")


@pagina_bp.route("/admin/leads")
def leads():
    return render_template("admin/leads.html")


@pagina_bp.route("/admin/clientes")
def clientes():
    return render_template("admin/clientes.html")


@pagina_bp.route("/admin/projetos")
def projetos():
    return render_template("admin/projetos.html")


@pagina_bp.route("/admin/configuracoes")
def configuracoes():
    return render_template("admin/configuracoes.html")


@pagina_bp.route("/admin/configuracoes/prioridades")
def prioridades():
    return render_template("admin/configuracoes/prioridades.html")


@pagina_bp.route("/admin/configuracoes/categorias")
def categorias():
    return render_template("admin/configuracoes/categorias.html")


@pagina_bp.route("/admin/configuracoes/status-projetos")
def status_projetos():
    return render_template("admin/configuracoes/status_projetos.html")


@pagina_bp.route("/admin/configuracoes/status-clientes")
def status_clientes():
    return render_template("admin/configuracoes/status_clientes.html")


@pagina_bp.route("/admin/configuracoes/status-leads")
def status_leads():
    return render_template("admin/configuracoes/status_leads.html")