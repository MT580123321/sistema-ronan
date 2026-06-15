async function carregarClientes(q = '') {
  const rows = await api('/api/clientes' + (q ? `?q=${encodeURIComponent(q)}` : ''));
  const tbody = document.getElementById('clientes-tbody');
  document.getElementById('cli-count').textContent = `(${rows.length})`;

  if (!rows.length) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="6">Nenhum cliente encontrado</td></tr>';
    return;
  }
  tbody.innerHTML = rows.map((c, i) => `
    <tr>
      <td style="color:var(--muted);font-family:var(--font-mono)">${i+1}</td>
      <td><strong>${c.nome}</strong></td>
      <td>${c.telefone}</td>
      <td style="font-family:var(--font-mono)">${c.cpf || '—'}</td>
      <td style="color:var(--muted);font-size:13px">${c.criado_em}</td>
      <td class="td-actions">
        <button class="btn-sm btn-del" onclick="delCliente(${c.id})">Remover</button>
      </td>
    </tr>`).join('');
}

async function addCliente() {
  const nome = document.getElementById('cli-nome').value.trim();
  const tel  = document.getElementById('cli-tel').value.trim();
  const cpf  = document.getElementById('cli-cpf').value.trim();
  if (!nome || !tel) { toast('Preencha Nome e Telefone', 'erro'); return; }

  const r = await api('/api/clientes', 'POST', { nome, telefone: tel, cpf });
  if (r.ok) {
    toast(r.msg);
    document.getElementById('cli-nome').value = '';
    document.getElementById('cli-tel').value  = '';
    document.getElementById('cli-cpf').value  = '';
    carregarClientes(document.getElementById('cli-busca').value);
  } else {
    toast(r.msg, 'erro');
  }
}

async function delCliente(id) {
  if (!confirm('Remover cliente?')) return;
  const r = await api(`/api/clientes/${id}`, 'DELETE');
  if (r.ok) toast(r.msg);
  else toast(r.msg, 'erro');
  carregarClientes(document.getElementById('cli-busca').value);
}

let buscaTimer;
document.addEventListener('DOMContentLoaded', () => {
  const inp = document.getElementById('cli-busca');
  if (inp) {
    inp.addEventListener('input', () => {
      clearTimeout(buscaTimer);
      buscaTimer = setTimeout(() => carregarClientes(inp.value.trim()), 300);
    });
  }
});

carregarClientes();
