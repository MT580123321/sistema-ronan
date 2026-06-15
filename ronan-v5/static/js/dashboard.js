async function carregarDashboard() {
  const d = await api('/api/dashboard');

  document.getElementById('dc-clientes').textContent = d.clientes;
  document.getElementById('dc-produtos').textContent = d.produtos;
  document.getElementById('dc-pedidos').textContent  = d.pedidos;
  document.getElementById('dc-estoque').textContent  = d.estoque;
  document.getElementById('dr-vendas').textContent   = fmt(d.total_vendas);
  document.getElementById('dr-recebido').textContent = fmt(d.recebido);
  document.getElementById('dr-pendente').textContent = fmt(d.pendente);

  const eb = document.getElementById('dr-estbaixo');
  eb.textContent = d.est_baixo;
  eb.style.color = d.est_baixo > 0 ? '#e74c3c' : '#2ecc71';

  const tbody = document.getElementById('dash-ultimos');
  if (!d.ultimos.length) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="6">Nenhum pedido ainda</td></tr>';
    return;
  }
  tbody.innerHTML = d.ultimos.map(p => `
    <tr>
      <td style="color:var(--muted);font-family:var(--font-mono)">${p.id}</td>
      <td><strong>${p.mesa}</strong></td>
      <td>${p.cliente_nome || '—'}</td>
      <td style="font-family:var(--font-mono);color:var(--gold)">${fmt(p.total)}</td>
      <td><span class="badge ${p.status==='Pago'?'badge-pago':'badge-pend'}">${p.status}</span></td>
      <td style="color:var(--muted);font-size:13px">${p.criado_em}</td>
    </tr>`).join('');
}

carregarDashboard();
