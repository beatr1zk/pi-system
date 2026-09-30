from functools import wraps
from flask import session, jsonify


def login_required(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if "id_admin" not in session:
            return jsonify({
                "erro": "Usuário não autenticado."
            }), 401

        return funcao(*args, **kwargs)
    
    return verificar