class Lead:
    def __init__(self, nome, email, telefone, servico, mensagem, status_id, cliente_id):
        self.id = None
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.servico = servico
        self.mensagem = mensagem
        self.status_id = status_id
        self.data_cadastro = None
        self.cliente_id = cliente_id