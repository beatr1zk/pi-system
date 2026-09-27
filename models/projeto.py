class Projeto:
    def __init__(self, cliente_id, categoria_id, nome, escopo, data_pedido, data_entrega, data_conclusao, prioridade_id, status_id):
        self.id = None
        self.cliente_id = cliente_id
        self.categoria_id = categoria_id
        self.nome = nome
        self.escopo = escopo
        self.data_pedido = data_pedido
        self.data_entrega = data_entrega
        self.data_conclusao = data_conclusao
        self.prioridade_id = prioridade_id
        self.status_id = status_id