import requests

BASE = "http://127.0.0.1:5000"
s = requests.Session()


def mostrar(titulo, r):
    print(f"{titulo:<42} {r.status_code}  {r.text.strip()[:400]}")


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
print("--- login ---")
mostrar("GET /categorias/ sem login (401)", requests.get(f"{BASE}/categorias/"))

usuario = input("Usuário: ")
senha = input("Senha: ")

mostrar("POST /login/ (200)", s.post(f"{BASE}/login/", json={"usuario": usuario, "senha": senha}))
mostrar("POST /login/ senha errada (401)", requests.post(f"{BASE}/login/", json={"usuario": usuario, "senha": "errada"}))
mostrar("POST /login/ usuario não texto (400)", requests.post(f"{BASE}/login/", json={"usuario": {"a": 1}, "senha": "x"}))

# ---------------------------------------------------------
# CATEGORIAS / PRIORIDADES / STATUS
# ---------------------------------------------------------
print("\n--- categorias / prioridades / status ---")
mostrar("GET /categorias/ (200)", s.get(f"{BASE}/categorias/"))

r = s.post(f"{BASE}/categorias/", json={"nome": "Categoria Teste"})
mostrar("POST categoria (201)", r)
cat_id = r.json().get("id")

mostrar("POST duplicada (409)", s.post(f"{BASE}/categorias/", json={"nome": "Categoria Teste"}))
mostrar("POST nome vazio (400)", s.post(f"{BASE}/categorias/", json={"nome": "  "}))
mostrar("POST nome numérico (400)", s.post(f"{BASE}/categorias/", json={"nome": 123}))
mostrar("POST nome longo (400)", s.post(f"{BASE}/categorias/", json={"nome": "x" * 200}))
mostrar("PUT inexistente (404)", s.put(f"{BASE}/categorias/9999", json={"nome": "A"}))
mostrar("PUT categoria (200)", s.put(f"{BASE}/categorias/{cat_id}", json={"nome": "Categoria Teste 2"}))
mostrar("DELETE categoria (200)", s.delete(f"{BASE}/categorias/{cat_id}"))

mostrar("GET /prioridades/ (200)", s.get(f"{BASE}/prioridades/"))
mostrar("GET /status/projetos/ (200)", s.get(f"{BASE}/status/projetos/"))
mostrar("GET /status/clientes/ (200)", s.get(f"{BASE}/status/clientes/"))
mostrar("GET /status/leads/ (200)", s.get(f"{BASE}/status/leads/"))
mostrar("DELETE status padrão (409)", s.delete(f"{BASE}/status/projetos/1"))

# ---------------------------------------------------------
# CLIENTES / PROJETOS / LEADS
# ---------------------------------------------------------
print("\n--- clientes / projetos / leads ---")

r = s.post(f"{BASE}/clientes/", json={"nome": "Cliente Teste", "email": "teste@exemplo.com",
                                      "cpf": "123.456.789-09", "status_id": 2})
mostrar("POST cliente (201, status_id 2)", r)
cid = r.json().get("id")

mostrar("GET lista: CPF mascarado", s.get(f"{BASE}/clientes/"))
mostrar("GET detalhe: CPF completo", s.get(f"{BASE}/clientes/{cid}"))
mostrar("POST e-mail inválido (400)", s.post(f"{BASE}/clientes/", json={"nome": "X", "email": "abc"}))
mostrar("POST CPF inválido (400)", s.post(f"{BASE}/clientes/", json={"nome": "X", "email": "a@b.com", "cpf": "123"}))
mostrar("POST status_id inexistente (409)", s.post(f"{BASE}/clientes/", json={"nome": "X", "email": "a@b.com", "status_id": 999}))
mostrar("PUT nome null (400)", s.put(f"{BASE}/clientes/{cid}", json={"nome": None}))

r = s.post(f"{BASE}/projetos/", json={"cliente_id": cid, "categoria_id": 1, "nome": "Projeto Teste",
                                      "servico": "Identidade visual",
                                      "escopo": "Logo, paleta e manual de marca completo"})
mostrar("POST projeto (201)", r)
pid = r.json().get("id")
print("   data_pedido preenchida?", bool(r.json().get("data_pedido")))
mostrar("GET projeto (servico/escopo certos?)", s.get(f"{BASE}/projetos/{pid}"))
mostrar("PUT projeto (200)", s.put(f"{BASE}/projetos/{pid}", json={"nome": "Projeto Teste 2"}))
mostrar("GET após PUT (continuam certos?)", s.get(f"{BASE}/projetos/{pid}"))
mostrar("POST cliente_id inexistente (409)", s.post(f"{BASE}/projetos/", json={"cliente_id": 9999, "categoria_id": 1, "nome": "X"}))
mostrar("POST url javascript: (400)", s.post(f"{BASE}/projetos/", json={"cliente_id": cid, "categoria_id": 1, "nome": "X", "url_proposta": "javascript:alert(1)"}))
mostrar("DELETE cliente com projeto (409)", s.delete(f"{BASE}/clientes/{cid}"))

r = s.post(f"{BASE}/leads/", json={"nome": "Lead Teste", "servico": "identidade-visual"})
mostrar("POST lead sem e-mail (201)", r)
lid = r.json().get("id")
mostrar("Converter sem e-mail (400)", s.post(f"{BASE}/leads/{lid}/converter", json={}))

r = s.post(f"{BASE}/leads/{lid}/converter", json={"email": "lead@exemplo.com"})
mostrar("Converter com e-mail (201)", r)
novo_cid = r.json().get("cliente_id")

mostrar("Converter de novo (409)", s.post(f"{BASE}/leads/{lid}/converter", json={"email": "lead@exemplo.com"}))
mostrar("GET lead (status_id 3 e cliente_id?)", s.get(f"{BASE}/leads/{lid}"))

# ---------------------------------------------------------
# LIMPEZA
# ---------------------------------------------------------
s.delete(f"{BASE}/projetos/{pid}")
s.delete(f"{BASE}/leads/{lid}")
s.delete(f"{BASE}/clientes/{novo_cid}")
s.delete(f"{BASE}/clientes/{cid}")
print("\n--- limpeza ---")
print("Limpeza feita.")

# ---------------------------------------------------------
# CONTATO PÚBLICO (sem login)
# ---------------------------------------------------------
print("\n--- contato público (sem login) ---")
pub = {"nome": "Contato Teste", "email": "c@exemplo.com", "servico": "ui-ux", "mensagem": "Olá!"}
mostrar("POST contato válido (201)", requests.post(f"{BASE}/contato/", json=pub))
mostrar("POST honeypot (201, não salva)", requests.post(f"{BASE}/contato/", json={**pub, "nome": "Robo Teste", "website": "x"}))
mostrar("POST serviço inválido (400)", requests.post(f"{BASE}/contato/", json={**pub, "servico": "hack"}))
mostrar("POST e-mail inválido (400)", requests.post(f"{BASE}/contato/", json={**pub, "email": "abc"}))
mostrar("POST tenta forçar status_id (201, ignorado)", requests.post(f"{BASE}/contato/", json={**pub, "status_id": 3, "cliente_id": 1}))
mostrar("POST corpo grande (413)", requests.post(f"{BASE}/contato/", json={**pub, "mensagem": "x" * 20000}))

r = s.get(f"{BASE}/leads/pesquisar", params={"termo": "Contato Teste"})
for l in r.json():
    print("   lead salvo: status_id", l["status_id"], "cliente_id", l["cliente_id"])
    s.delete(f"{BASE}/leads/{l['id']}")
print("   'Robo Teste' salvo?", bool(s.get(f"{BASE}/leads/pesquisar", params={"termo": "Robo Teste"}).json()))

# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------
mostrar("POST /login/logout (200)", s.post(f"{BASE}/login/logout"))
mostrar("GET /categorias/ após logout (401)", s.get(f"{BASE}/categorias/"))