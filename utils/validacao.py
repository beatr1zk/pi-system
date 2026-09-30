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