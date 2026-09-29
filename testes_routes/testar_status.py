import requests


BASE_URL = "http://127.0.0.1:5000"


# =========================================================
# STATUS DE CLIENTES
# =========================================================

print("\n--- STATUS DE CLIENTES ---")

resposta = requests.get(
    f"{BASE_URL}/status/clientes/"
)
print("GET:", resposta.status_code)
print(resposta.json())


dados = {
    "nome": "Cliente Novo"
}

resposta = requests.post(
    f"{BASE_URL}/status/clientes/",
    json=dados
)
print("POST:", resposta.status_code)
print(resposta.json())

id_status_cliente = resposta.json()["id"]


dados = {
    "nome": "Cliente Ativo"
}

resposta = requests.put(
    f"{BASE_URL}/status/clientes/{id_status_cliente}",
    json=dados
)
print("PUT:", resposta.status_code)
print(resposta.json())


resposta = requests.delete(
    f"{BASE_URL}/status/clientes/{id_status_cliente}"
)
print("DELETE:", resposta.status_code)
print(resposta.json())


# =========================================================
# STATUS DE LEADS
# =========================================================

print("\n--- STATUS DE LEADS ---")

resposta = requests.get(
    f"{BASE_URL}/status/leads/"
)
print("GET:", resposta.status_code)
print(resposta.json())


dados = {
    "nome": "Lead Novo"
}

resposta = requests.post(
    f"{BASE_URL}/status/leads/",
    json=dados
)
print("POST:", resposta.status_code)
print(resposta.json())

id_status_lead = resposta.json()["id"]


dados = {
    "nome": "Lead Contatado"
}

resposta = requests.put(
    f"{BASE_URL}/status/leads/{id_status_lead}",
    json=dados
)
print("PUT:", resposta.status_code)
print(resposta.json())


resposta = requests.delete(
    f"{BASE_URL}/status/leads/{id_status_lead}"
)
print("DELETE:", resposta.status_code)
print(resposta.json())


# =========================================================
# STATUS DE PROJETOS
# =========================================================

print("\n--- STATUS DE PROJETOS ---")

resposta = requests.get(
    f"{BASE_URL}/status/projetos/"
)
print("GET:", resposta.status_code)
print(resposta.json())


dados = {
    "nome": "Projeto Novo"
}

resposta = requests.post(
    f"{BASE_URL}/status/projetos/",
    json=dados
)
print("POST:", resposta.status_code)
print(resposta.json())

id_status_projeto = resposta.json()["id"]


dados = {
    "nome": "Projeto Em Andamento"
}

resposta = requests.put(
    f"{BASE_URL}/status/projetos/{id_status_projeto}",
    json=dados
)
print("PUT:", resposta.status_code)
print(resposta.json())


resposta = requests.delete(
    f"{BASE_URL}/status/projetos/{id_status_projeto}"
)
print("DELETE:", resposta.status_code)
print(resposta.json())