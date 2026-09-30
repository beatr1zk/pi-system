from datetime import date, datetime

from flask import Blueprint, request, jsonify

from utils.autenticacao import login_required

from repositories import rep_projetos
from models.projeto import Projeto


projeto_bp = Blueprint("projeto", __name__, url_prefix="/projetos")

CAMPOS_DATA = ("data_pedido", "data_entrega", "data_conclusao")
CAMPOS_ID = ("cliente_id", "categoria_id", "prioridade_id", "status_id")
NAO_NULOS = ("nome", "cliente_id", "categoria_id")


def _iso(valor):
    return valor.isoformat() if hasattr(valor, "isoformat") else valor


def projeto_para_dict(projeto):
    return {
        "id": projeto.id,
        "cliente_id": projeto.cliente_id,
        "categoria_id": projeto.categoria_id,
        "nome": projeto.nome,
        "escopo": projeto.escopo,
        "servico": projeto.servico,
        "url_proposta": projeto.url_proposta,
        "data_pedido": _iso(projeto.data_pedido),
        "data_entrega": _iso(projeto.data_entrega),
        "data_conclusao": _iso(projeto.data_conclusao),
        "prioridade_id": projeto.prioridade_id,
        "status_id": projeto.status_id,
    }


def _validar(dados):
    """Valida apenas os campos presentes em 'dados'.
    Retorna uma mensagem de erro, ou None se estiver tudo certo."""

    for campo in CAMPOS_DATA:               # "" (formulário vazio) vira None
        if dados.get(campo) == "":
            dados[campo] = None

    for campo in NAO_NULOS:
        if campo in dados and dados[campo] in (None, ""):
            return f"O campo '{campo}' não pode ser vazio."

    if "nome" in dados:
        nome = dados["nome"]
        if not isinstance(nome, str) or not nome.strip() or len(nome) > 150:
            return "O nome deve ser um texto de 1 a 150 caracteres."
        dados["nome"] = nome.strip()

    if dados.get("servico") is not None:
        if not isinstance(dados["servico"], str) or len(dados["servico"]) > 100:
            return "O serviço deve ser um texto de até 100 caracteres."

    if dados.get("escopo") is not None and not isinstance(dados["escopo"], str):
        return "O escopo deve ser um texto."

    url = dados.get("url_proposta")
    if url is not None:
        if (not isinstance(url, str) or len(url) > 255
                or not url.lower().startswith(("http://", "https://"))):
            return "A URL da proposta deve começar com http:// ou https://."

    for campo in CAMPOS_ID:
        valor = dados.get(campo)
        if valor is not None and (not isinstance(valor, int) or isinstance(valor, bool)):
            return f"O campo '{campo}' deve ser um número inteiro."

    for campo in CAMPOS_DATA:
        valor = dados.get(campo)
        if valor is None:
            continue
        try:
            if campo == "data_pedido":
                datetime.fromisoformat(valor)
            else:
                date.fromisoformat(valor)
        except (TypeError, ValueError):
            formato = "AAAA-MM-DD" + (" ou AAAA-MM-DDTHH:MM:SS" if campo == "data_pedido" else "")
            return f"O campo '{campo}' deve estar no formato {formato}."

    return None


# ============================================================
# LISTAR / BUSCAR / PESQUISAR
# ============================================================

@projeto_bp.route("/", methods=["GET"])
@login_required
def listar_projetos():
    projetos = rep_projetos.listar_projetos()
    return jsonify([projeto_para_dict(p) for p in projetos]), 200


@projeto_bp.route("/<int:id_projeto>", methods=["GET"])
@login_required
def buscar_projeto(id_projeto):
    projeto = rep_projetos.buscar_por_id(id_projeto)
    if projeto is None:
        return jsonify({"erro": "Projeto não encontrado."}), 404
    return jsonify(projeto_para_dict(projeto)), 200


@projeto_bp.route("/pesquisar", methods=["GET"])
@login_required
def pesquisar_projetos():
    termo = request.args.get("termo", "").strip()
    if not termo:
        return jsonify({"erro": "O termo de pesquisa é obrigatório."}), 400

    projetos = rep_projetos.pesquisar_projetos(termo)
    return jsonify([projeto_para_dict(p) for p in projetos]), 200


# ============================================================
# CRIAR
# ============================================================

@projeto_bp.route("/", methods=["POST"])
@login_required
def criar_projeto():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or not dados:
        return jsonify({"erro": "Os dados do projeto são obrigatórios."}), 400

    for campo in NAO_NULOS:
        if not dados.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

    erro = _validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    projeto = Projeto(
        cliente_id=dados["cliente_id"],
        categoria_id=dados["categoria_id"],
        nome=dados["nome"],
        escopo=dados.get("escopo"),
        servico=dados.get("servico"),
        data_pedido=dados.get("data_pedido"),
        data_entrega=dados.get("data_entrega"),
        data_conclusao=dados.get("data_conclusao"),
        prioridade_id=dados.get("prioridade_id"),
        status_id=dados.get("status_id") or 1,
        url_proposta=dados.get("url_proposta"),
    )

    projeto = rep_projetos.criar_projeto(projeto)
    # Relê do banco para devolver data_pedido já preenchida pelo MySQL
    projeto = rep_projetos.buscar_por_id(projeto.id)
    return jsonify(projeto_para_dict(projeto)), 201


# ============================================================
# ATUALIZAR
# ============================================================

@projeto_bp.route("/<int:id_projeto>", methods=["PUT"])
@login_required
def atualizar_projeto(id_projeto):
    projeto = rep_projetos.buscar_por_id(id_projeto)
    if projeto is None:
        return jsonify({"erro": "Projeto não encontrado."}), 404

    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or not dados:
        return jsonify({"erro": "Os dados para atualização são obrigatórios."}), 400

    erro = _validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    for campo in ("cliente_id", "categoria_id", "nome", "escopo", "servico",
                  "url_proposta", "data_pedido", "data_entrega",
                  "data_conclusao", "prioridade_id", "status_id"):
        if campo in dados:
            setattr(projeto, campo, dados[campo])

    rep_projetos.atualizar_projeto(projeto)
    projeto = rep_projetos.buscar_por_id(id_projeto)
    return jsonify(projeto_para_dict(projeto)), 200


# ============================================================
# EXCLUIR
# ============================================================

@projeto_bp.route("/<int:id_projeto>", methods=["DELETE"])
@login_required
def excluir_projeto(id_projeto):
    if rep_projetos.buscar_por_id(id_projeto) is None:
        return jsonify({"erro": "Projeto não encontrado."}), 404

    rep_projetos.excluir_projeto(id_projeto)
    return jsonify({"mensagem": "Projeto excluído com sucesso."}), 200