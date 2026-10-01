(function () {
    const SERVICOS = {
        "identidade-visual": "Identidade Visual",
        "design-grafico": "Design Gráfico",
        "ui-ux": "UI/UX",
        "desenvolvimento-web": "Desenvolvimento Web",
        "outro": "Outro",
    };

    const area = document.getElementById("area-projeto");
    const id = Number(area.dataset.id);
    const aviso = document.getElementById("aviso");

    const f = {
        nome: document.getElementById("p-nome"),
        cliente: document.getElementById("p-cliente"),
        categoria: document.getElementById("p-categoria"),
        status: document.getElementById("p-status"),
        prioridade: document.getElementById("p-prioridade"),
        servico: document.getElementById("p-servico"),
        entrega: document.getElementById("p-entrega"),
        conclusao: document.getElementById("p-conclusao"),
        url: document.getElementById("p-url"),
        escopo: document.getElementById("p-escopo"),
    };

    let projeto = null;
    let statusLista = [];

    function mostrarAviso(t) { aviso.textContent = t || ""; }

    function preencherSelect(select, lista, vazio) {
        select.replaceChildren();
        if (vazio) select.append(new Option(vazio, ""));
        lista.forEach(i => select.append(new Option(i.nome, i.id)));
    }

    function opcoesServico(atual) {
        f.servico.replaceChildren(new Option("Não informado", ""));
        const slugs = Object.keys(SERVICOS);
        if (atual && !slugs.includes(atual)) slugs.push(atual);
        slugs.forEach(s => f.servico.append(new Option(SERVICOS[s] || s, s)));
    }

    function preencher() {
        f.nome.value = projeto.nome;
        f.cliente.value = projeto.cliente_id;
        f.categoria.value = projeto.categoria_id;
        f.status.value = projeto.status_id;
        f.prioridade.value = projeto.prioridade_id ?? "";
        opcoesServico(projeto.servico);
        f.servico.value = projeto.servico || "";
        f.entrega.value = projeto.data_entrega ? projeto.data_entrega.slice(0, 10) : "";
        f.conclusao.value = projeto.data_conclusao ? projeto.data_conclusao.slice(0, 10) : "";
        f.url.value = projeto.url_proposta || "";
        f.escopo.value = projeto.escopo || "";
        document.getElementById("info-ids").textContent =
            "Projeto ID: " + projeto.id + " · Pedido em: " +
            (projeto.data_pedido ? new Date(projeto.data_pedido).toLocaleString("pt-BR") : "—");
    }

    document.getElementById("botao-salvar").addEventListener("click", async () => {
        if (!f.nome.value.trim()) { mostrarAviso("O nome é obrigatório."); return; }

        const statusNome = (statusLista.find(s => s.id === Number(f.status.value)) || {}).nome;
        if (statusNome === "Concluído" && !f.conclusao.value) {
            if (!window.confirm("O projeto está como Concluído, mas sem data de conclusão. Salvar assim mesmo?")) return;
        }

        const res = await api("/projetos/" + id, "PUT", {
            nome: f.nome.value,
            cliente_id: Number(f.cliente.value),
            categoria_id: Number(f.categoria.value),
            status_id: Number(f.status.value),
            prioridade_id: f.prioridade.value ? Number(f.prioridade.value) : null,
            servico: f.servico.value || null,
            data_entrega: f.entrega.value || null,
            data_conclusao: f.conclusao.value || null,
            url_proposta: f.url.value.trim() || null,
            escopo: f.escopo.value.trim() || null,
        });
        if (!res) return;
        if (res.ok) { projeto = res.dados; preencher(); mostrarAviso("Alterações salvas."); }
        else mostrarAviso(res.dados.erro || "Não foi possível salvar.");
    });

    document.getElementById("botao-excluir").addEventListener("click", async () => {
        if (!window.confirm('Você deseja excluir o projeto "' + projeto.nome + '"?')) return;
        const res = await api("/projetos/" + id, "DELETE");
        if (!res) return;
        if (res.ok) window.location.href = "/admin/projetos";
        else mostrarAviso(res.dados.erro || "Não foi possível excluir.");
    });

    (async function () {
        const respostas = await Promise.all([
            api("/projetos/" + id), api("/clientes/"), api("/categorias/"),
            api("/status/projetos/"), api("/prioridades/"),
        ]);
        if (respostas.some(r => r === null)) return;
        if (respostas[0].status === 404) { mostrarAviso("Projeto não encontrado."); return; }
        if (respostas.some(r => !r.ok)) { mostrarAviso("Não foi possível carregar os dados."); return; }

        const [rProj, rCli, rCat, rSt, rPri] = respostas;
        projeto = rProj.dados;
        statusLista = rSt.dados;
        preencherSelect(f.cliente, rCli.dados);
        preencherSelect(f.categoria, rCat.dados);
        preencherSelect(f.status, rSt.dados);
        preencherSelect(f.prioridade, rPri.dados, "Sem prioridade");

        preencher();
        area.hidden = false;
    })();
})();