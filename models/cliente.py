class Cliente:
    def __init__(self, nome, email, telefone, cpf, servico, detalhes, url_proposta, status):
        self.id = None
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self._cpf = cpf
        self.servico = servico
        self.detalhes = detalhes
        self.url_proposta = url_proposta
        self.status = status
        self.data_cadastro = None
        self.data_atualizacao = None