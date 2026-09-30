from werkzeug.security import generate_password_hash


class Admin:
    def __init__(self, usuario, senha):

        self.id = None
        self.usuario = usuario
        self.senha = generate_password_hash(senha)
        self.ativo = True