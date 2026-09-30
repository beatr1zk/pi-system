from flask import Blueprint, request, jsonify

from utils.autenticacao import login_required
from utils.validacao import validar_cliente

from repositories import rep_clientes
from models.cliente import Cliente


cliente_bp = Blueprint("cliente", __name__, url_prefix="/clientes")

CAMPOS_EDITAVEIS = ("nome", "email", "telefone", "detalhes", "status_id")


def _mascarar_cpf(cpf):
    return f"***.***.***-{cpf[-2:]}" if cpf else None


def cliente_para_dict(cliente, completo=False):
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "telefone": cliente.telefone,
        "cpf": cliente._cpf if completo else _mascarar_cpf(cliente._cpf),
        "detalhes": cliente.detalhes,
        "status_id": cliente.status_id,
        "data_cadastro": cliente.data_cadastro.isoformat() if cliente.data_cadastro else None,
        "data_atualizacao": cliente.data_atualizacao.isoformat() if cliente.data_atualizacao else None,
    }


@cliente_bp.route("/", methods=["GET"])
@login_required
def listar_clientes():
    clientes = rep_clientes.listar_clientes()
    return jsonify([cliente_para_dict(c) for c in clientes]), 200


@cliente_bp.route("/<int:id_cliente>", methods=["GET"])
@login_required
def buscar_cliente(id_cliente):
    cliente = rep_clientes.buscar_por_id(id_cliente)
    if cliente is None:
        return jsonify({"erro": "Cliente não encontrado."}), 404
    return jsonify(cliente_para_dict(cliente, completo=True)), 200


@cliente_bp.route("/pesquisar", methods=["GET"])
@login_required
def pesquisar_clientes():
    termo = request.args.get("termo", "").strip()
    if not termo:
        return jsonify({"erro": "O termo de pesquisa é obrigatório."}), 400
    clientes = rep_clientes.pesquisar_clientes(termo)
    return jsonify([cliente_para_dict(c) for c in clientes]), 200


@cliente_bp.route("/", methods=["POST"])
@login_required
def criar_cliente():
    dados = request.get_json(silent=True)
    erro = validar_cliente(dados, criando=True)
    if erro:
        return jsonify({"erro": erro}), 400

    cliente = Cliente(
        nome=dados["nome"],
        email=dados["email"],
        telefone=dados.get("telefone"),
        cpf=dados.get("cpf"),
        detalhes=dados.get("detalhes"),
        status_id=dados.get("status_id"),
    )
    cliente = rep_clientes.criar_cliente(cliente)
    cliente = rep_clientes.buscar_por_id(cliente.id)  # relê: datas e status final
    return jsonify(cliente_para_dict(cliente, completo=True)), 201


@cliente_bp.route("/<int:id_cliente>", methods=["PUT"])
@login_required
def atualizar_cliente(id_cliente):
    cliente = rep_clientes.buscar_por_id(id_cliente)
    if cliente is None:
        return jsonify({"erro": "Cliente não encontrado."}), 404

    dados = request.get_json(silent=True)
    erro = validar_cliente(dados, criando=False)
    if erro:
        return jsonify({"erro": erro}), 400

    for campo in CAMPOS_EDITAVEIS:
        if campo in dados:
            setattr(cliente, campo, dados[campo])
    if "cpf" in dados:
        cliente._cpf = dados["cpf"]

    rep_clientes.atualizar_cliente(cliente)
    cliente = rep_clientes.buscar_por_id(id_cliente)
    return jsonify(cliente_para_dict(cliente, completo=True)), 200


@cliente_bp.route("/<int:id_cliente>", methods=["DELETE"])
@login_required
def excluir_cliente(id_cliente):
    if rep_clientes.buscar_por_id(id_cliente) is None:
        return jsonify({"erro": "Cliente não encontrado."}), 404
    rep_clientes.excluir_cliente(id_cliente)  # em uso por projeto/lead -> 409 (handler)
    return jsonify({"mensagem": "Cliente excluído com sucesso."}), 200