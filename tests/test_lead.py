
from models.contato import Contato
from models.lead import Lead

def test_lead_e_contato():
    lead = Lead("Bruno", "b@x.com", "4188888", "Logo", "Quero um logo", 1, None)
    assert isinstance(lead, Contato)
    assert lead.servico == "Logo"
    assert lead.mensagem == "Quero um logo"
    assert lead.cliente_id is None

def test_resumo_do_lead():
    lead = Lead("Bruno", "b@x.com", "4188888", "Logo", "Oi", 1, None)
    assert lead.resumo() == "Lead: Bruno (interesse em Logo)"