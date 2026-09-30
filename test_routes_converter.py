import requests


BASE_URL = "http://127.0.0.1:5000"


def criar_lead():
    url = f"{BASE_URL}/leads/"

    dados = {
        "nome": "João Teste",
        "email": "joao.teste@email.com",
        "telefone": "41999999999",
        "servico": "Identidade Visual",
        "mensagem": "Gostaria de orçamento para criação de marca"
    }

    resposta = requests.post(url, json=dados)

    print("\nCRIAR LEAD")
    print(resposta.status_code)
    print(resposta.json())

    return resposta.json()["id"]


def buscar_lead(id_lead):
    url = f"{BASE_URL}/leads/{id_lead}"

    resposta = requests.get(url)

    print("\nBUSCAR LEAD")
    print(resposta.status_code)
    print(resposta.json())


def converter_lead(id_lead):
    url = f"{BASE_URL}/leads/{id_lead}/converter"

    dados = {
        "cpf": "12345678900",
        "detalhes": "Cliente convertido através do formulário de contato"
    }

    resposta = requests.post(url, json=dados)

    print("\nCONVERTER LEAD")
    print(resposta.status_code)
    print(resposta.json())


def buscar_lead_convertido(id_lead):
    url = f"{BASE_URL}/leads/{id_lead}"

    resposta = requests.get(url)

    print("\nVERIFICAR LEAD CONVERTIDO")
    print(resposta.status_code)
    print(resposta.json())


def converter_lead_novamente(id_lead):
    url = f"{BASE_URL}/leads/{id_lead}/converter"

    resposta = requests.post(url, json={})

    print("\nTENTAR CONVERTER NOVAMENTE")
    print(resposta.status_code)
    print(resposta.json())


def main():

    print("INICIANDO TESTE DE CONVERSÃO LEAD → CLIENTE")

    id_lead = criar_lead()

    buscar_lead(id_lead)

    converter_lead(id_lead)

    buscar_lead_convertido(id_lead)

    converter_lead_novamente(id_lead)


if __name__ == "__main__":
    main()