from flask import Blueprint, request, jsonify

from utils.autenticacao import login_required
from utils.validacao import ler_nome

from repositories import rep_status_clientes, rep_status_leads, rep_status_projetos
from models.status_cliente import StatusCliente
from models.status_lead import StatusLead
from models.status_projeto import StatusProjeto


status_bp = Blueprint("status", __name__, url_prefix="/status")

ID_PADRAO = 1  # status usado como padrão; não pode ser excluído

TIPOS = {
    "clientes": {
        "rotulo": "cliente",
        "modelo": StatusCliente,
        "listar": rep_status_clientes.listar_status_clientes,
        "criar": rep_status_clientes.criar_status_cliente,
        "atualizar": rep_status_clientes.atualizar_status_cliente,
        "excluir": rep_status_clientes.excluir_status_cliente,
    },
    "leads": {
        "rotulo": "lead",
        "modelo": StatusLead,
        "listar": rep_status_leads.listar_status_leads,
        "criar": rep_status_leads.criar_status_lead,
        "atualizar": rep_status_leads.atualizar_status_lead,
        "excluir": rep_status_leads.excluir_status_lead,
    },
    "projetos": {
        "rotulo": "projeto",
        "modelo": StatusProjeto,
        "listar": rep_status_projetos.listar_status_projetos,
        "criar": rep_status_projetos.criar_status_projeto,
        "atualizar": rep_status_projetos.atualizar_status_projeto,
        "excluir": rep_status_projetos.excluir_status_projeto,
    },
}


def _para_dict(status):
    return {"id": status.id, "nome": status.nome}


def _registrar(prefixo, cfg):
    rotulo = cfg["rotulo"]

    def achar(id_status):
        for item in cfg["listar"]():
            if item.id == id_status:
                return item
        return None

    def nao_encontrado():
        return jsonify({"erro": f"Status de {rotulo} não encontrado."}), 404

    @login_required
    def listar():
        return jsonify([_para_dict(s) for s in cfg["listar"]()]), 200

    @login_required
    def criar():
        nome, erro = ler_nome(request.get_json(silent=True))
        if erro:
            return jsonify({"erro": erro}), 400
        status = cfg["criar"](cfg["modelo"](nome))
        return jsonify(_para_dict(status)), 201

    @login_required
    def atualizar(id_status):
        status = achar(id_status)
        if status is None:
            return nao_encontrado()
        nome, erro = ler_nome(request.get_json(silent=True))
        if erro:
            return jsonify({"erro": erro}), 400
        status.nome = nome
        cfg["atualizar"](status)
        return jsonify(_para_dict(status)), 200

    @login_required
    def excluir(id_status):
        if achar(id_status) is None:
            return nao_encontrado()
        if id_status == ID_PADRAO:
            return jsonify({
                "erro": "O status padrão (id 1) não pode ser excluído."
            }), 409
        cfg["excluir"](id_status)
        return jsonify({"mensagem": f"Status de {rotulo} excluído com sucesso."}), 200

    base = f"/{prefixo}/"
    status_bp.add_url_rule(base, endpoint=f"listar_{prefixo}", view_func=listar, methods=["GET"])
    status_bp.add_url_rule(base, endpoint=f"criar_{prefixo}", view_func=criar, methods=["POST"])
    status_bp.add_url_rule(base + "<int:id_status>", endpoint=f"atualizar_{prefixo}", view_func=atualizar, methods=["PUT"])
    status_bp.add_url_rule(base + "<int:id_status>", endpoint=f"excluir_{prefixo}", view_func=excluir, methods=["DELETE"])


for _prefixo, _cfg in TIPOS.items():
    _registrar(_prefixo, _cfg)