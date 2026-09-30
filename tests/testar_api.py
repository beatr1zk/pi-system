import getpass

import requests

BASE = "http://127.0.0.1:5000"
s = requests.Session()


def mostrar(titulo, r):
    print(f"{titulo:<42} {r.status_code}  {r.text.strip()[:400]}")


def dados(r):
    """Devolve o JSON da resposta, ou {} se a resposta não for JSON (ex.: página 404 em HTML)."""
    try:
        resultado = r.json()
        return resultado if isinstance(resultado, dict) else {}
    except ValueError:
        return {}


def exigir(valor, nome):
    """Interrompe o teste se um id necessário não foi criado, em vez de gerar URLs como /None."""
    if valor is None:
        raise SystemExit(f"\nParando: '{nome}' não foi criado na etapa anterior. Veja o erro acima.")
    return valor


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
print("--- login ---")
mostrar("GET /categorias/ sem login (401)", requests.get(f"{BASE}/categorias/"))

usuario = input("Usuário: ")
senha = getpass.getpass("Senha (não aparece na tela): ")

r = s.post(f"{BASE}/login/", json={"usuario": usuario, "senha": senha})
mostrar("POST /login/ (200)", r)
if r.status_code != 200:
    raise SystemExit("\nLogin falhou: corrija antes de continuar (o resto dos testes depende dele).")

mostrar("POST /login/ senha errada (401)", requests.post(f"{BASE}/login/", json={"usuario": usuario, "senha": "errada"}))
mostrar("POST /login/ usuario não texto (400)", requests.post(f"{BASE}/login/", json={"usuario": {"a": 1}, "senha": "x"}))

# IDs criados durante o teste (para a limpeza, mesmo se algo falhar no meio)
cat_id = cid = pid = lid = novo_cid = None

try:
    # ---------------------------------------------------------
    # CATEGORIAS / PRIORIDADES / STATUS
    # ---------------------------------------------------------
    print("\n--- categorias / prioridades / status ---")
    mostrar("GET /categorias/ (200)", s.get(f"{BASE}/categorias/"))

    r = s.post(f"{BASE}/categorias/", json={"nome": "Categoria Teste"})
    mostrar("POST categoria (201)", r)
    cat_id = exigir(dados(r).get("id"), "categoria")

    mostrar("POST duplicada (409)", s.post(f"{BASE}/categorias/", json={"nome": "Categoria Teste"}))
    mostrar("POST nome vazio (400)", s.post(f"{BASE}/categorias/", json={"nome": "  "}))
    mostrar("POST nome numérico (400)", s.post(f"{BASE}/categorias/", json={"nome": 123}))
    mostrar("POST nome longo (400)", s.post(f"{BASE}/categorias/", json={"nome": "x" * 200}))
    mostrar("PUT inexistente (404)", s.put(f"{BASE}/categorias/9999", json={"nome": "A"}))
    mostrar("PUT categoria (200)", s.put(f"{BASE}/categorias/{cat_id}", json={"nome": "Categoria Teste 2"}))
    r = s.delete(f"{BASE}/categorias/{cat_id}")
    mostrar("DELETE categoria (200)", r)
    if r.status_code == 200:
        cat_id = None  # já removida

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
    cid = exigir(dados(r).get("id"), "cliente")

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
    pid = exigir(dados(r).get("id"), "projeto")
    print("   data_pedido preenchida?", bool(dados(r).get("data_pedido")))

    mostrar("GET projeto (servico/escopo certos?)", s.get(f"{BASE}/projetos/{pid}"))
    mostrar("PUT projeto (200)", s.put(f"{BASE}/projetos/{pid}", json={"nome": "Projeto Teste 2"}))
    mostrar("GET após PUT (continuam certos?)", s.get(f"{BASE}/projetos/{pid}"))
    mostrar("POST cliente_id inexistente (409)", s.post(f"{BASE}/projetos/", json={"cliente_id": 9999, "categoria_id": 1, "nome": "X"}))
    mostrar("POST url javascript: (400)", s.post(f"{BASE}/projetos/", json={"cliente_id": cid, "categoria_id": 1, "nome": "X", "url_proposta": "javascript:alert(1)"}))
    mostrar("DELETE cliente com projeto (409)", s.delete(f"{BASE}/clientes/{cid}"))

    r = s.post(f"{BASE}/leads/", json={"nome": "Lead Teste", "servico": "identidade-visual"})
    mostrar("POST lead sem e-mail (201)", r)
    lid = exigir(dados(r).get("id"), "lead")
    mostrar("Converter sem e-mail (400)", s.post(f"{BASE}/leads/{lid}/converter", json={}))

    r = s.post(f"{BASE}/leads/{lid}/converter", json={"email": "lead@exemplo.com"})
    mostrar("Converter com e-mail (201)", r)
    novo_cid = dados(r).get("cliente_id")

    mostrar("Converter de novo (409)", s.post(f"{BASE}/leads/{lid}/converter", json={"email": "lead@exemplo.com"}))
    mostrar("GET lead (status_id 3 e cliente_id?)", s.get(f"{BASE}/leads/{lid}"))

finally:
    # ---------------------------------------------------------
    # LIMPEZA (roda mesmo se algum passo acima falhar)
    # ---------------------------------------------------------
    print("\n--- limpeza ---")
    if cat_id:
        s.delete(f"{BASE}/categorias/{cat_id}")
    if pid:
        s.delete(f"{BASE}/projetos/{pid}")
    if lid:
        s.delete(f"{BASE}/leads/{lid}")
    if novo_cid:
        s.delete(f"{BASE}/clientes/{novo_cid}")
    if cid:
        s.delete(f"{BASE}/clientes/{cid}")
    print("Limpeza feita.")

# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------
mostrar("POST /login/logout (200)", s.post(f"{BASE}/login/logout"))
mostrar("GET /categorias/ após logout (401)", s.get(f"{BASE}/categorias/"))