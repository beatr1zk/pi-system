(function () {
    const area = document.getElementById("area-cliente");
    const id = Number(area.dataset.id);
    const aviso = document.getElementById("aviso");

    const f = {
        nome: document.getElementById("c-nome"),
        email: document.getElementById("c-email"),
        telefone: document.getElementById("c-telefone"),
        cpf: document.getElementById("c-cpf"),
        status: document.getElementById("c-status"),
        detalhes: document.getElementById("c-detalhes"),
    };
    const botaoSalvar = document.getElementById("botao-salvar");
    const botaoExcluir = document.getElementById("botao-excluir");
    const motivo = document.getElementById("motivo-excluir");

    let cliente = null;
    let leadsDoCliente = [];
    let projetosDoCliente = [];

    function el(tag, props, ...filhos) {
        const e = document.createElement(tag);
        Object.assign(e, props || {});
        e.append(...filhos);
        return e;
    }

    function mostrarAviso(t) { aviso.textContent = t || ""; }

    function formatarDataHora(iso) {
        return iso ? new Date(iso).toLocaleString("pt-BR") : "—";
    }

    function formatarData(iso) {
        return iso ? new Date(iso).toLocaleDateString("pt-BR") : "";
    }

    function preencher() {
        f.nome.value = cliente.nome;
        f.email.value = cliente.email;
        f.telefone.value = cliente.telefone || "";
        f.cpf.value = cliente.cpf || "";
        f.status.value = cliente.status_id;
        f.detalhes.value = cliente.detalhes || "";
        document.getElementById("info-ids").textContent =
            "Cliente ID: " + cliente.id +
            " · Cadastro: " + formatarDataHora(cliente.data_cadastro) +
            " · Última atualização: " + formatarDataHora(cliente.data_atualizacao);
    }

    function atualizarExclusao() {
        const temProjetos = projetosDoCliente.length > 0;
        const temLeads = leadsDoCliente.length > 0;
        botaoExcluir.disabled = temProjetos;
        if (temProjetos) {
            motivo.textContent = "Este cliente tem projetos e não pode ser excluído. Use o status Inativo.";
        } else if (temLeads) {
            motivo.textContent = "Este cliente veio de um lead. Exclua o lead antes de excluir o cliente.";
        } else {
            motivo.textContent = "";
        }
    }

    function montarOrigem() {
        const origem = document.getElementById("origem");
        origem.textContent = leadsDoCliente.length
            ? leadsDoCliente.map(l => "Veio do lead #" + l.id + " (" + l.nome + ")").join(" · ")
            : "Cliente cadastrado diretamente, sem lead de origem.";
    }

    function montarProjetos(statusProjetos) {
        const corpo = document.getElementById("corpo-projetos");
        corpo.replaceChildren();
        if (!projetosDoCliente.length) {
            corpo.append(el("tr", {}, el("td", { colSpan: 4, textContent: "Nenhum projeto." })));
            return;
        }
        projetosDoCliente.forEach(p => {
            const st = statusProjetos.find(s => s.id === p.status_id);
            corpo.append(el("tr", {},
                el("td", { textContent: p.id }),
                el("td", { textContent: p.nome }),
                el("td", { textContent: st ? st.nome : "" }),
                el("td", { textContent: formatarData(p.data_entrega) }),
            ));
        });
    }

    botaoSalvar.addEventListener("click", async () => {
        if (!f.nome.value.trim() || !f.email.value.trim()) {
            mostrarAviso("Nome e e-mail são obrigatórios.");
            return;
        }
        const res = await api("/clientes/" + id, "PUT", {
            nome: f.nome.value, email: f.email.value, telefone: f.telefone.value,
            cpf: f.cpf.value, detalhes: f.detalhes.value, status_id: Number(f.status.value),
        });
        if (!res) return;
        if (res.ok) { cliente = res.dados; preencher(); mostrarAviso("Alterações salvas."); }
        else mostrarAviso(res.dados.erro || "Não foi possível salvar.");
    });

    botaoExcluir.addEventListener("click", async () => {
        if (!window.confirm('Você deseja excluir o cliente "' + cliente.nome + '"?')) return;
        const res = await api("/clientes/" + id, "DELETE");
        if (!res) return;
        if (res.ok) { window.location.href = "/admin/clientes"; return; }
        mostrarAviso(leadsDoCliente.length
            ? "Não foi possível excluir: exclua antes o lead de origem."
            : (res.dados.erro || "Não foi possível excluir."));
    });

    (async function () {
        const respostas = await Promise.all([
            api("/clientes/" + id),
            api("/status/clientes/"),
            api("/projetos/"),
            api("/status/projetos/"),
            api("/leads/"),
        ]);
        if (respostas.some(r => r === null)) return;

        const [rCliente, rStatus, rProjetos, rStatusProj, rLeads] = respostas;
        if (rCliente.status === 404) { mostrarAviso("Cliente não encontrado."); return; }
        if (respostas.some(r => !r.ok)) { mostrarAviso("Não foi possível carregar os dados."); return; }

        cliente = rCliente.dados;
        rStatus.dados.forEach(s => f.status.append(new Option(s.nome, s.id)));
        projetosDoCliente = rProjetos.dados.filter(p => p.cliente_id === id);
        leadsDoCliente = rLeads.dados.filter(l => l.cliente_id === id);

        preencher();
        montarOrigem();
        montarProjetos(rStatusProj.dados);
        atualizarExclusao();
        area.hidden = false;
    })();
})();