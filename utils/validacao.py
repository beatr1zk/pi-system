import re

def ler_nome(dados, limite=50):
    """Retorna (nome_limpo, None) ou (None, mensagem_de_erro)."""
    if not isinstance(dados, dict) or not dados:
        return None, "Os dados são obrigatórios."

    nome = dados.get("nome")
    if not isinstance(nome, str) or not nome.strip():
        return None, "O campo 'nome' é obrigatório."

    nome = nome.strip()
    if len(nome) > limite:
        return None, f"O nome deve ter no máximo {limite} caracteres."

    return nome, None

    
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CPF_RE = re.compile(r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$")


def limpar_texto(dados, campo, limite, obrigatorio=False):
    """Valida e normaliza dados[campo], se presente. Retorna erro ou None."""
    if campo not in dados:
        return None
    valor = dados[campo]
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        if obrigatorio:
            return f"O campo '{campo}' não pode ser vazio."
        dados[campo] = None
        return None
    if not isinstance(valor, str):
        return f"O campo '{campo}' deve ser um texto."
    valor = valor.strip()
    if limite and len(valor) > limite:
        return f"O campo '{campo}' deve ter no máximo {limite} caracteres."
    dados[campo] = valor
    return None


def _regras(dados, regras):
    for campo, limite, obrigatorio in regras:
        erro = limpar_texto(dados, campo, limite, obrigatorio)
        if erro:
            return erro
    return None


def _inteiros(dados, campos):
    for campo in campos:
        valor = dados.get(campo)
        if valor is not None and (not isinstance(valor, int) or isinstance(valor, bool)):
            return f"O campo '{campo}' deve ser um número inteiro."
    return None


def validar_cliente(dados, criando):
    if not isinstance(dados, dict) or not dados:
        return "Os dados são obrigatórios."
    if criando:
        for campo in ("nome", "email"):
            if campo not in dados:
                return f"O campo '{campo}' é obrigatório."

    erro = _regras(dados, [
        ("nome", 100, True), ("email", 150, True),
        ("telefone", 20, False), ("cpf", 14, False), ("detalhes", 5000, False),
    ])
    if erro:
        return erro

    if dados.get("email") and not EMAIL_RE.match(dados["email"]):
        return "E-mail inválido."
    if dados.get("cpf") and not CPF_RE.match(dados["cpf"]):
        return "CPF inválido. Use 000.000.000-00 ou 11 dígitos."
    if "status_id" in dados and dados["status_id"] is None and not criando:
        return "O campo 'status_id' não pode ser nulo."
    return _inteiros(dados, ["status_id"])


def validar_lead(dados, criando):
    if not isinstance(dados, dict) or not dados:
        return "Os dados são obrigatórios."
    if criando:
        for campo in ("nome", "servico"):
            if campo not in dados:
                return f"O campo '{campo}' é obrigatório."

    erro = _regras(dados, [
        ("nome", 100, True), ("servico", 100, True), ("email", 150, False),
        ("telefone", 20, False), ("mensagem", 5000, False),
    ])
    if erro:
        return erro

    if dados.get("email") and not EMAIL_RE.match(dados["email"]):
        return "E-mail inválido."
    if "status_id" in dados and dados["status_id"] is None and not criando:
        return "O campo 'status_id' não pode ser nulo."
    return _inteiros(dados, ["status_id", "cliente_id"])