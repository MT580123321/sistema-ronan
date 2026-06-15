//  UTILITÁRIOS GLOBAIS 
function fmt(n) {
  return 'R$ ' + Number(n).toFixed(2).replace('.', ',');
}

let toastTimer;
function toast(msg, tipo = 'ok') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'show' + (tipo === 'erro' ? ' toast-error' : '');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.className = ''; }, 3000);
}

async function api(url, method = 'GET', body = null) {
  try {
    const opts = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) opts.body = JSON.stringify(body);
    const r = await fetch(url, opts);
    if (!r.ok && r.status === 401) {
      window.location.href = '/login';
      return { ok: false, msg: 'Sessão expirada' };
    }
    return r.json();
  } catch (err) {
    toast('Erro de conexão com o servidor', 'erro');
    return { ok: false, msg: 'Erro de conexão' };
  }
}

async function logout() {
  await api('/api/logout', 'POST');
  window.location.href = '/login';
}

function fecharModal() {
  const m = document.getElementById('modal-edit');
  if (m) m.style.display = 'none';
}

// Fechar modais clicando fora
document.addEventListener('click', e => {
  ['modal-edit', 'modal-trocar-senha', 'modal-pedido', 'modal-peso'].forEach(id => {
    const m = document.getElementById(id);
    if (m && e.target === m) m.style.display = 'none';
  });
});

// Fechar com ESC
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    ['modal-edit', 'modal-trocar-senha', 'modal-pedido', 'modal-peso'].forEach(id => {
      const m = document.getElementById(id);
      if (m) m.style.display = 'none';
    });
  }
});

//  TROCAR SENHA 
function abrirTrocarSenha() {
  ['ts-atual', 'ts-nova', 'ts-confirma'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
  document.getElementById('modal-trocar-senha').style.display = 'flex';
  setTimeout(() => document.getElementById('ts-atual')?.focus(), 50);
}

function fecharTrocarSenha() {
  document.getElementById('modal-trocar-senha').style.display = 'none';
}

async function salvarSenha() {
  const atual    = document.getElementById('ts-atual').value;
  const nova     = document.getElementById('ts-nova').value;
  const confirma = document.getElementById('ts-confirma').value;
  const r = await api('/api/trocar-senha', 'POST', { atual, nova, confirma });
  if (r.ok) {
    toast(r.msg);
    fecharTrocarSenha();
  } else {
    toast(r.msg, 'erro');
  }
}

//  MODAL DETALHES PEDIDO 
let _pedidoParaImprimir = null;

async function verDetalhesPedido(pid) {
  const d = await api(`/api/pedidos/${pid}/itens`);
  if (!d || !d.pedido) { toast('Erro ao carregar pedido', 'erro'); return; }

  _pedidoParaImprimir = d;
  const p = d.pedido;
  const statusCls = p.status === 'Pago' ? 'badge-pago' : 'badge-pend';

  const itensHtml = d.itens.map(i => {
    const isPeso = i.por_peso;
    const qtdCol = isPeso
      ? `<span style="color:var(--gold)">carne</span>`
      : i.quantidade;
    const unitLabel = isPeso ? '—' : fmt(i.preco_unit);
    return `
    <tr>
      <td>${i.produto_nome}</td>
      <td style="text-align:center;font-family:var(--font-mono)">${qtdCol}</td>
      <td style="text-align:right;font-family:var(--font-mono);color:var(--muted)">${unitLabel}</td>
      <td style="text-align:right;font-family:var(--font-mono);color:var(--gold)">${fmt(i.subtotal)}</td>
    </tr>`;
  }).join('');

  document.getElementById('modal-pedido-content').innerHTML = `
    <div class="pedido-detail-header">
      <div><span class="pd-label">Mesa</span><span class="pd-val">${p.mesa}</span></div>
      <div><span class="pd-label">Cliente</span><span class="pd-val">${p.cliente_nome || '—'}</span></div>
      <div><span class="pd-label">Data</span><span class="pd-val" style="font-size:13px">${p.criado_em}</span></div>
      <div><span class="pd-label">Status</span><span class="badge ${statusCls}">${p.status}</span></div>
    </div>
    <div class="table-wrap" style="margin-top:16px">
      <table>
        <thead><tr><th>Produto</th><th style="text-align:center">Qtd / Peso</th><th style="text-align:right">Unit.</th><th style="text-align:right">Subtotal</th></tr></thead>
        <tbody>${itensHtml}</tbody>
      </table>
    </div>
    <div class="pedido-total-row">
      <span>TOTAL</span>
      <span style="font-family:var(--font-mono);color:var(--gold);font-size:22px">${fmt(p.total)}</span>
    </div>`;

  document.getElementById('modal-pedido').style.display = 'flex';
}

function fecharModalPedido() {
  document.getElementById('modal-pedido').style.display = 'none';
  _pedidoParaImprimir = null;
}

function imprimirPedido() {
  if (!_pedidoParaImprimir) return;
  const d = _pedidoParaImprimir;
  const p = d.pedido;

  const linhas = d.itens.map(i => {
    const isPeso = i.peso_kg != null && i.peso_kg > 0;
    const qtdStr = isPeso ? `${parseFloat(i.peso_kg).toFixed(3)}kg` : `${i.quantidade}x `;
    const nome = i.produto_nome.substring(0, 20).padEnd(20);
    return `${nome}  ${qtdStr.padStart(8)}  ${fmt(i.subtotal).padStart(12)}`;
  }).join('\n');

  const comanda = `
════════════════════════════════════
      CHURRASCARIA DO RONAN
════════════════════════════════════
Mesa    : ${p.mesa}
Cliente : ${p.cliente_nome || '—'}
Data    : ${p.criado_em}
Status  : ${p.status}
────────────────────────────────────
PRODUTO              QTD       TOTAL
────────────────────────────────────
${linhas}
────────────────────────────────────
TOTAL   :              ${fmt(p.total).padStart(12)}
════════════════════════════════════
       Obrigado pela preferência!
════════════════════════════════════
`;

  const win = window.open('', '_blank', 'width=500,height=640');
  if (!win) { toast('Popup bloqueado. Permita popups.', 'erro'); return; }
  win.document.write(`<html><head><title>Comanda #${p.id}</title>
    <style>
      body { font-family: 'Courier New', monospace; font-size: 13px;
             background:#fff; color:#000; padding:20px; white-space:pre; }
      @media print { body { margin:0; padding:8px; } }
    </style></head><body>${comanda.replace(/\n/g,'<br>')}</body></html>`);
  win.document.close();
  win.focus();
  setTimeout(() => win.print(), 400);
}
