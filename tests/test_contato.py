 
from models.contato import Contato

def test_contato_guarda_dados():
    contato = Contato("Ana", "ana@x.com", "4199999")
    assert contato.nome == "Ana"
    assert contato.email == "ana@x.com"
    assert contato.id is None

def test_resumo_do_contato():
    contato = Contato("Ana", "ana@x.com", "4199999")
    assert contato.resumo() == "Ana > ana@x.com"