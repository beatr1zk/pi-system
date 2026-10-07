from models.contato import Contato


class Cliente(Contato):
    def __init__(self, nome, email, telefone, cpf, detalhes, status_id):
        super().__init__(nome, email, telefone)
        self._cpf = cpf
        self.detalhes = detalhes
        self.status_id = status_id
        self.data_atualizacao = None

    @property
    def cpf(self):
        return self._cpf

    def resumo(self):
        return f"Cliente: {self.nome} (CPF {self._cpf})"