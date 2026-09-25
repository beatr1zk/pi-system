class Lead:
    def __init__(self, nome, email, telefone, servico, mensagem, status, cliente_id):
        self.id = None
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.servico = servico
        self.mensagem = mensagem
        self.status = status
        self.data_cadastro = None
        self.cliente_id = cliente_id