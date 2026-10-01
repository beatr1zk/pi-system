(function () {
    const SERVICOS = {
        "identidade-visual": "Identidade Visual",
        "design-grafico": "Design Gráfico",
        "ui-ux": "UI/UX",
        "desenvolvimento-web": "Desenvolvimento Web",
        "outro": "Outro",
    };

    const corpo = document.getElementById("corpo-leads");
    const aviso = document.getElementById("aviso");
    const busca = document.getElementById("busca");
    const dlgNovo = document.getElementById("dialogo-novo");
    const dlgConverter = document.getElementById("dialogo-converter");
    const formNovo = document.getElementById("form-novo");
    const formConverter = document.getElementById("form-converter");

    let leads = [];
    let statusLista = [];
    let leadConvertendo = null;

    function el(tag, props, ...filhos) {
        const e = document.createElement(tag);
        Object.assign(e, props || {});
        e.append(...filhos);
        return e;
    }

    function mostrarAviso(t) { aviso.textContent = t || ""; }

    function nomeServico(slug) { return SERVICOS[slug] || slug; }

    function opcoesServico(select, atual) {
        select.replaceChildren();
        const slugs = Object.keys(SERVICOS);
        if (atual && !slugs.includes(atual)) slugs.push(atual);
        slugs.forEach(s => select.append(new Option(nomeServico(s), s)));
        if (atual) select.value = atual;
    }

    function formatarData(iso) {
        return iso ? new Date(iso).toLocaleDateString("pt-BR") : "";
    }

    function idConvertido() {
        const s = statusLista.find(x => x.nome === "Convertido");
        return s ? s.id : null;
    }

    // ---------- carregar ----------
    async function carregar() {
        const termo = busca.value.trim();
        const url = termo ? "/leads/pesquisar?termo=" + encodeURIComponent(termo) : "/leads/";
        const res = await api(url);
        if (!res) return;
        if (!res.ok) { mostrarAviso(res.dados.erro || "Não foi possível carregar."); return; }
        leads = res.dados;
        render();
        mostrarAviso(leads.length ? "" : "Nenhum lead encontrado.");
    }

    function render() {
        corpo.replaceChildren();
        leads.forEach(lead => {
            const { tr, detalhe } = montarLinha(lead);
            corpo.append(tr, detalhe);
        });
    }

    // ---------- linha ----------
    function montarLinha(lead) {
        const convertido = lead.cliente_id !== null;
        const detalhe = montarDetalhe(lead);
        const alternar = () => { detalhe.hidden = !detalhe.hidden; };

        const select = el("select", { disabled: convertido, ariaLabel: "Status do lead" });
        statusLista.forEach(s => {
            if (s.id === idConvertido() && !convertido) return;  // só a conversão leva a "Convertido"
            select.append(new Option(s.nome, s.id));
        });
        select.value = lead.status_id;
        select.addEventListener("change", async () => {
            const res = await api("/leads/" + lead.id, "PUT", { status_id: Number(select.value) });
            if (!res) return;
            if (res.ok) { lead.status_id = Number(select.value); mostrarAviso("Status atualizado."); }
            else { select.value = lead.status_id; mostrarAviso(res.dados.erro || "Não foi possível salvar o status."); }
        });

        const btnDetalhes = el("button", { type: "button", className: "botao-linha", textContent: "Detalhes" });
        btnDetalhes.addEventListener("click", alternar);

        const btnConverter = el("button", {
            type: "button", className: "botao-linha",
            textContent: convertido ? "Convertido" : "Converter",
            disabled: convertido,
        });
        btnConverter.addEventListener("click", () => abrirConverter(lead));

        const tr = el("tr", { className: convertido ? "linha-convertida" : "" },
            el("td", { textContent: lead.id }),
            el("td", { textContent: lead.nome }),
            el("td", { textContent: lead.email || "" }),
            el("td", { textContent: lead.telefone || "" }),
            el("td", { textContent: nomeServico(lead.servico) }),
            el("td", {}, select),
            el("td", { textContent: formatarData(lead.data_cadastro) }),
            el("td", {}, btnDetalhes),
            el("td", {}, btnConverter),
        );
        tr.addEventListener("dblclick", e => {
            if (e.target.closest("button, select, input")) return;
            alternar();
        });
        return { tr, detalhe };
    }

    // ---------- detalhes ----------
    function montarDetalhe(lead) {
        const convertido = lead.cliente_id !== null;
        const campo = (rotulo, input) => el("label", {}, rotulo, input);

        const nome = el("input", { value: lead.nome, maxLength: 100, required: true });
        const email = el("input", { type: "email", value: lead.email || "", maxLength: 150 });
        const telefone = el("input", { value: lead.telefone || "", maxLength: 20 });
        const servico = el("select");
        opcoesServico(servico, lead.servico);
        const mensagem = el("textarea", { rows: 5, maxLength: 2000, value: lead.mensagem || "" });

        const info = el("p", { className: "info-ids",
            textContent: "Lead ID: " + lead.id + " · Cliente ID: " + (lead.cliente_id ?? "—") });

        const salvar = el("button", { type: "button", className: "botao", textContent: "Salvar alterações" });
        salvar.addEventListener("click", async () => {
            if (!nome.value.trim()) { mostrarAviso("O nome é obrigatório."); return; }
            const res = await api("/leads/" + lead.id, "PUT", {
                nome: nome.value, email: email.value, telefone: telefone.value,
                servico: servico.value, mensagem: mensagem.value,
            });
            if (!res) return;
            mostrarAviso(res.ok ? "Alterações salvas." : (res.dados.erro || "Não foi possível salvar."));
            if (res.ok) carregar();
        });

        const excluir = el("button", {
            type: "button",
            className: "botao botao-secundario",
            textContent: "Excluir",
        });
        excluir.addEventListener("click", async () => {
            let pergunta = 'Você deseja excluir o lead "' + lead.nome + '"?';
            if (convertido) {
                pergunta += "\n\nEle já foi convertido: o cliente #" + lead.cliente_id + " será mantido.";
            }
            if (!window.confirm(pergunta)) return;
            const res = await api("/leads/" + lead.id, "DELETE");
            if (!res) return;
            mostrarAviso(res.ok ? "Lead excluído." : (res.dados.erro || "Não foi possível excluir."));
            if (res.ok) carregar();
        });

        const grade = el("div", { className: "grade-detalhe" },
            campo("Nome", nome), campo("E-mail", email), campo("Telefone", telefone),
            campo("Serviço", servico),
            el("label", { className: "ocupa-tudo" }, "Mensagem", mensagem),
        );

        const td = el("td", { colSpan: 9 }, info, grade, el("div", { className: "acoes-dialogo" }, excluir, salvar));
        return el("tr", { className: "linha-detalhe", hidden: true }, td);
    }

    // ---------- converter ----------
    function abrirConverter(lead) {
        leadConvertendo = lead;
        formConverter.reset();
        formConverter.querySelector(".erro-dialogo").textContent = "";
        formConverter.elements.email.value = lead.email || "";
        dlgConverter.showModal();
    }

    formConverter.addEventListener("submit", async e => {
        e.preventDefault();
        const corpoReq = { email: formConverter.elements.email.value.trim() };
        const cpf = formConverter.elements.cpf.value.trim();
        if (cpf) corpoReq.cpf = cpf;

        const res = await api("/leads/" + leadConvertendo.id + "/converter", "POST", corpoReq);
        if (!res) return;
        if (res.ok) {
            dlgConverter.close();
            mostrarAviso("Lead convertido em cliente.");
            carregar();
        } else {
            formConverter.querySelector(".erro-dialogo").textContent = res.dados.erro || "Não foi possível converter.";
        }
    });

    // ---------- novo lead ----------
    document.getElementById("botao-novo").addEventListener("click", () => {
        formNovo.reset();
        formNovo.querySelector(".erro-dialogo").textContent = "";
        opcoesServico(document.getElementById("novo-servico"));
        dlgNovo.showModal();
    });

    formNovo.addEventListener("submit", async e => {
        e.preventDefault();
        const f = formNovo.elements;
        const res = await api("/leads/", "POST", {
            nome: f.nome.value, email: f.email.value, telefone: f.telefone.value,
            servico: f.servico.value, mensagem: f.mensagem.value,
        });
        if (!res) return;
        if (res.ok) { dlgNovo.close(); mostrarAviso("Lead criado."); carregar(); }
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
        const res = await api("/status/leads/");
        if (!res) return;
        if (!res.ok) { mostrarAviso("Não foi possível carregar os status."); return; }
        statusLista = res.dados;
        carregar();
    })();
})();