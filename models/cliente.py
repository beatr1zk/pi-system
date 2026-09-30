class Cliente:
    def __init__( self, nome, email, telefone, cpf, servico, detalhes, status_id):
        self.id = None
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self._cpf = cpf
        self.servico = servico
        self.detalhes = detalhes
        self.status_id = status_id
        self.data_cadastro = None
        self.data_atualizacao = None