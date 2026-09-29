import requests

dados = {
    "nome": "Teste"
}

# resposta = requests.post(
#     "http://127.0.0.1:5000/prioridades/",
#     json=dados
# )


# dados = {
#     "nome": "Design Editorial"
# }

# resposta = requests.put(
#     "http://127.0.0.1:5000/prioridades/1",
#     json=dados
# )


resposta = requests.delete(
    "http://127.0.0.1:5000/prioridades/1"
)

print(resposta.status_code)
print(resposta.json())