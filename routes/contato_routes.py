import re
import threading
import time
from collections import defaultdict, deque

from flask import Blueprint, request, jsonify

from utils.validacao import limpar_texto, EMAIL_RE

from repositories import rep_leads
from models.lead import Lead


contato_bp = Blueprint("contato", __name__, url_prefix="/contato")

# Os mesmos valores do <select> do index.html
SERVICOS = {"identidade-visual", "design-grafico", "ui-ux",
            "desenvolvimento-web", "outro"}

TELEFONE_RE = re.compile(r"^[0-9+()\-\s]{8,20}$")

LIMITE_ENVIOS = 5        # por IP
JANELA_SEGUNDOS = 3600   # por hora

_envios = defaultdict(deque)
_trava = threading.Lock()


def _excedeu_limite(ip):
    agora = time.monotonic()
    with _trava:
        fila = _envios[ip]
        while fila and agora - fila[0] > JANELA_SEGUNDOS:
            fila.popleft()
        if len(fila) >= LIMITE_ENVIOS:
            return True
        fila.append(agora)
        return False


def _ler_corpo():
    dados = request.get_json(silent=True)
    if isinstance(dados, dict):
        return dados
    return request.form.to_dict()


@contato_bp.route("/", methods=["POST"])
def enviar_contato():
    corpo = _ler_corpo()

    # Honeypot: campo escondido que só robôs preenchem.
    # Responde como se tivesse dado certo, para o robô não perceber.
    if corpo.get("website"):
        return jsonify({"mensagem": "Mensagem enviada. Obrigada pelo contato!"}), 201

    if _excedeu_limite(request.remote_addr):
        return jsonify({"erro": "Muitas tentativas. Tente novamente mais tarde."}), 429

    # Só os 5 campos do formulário; qualquer outro (status_id, cliente_id...) é ignorado
    dados = {c: corpo.get(c) for c in ("nome", "email", "telefone", "servico", "mensagem")}

    for campo, limite, obrigatorio in (
        ("nome", 100, True),
        ("email", 150, True),
        ("telefone", 20, False),
        ("servico", 100, True),
        ("mensagem", 2000, True),
    ):
        erro = limpar_texto(dados, campo, limite, obrigatorio)
        if erro:
            return jsonify({"erro": erro}), 400

    if not EMAIL_RE.match(dados["email"]):
        return jsonify({"erro": "E-mail inválido."}), 400
    if dados["telefone"] and not TELEFONE_RE.match(dados["telefone"]):
        return jsonify({"erro": "Telefone inválido."}), 400
    if dados["servico"] not in SERVICOS:
        return jsonify({"erro": "Serviço inválido."}), 400

    # status_id None -> "Novo" (id 1); cliente_id sempre None
    lead = Lead(
        nome=dados["nome"],
        email=dados["email"],
        telefone=dados["telefone"],
        servico=dados["servico"],
        mensagem=dados["mensagem"],
        status_id=None,
        cliente_id=None,
    )
    rep_leads.criar_lead(lead)

    # Não devolve o id nem nada do banco
    return jsonify({"mensagem": "Mensagem enviada. Obrigada pelo contato!"}), 201