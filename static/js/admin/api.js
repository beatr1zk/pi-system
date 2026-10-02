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

function hojeISO() {
    const d = new Date();
    return d.getFullYear() + "-" +
        String(d.getMonth() + 1).padStart(2, "0") + "-" +
        String(d.getDate()).padStart(2, "0");
}

// Retorna true se pode continuar (data vazia, de hoje/futura, ou confirmada).
function confirmarDataPassada(valor) {
    if (valor && valor < hojeISO()) {
        return window.confirm("A data selecionada é anterior ao dia de hoje. Você tem certeza que deseja continuar?");
    }
    return true;
}