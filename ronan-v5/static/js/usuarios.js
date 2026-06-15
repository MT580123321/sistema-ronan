async function carregarUsuarios() {
  const rows  = await api('/api/usuarios');
  const tbody = document.getElementById('usuarios-tbody');

  if (!rows.length) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="4">Nenhum usuário</td></tr>';
    return;
  }

  // Detecta o usuário logado pelo nome exibido no sidebar
  const nomeLogado = document.querySelector('.user-name')?.textContent.trim() || '';

  tbody.innerHTML = rows.map((u, i) => {
    const isMe  = u.username === nomeLogado;
    const badge = u.nivel === 'admin' ? 'badge-pago' : 'badge-pend';
    return `
    <tr>
      <td style="color:var(--muted);font-family:var(--font-mono)">${i+1}</td>
      <td><strong>${u.username}</strong> ${isMe ? '<span class="badge badge-ok" style="font-size:10px">você</span>' : ''}</td>
      <td><span class="badge ${badge}">${u.nivel}</span></td>
      <td style="color:var(--muted);font-size:13px">${u.criado_em}</td>
      <td class="td-actions">
        <button class="btn-sm btn-edit" onclick="abrirResetSenha(${u.id}, '${u.username}')">Redefinir Senha</button>
        ${!isMe ? `<button class="btn-sm btn-del" onclick="delUsuario(${u.id}, '${u.username}')">Remover</button>` : ''}
      </td>
    </tr>`;
  }).join('');
}

async function addUsuario() {
  const username = document.getElementById('usu-nome').value.trim();
  const senha    = document.getElementById('usu-senha').value.trim();
  const nivel    = document.getElementById('usu-nivel').value;
  if (!username || !senha) { toast('Preencha usuário e senha', 'erro'); return; }

  const r = await api('/api/usuarios', 'POST', { username, senha, nivel });
  if (r.ok) {
    toast(r.msg);
    document.getElementById('usu-nome').value  = '';
    document.getElementById('usu-senha').value = '';
    carregarUsuarios();
  } else {
    toast(r.msg, 'erro');
  }
}

async function delUsuario(id, nome) {
  if (!confirm(`Remover usuário "${nome}"?`)) return;
  const r = await api(`/api/usuarios/${id}`, 'DELETE');
  if (r.ok) toast(r.msg);
  else toast(r.msg, 'erro');
  carregarUsuarios();
}

function abrirResetSenha(id, nome) {
  document.getElementById('rs-id').value = id;
  document.getElementById('rs-nome').textContent = nome;
  document.getElementById('rs-senha').value = '';
  document.getElementById('modal-reset-senha').style.display = 'flex';
  setTimeout(() => document.getElementById('rs-senha').focus(), 50);
}

function fecharResetSenha() {
  document.getElementById('modal-reset-senha').style.display = 'none';
}

async function salvarResetSenha() {
  const id    = document.getElementById('rs-id').value;
  const senha = document.getElementById('rs-senha').value.trim();
  if (!senha) { toast('Digite a nova senha', 'erro'); return; }
  const r = await api(`/api/usuarios/${id}/reset-senha`, 'PUT', { senha });
  if (r.ok) { toast(r.msg); fecharResetSenha(); }
  else toast(r.msg, 'erro');
}

document.addEventListener('click', e => {
  const m = document.getElementById('modal-reset-senha');
  if (m && e.target === m) fecharResetSenha();
});

document.addEventListener('DOMContentLoaded', carregarUsuarios);
