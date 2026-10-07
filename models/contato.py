class Contato:
    def __init__(self, nome, email, telefone):
        self.id = None
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.data_cadastro = None

    def resumo(self):
        return f"{self.nome} > {self.email}"