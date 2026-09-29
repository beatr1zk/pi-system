import requests

dados = {
    "nome": "Lead Atualizado",
    "servico": "Design de Marca",
    "mensagem": "Mensagem atualizada"
}

resposta = requests.put(
    "http://127.0.0.1:5000/leads/1",
    json=dados
)

import requests

resposta = requests.delete(
    "http://127.0.0.1:5000/leads/1"
)
resposta = requests.delete(
    "http://127.0.0.1:5000/leads/2"
)

print(resposta.status_code)
print(resposta.json())
