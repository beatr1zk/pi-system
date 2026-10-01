(function () {
    const SERVICOS = {
        "identidade-visual": "Identidade Visual",
        "design-grafico": "Design Gráfico",
        "ui-ux": "UI/UX",
        "desenvolvimento-web": "Desenvolvimento Web",
        "outro": "Outro",
    };

    const corpo = document.getElementById("corpo-projetos");
    const aviso = document.getElementById("aviso");
    const busca = document.getElementById("busca");
    const dlgNovo = document.getElementById("dialogo-novo");
    const formNovo = document.getElementById("form-novo");

    let projetos = [], clientes = [], categorias = [], statusLista = [], prioridades = [];

    function el(tag, props, ...filhos) {
        const e = document.createElement(tag);
        Object.assign(e, props || {});
        e.append(...filhos);
        return e;
    }

    function mostrarAviso(t) { aviso.textContent = t || ""; }

    function nomeDe(lista, id) {
        const item = lista.find(x => x.id === id);
        return item ? item.nome : "";
    }

    function nomeServico(slug) { return slug ? (SERVICOS[slug] || slug) : ""; }

    // datas "AAAA-MM-DD" não passam por new Date (evita erro de fuso)
    function formatarData(iso) {
        return iso ? iso.slice(0, 10).split("-").reverse().join("/") : "";
    }

    function formatarDataHora(iso) {
        return iso ? new Date(iso).toLocaleString("pt-BR") : "";
    }

    function preencherSelect(select, lista, vazio) {
        select.replaceChildren();
        if (vazio) select.append(new Option(vazio, ""));
        lista.forEach(i => select.append(new Option(i.nome, i.id)));
    }

    // ---------- carregar ----------
    async function carregar() {
        const termo = busca.value.trim();
        const url = termo ? "/projetos/pesquisar?termo=" + encodeURIComponent(termo) : "/projetos/";
        const res = await api(url);
        if (!res) return;
        if (!res.ok) { mostrarAviso(res.dados.erro || "Não foi possível carregar."); return; }
        projetos = res.dados;
        render();
        mostrarAviso(projetos.length ? "" : "Nenhum projeto encontrado.");
    }

    function render() {
        corpo.replaceChildren();
        projetos.forEach(p => {
            const { tr, extra } = montarLinha(p);
            corpo.append(tr, extra);
        });
    }

    // ---------- linha ----------
    function montarLinha(p) {
        const extra = montarExtra(p);
        const alternar = () => { extra.hidden = !extra.hidden; };

        const select = el("select", { ariaLabel: "Status do projeto" });
        statusLista.forEach(s => select.append(new Option(s.nome, s.id)));
        select.value = p.status_id;
        select.addEventListener("change", async () => {
            const res = await api("/projetos/" + p.id, "PUT", { status_id: Number(select.value) });
            if (!res) return;
            if (res.ok) { p.status_id = Number(select.value); mostrarAviso("Status atualizado."); }
            else { select.value = p.status_id; mostrarAviso(res.dados.erro || "Não foi possível salvar o status."); }
        });

        const detalhes = el("a", {
            className: "botao-linha",
            href: "/admin/projetos/" + p.id,
            textContent: "Detalhes",
        });

        const tr = el("tr", {},
            el("td", { textContent: p.id }),
            el("td", { textContent: p.nome }),
            el("td", { textContent: nomeDe(clientes, p.cliente_id) }),
            el("td", { textContent: nomeDe(categorias, p.categoria_id) }),
            el("td", {}, select),
            el("td", { textContent: nomeDe(prioridades, p.prioridade_id) }),
            el("td", { textContent: formatarData(p.data_entrega) }),
            el("td", {}, detalhes),
        );
        tr.addEventListener("dblclick", e => {
            if (e.target.closest("a, button, select, input")) return;
            alternar();
        });
        return { tr, extra };
    }

    // ---------- informações extras (duplo clique) ----------
    function montarExtra(p) {
        const item = (rotulo, conteudo) =>
            el("p", {}, el("strong", { textContent: rotulo + ": " }), conteudo);

        let proposta = "—";
        if (p.url_proposta && /^https?:\/\//i.test(p.url_proposta)) {
            proposta = el("a", {
                href: p.url_proposta, textContent: p.url_proposta,
                target: "_blank", rel: "noopener noreferrer",
            });
        }

        const td = el("td", { colSpan: 8 },
            item("Serviço", nomeServico(p.servico) || "—"),
            item("Escopo", p.escopo || "—"),
            item("URL da proposta", proposta),
            item("Data do pedido", formatarDataHora(p.data_pedido) || "—"),
            item("Prazo de entrega", formatarData(p.data_entrega) || "—"),
            item("Data de conclusão", formatarData(p.data_conclusao) || "—"),
        );
        return el("tr", { className: "linha-detalhe", hidden: true }, td);
    }

    // ---------- novo projeto ----------
    document.getElementById("botao-novo").addEventListener("click", () => {
        if (!clientes.length) {
            mostrarAviso("Cadastre um cliente antes de criar um projeto.");
            return;
        }
        formNovo.reset();
        formNovo.querySelector(".erro-dialogo").textContent = "";
        const f = formNovo.elements;
        preencherSelect(f.cliente_id, clientes);
        preencherSelect(f.categoria_id, categorias);
        preencherSelect(f.prioridade_id, prioridades, "Sem prioridade");
        f.servico.replaceChildren(new Option("Não informado", ""));
        Object.keys(SERVICOS).forEach(s => f.servico.append(new Option(SERVICOS[s], s)));
        dlgNovo.showModal();
    });

    formNovo.addEventListener("submit", async e => {
        e.preventDefault();
        const f = formNovo.elements;
        const corpoReq = {
            nome: f.nome.value,
            cliente_id: Number(f.cliente_id.value),
            categoria_id: Number(f.categoria_id.value),
        };
        if (f.servico.value) corpoReq.servico = f.servico.value;
        if (f.prioridade_id.value) corpoReq.prioridade_id = Number(f.prioridade_id.value);
        if (f.data_entrega.value) corpoReq.data_entrega = f.data_entrega.value;

        const res = await api("/projetos/", "POST", corpoReq);
        if (!res) return;
        if (res.ok) { dlgNovo.close(); mostrarAviso("Projeto criado."); carregar(); }
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
        const respostas = await Promise.all([
            api("/clientes/"), api("/categorias/"), api("/status/projetos/"), api("/prioridades/"),
        ]);
        if (respostas.some(r => r === null)) return;
        if (respostas.some(r => !r.ok)) { mostrarAviso("Não foi possível carregar os dados de apoio."); return; }
        [clientes, categorias, statusLista, prioridades] = respostas.map(r => r.dados);
        carregar();
    })();
})();