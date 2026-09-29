import requests

dados = {
    "nome": "Identidade Visual"
}

# resposta = requests.post(
#     "http://127.0.0.1:5000/categorias/",
#     json=dados
# )


# dados = {
#     "nome": "Design Editorial"
# }

# resposta = requests.put(
#     "http://127.0.0.1:5000/categorias/1",
#     json=dados
# )


resposta = requests.delete(
    "http://127.0.0.1:5000/categorias/1"
)

print(resposta.status_code)
print(resposta.json())