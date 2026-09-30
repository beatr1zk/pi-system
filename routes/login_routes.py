from flask import Blueprint, request, jsonify, session

from repositories import rep_admin


login_bp = Blueprint(
    "login",
    __name__,
    url_prefix="/login"
)


@login_bp.route("/", methods=["POST"])
def login():

    dados = request.get_json(silent=True)


    if not dados:

        return jsonify({
            "erro": "Dados obrigatórios."
        }), 400



    usuario = dados.get("usuario")
    senha = dados.get("senha")



    if not usuario or not senha:

        return jsonify({
            "erro": "Usuário e senha são obrigatórios."
        }), 400



    admin = rep_admin.buscar_por_usuario(usuario)



    if admin is None:

        return jsonify({
            "erro": "Usuário ou senha inválidos."
        }), 401



    if not admin.ativo:

        return jsonify({
            "erro": "Usuário desativado."
        }), 401



    if not rep_admin.validar_senha(admin, senha):
        return jsonify({
            "erro": "Usuário ou senha inválidos."
        }), 401



    session.permanent = True

    session["id_admin"] = admin.id


    return jsonify({
        "mensagem": "Login realizado com sucesso.",
        "usuario": admin.usuario
    }), 200



@login_bp.route("/logout", methods=["POST"])
def logout():

    session.pop(
        "id_admin",
        None
    )


    return jsonify({
        "mensagem": "Logout realizado com sucesso."
    }), 200