from flask import Blueprint, request, jsonify

from utils.autenticacao import login_required
from utils.validacao import validar_lead, validar_cliente

from repositories import rep_leads
from models.cliente import Cliente
from models.lead import Lead


lead_bp = Blueprint("lead", __name__, url_prefix="/leads")

CAMPOS_EDITAVEIS = ("nome", "email", "telefone", "servico",
                    "mensagem", "status_id", "cliente_id")


def lead_para_dict(lead):
    return {
        "id": lead.id,
        "nome": lead.nome,
        "email": lead.email,
        "telefone": lead.telefone,
        "servico": lead.servico,
        "mensagem": lead.mensagem,
        "status_id": lead.status_id,
        "data_cadastro": lead.data_cadastro.isoformat() if lead.data_cadastro else None,
        "cliente_id": lead.cliente_id,
    }


@lead_bp.route("/", methods=["GET"])
@login_required
def listar_leads():
    leads = rep_leads.listar_leads()
    return jsonify([lead_para_dict(l) for l in leads]), 200


@lead_bp.route("/<int:id_lead>", methods=["GET"])
@login_required
def buscar_lead(id_lead):
    lead = rep_leads.buscar_por_id(id_lead)
    if lead is None:
        return jsonify({"erro": "Lead não encontrado."}), 404
    return jsonify(lead_para_dict(lead)), 200


@lead_bp.route("/pesquisar", methods=["GET"])
@login_required
def pesquisar_leads():
    termo = request.args.get("termo", "").strip()
    if not termo:
        return jsonify({"erro": "O termo de pesquisa é obrigatório."}), 400
    leads = rep_leads.pesquisar_leads(termo)
    return jsonify([lead_para_dict(l) for l in leads]), 200


@lead_bp.route("/", methods=["POST"])
@login_required
def criar_lead():
    dados = request.get_json(silent=True)
    erro = validar_lead(dados, criando=True)
    if erro:
        return jsonify({"erro": erro}), 400

    lead = Lead(
        nome=dados["nome"],
        email=dados.get("email"),
        telefone=dados.get("telefone"),
        servico=dados["servico"],
        mensagem=dados.get("mensagem"),
        status_id=dados.get("status_id"),
        cliente_id=dados.get("cliente_id"),
    )
    lead = rep_leads.criar_lead(lead)
    lead = rep_leads.buscar_por_id(lead.id)
    return jsonify(lead_para_dict(lead)), 201


@lead_bp.route("/<int:id_lead>/converter", methods=["POST"])
@login_required
def converter_lead(id_lead):
    lead = rep_leads.buscar_por_id(id_lead)
    if lead is None:
        return jsonify({"erro": "Lead não encontrado."}), 404
    if lead.cliente_id is not None:
        return jsonify({"erro": "Este lead já foi convertido."}), 409

    corpo = request.get_json(silent=True)
    if not isinstance(corpo, dict):
        corpo = {}

    dados_cliente = {
        "nome": lead.nome,
        "email": corpo.get("email") or lead.email,
        "telefone": lead.telefone,
        "cpf": corpo.get("cpf"),
        "detalhes": corpo.get("detalhes"),
    }
    if not dados_cliente["email"]:
        return jsonify({
            "erro": "Este lead não tem e-mail. Informe 'email' no corpo da requisição."
        }), 400

    erro = validar_cliente(dados_cliente, criando=True)
    if erro:
        return jsonify({"erro": erro}), 400

    cliente = Cliente(
        nome=dados_cliente["nome"],
        email=dados_cliente["email"],
        telefone=dados_cliente["telefone"],
        cpf=dados_cliente["cpf"],
        detalhes=dados_cliente["detalhes"],
        status_id=None,
    )

    try:
        cliente = rep_leads.converter_lead(id_lead, cliente)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 409

    lead = rep_leads.buscar_por_id(id_lead)
    return jsonify({
        "mensagem": "Lead convertido com sucesso.",
        "lead": lead_para_dict(lead),
        "cliente_id": cliente.id,
    }), 201


@lead_bp.route("/<int:id_lead>", methods=["PUT"])
@login_required
def atualizar_lead(id_lead):
    lead = rep_leads.buscar_por_id(id_lead)
    if lead is None:
        return jsonify({"erro": "Lead não encontrado."}), 404

    dados = request.get_json(silent=True)
    erro = validar_lead(dados, criando=False)
    if erro:
        return jsonify({"erro": erro}), 400

    for campo in CAMPOS_EDITAVEIS:
        if campo in dados:
            setattr(lead, campo, dados[campo])

    rep_leads.atualizar_lead(lead)
    lead = rep_leads.buscar_por_id(id_lead)
    return jsonify(lead_para_dict(lead)), 200


@lead_bp.route("/<int:id_lead>", methods=["DELETE"])
@login_required
def excluir_lead(id_lead):
    if rep_leads.buscar_por_id(id_lead) is None:
        return jsonify({"erro": "Lead não encontrado."}), 404
    rep_leads.excluir_lead(id_lead)
    return jsonify({"mensagem": "Lead excluído com sucesso."}), 200