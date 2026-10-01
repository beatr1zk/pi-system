async function api(url, metodo = "GET", corpo = null) {
    const opcoes = { method: metodo, headers: {} };
    if (corpo !== null) {
        opcoes.headers["Content-Type"] = "application/json";
        opcoes.body = JSON.stringify(corpo);
    }
    const r = await fetch(url, opcoes);
    if (r.status === 401) {
        window.location.href = "/admin/login";
        return null;
    }
    const dados = await r.json().catch(() => ({}));
    return { ok: r.ok, status: r.status, dados: dados };
}