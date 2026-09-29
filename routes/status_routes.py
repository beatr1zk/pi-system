from flask import Blueprint, request, jsonify

from repositories import rep_status_clientes
from repositories import rep_status_leads
from repositories import rep_status_projetos

from models.status_cliente import StatusCliente
from models.status_lead import StatusLead
from models.status_projeto import StatusProjeto


status_bp = Blueprint(
    "status",
    __name__,
    url_prefix="/status"
)


# =========================================================
# STATUS DE CLIENTES
# =========================================================

def status_cliente_para_dict(status):
    return {
        "id": status.id,
        "nome": status.nome
    }


@status_bp.route("/clientes/", methods=["GET"])
def listar_status_clientes():
    status = rep_status_clientes.listar_status_clientes()

    return jsonify([
        status_cliente_para_dict(item)
        for item in status
    ]), 200


@status_bp.route("/clientes/", methods=["POST"])
def criar_status_cliente():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados do status são obrigatórios."
        }), 400

    if not dados.get("nome"):
        return jsonify({
            "erro": "O campo 'nome' é obrigatório."
        }), 400

    status = StatusCliente(dados["nome"])

    status = rep_status_clientes.criar_status_cliente(status)

    return jsonify(
        status_cliente_para_dict(status)
    ), 201


@status_bp.route("/clientes/<int:id_status>", methods=["PUT"])
def atualizar_status_cliente(id_status):
    status = rep_status_clientes.listar_status_clientes()

    status_existente = None

    for item in status:
        if item.id == id_status:
            status_existente = item
            break

    if status_existente is None:
        return jsonify({
            "erro": "Status de cliente não encontrado."
        }), 404

    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados para atualização são obrigatórios."
        }), 400

    if not dados.get("nome"):
        return jsonify({
            "erro": "O campo 'nome' é obrigatório."
        }), 400

    status_existente.nome = dados["nome"]

    rep_status_clientes.atualizar_status_cliente(
        status_existente
    )

    return jsonify(
        status_cliente_para_dict(status_existente)
    ), 200


@status_bp.route("/clientes/<int:id_status>", methods=["DELETE"])
def excluir_status_cliente(id_status):
    status = rep_status_clientes.listar_status_clientes()

    status_existente = None

    for item in status:
        if item.id == id_status:
            status_existente = item
            break

    if status_existente is None:
        return jsonify({
            "erro": "Status de cliente não encontrado."
        }), 404

    rep_status_clientes.excluir_status_cliente(id_status)

    return jsonify({
        "mensagem": "Status de cliente excluído com sucesso."
    }), 200


# =========================================================
# STATUS DE LEADS
# =========================================================

def status_lead_para_dict(status):
    return {
        "id": status.id,
        "nome": status.nome
    }


@status_bp.route("/leads/", methods=["GET"])
def listar_status_leads():
    status = rep_status_leads.listar_status_leads()

    return jsonify([
        status_lead_para_dict(item)
        for item in status
    ]), 200


@status_bp.route("/leads/", methods=["POST"])
def criar_status_lead():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados do status são obrigatórios."
        }), 400

    if not dados.get("nome"):
        return jsonify({
            "erro": "O campo 'nome' é obrigatório."
        }), 400

    status = StatusLead(dados["nome"])

    status = rep_status_leads.criar_status_lead(status)

    return jsonify(
        status_lead_para_dict(status)
    ), 201


@status_bp.route("/leads/<int:id_status>", methods=["PUT"])
def atualizar_status_lead(id_status):
    status = rep_status_leads.listar_status_leads()

    status_existente = None

    for item in status:
        if item.id == id_status:
            status_existente = item
            break

    if status_existente is None:
        return jsonify({
            "erro": "Status de lead não encontrado."
        }), 404

    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados para atualização são obrigatórios."
        }), 400

    if not dados.get("nome"):
        return jsonify({
            "erro": "O campo 'nome' é obrigatório."
        }), 400

    status_existente.nome = dados["nome"]

    rep_status_leads.atualizar_status_lead(
        status_existente
    )

    return jsonify(
        status_lead_para_dict(status_existente)
    ), 200


@status_bp.route("/leads/<int:id_status>", methods=["DELETE"])
def excluir_status_lead(id_status):
    status = rep_status_leads.listar_status_leads()

    status_existente = None

    for item in status:
        if item.id == id_status:
            status_existente = item
            break

    if status_existente is None:
        return jsonify({
            "erro": "Status de lead não encontrado."
        }), 404

    rep_status_leads.excluir_status_lead(id_status)

    return jsonify({
        "mensagem": "Status de lead excluído com sucesso."
    }), 200


# =========================================================
# STATUS DE PROJETOS
# =========================================================

def status_projeto_para_dict(status):
    return {
        "id": status.id,
        "nome": status.nome
    }


@status_bp.route("/projetos/", methods=["GET"])
def listar_status_projetos():
    status = rep_status_projetos.listar_status_projetos()

    return jsonify([
        status_projeto_para_dict(item)
        for item in status
    ]), 200


@status_bp.route("/projetos/", methods=["POST"])
def criar_status_projeto():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados do status são obrigatórios."
        }), 400

    if not dados.get("nome"):
        return jsonify({
            "erro": "O campo 'nome' é obrigatório."
        }), 400

    status = StatusProjeto(dados["nome"])

    status = rep_status_projetos.criar_status_projeto(status)

    return jsonify(
        status_projeto_para_dict(status)
    ), 201


@status_bp.route("/projetos/<int:id_status>", methods=["PUT"])
def atualizar_status_projeto(id_status):
    status = rep_status_projetos.listar_status_projetos()

    status_existente = None

    for item in status:
        if item.id == id_status:
            status_existente = item
            break

    if status_existente is None:
        return jsonify({
            "erro": "Status de projeto não encontrado."
        }), 404

    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados para atualização são obrigatórios."
        }), 400

    if not dados.get("nome"):
        return jsonify({
            "erro": "O campo 'nome' é obrigatório."
        }), 400

    status_existente.nome = dados["nome"]

    rep_status_projetos.atualizar_status_projeto(
        status_existente
    )

    return jsonify(
        status_projeto_para_dict(status_existente)
    ), 200


@status_bp.route("/projetos/<int:id_status>", methods=["DELETE"])
def excluir_status_projeto(id_status):
    status = rep_status_projetos.listar_status_projetos()

    status_existente = None

    for item in status:
        if item.id == id_status:
            status_existente = item
            break

    if status_existente is None:
        return jsonify({
            "erro": "Status de projeto não encontrado."
        }), 404

    rep_status_projetos.excluir_status_projeto(id_status)

    return jsonify({
        "mensagem": "Status de projeto excluído com sucesso."
    }), 200