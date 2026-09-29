from flask import Blueprint, render_template


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

@admin_bp.route("/")
def dashboard():
    return render_template(
        "admin/dashboard.html",
        titulo_pagina="Dashboard"
    )

@admin_bp.route("/clientes")
def clientes():
    return render_template(
        "admin/clientes.html",
        titulo_pagina="Clientes"
    )