import threading
import time
from collections import defaultdict, deque

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from repositories import rep_admin


login_bp = Blueprint("login", __name__, url_prefix="/login")

MAX_FALHAS = 5            # senhas erradas permitidas por IP
JANELA_SEGUNDOS = 15 * 60 # e quanto tempo elas contam

_falhas = defaultdict(deque)
_trava = threading.Lock()

# Hash de mentira: usuário inexistente gasta o mesmo tempo que senha errada,
# então o tempo de resposta não revela se o usuário existe.
_HASH_FALSO = generate_password_hash("senha-falsa-para-igualar-tempo")


def _segundos_bloqueado(ip):
    """0 se pode tentar; senão, quantos segundos faltam."""
    agora = time.monotonic()
    with _trava:
        fila = _falhas[ip]
        while fila and agora - fila[0] > JANELA_SEGUNDOS:
            fila.popleft()
        if len(fila) >= MAX_FALHAS:
            return int(JANELA_SEGUNDOS - (agora - fila[0])) + 1
        return 0


def _registrar_falha(ip):
    with _trava:
        _falhas[ip].append(time.monotonic())


def _limpar_falhas(ip):
    with _trava:
        _falhas.pop(ip, None)


@login_bp.route("/", methods=["POST"])
def login():
    ip = request.remote_addr

    espera = _segundos_bloqueado(ip)
    if espera:
        resposta = jsonify({
            "erro": "Muitas tentativas. Tente novamente em alguns minutos."
        })
        resposta.headers["Retry-After"] = str(espera)
        return resposta, 429

    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados obrigatórios."}), 400

    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if not isinstance(usuario, str) or not isinstance(senha, str) \
            or not usuario or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios."}), 400

    admin = rep_admin.buscar_por_usuario(usuario)

    if admin is None:
        check_password_hash(_HASH_FALSO, senha)
        senha_ok = False
    else:
        senha_ok = rep_admin.validar_senha(admin, senha)

    # mesma resposta para usuário inexistente, senha errada ou conta inativa
    if admin is None or not senha_ok or not admin.ativo:
        _registrar_falha(ip)
        return jsonify({"erro": "Usuário ou senha inválidos."}), 401

    _limpar_falhas(ip)
    session.clear()
    session.permanent = True
    session["id_admin"] = admin.id

    return jsonify({
        "mensagem": "Login realizado com sucesso.",
        "usuario": admin.usuario
    }), 200


@login_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensagem": "Logout realizado com sucesso."}), 200