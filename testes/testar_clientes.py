import requests

url = "http://127.0.0.1:5000/clientes/1"

resposta = requests.delete(url)

print("Status:", resposta.status_code)
print("Resposta:")
print(resposta.json())