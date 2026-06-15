let produtosLista = [];
let clientesLista = [];
let comanda = {}; // { produto_id: { produto, quantidade, valor_carne } }
let catAtiva = 'Todos';

async function iniciarPedidos() {
  produtosLista = await api('/api/produtos');
  clientesLista = await api('/api/clientes');

  const selCli = document.getElementById('ped-cliente');
  if (selCli) {
    selCli.innerHTML = '<option value="">— Sem cliente —</option>' +
      clientesLista.map(c => `<option value="${c.id}">${c.nome}</option>`).join('');
  }

  renderCategorias();
  renderCardapio();
  carregarPedidos();
}

// ── CATEGORIAS ─────────────────────────────────────────────────
function renderCategorias() {
  const order = ['Todos','Carnes','Frango','Linguiça','Acompanhamentos','Bebidas Alcoólicas','Bebidas Não Alcoólicas','Sobremesas','Outros'];
  const fromDB = new Set(produtosLista.map(p => p.categoria).filter(Boolean));
  const cats = ['Todos', ...order.filter(c => c !== 'Todos' && fromDB.has(c)),
                ...([...fromDB].filter(c => !order.includes(c)))];
  const tabs = document.getElementById('cat-tabs');
  if (!tabs) return;
  tabs.innerHTML = cats.map(c => `
    <button class="cat-tab ${c === catAtiva ? 'active' : ''}" onclick="selecionarCat('${c.replace(/'/g,"\\'")}')">
      ${catEmoji(c)} ${c}
    </button>
  `).join('');
}

function catEmoji(cat) { return ''; }

function selecionarCat(cat) {
  catAtiva = cat;
  renderCategorias();
  renderCardapio();
}

// ── CARDÁPIO GRID ──────────────────────────────────────────────
function renderCardapio(filtro = '') {
  const grid = document.getElementById('cardapio-grid');
  if (!grid) return;
  let lista = produtosLista;

  if (catAtiva !== 'Todos') lista = lista.filter(p => p.categoria === catAtiva);
  if (filtro) lista = lista.filter(p => p.nome.toLowerCase().includes(filtro.toLowerCase()));

  if (!lista.length) {
    grid.innerHTML = '<div style="color:var(--muted);padding:20px;text-align:center;font-family:var(--font-mono);font-size:12px">Nenhum produto encontrado</div>';
    return;
  }

  grid.innerHTML = lista.map(p => {
    const semEstoque   = !p.por_peso && p.estoque <= 0;
    const naComanda    = !!comanda[p.id];
    const precoLabel   = p.por_peso ? `${fmt(p.preco)}/kg` : fmt(p.preco);
    const estoqueLabel = p.por_peso
      ? '<span class="cp-peso-tag">KG</span>'
      : (semEstoque ? 'Esgotado' : `${p.estoque} un`);
    const badge = naComanda
      ? `<div class="cp-badge">${p.por_peso ? 'V' : comanda[p.id].quantidade}</div>`
      : '';
    const clickFn = semEstoque ? '' : (p.por_peso ? `abrirModalPeso(${p.id})` : `adicionarItem(${p.id})`);

    return `
    <div class="card-produto ${semEstoque ? 'sem-estoque' : ''} ${naComanda ? 'na-comanda' : ''}"
         onclick="${clickFn}">
      <div class="cp-cat">${p.categoria}</div>
      <div class="cp-nome">${p.nome}</div>
      <div class="cp-preco">${precoLabel}</div>
      <div class="cp-est ${!p.por_peso && p.estoque <= 5 && p.estoque > 0 ? 'est-baixo' : ''}">${estoqueLabel}</div>
      ${badge}
    </div>`;
  }).join('');
}

function filtrarCardapio(val) {
  renderCardapio(val);
}

// ── MODAL PESO ─────────────────────────────────────────────────
function abrirModalPeso(prodId) {
  const prod = produtosLista.find(p => p.id === prodId);
  if (!prod) return;
  const modal = document.getElementById('modal-peso');
  if (!modal) return;

  document.getElementById('modal-peso-titulo').textContent = prod.nome;
  const inputVal = document.getElementById('modal-peso-kg');
  inputVal.value = comanda[prodId]?.valor_carne || '';
  modal.dataset.prodId = prodId;
  modal.style.display  = 'flex';
  setTimeout(() => inputVal.focus(), 100);
}

function calcularSubtotalPeso() {
  // campo agora é o valor em reais — preview em tempo real
  const val = parseFloat(document.getElementById('modal-peso-kg').value) || 0;
  const el  = document.getElementById('modal-peso-subtotal');
  if (val > 0) {
    el.textContent = `Total: ${fmt(val)}`;
    el.style.color = 'var(--gold)';
  } else {
    el.textContent = '';
  }
}

function confirmarPeso() {
  const modal  = document.getElementById('modal-peso');
  if (!modal) return;
  const prodId = parseInt(modal.dataset.prodId);
  const prod   = produtosLista.find(p => p.id === prodId);
  const valor  = parseFloat(document.getElementById('modal-peso-kg').value);
  if (!valor || valor <= 0) { toast('Informe um valor válido em R$', 'erro'); return; }

  comanda[prodId] = { produto: prod, quantidade: 1, valor_carne: valor };
  modal.style.display = 'none';
  renderComanda();
  renderCardapio(document.getElementById('card-busca')?.value || '');
}

function fecharModalPeso() {
  const modal = document.getElementById('modal-peso');
  if (modal) modal.style.display = 'none';
}

// Enter no campo peso confirma
document.addEventListener('keydown', e => {
  const modal = document.getElementById('modal-peso');
  if (modal && modal.style.display !== 'none' && e.key === 'Enter') {
    confirmarPeso();
  }
});

// ── COMANDA ────────────────────────────────────────────────────
function adicionarItem(prodId) {
  const prod = produtosLista.find(p => p.id === prodId);
  if (!prod) return;

  if (comanda[prodId]) {
    if (comanda[prodId].quantidade >= prod.estoque) {
      toast(`Estoque máximo: ${prod.estoque} un`, 'erro');
      return;
    }
    comanda[prodId].quantidade++;
  } else {
    comanda[prodId] = { produto: prod, quantidade: 1 };
  }

  renderComanda();
  renderCardapio(document.getElementById('card-busca')?.value || '');
}

function alterarQtd(prodId, delta) {
  if (!comanda[prodId]) return;
  if (comanda[prodId].produto.por_peso) { abrirModalPeso(prodId); return; }
  comanda[prodId].quantidade += delta;
  if (comanda[prodId].quantidade <= 0) delete comanda[prodId];
  renderComanda();
  renderCardapio(document.getElementById('card-busca')?.value || '');
}

function removerItemComanda(prodId) {
  delete comanda[prodId];
  renderComanda();
  renderCardapio(document.getElementById('card-busca')?.value || '');
}

function renderComanda() {
  const lista  = document.getElementById('comanda-lista');
  const badge  = document.getElementById('comanda-qtd-badge');
  const itens  = Object.values(comanda);
  if (!lista) return;

  const totalItens = itens.reduce((s, i) => s + (i.produto.por_peso ? 1 : i.quantidade), 0);
  if (badge) badge.textContent = totalItens > 0 ? `(${totalItens})` : '';

  if (!itens.length) {
    lista.innerHTML = '<div class="comanda-empty">Nenhum item adicionado</div>';
    const el = document.getElementById('ped-total');
    if (el) el.textContent = 'R$ 0,00';
    return;
  }

  let total = 0;
  lista.innerHTML = itens.map(({ produto: p, quantidade: q, valor_carne }) => {
    let sub, controles;
    if (p.por_peso) {
      sub    = valor_carne;
      total += sub;
      controles = `
        <button class="ci-btn" onclick="abrirModalPeso(${p.id})" title="Editar valor">Editar</button>
        <span class="ci-qtd" style="min-width:64px">${fmt(sub)}</span>
        <button class="ci-del" onclick="removerItemComanda(${p.id})" title="Remover">✕</button>`;
    } else {
      sub    = p.preco * q;
      total += sub;
      controles = `
        <button class="ci-btn" onclick="alterarQtd(${p.id}, -1)">−</button>
        <span class="ci-qtd">${q}</span>
        <button class="ci-btn" onclick="alterarQtd(${p.id}, 1)">+</button>
        <span class="ci-sub">${fmt(sub)}</span>
        <button class="ci-del" onclick="removerItemComanda(${p.id})" title="Remover">✕</button>`;
    }

    const precoRef = p.por_peso ? 'Valor informado' : `${fmt(p.preco)} un`;
    return `
    <div class="comanda-item">
      <div class="ci-info">
        <div class="ci-nome">${p.nome}</div>
        <div class="ci-preco">${precoRef}</div>
      </div>
      <div class="ci-controles">${controles}</div>
    </div>`;
  }).join('');

  const totalEl = document.getElementById('ped-total');
  if (totalEl) totalEl.textContent = fmt(total);
}

// ── REGISTRAR ──────────────────────────────────────────────────
async function registrarPedido() {
  const mesa       = document.getElementById('ped-mesa')?.value;
  const cliente_id = document.getElementById('ped-cliente')?.value || null;

  if (!mesa)                          { toast('Selecione a mesa', 'erro'); return; }
  if (!Object.keys(comanda).length)   { toast('Adicione pelo menos um item', 'erro'); return; }

  const itens = Object.entries(comanda).map(([produto_id, { quantidade, valor_carne }]) => ({
    produto_id: parseInt(produto_id),
    quantidade,
    valor_carne: valor_carne || null
  }));

  const r = await api('/api/pedidos', 'POST', { mesa, cliente_id, itens });
  if (r.ok) {
    toast(`Pedido registrado! Total: ${fmt(r.total)}`);
    comanda = {};
    if (document.getElementById('ped-mesa')) document.getElementById('ped-mesa').value = '';
    if (document.getElementById('ped-cliente')) document.getElementById('ped-cliente').value = '';
    const busca = document.getElementById('card-busca');
    if (busca) busca.value = '';
    catAtiva = 'Todos';
    renderCategorias();
    renderCardapio();
    renderComanda();
    produtosLista = await api('/api/produtos');
    renderCardapio();
    carregarPedidos();
  } else {
    toast(r.msg || 'Erro ao registrar pedido', 'erro');
  }
}

// ── LISTA DE PEDIDOS ───────────────────────────────────────────
async function carregarPedidos() {
  const status = document.getElementById('ped-filtro-status')?.value || '';
  const q      = document.getElementById('ped-busca')?.value.trim() || '';
  let url = '/api/pedidos';
  const ps = [];
  if (status) ps.push(`status=${encodeURIComponent(status)}`);
  if (q)      ps.push(`q=${encodeURIComponent(q)}`);
  if (ps.length) url += '?' + ps.join('&');

  const rows  = await api(url);
  const tbody = document.getElementById('pedidos-tbody');
  const count = document.getElementById('ped-count');
  if (!tbody) return;

  if (count) count.textContent = `(${rows.length})`;

  if (!rows.length) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="7">Nenhum pedido encontrado</td></tr>';
    return;
  }
  tbody.innerHTML = rows.map(p => `
    <tr>
      <td style="color:var(--muted);font-family:var(--font-mono);font-size:12px">#${p.id}</td>
      <td><strong>${p.mesa}</strong></td>
      <td>${p.cliente_nome || '<span style="color:var(--muted)">—</span>'}</td>
      <td style="font-family:var(--font-mono);color:var(--gold)">${fmt(p.total)}</td>
      <td><span class="badge ${p.status==='Pago'?'badge-pago':'badge-pend'}">${p.status}</span></td>
      <td style="color:var(--muted);font-size:12px;white-space:nowrap">${p.criado_em}</td>
      <td class="td-actions">
        <button class="btn-sm btn-edit" onclick="verDetalhesPedido(${p.id})">Detalhes</button>
        ${p.status!=='Pago'?`<button class="btn-sm btn-ok" onclick="pagarPedido(${p.id})">Pagar</button>`:''}
        <button class="btn-sm btn-del" onclick="delPedido(${p.id})">Remover</button>
      </td>
    </tr>`).join('');
}

async function pagarPedido(id) {
  if (!confirm('Confirmar pagamento deste pedido?')) return;
  const r = await api(`/api/pedidos/${id}/pagar`, 'PUT');
  if (r.ok) toast(r.msg || 'Pedido marcado como pago!');
  else toast(r.msg || 'Erro ao pagar pedido', 'erro');
  carregarPedidos();
}

async function delPedido(id) {
  if (!confirm('Remover este pedido? O estoque será reabastecido.')) return;
  const r = await api(`/api/pedidos/${id}`, 'DELETE');
  if (r.ok) toast('Pedido removido');
  else toast(r.msg || 'Erro ao remover', 'erro');
  produtosLista = await api('/api/produtos');
  renderCardapio(document.getElementById('card-busca')?.value || '');
  carregarPedidos();
}

// ── INICIALIZAR ────────────────────────────────────────────────
let buscaTimer;
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('ped-busca')?.addEventListener('input', () => {
    clearTimeout(buscaTimer);
    buscaTimer = setTimeout(carregarPedidos, 300);
  });
  document.getElementById('ped-filtro-status')?.addEventListener('change', carregarPedidos);
  iniciarPedidos();
});
