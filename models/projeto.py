class Projeto:
    def __init__(self, cliente_id, categoria_id, nome, escopo, data_pedido, data_entrega, prioridade, status):
        self.id = None
        self.cliente_id = cliente_id
        self.categoria_id = categoria_id
        self.nome = nome
        self.escopo = escopo
        self.data_pedido = data_pedido
        self.data_entrega = data_entrega
        self.prioridade = prioridade
        self.status = status