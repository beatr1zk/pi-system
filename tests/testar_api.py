import requests

BASE = "http://127.0.0.1:5000"
s = requests.Session()


def mostrar(titulo, r):
    print(f"{titulo:<45} {r.status_code}  {r.text.strip()[:120]}")


# sem login -> tem que dar 401
mostrar("GET /categorias/ sem login", requests.get(f"{BASE}/categorias/"))

# login: AJUSTE a URL e os campos conforme o seu login_routes.py
mostrar("POST login", s.post(f"{BASE}/login/", json={"usuario": "SEU_USUARIO", "senha": "SUA_SENHA"}))

mostrar("GET /categorias/", s.get(f"{BASE}/categorias/"))
mostrar("POST categoria válida", s.post(f"{BASE}/categorias/", json={"nome": "Teste"}))
mostrar("POST categoria duplicada (409)", s.post(f"{BASE}/categorias/", json={"nome": "Teste"}))
mostrar("POST nome vazio (400)", s.post(f"{BASE}/categorias/", json={"nome": "  "}))
mostrar("POST nome numérico (400)", s.post(f"{BASE}/categorias/", json={"nome": 123}))
mostrar("POST nome longo (400)", s.post(f"{BASE}/categorias/", json={"nome": "x" * 200}))
mostrar("PUT inexistente (404)", s.put(f"{BASE}/categorias/9999", json={"nome": "A"}))
mostrar("DELETE status padrão (409)", s.delete(f"{BASE}/status/projetos/1"))
mostrar("GET /status/projetos/", s.get(f"{BASE}/status/projetos/"))