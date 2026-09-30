from flask import Blueprint, request, jsonify

from utils.autenticacao import login_required
from utils.validacao import ler_nome

from repositories import rep_categorias
from models.categoria import Categoria


categoria_bp = Blueprint("categoria", __name__, url_prefix="/categorias")


def categoria_para_dict(categoria):
    return {"id": categoria.id, "nome": categoria.nome}


@categoria_bp.route("/", methods=["GET"])
@login_required
def listar_categorias():
    categorias = rep_categorias.listar_categorias()
    return jsonify([categoria_para_dict(c) for c in categorias]), 200


@categoria_bp.route("/<int:id_categoria>", methods=["GET"])
@login_required
def buscar_categoria(id_categoria):
    categoria = rep_categorias.buscar_por_id(id_categoria)
    if categoria is None:
        return jsonify({"erro": "Categoria não encontrada."}), 404
    return jsonify(categoria_para_dict(categoria)), 200


@categoria_bp.route("/", methods=["POST"])
@login_required
def criar_categoria():
    nome, erro = ler_nome(request.get_json(silent=True))
    if erro:
        return jsonify({"erro": erro}), 400

    categoria = rep_categorias.criar_categoria(Categoria(nome))
    return jsonify(categoria_para_dict(categoria)), 201


@categoria_bp.route("/<int:id_categoria>", methods=["PUT"])
@login_required
def atualizar_categoria(id_categoria):
    categoria = rep_categorias.buscar_por_id(id_categoria)
    if categoria is None:
        return jsonify({"erro": "Categoria não encontrada."}), 404

    nome, erro = ler_nome(request.get_json(silent=True))
    if erro:
        return jsonify({"erro": erro}), 400

    categoria.nome = nome
    rep_categorias.atualizar_categoria(categoria)
    return jsonify(categoria_para_dict(categoria)), 200


@categoria_bp.route("/<int:id_categoria>", methods=["DELETE"])
@login_required
def excluir_categoria(id_categoria):
    if rep_categorias.buscar_por_id(id_categoria) is None:
        return jsonify({"erro": "Categoria não encontrada."}), 404

    rep_categorias.excluir_categoria(id_categoria)
    return jsonify({"mensagem": "Categoria excluída com sucesso."}), 200