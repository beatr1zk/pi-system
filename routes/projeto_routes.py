from flask import Blueprint, request, jsonify

from repositories import rep_projetos
from models.projeto import Projeto


projeto_bp = Blueprint(
    "projeto",
    __name__,
    url_prefix="/projetos"
)


def projeto_para_dict(projeto):
    return {
        "id": projeto.id,
        "cliente_id": projeto.cliente_id,
        "categoria_id": projeto.categoria_id,
        "nome": projeto.nome,
        "escopo": projeto.escopo,

        "data_pedido": (
            projeto.data_pedido.isoformat()
            if hasattr(projeto.data_pedido, "isoformat")
            else projeto.data_pedido
        ),

        "data_entrega": (
            projeto.data_entrega.isoformat()
            if hasattr(projeto.data_entrega, "isoformat")
            else projeto.data_entrega
        ),

        "data_conclusao": (
            projeto.data_conclusao.isoformat()
            if hasattr(projeto.data_conclusao, "isoformat")
            else projeto.data_conclusao
        ),

        "prioridade_id": projeto.prioridade_id,
        "status_id": projeto.status_id
    }


# ============================================================
# LISTAR PROJETOS
# ============================================================

@projeto_bp.route("/", methods=["GET"])
def listar_projetos():

    projetos = rep_projetos.listar_projetos()

    return jsonify([
        projeto_para_dict(projeto)
        for projeto in projetos
    ]), 200


# ============================================================
# BUSCAR PROJETO POR ID
# ============================================================

@projeto_bp.route("/<int:id_projeto>", methods=["GET"])
def buscar_projeto(id_projeto):

    projeto = rep_projetos.buscar_por_id(id_projeto)

    if projeto is None:
        return jsonify({
            "erro": "Projeto não encontrado."
        }), 404

    return jsonify(
        projeto_para_dict(projeto)
    ), 200


# ============================================================
# PESQUISAR PROJETOS
# ============================================================

@projeto_bp.route("/pesquisar", methods=["GET"])
def pesquisar_projetos():

    termo = request.args.get("termo", "").strip()

    if not termo:
        return jsonify({
            "erro": "O termo de pesquisa é obrigatório."
        }), 400

    projetos = rep_projetos.pesquisar_projetos(termo)

    return jsonify([
        projeto_para_dict(projeto)
        for projeto in projetos
    ]), 200


# ============================================================
# CRIAR PROJETO
# ============================================================

@projeto_bp.route("/", methods=["POST"])
def criar_projeto():

    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados do projeto são obrigatórios."
        }), 400

    campos_obrigatorios = [
        "cliente_id",
        "categoria_id",
        "nome"
    ]

    for campo in campos_obrigatorios:

        if not dados.get(campo):
            return jsonify({
                "erro": f"O campo '{campo}' é obrigatório."
            }), 400

    projeto = Projeto(
        dados["cliente_id"],
        dados["categoria_id"],
        dados["nome"],
        dados.get("escopo"),
        dados.get("data_pedido"),
        dados.get("data_entrega"),
        dados.get("data_conclusao"),
        dados.get("prioridade_id"),
        dados.get("status_id")
    )

    projeto = rep_projetos.criar_projeto(projeto)

    return jsonify(
        projeto_para_dict(projeto)
    ), 201


# ============================================================
# ATUALIZAR PROJETO
# ============================================================

@projeto_bp.route("/<int:id_projeto>", methods=["PUT"])
def atualizar_projeto(id_projeto):

    projeto_existente = rep_projetos.buscar_por_id(
        id_projeto
    )

    if projeto_existente is None:
        return jsonify({
            "erro": "Projeto não encontrado."
        }), 404

    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Os dados para atualização são obrigatórios."
        }), 400

    projeto_existente.cliente_id = dados.get(
        "cliente_id",
        projeto_existente.cliente_id
    )

    projeto_existente.categoria_id = dados.get(
        "categoria_id",
        projeto_existente.categoria_id
    )

    projeto_existente.nome = dados.get(
        "nome",
        projeto_existente.nome
    )

    projeto_existente.escopo = dados.get(
        "escopo",
        projeto_existente.escopo
    )

    projeto_existente.data_pedido = dados.get(
        "data_pedido",
        projeto_existente.data_pedido
    )

    projeto_existente.data_entrega = dados.get(
        "data_entrega",
        projeto_existente.data_entrega
    )

    projeto_existente.data_conclusao = dados.get(
        "data_conclusao",
        projeto_existente.data_conclusao
    )

    projeto_existente.prioridade_id = dados.get(
        "prioridade_id",
        projeto_existente.prioridade_id
    )

    projeto_existente.status_id = dados.get(
        "status_id",
        projeto_existente.status_id
    )

    rep_projetos.atualizar_projeto(
        projeto_existente
    )

    projeto_atualizado = rep_projetos.buscar_por_id(
        id_projeto
    )

    return jsonify(
        projeto_para_dict(projeto_atualizado)
    ), 200


# ============================================================
# EXCLUIR PROJETO
# ============================================================

@projeto_bp.route("/<int:id_projeto>", methods=["DELETE"])
def excluir_projeto(id_projeto):

    projeto = rep_projetos.buscar_por_id(
        id_projeto
    )

    if projeto is None:
        return jsonify({
            "erro": "Projeto não encontrado."
        }), 404

    rep_projetos.excluir_projeto(
        id_projeto
    )

    return jsonify({
        "mensagem": "Projeto excluído com sucesso."
    }), 200