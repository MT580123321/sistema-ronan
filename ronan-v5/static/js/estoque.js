async function carregarEstoque(q = '') {
  const rows  = await api('/api/estoque' + (q ? `?q=${encodeURIComponent(q)}` : ''));
  const tbody = document.getElementById('estoque-tbody');
  const sel   = document.getElementById('est-prod');

  const todos = await api('/api/estoque');
  sel.innerHTML = '<option value="">— Selecionar —</option>' +
    todos.map(e => `<option value="${e.produto_id}">${e.nome}</option>`).join('');

  if (!rows.length) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="6">Nenhum item encontrado</td></tr>';
    return;
  }

  tbody.innerHTML = rows.map((e, i) => {
    let sit, cls;
    if (e.quantidade === 0)      { sit = 'ESGOTADO'; cls = 'badge-low'; }
    else if (e.quantidade <= 5)  { sit = 'CRÍTICO';  cls = 'badge-low'; }
    else if (e.quantidade <= 10) { sit = 'BAIXO';    cls = 'badge-warn'; }
    else                         { sit = 'OK';       cls = 'badge-ok'; }
    return `
    <tr>
      <td style="color:var(--muted);font-family:var(--font-mono)">${i+1}</td>
      <td><strong>${e.nome}</strong></td>
      <td><span class="badge badge-pend">${e.categoria}</span></td>
      <td style="font-family:var(--font-mono);font-size:18px">${e.quantidade}</td>
      <td><span class="badge ${cls}">${sit}</span></td>
      <td style="color:var(--muted);font-size:13px">${e.atualizado_em}</td>
    </tr>`;
  }).join('');
}

async function ajustarEstoque() {
  const pid = document.getElementById('est-prod').value;
  const qtd = parseInt(document.getElementById('est-qtd').value);
  if (!pid || isNaN(qtd) || qtd < 0) { toast('Selecione produto e quantidade válida', 'erro'); return; }

  const r = await api(`/api/estoque/${pid}`, 'PUT', { quantidade: qtd });
  if (r.ok) {
    toast(r.msg);
    document.getElementById('est-qtd').value = '';
    carregarEstoque(document.getElementById('est-busca')?.value || '');
  } else {
    toast(r.msg || 'Erro ao atualizar estoque', 'erro');
  }
}

let buscaTimer;
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('est-busca')?.addEventListener('input', e => {
    clearTimeout(buscaTimer);
    buscaTimer = setTimeout(() => carregarEstoque(e.target.value.trim()), 300);
  });
});

carregarEstoque();
