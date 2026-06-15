//  HELPERS 
function atualizarLabelPreco(catSelectId, labelId) {
  const cat      = document.getElementById(catSelectId)?.value || '';
  const pesoBool = document.getElementById(
    catSelectId === 'prod-cat' ? 'prod-por-peso' : 'ep-por-peso'
  )?.value === '1';
  const lbl = document.getElementById(labelId);
  if (lbl) lbl.textContent = pesoBool ? 'Preço (R$/kg)' : 'Preço (R$/un)';
  // mostra/esconde dica
  const hint = document.getElementById('prod-peso-hint');
  if (hint) hint.style.display = pesoBool ? 'block' : 'none';
}

//  LISTAR 
async function carregarProdutos(q = '', cat = '') {
  let url = '/api/produtos';
  const params = [];
  if (q)   params.push(`q=${encodeURIComponent(q)}`);
  if (cat) params.push(`cat=${encodeURIComponent(cat)}`);
  if (params.length) url += '?' + params.join('&');

  const rows = await api(url);
  const tbody = document.getElementById('produtos-tbody');
  document.getElementById('prod-count').textContent = `(${rows.length})`;

  if (!rows.length) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="7">Nenhum produto encontrado</td></tr>';
    return;
  }
  tbody.innerHTML = rows.map((p, i) => {
    const sit       = p.estoque > 10 ? 'badge-ok' : p.estoque > 5 ? 'badge-warn' : 'badge-low';
    const pesoLabel = p.por_peso ? '<span class="badge badge-pend">Kg</span>' : '<span class="badge badge-muted">Un</span>';
    const precoFmt  = p.por_peso ? `${fmt(p.preco)}/kg` : fmt(p.preco);
    return `
    <tr>
      <td style="color:var(--muted);font-family:var(--font-mono)">${i+1}</td>
      <td><strong>${p.nome}</strong></td>
      <td><span class="badge badge-pend">${p.categoria}</span></td>
      <td style="font-family:var(--font-mono);color:var(--gold)">${precoFmt}</td>
      <td>${pesoLabel}</td>
      <td><span class="badge ${sit}">${p.por_peso ? '—' : p.estoque + ' un'}</span></td>
      <td class="td-actions">
        <button class="btn-sm btn-edit"
          data-id="${p.id}"
          data-nome="${encodeURIComponent(p.nome)}"
          data-preco="${p.preco}"
          data-est="${p.estoque}"
          data-cat="${encodeURIComponent(p.categoria)}"
          data-por-peso="${p.por_peso || 0}"
          onclick="abrirEditProduto(this)">Editar</button>
        <button class="btn-sm btn-del" onclick="delProduto(${p.id})">Remover</button>
      </td>
    </tr>`;
  }).join('');
}

function getFiltros() {
  return {
    q:   (document.getElementById('prod-busca')?.value || '').trim(),
    cat: document.getElementById('prod-filtro-cat')?.value || ''
  };
}

//  ADICIONAR 
async function addProduto() {
  const nome     = document.getElementById('prod-nome').value.trim();
  const preco    = parseFloat(document.getElementById('prod-preco').value);
  const estoque  = parseInt(document.getElementById('prod-estoque').value) || 0;
  const cat      = document.getElementById('prod-cat').value;
  const por_peso = document.getElementById('prod-por-peso').value === '1';
  if (!nome || isNaN(preco) || preco < 0) { toast('Preencha nome e preço válido', 'erro'); return; }

  const r = await api('/api/produtos', 'POST', { nome, preco, estoque, categoria: cat, por_peso });
  if (r.ok) {
    toast(r.msg);
    document.getElementById('prod-nome').value     = '';
    document.getElementById('prod-preco').value    = '';
    document.getElementById('prod-estoque').value  = '';
    document.getElementById('prod-por-peso').value = '0';
    atualizarLabelPreco('prod-cat', 'prod-preco-label');
    const f = getFiltros();
    carregarProdutos(f.q, f.cat);
  } else {
    toast(r.msg, 'erro');
  }
}

//  EDITAR 
function abrirEditProduto(btn) {
  const id       = btn.dataset.id;
  const nome     = decodeURIComponent(btn.dataset.nome);
  const preco    = btn.dataset.preco;
  const est      = btn.dataset.est;
  const cat      = decodeURIComponent(btn.dataset.cat || '');
  const porPeso  = btn.dataset.porPeso || '0';
  document.getElementById('ep-id').value        = id;
  document.getElementById('ep-nome').value      = nome;
  document.getElementById('ep-preco').value     = preco;
  document.getElementById('ep-est').value       = est;
  document.getElementById('ep-por-peso').value  = porPeso;
  const selCat = document.getElementById('ep-cat');
  if (selCat) for (let opt of selCat.options) opt.selected = opt.value === cat;
  atualizarLabelPreco('ep-cat', 'ep-preco-label');
  document.getElementById('modal-edit').style.display = 'flex';
}

async function salvarEditProduto() {
  const id       = document.getElementById('ep-id').value;
  const nome     = document.getElementById('ep-nome').value.trim();
  const preco    = parseFloat(document.getElementById('ep-preco').value);
  const est      = parseInt(document.getElementById('ep-est').value) || 0;
  const cat      = document.getElementById('ep-cat')?.value;
  const por_peso = document.getElementById('ep-por-peso').value === '1';
  if (!nome || isNaN(preco)) { toast('Preencha nome e preço', 'erro'); return; }
  const body = { nome, preco, estoque: est, por_peso };
  if (cat) body.categoria = cat;
  const r = await api(`/api/produtos/${id}`, 'PUT', body);
  if (r.ok) {
    toast(r.msg); fecharModal();
    const f = getFiltros();
    carregarProdutos(f.q, f.cat);
  } else toast(r.msg, 'erro');
}

async function delProduto(id) {
  if (!confirm('Remover produto?')) return;
  await api(`/api/produtos/${id}`, 'DELETE');
  toast('Produto removido');
  const f = getFiltros();
  carregarProdutos(f.q, f.cat);
}

let buscaTimer;
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('prod-busca')?.addEventListener('input', () => {
    clearTimeout(buscaTimer);
    buscaTimer = setTimeout(() => { const f = getFiltros(); carregarProdutos(f.q, f.cat); }, 300);
  });
  document.getElementById('prod-filtro-cat')?.addEventListener('change', () => {
    const f = getFiltros(); carregarProdutos(f.q, f.cat);
  });
  document.getElementById('prod-por-peso')?.addEventListener('change', () => {
    atualizarLabelPreco('prod-cat', 'prod-preco-label');
  });
});

carregarProdutos();
