from flask import Blueprint, request, jsonify

from repositories import rep_clientes
from models.cliente import Cliente

cliente_bp = Blueprint("cliente", __name__, url_prefix="/clientes")


def cliente_para_dict(cliente):
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "telefone": cliente.telefone,
        "cpf": cliente._cpf,
        "servico": cliente.servico,
        "detalhes": cliente.detalhes,
        "url_proposta": cliente.url_proposta,
        "status_id": cliente.status_id,
        "data_cadastro": (
            cliente.data_cadastro.isoformat()
            if cliente.data_cadastro else None
        ),
        "data_atualizacao": (
            cliente.data_atualizacao.isoformat()
            if cliente.data_atualizacao else None
        )
    }


@cliente_bp.route("/", methods=["GET"])
def listar_clientes():
    clientes = rep_clientes.listar_clientes()

    return jsonify([
        cliente_para_dict(cliente)
        for cliente in clientes
    ]), 200


@cliente_bp.route("/<int:id_cliente>", methods=["GET"])
def buscar_cliente(id_cliente):
    cliente = rep_clientes.buscar_por_id(id_cliente)

    if cliente is None:
        return jsonify({
            "erro": "Cliente não encontrado."
        }), 404

    return jsonify(cliente_para_dict(cliente)), 200


@cliente_bp.route("/pesquisar", methods=["GET"])
def pesquisar_clientes():
    termo = request.args.get("termo", "").strip()

    if not termo:
        return jsonify({
            "erro": "O termo de pesquisa é obrigatório."
        }), 400

    clientes = rep_clientes.pesquisar_clientes(termo)

    return jsonify([
        cliente_para_dict(cliente)
        for cliente in clientes
    ]), 200


@cliente_bp.route("/", methods=["POST"])
def criar_cliente():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados do cliente são obrigatórios."
        }), 400

    campos_obrigatorios = ["nome", "email"]

    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({
                "erro": f"O campo '{campo}' é obrigatório."
            }), 400

    cliente = Cliente(
        dados["nome"],
        dados["email"],
        dados.get("telefone"),
        dados.get("cpf"),
        dados.get("servico"),
        dados.get("detalhes"),
        dados.get("url_proposta"),
        dados.get("status_id")
    )

    cliente = rep_clientes.criar_cliente(cliente)

    return jsonify(cliente_para_dict(cliente)), 201


@cliente_bp.route("/<int:id_cliente>", methods=["PUT"])
def atualizar_cliente(id_cliente):
    cliente_existente = rep_clientes.buscar_por_id(id_cliente)

    if cliente_existente is None:
        return jsonify({
            "erro": "Cliente não encontrado."
        }), 404

    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados para atualização são obrigatórios."
        }), 400

    cliente_existente.nome = dados.get(
        "nome",
        cliente_existente.nome
    )

    cliente_existente.email = dados.get(
        "email",
        cliente_existente.email
    )

    cliente_existente.telefone = dados.get(
        "telefone",
        cliente_existente.telefone
    )

    cliente_existente._cpf = dados.get(
        "cpf",
        cliente_existente._cpf
    )

    cliente_existente.servico = dados.get(
        "servico",
        cliente_existente.servico
    )

    cliente_existente.detalhes = dados.get(
        "detalhes",
        cliente_existente.detalhes
    )

    cliente_existente.url_proposta = dados.get(
        "url_proposta",
        cliente_existente.url_proposta
    )

    cliente_existente.status_id = dados.get(
        "status_id",
        cliente_existente.status_id
    )

    rep_clientes.atualizar_cliente(cliente_existente)

    cliente_atualizado = rep_clientes.buscar_por_id(id_cliente)

    return jsonify(
        cliente_para_dict(cliente_atualizado)
    ), 200


@cliente_bp.route("/<int:id_cliente>", methods=["DELETE"])
def excluir_cliente(id_cliente):
    cliente = rep_clientes.buscar_por_id(id_cliente)

    if cliente is None:
        return jsonify({
            "erro": "Cliente não encontrado."
        }), 404

    rep_clientes.excluir_cliente(id_cliente)

    return jsonify({
        "mensagem": "Cliente excluído com sucesso."
    }), 200