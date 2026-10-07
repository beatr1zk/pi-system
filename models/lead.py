from models.contato import Contato

class Lead(Contato):
    def __init__(self, nome, email, telefone, servico, mensagem, status_id, cliente_id):
        super().__init__(nome, email, telefone)
        self.servico = servico
        self.mensagem = mensagem
        self.status_id = status_id
        self.cliente_id = cliente_id
        
    def resumo(self):
        return f"Lead: {self.nome} (interesse em {self.servico})"