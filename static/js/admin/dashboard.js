(function () {
    const aviso = document.getElementById("aviso-dashboard");

    (async function () {
        try {
            const [leads, clientes, statusClientes] = await Promise.all([
                api("/leads/"),
                api("/clientes/"),
                api("/status/clientes/"),
            ]);
            if (!leads || !clientes || !statusClientes) return;
            if (!leads.ok || !clientes.ok || !statusClientes.ok) {
                aviso.textContent = "Não foi possível carregar o resumo.";
                return;
            }

            // lead ativo = ainda não convertido em cliente
            const leadsAtivos = leads.dados.filter(l => l.cliente_id === null).length;

            // cliente ativo = status diferente de "Inativo"
            const inativo = statusClientes.dados.find(s => s.nome === "Inativo");
            const idInativo = inativo ? inativo.id : null;
            const clientesAtivos = clientes.dados.filter(c => c.status_id !== idInativo).length;

            document.getElementById("num-leads").textContent = leadsAtivos;
            document.getElementById("num-clientes").textContent = clientesAtivos;
        } catch (e) {
            aviso.textContent = "Erro de conexão com o servidor.";
        }
    })();
})();