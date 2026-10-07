
from utils.validacao import validar_cliente


def test_email_curto_demais_e_rejeitado():
    dados = {"nome": "Ana", "email": "ab"}
    erro = validar_cliente(dados, criando=True)
    assert erro  


def test_dados_validos_nao_geram_erro():
    dados = {"nome": "Ana", "email": "ana@x.com"}
    erro = validar_cliente(dados, criando=True)
    assert not erro