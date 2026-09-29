from flask import Blueprint, request, jsonify

from repositories import rep_leads
from models.lead import Lead


lead_bp = Blueprint("lead", __name__, url_prefix="/leads")


def lead_para_dict(lead):
    return {
        "id": lead.id,
        "nome": lead.nome,
        "email": lead.email,
        "telefone": lead.telefone,
        "servico": lead.servico,
        "mensagem": lead.mensagem,
        "status_id": lead.status_id,
        "data_cadastro": (
            lead.data_cadastro.isoformat()
            if lead.data_cadastro else None
        ),
        "cliente_id": lead.cliente_id
    }


@lead_bp.route("/", methods=["GET"])
def listar_leads():
    leads = rep_leads.listar_leads()

    return jsonify([
        lead_para_dict(lead)
        for lead in leads
    ]), 200


@lead_bp.route("/<int:id_lead>", methods=["GET"])
def buscar_lead(id_lead):
    lead = rep_leads.buscar_por_id(id_lead)

    if lead is None:
        return jsonify({
            "erro": "Lead não encontrado."
        }), 404

    return jsonify(lead_para_dict(lead)), 200


@lead_bp.route("/pesquisar", methods=["GET"])
def pesquisar_leads():
    termo = request.args.get("termo", "").strip()

    if not termo:
        return jsonify({
            "erro": "O termo de pesquisa é obrigatório."
        }), 400

    leads = rep_leads.pesquisar_leads(termo)

    return jsonify([
        lead_para_dict(lead)
        for lead in leads
    ]), 200


@lead_bp.route("/", methods=["POST"])
def criar_lead():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados do lead são obrigatórios."
        }), 400

    campos_obrigatorios = ["nome", "servico"]

    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({
                "erro": f"O campo '{campo}' é obrigatório."
            }), 400

    lead = Lead(
        dados["nome"],
        dados.get("email"),
        dados.get("telefone"),
        dados["servico"],
        dados.get("mensagem"),
        dados.get("status_id"),
        dados.get("cliente_id")
    )

    lead = rep_leads.criar_lead(lead)

    return jsonify(lead_para_dict(lead)), 201


@lead_bp.route("/<int:id_lead>", methods=["PUT"])
def atualizar_lead(id_lead):
    lead_existente = rep_leads.buscar_por_id(id_lead)

    if lead_existente is None:
        return jsonify({
            "erro": "Lead não encontrado."
        }), 404

    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados para atualização são obrigatórios."
        }), 400

    lead_existente.nome = dados.get(
        "nome",
        lead_existente.nome
    )

    lead_existente.email = dados.get(
        "email",
        lead_existente.email
    )

    lead_existente.telefone = dados.get(
        "telefone",
        lead_existente.telefone
    )

    lead_existente.servico = dados.get(
        "servico",
        lead_existente.servico
    )

    lead_existente.mensagem = dados.get(
        "mensagem",
        lead_existente.mensagem
    )

    lead_existente.status_id = dados.get(
        "status_id",
        lead_existente.status_id
    )

    lead_existente.cliente_id = dados.get(
        "cliente_id",
        lead_existente.cliente_id
    )

    rep_leads.atualizar_lead(lead_existente)

    lead_atualizado = rep_leads.buscar_por_id(id_lead)

    return jsonify(
        lead_para_dict(lead_atualizado)
    ), 200


@lead_bp.route("/<int:id_lead>", methods=["DELETE"])
def excluir_lead(id_lead):
    lead = rep_leads.buscar_por_id(id_lead)

    if lead is None:
        return jsonify({
            "erro": "Lead não encontrado."
        }), 404

    rep_leads.excluir_lead(id_lead)

    return jsonify({
        "mensagem": "Lead excluído com sucesso."
    }), 200