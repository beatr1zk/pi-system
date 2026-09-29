from flask import Blueprint, request, jsonify

from repositories import rep_prioridades_projeto
from models.prioridade_projeto import PrioridadeProjeto


prioridade_bp = Blueprint(
    "prioridade",
    __name__,
    url_prefix="/prioridades"
)


def prioridade_para_dict(prioridade):
    return {
        "id": prioridade.id,
        "nome": prioridade.nome
    }


@prioridade_bp.route("/", methods=["GET"])
def listar_prioridades():
    prioridades = rep_prioridades_projeto.listar_prioridades_projeto()

    return jsonify([
        prioridade_para_dict(prioridade)
        for prioridade in prioridades
    ]), 200


@prioridade_bp.route("/<int:id_prioridade>", methods=["GET"])
def buscar_prioridade(id_prioridade):
    prioridades = rep_prioridades_projeto.listar_prioridades_projeto()

    for prioridade in prioridades:
        if prioridade.id == id_prioridade:
            return jsonify(
                prioridade_para_dict(prioridade)
            ), 200

    return jsonify({
        "erro": "Prioridade não encontrada."
    }), 404


@prioridade_bp.route("/", methods=["POST"])
def criar_prioridade():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados da prioridade são obrigatórios."
        }), 400

    if not dados.get("nome"):
        return jsonify({
            "erro": "O campo 'nome' é obrigatório."
        }), 400

    prioridade = PrioridadeProjeto(
        dados["nome"]
    )

    prioridade = rep_prioridades_projeto.criar_prioridade_projeto(
        prioridade
    )

    return jsonify(
        prioridade_para_dict(prioridade)
    ), 201


@prioridade_bp.route("/<int:id_prioridade>", methods=["PUT"])
def atualizar_prioridade(id_prioridade):
    prioridades = rep_prioridades_projeto.listar_prioridades_projeto()

    prioridade_existente = None

    for prioridade in prioridades:
        if prioridade.id == id_prioridade:
            prioridade_existente = prioridade
            break

    if prioridade_existente is None:
        return jsonify({
            "erro": "Prioridade não encontrada."
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

    prioridade_existente.nome = dados["nome"]

    rep_prioridades_projeto.atualizar_prioridade_projeto(
        prioridade_existente
    )

    return jsonify(
        prioridade_para_dict(prioridade_existente)
    ), 200


@prioridade_bp.route("/<int:id_prioridade>", methods=["DELETE"])
def excluir_prioridade(id_prioridade):
    prioridades = rep_prioridades_projeto.listar_prioridades_projeto()

    prioridade_existente = None

    for prioridade in prioridades:
        if prioridade.id == id_prioridade:
            prioridade_existente = prioridade
            break

    if prioridade_existente is None:
        return jsonify({
            "erro": "Prioridade não encontrada."
        }), 404

    rep_prioridades_projeto.excluir_prioridade_projeto(
        id_prioridade
    )

    return jsonify({
        "mensagem": "Prioridade excluída com sucesso."
    }), 200