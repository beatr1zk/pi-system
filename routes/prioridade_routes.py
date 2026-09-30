from flask import Blueprint, request, jsonify

from utils.autenticacao import login_required
from utils.validacao import ler_nome

from repositories import rep_prioridades_projeto
from models.prioridade_projeto import PrioridadeProjeto


prioridade_bp = Blueprint("prioridade", __name__, url_prefix="/prioridades")


def prioridade_para_dict(prioridade):
    return {"id": prioridade.id, "nome": prioridade.nome}


def _achar(id_prioridade):
    for p in rep_prioridades_projeto.listar_prioridades_projeto():
        if p.id == id_prioridade:
            return p
    return None


@prioridade_bp.route("/", methods=["GET"])
@login_required
def listar_prioridades():
    prioridades = rep_prioridades_projeto.listar_prioridades_projeto()
    return jsonify([prioridade_para_dict(p) for p in prioridades]), 200


@prioridade_bp.route("/<int:id_prioridade>", methods=["GET"])
@login_required
def buscar_prioridade(id_prioridade):
    prioridade = _achar(id_prioridade)
    if prioridade is None:
        return jsonify({"erro": "Prioridade não encontrada."}), 404
    return jsonify(prioridade_para_dict(prioridade)), 200


@prioridade_bp.route("/", methods=["POST"])
@login_required
def criar_prioridade():
    nome, erro = ler_nome(request.get_json(silent=True))
    if erro:
        return jsonify({"erro": erro}), 400

    prioridade = rep_prioridades_projeto.criar_prioridade_projeto(
        PrioridadeProjeto(nome)
    )
    return jsonify(prioridade_para_dict(prioridade)), 201


@prioridade_bp.route("/<int:id_prioridade>", methods=["PUT"])
@login_required
def atualizar_prioridade(id_prioridade):
    prioridade = _achar(id_prioridade)
    if prioridade is None:
        return jsonify({"erro": "Prioridade não encontrada."}), 404

    nome, erro = ler_nome(request.get_json(silent=True))
    if erro:
        return jsonify({"erro": erro}), 400

    prioridade.nome = nome
    rep_prioridades_projeto.atualizar_prioridade_projeto(prioridade)
    return jsonify(prioridade_para_dict(prioridade)), 200


@prioridade_bp.route("/<int:id_prioridade>", methods=["DELETE"])
@login_required
def excluir_prioridade(id_prioridade):
    if _achar(id_prioridade) is None:
        return jsonify({"erro": "Prioridade não encontrada."}), 404

    rep_prioridades_projeto.excluir_prioridade_projeto(id_prioridade)
    return jsonify({"mensagem": "Prioridade excluída com sucesso."}), 200