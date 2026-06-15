let dadosRel = null;

async function carregarRelatorios() {
  dadosRel = await api('/api/relatorios');
  const r  = dadosRel.resumo;

  document.getElementById('rel-total').textContent    = fmt(r.total_vendas);
  document.getElementById('rel-recebido').textContent = fmt(r.recebido);
  document.getElementById('rel-pendente').textContent = fmt(r.a_receber);

  // Relatório texto
  document.getElementById('rel-texto').innerHTML = `
<span style="color:var(--gold)">===== RELATÓRIO GERAL — CHURRASCARIA DO RONAN =====</span>
Gerado em: ${new Date().toLocaleString('pt-BR')}

<span style="color:var(--gold)">— CLIENTES —</span>
Total cadastrados: <span style="color:#2ecc71">${r.total_clientes}</span>

<span style="color:var(--gold)">— PRODUTOS —</span>
Total no cardápio: <span style="color:#2ecc71">${r.total_produtos}</span>

<span style="color:var(--gold)">— PEDIDOS —</span>
Total de pedidos : <span style="color:#2ecc71">${r.total_pedidos}</span>
  Pagos           : <span style="color:#2ecc71">${r.pagos}</span>
  Pendentes       : <span style="color:var(--acc)">${r.pendentes}</span>

<span style="color:var(--gold)">— FINANCEIRO —</span>
Total bruto       : <span style="color:#2ecc71">${fmt(r.total_vendas)}</span>
Valor recebido    : <span style="color:#2ecc71">${fmt(r.recebido)}</span>
A receber         : <span style="color:var(--acc)">${fmt(r.a_receber)}</span>

<span style="color:var(--gold)"> FIM DO RELATÓRIO </span>`;

  // Top produtos
  if (dadosRel.top_produtos.length) {
    document.getElementById('top-prod-section').style.display = 'block';
    document.getElementById('rel-top').innerHTML = dadosRel.top_produtos.map((p, i) => `
      <tr>
        <td style="font-family:var(--font-head);font-size:22px;color:var(--gold)">${i+1}º</td>
        <td><strong>${p.nome}</strong></td>
        <td style="font-family:var(--font-mono)">${p.total_vendido} un</td>
        <td style="font-family:var(--font-mono);color:var(--gold)">${fmt(p.receita)}</td>
      </tr>`).join('');
  }

  // Estoque crítico
  if (dadosRel.est_critico.length) {
    document.getElementById('est-critico-section').style.display = 'block';
    document.getElementById('rel-est-critico').innerHTML = dadosRel.est_critico.map(e => `
      <tr>
        <td><strong>${e.nome}</strong></td>
        <td style="font-family:var(--font-mono)">${e.quantidade}</td>
        <td><span class="badge ${e.quantidade===0?'badge-low':'badge-warn'}">${e.quantidade===0?'ESGOTADO':'CRÍTICO'}</span></td>
      </tr>`).join('');
  }
}

function exportarRelatorio() {
  if (!dadosRel) return;
  const r = dadosRel.resumo;
  const texto = `===== RELATÓRIO — CHURRASCARIA DO RONAN =====
Gerado em: ${new Date().toLocaleString('pt-BR')}

CLIENTES:  ${r.total_clientes}
PRODUTOS:  ${r.total_produtos}
PEDIDOS:   ${r.total_pedidos} (${r.pagos} pagos / ${r.pendentes} pendentes)

FINANCEIRO:
  Total:      ${fmt(r.total_vendas)}
  Recebido:   ${fmt(r.recebido)}
  A receber:  ${fmt(r.a_receber)}

TOP PRODUTOS:
${dadosRel.top_produtos.map((p,i)=>`  ${i+1}. ${p.nome} — ${p.total_vendido} un — ${fmt(p.receita)}`).join('\n') || '  Nenhum'}

 FIM `;

  const blob = new Blob([texto], { type: 'text/plain;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `relatorio-ronan-${Date.now()}.txt`;
  a.click();
  toast('Relatório exportado!');
}

carregarRelatorios();
