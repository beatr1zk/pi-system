from flask import Blueprint, request, jsonify

from repositories import rep_categorias
from models.categoria import Categoria


categoria_bp = Blueprint(
    "categoria",
    __name__,
    url_prefix="/categorias"
)


def categoria_para_dict(categoria):
    return {
        "id": categoria.id,
        "nome": categoria.nome
    }


@categoria_bp.route("/", methods=["GET"])
def listar_categorias():
    categorias = rep_categorias.listar_categorias()

    return jsonify([
        categoria_para_dict(categoria)
        for categoria in categorias
    ]), 200


@categoria_bp.route("/<int:id_categoria>", methods=["GET"])
def buscar_categoria(id_categoria):
    categoria = rep_categorias.buscar_por_id(id_categoria)

    if categoria is None:
        return jsonify({
            "erro": "Categoria não encontrada."
        }), 404

    return jsonify(
        categoria_para_dict(categoria)
    ), 200


@categoria_bp.route("/", methods=["POST"])
def criar_categoria():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados da categoria são obrigatórios."
        }), 400

    if not dados.get("nome"):
        return jsonify({
            "erro": "O campo 'nome' é obrigatório."
        }), 400

    categoria = Categoria(
        dados["nome"]
    )

    categoria = rep_categorias.criar_categoria(categoria)

    return jsonify(
        categoria_para_dict(categoria)
    ), 201

@categoria_bp.route("/<int:id_categoria>", methods=["PUT"])
def atualizar_categoria(id_categoria):
    categoria_existente = rep_categorias.buscar_por_id(id_categoria)

    if categoria_existente is None:
        return jsonify({
            "erro": "Categoria não encontrada."
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

    categoria_existente.nome = dados["nome"]

    rep_categorias.atualizar_categoria(categoria_existente)

    categoria_atualizada = rep_categorias.buscar_por_id(id_categoria)

    return jsonify(
        categoria_para_dict(categoria_atualizada)
    ), 200


@categoria_bp.route("/<int:id_categoria>", methods=["DELETE"])
def excluir_categoria(id_categoria):
    categoria = rep_categorias.buscar_por_id(id_categoria)

    if categoria is None:
        return jsonify({
            "erro": "Categoria não encontrada."
        }), 404

    rep_categorias.excluir_categoria(id_categoria)

    return jsonify({
        "mensagem": "Categoria excluída com sucesso."
    }), 200