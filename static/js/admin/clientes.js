(function () {
    const corpo = document.getElementById("corpo-clientes");
    const aviso = document.getElementById("aviso");
    const busca = document.getElementById("busca");
    const dlgNovo = document.getElementById("dialogo-novo");
    const formNovo = document.getElementById("form-novo");

    let clientes = [];
    let statusLista = [];

    function el(tag, props, ...filhos) {
        const e = document.createElement(tag);
        Object.assign(e, props || {});
        e.append(...filhos);
        return e;
    }

    function mostrarAviso(t) { aviso.textContent = t || ""; }

    function formatarData(iso) {
        return iso ? new Date(iso).toLocaleDateString("pt-BR") : "";
    }

    async function carregar() {
        const termo = busca.value.trim();
        const url = termo ? "/clientes/pesquisar?termo=" + encodeURIComponent(termo) : "/clientes/";
        const res = await api(url);
        if (!res) return;
        if (!res.ok) { mostrarAviso(res.dados.erro || "Não foi possível carregar."); return; }
        clientes = res.dados;
        render();
        mostrarAviso(clientes.length ? "" : "Nenhum cliente encontrado.");
    }

    function render() {
        corpo.replaceChildren();
        clientes.forEach(c => corpo.append(montarLinha(c)));
    }

    function montarLinha(cliente) {
        const irParaCliente = () => { window.location.href = "/admin/clientes/" + cliente.id; };

        const select = el("select", { ariaLabel: "Status do cliente" });
        statusLista.forEach(s => select.append(new Option(s.nome, s.id)));
        select.value = cliente.status_id;
        select.addEventListener("change", async () => {
            const res = await api("/clientes/" + cliente.id, "PUT", { status_id: Number(select.value) });
            if (!res) return;
            if (res.ok) { cliente.status_id = Number(select.value); mostrarAviso("Status atualizado."); }
            else { select.value = cliente.status_id; mostrarAviso(res.dados.erro || "Não foi possível salvar o status."); }
        });

        const abrir = el("a", {
            className: "botao-linha",
            href: "/admin/clientes/" + cliente.id,
            textContent: "Abrir",
        });

        const tr = el("tr", { className: "linha-clicavel" },
            el("td", { textContent: cliente.id }),
            el("td", { textContent: cliente.nome }),
            el("td", { textContent: cliente.email }),
            el("td", { textContent: cliente.telefone || "" }),
            el("td", {}, select),
            el("td", { textContent: formatarData(cliente.data_cadastro) }),
            el("td", {}, abrir),
        );
        tr.addEventListener("click", e => {
            if (e.target.closest("a, button, select, input")) return;
            irParaCliente();
        });
        return tr;
    }

    // ---------- novo cliente ----------
    document.getElementById("botao-novo").addEventListener("click", () => {
        formNovo.reset();
        formNovo.querySelector(".erro-dialogo").textContent = "";
        dlgNovo.showModal();
    });

    formNovo.addEventListener("submit", async e => {
        e.preventDefault();
        const f = formNovo.elements;
        const res = await api("/clientes/", "POST", {
            nome: f.nome.value, email: f.email.value, telefone: f.telefone.value,
            cpf: f.cpf.value, detalhes: f.detalhes.value,
        });
        if (!res) return;
        if (res.ok) { dlgNovo.close(); mostrarAviso("Cliente criado."); carregar(); }
        else formNovo.querySelector(".erro-dialogo").textContent = res.dados.erro || "Não foi possível criar.";
    });

    document.querySelectorAll("[data-fechar]").forEach(b =>
        b.addEventListener("click", () => b.closest("dialog").close()));

    // ---------- busca ----------
    let espera;
    busca.addEventListener("input", () => {
        clearTimeout(espera);
        espera = setTimeout(carregar, 300);
    });

    // ---------- início ----------
    (async function () {
        const res = await api("/status/clientes/");
        if (!res) return;
        if (!res.ok) { mostrarAviso("Não foi possível carregar os status."); return; }
        statusLista = res.dados;
        carregar();
    })();
})();