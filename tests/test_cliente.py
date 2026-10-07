from models.contato import Contato
from models.cliente import Cliente

def test_cliente_e_contato():
    cliente = Cliente("Ana", "ana@x.com", "4199999", "123.456.789-00", "VIP", 1)
    assert isinstance(cliente, Contato)
    assert cliente.nome == "Ana"
    assert cliente._cpf == "123.456.789-00"
    assert cliente.cpf == "123.456.789-00"
    assert cliente.detalhes == "VIP"

def test_resumo_do_cliente():
    cliente = Cliente("Ana", "ana@x.com", "4199999", "123.456.789-00", "VIP", 1)
    assert cliente.resumo() == "Cliente: Ana (CPF 123.456.789-00)"