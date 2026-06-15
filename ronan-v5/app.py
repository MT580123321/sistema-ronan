from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'ronan_churrascaria_2025_seguro'

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'ronan.db')
SCHEMA  = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')

# ── BANCO ──────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as conn:
        with open(SCHEMA, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        # Cria usuários padrão se não existirem
        exists = conn.execute("SELECT id FROM usuarios WHERE username='admin'").fetchone()
        if not exists:
            conn.execute("INSERT INTO usuarios (username, senha, nivel) VALUES (?,?,?)",
                ('admin', generate_password_hash('ronan2025'), 'admin'))
        garcom = conn.execute("SELECT id FROM usuarios WHERE username='garcom'").fetchone()
        if not garcom:
            conn.execute("INSERT INTO usuarios (username, senha, nivel) VALUES (?,?,?)",
                ('garcom', generate_password_hash('ronan2025'), 'operador'))
        conn.commit()

init_db()

# ── AUTH ───────────────────────────────────────────────────────
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'ok': False, 'msg': 'Não autenticado'}), 401
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('nivel') != 'admin':
            return jsonify({'ok': False, 'msg': 'Acesso negado: apenas administradores'}), 403
        return f(*args, **kwargs)
    return decorated

# ── PÁGINAS ────────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('base.html', pagina='dashboard', usuario=session.get('user'), nivel=session.get('nivel'))

@app.route('/clientes')
@login_required
def clientes_page():
    return render_template('base.html', pagina='clientes', usuario=session.get('user'), nivel=session.get('nivel'))

@app.route('/produtos')
@login_required
def produtos_page():
    return render_template('base.html', pagina='produtos', usuario=session.get('user'), nivel=session.get('nivel'))

@app.route('/pedidos')
@login_required
def pedidos_page():
    return render_template('base.html', pagina='pedidos', usuario=session.get('user'), nivel=session.get('nivel'))

@app.route('/estoque')
@login_required
def estoque_page():
    if session.get('nivel') != 'admin':
        return redirect(url_for('pedidos_page'))
    return render_template('base.html', pagina='estoque', usuario=session.get('user'), nivel=session.get('nivel'))

@app.route('/relatorios')
@login_required
def relatorios_page():
    if session.get('nivel') != 'admin':
        return redirect(url_for('pedidos_page'))
    return render_template('base.html', pagina='relatorios', usuario=session.get('user'), nivel=session.get('nivel'))

@app.route('/usuarios')
@login_required
def usuarios_page():
    if session.get('nivel') != 'admin':
        return redirect(url_for('pedidos_page'))
    return render_template('base.html', pagina='usuarios', usuario=session.get('user'), nivel=session.get('nivel'))

# ── API AUTH ───────────────────────────────────────────────────
@app.route('/api/login', methods=['POST'])
def api_login():
    data  = request.get_json()
    user  = data.get('username', '').strip()
    senha = data.get('senha', '')
    with get_db() as conn:
        row = conn.execute(
            'SELECT * FROM usuarios WHERE username=?', (user,)
        ).fetchone()
    if row and check_password_hash(row['senha'], senha):
        session['user']  = user
        session['nivel'] = row['nivel']
        return jsonify({'ok': True, 'nivel': row['nivel']})
    return jsonify({'ok': False, 'msg': 'Usuário ou senha inválidos'}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'ok': True})

@app.route('/api/trocar-senha', methods=['POST'])
@login_required
def api_trocar_senha():
    d        = request.get_json()
    atual    = d.get('atual', '')
    nova     = d.get('nova', '').strip()
    confirma = d.get('confirma', '').strip()
    if not nova or len(nova) < 4:
        return jsonify({'ok': False, 'msg': 'Nova senha deve ter ao menos 4 caracteres'}), 400
    if nova != confirma:
        return jsonify({'ok': False, 'msg': 'Confirmação não confere'}), 400
    with get_db() as conn:
        row = conn.execute('SELECT senha FROM usuarios WHERE username=?', (session['user'],)).fetchone()
        if not row or not check_password_hash(row['senha'], atual):
            return jsonify({'ok': False, 'msg': 'Senha atual incorreta'}), 400
        conn.execute('UPDATE usuarios SET senha=? WHERE username=?',
                     (generate_password_hash(nova), session['user']))
        conn.commit()
    return jsonify({'ok': True, 'msg': 'Senha alterada com sucesso!'})

# ── API USUÁRIOS ───────────────────────────────────────────────
@app.route('/api/usuarios', methods=['GET'])
@login_required
def api_usuarios_get():
    with get_db() as conn:
        rows = conn.execute('SELECT id, username, nivel, criado_em FROM usuarios ORDER BY id').fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/usuarios', methods=['POST'])
@login_required
@admin_required
def api_usuarios_post():
    d     = request.get_json()
    user  = d.get('username', '').strip()
    senha = d.get('senha', '').strip()
    nivel = d.get('nivel', 'operador')
    if not user or not senha or len(senha) < 4:
        return jsonify({'ok': False, 'msg': 'Usuário e senha (mín. 4 chars) obrigatórios'}), 400
    if nivel not in ('admin', 'operador'):
        return jsonify({'ok': False, 'msg': 'Nível inválido'}), 400
    with get_db() as conn:
        existe = conn.execute('SELECT id FROM usuarios WHERE username=?', (user,)).fetchone()
        if existe:
            return jsonify({'ok': False, 'msg': 'Usuário já existe'}), 400
        conn.execute('INSERT INTO usuarios (username, senha, nivel) VALUES (?,?,?)',
                     (user, generate_password_hash(senha), nivel))
        conn.commit()
    return jsonify({'ok': True, 'msg': f'Usuário {user} criado!'})

@app.route('/api/usuarios/<int:uid>', methods=['DELETE'])
@login_required
@admin_required
def api_usuarios_del(uid):
    with get_db() as conn:
        row = conn.execute('SELECT username FROM usuarios WHERE id=?', (uid,)).fetchone()
        if not row:
            return jsonify({'ok': False, 'msg': 'Usuário não encontrado'}), 404
        if row['username'] == session['user']:
            return jsonify({'ok': False, 'msg': 'Você não pode remover seu próprio usuário'}), 400
        # Impede remover o último admin
        admins = conn.execute("SELECT COUNT(*) as n FROM usuarios WHERE nivel='admin'").fetchone()['n']
        nivel_alvo = conn.execute("SELECT nivel FROM usuarios WHERE id=?", (uid,)).fetchone()['nivel']
        if nivel_alvo == 'admin' and admins <= 1:
            return jsonify({'ok': False, 'msg': 'Não é possível remover o único administrador'}), 400
        conn.execute('DELETE FROM usuarios WHERE id=?', (uid,))
        conn.commit()
    return jsonify({'ok': True, 'msg': 'Usuário removido!'})

@app.route('/api/usuarios/<int:uid>/reset-senha', methods=['PUT'])
@login_required
@admin_required
def api_usuarios_reset_senha(uid):
    d         = request.get_json()
    nova_senha = d.get('senha', '').strip()
    if not nova_senha or len(nova_senha) < 4:
        return jsonify({'ok': False, 'msg': 'Senha deve ter ao menos 4 caracteres'}), 400
    with get_db() as conn:
        conn.execute('UPDATE usuarios SET senha=? WHERE id=?',
                     (generate_password_hash(nova_senha), uid))
        conn.commit()
    return jsonify({'ok': True, 'msg': 'Senha redefinida!'})

# ── API DASHBOARD ──────────────────────────────────────────────
@app.route('/api/dashboard')
@login_required
def api_dashboard():
    with get_db() as conn:
        clientes  = conn.execute('SELECT COUNT(*) as n FROM clientes').fetchone()['n']
        produtos  = conn.execute('SELECT COUNT(*) as n FROM produtos').fetchone()['n']
        pedidos   = conn.execute('SELECT COUNT(*) as n FROM pedidos').fetchone()['n']
        estoque   = conn.execute('SELECT COUNT(*) as n FROM estoque').fetchone()['n']
        total_vendas = conn.execute("SELECT COALESCE(SUM(total),0) as t FROM pedidos").fetchone()['t']
        recebido = conn.execute("SELECT COALESCE(SUM(total),0) as t FROM pedidos WHERE status='Pago'").fetchone()['t']
        pendente = conn.execute("SELECT COALESCE(SUM(total),0) as t FROM pedidos WHERE status='Pendente'").fetchone()['t']
        est_baixo = conn.execute('SELECT COUNT(*) as n FROM estoque WHERE quantidade <= 5').fetchone()['n']
        ultimos = conn.execute('''
            SELECT p.id, p.mesa, p.status, p.total, p.criado_em,
                   c.nome as cliente_nome
            FROM pedidos p
            LEFT JOIN clientes c ON c.id = p.cliente_id
            ORDER BY p.id DESC LIMIT 5
        ''').fetchall()
    return jsonify({
        'clientes': clientes, 'produtos': produtos,
        'pedidos': pedidos, 'estoque': estoque,
        'total_vendas': total_vendas, 'recebido': recebido,
        'pendente': pendente, 'est_baixo': est_baixo,
        'ultimos': [dict(r) for r in ultimos]
    })

# ── API CLIENTES ───────────────────────────────────────────────
@app.route('/api/clientes', methods=['GET'])
@login_required
def api_clientes_get():
    q = request.args.get('q', '').strip()
    with get_db() as conn:
        if q:
            like = f'%{q}%'
            rows = conn.execute(
                'SELECT * FROM clientes WHERE nome LIKE ? OR telefone LIKE ? OR cpf LIKE ? ORDER BY id DESC',
                (like, like, like)
            ).fetchall()
        else:
            rows = conn.execute('SELECT * FROM clientes ORDER BY id DESC').fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/clientes', methods=['POST'])
@login_required
def api_clientes_post():
    d    = request.get_json()
    nome = d.get('nome','').strip()
    tel  = d.get('telefone','').strip()
    cpf  = d.get('cpf','').strip()
    if not nome or not tel:
        return jsonify({'ok': False, 'msg': 'Nome e telefone obrigatórios'}), 400
    with get_db() as conn:
        conn.execute('INSERT INTO clientes (nome,telefone,cpf) VALUES (?,?,?)', (nome,tel,cpf))
        conn.commit()
    return jsonify({'ok': True, 'msg': 'Cliente cadastrado!'})

@app.route('/api/clientes/<int:cid>', methods=['DELETE'])
@login_required
def api_clientes_del(cid):
    with get_db() as conn:
        n = conn.execute('SELECT COUNT(*) as n FROM pedidos WHERE cliente_id=?', (cid,)).fetchone()['n']
        if n > 0:
            return jsonify({'ok': False, 'msg': f'Não é possível remover: cliente possui {n} pedido(s)'}), 400
        conn.execute('DELETE FROM clientes WHERE id=?', (cid,))
        conn.commit()
    return jsonify({'ok': True, 'msg': 'Cliente removido!'})

# ── API PRODUTOS ───────────────────────────────────────────────
@app.route('/api/produtos', methods=['GET'])
@login_required
def api_produtos_get():
    q   = request.args.get('q', '').strip()
    cat = request.args.get('cat', '').strip()
    with get_db() as conn:
        sql    = 'SELECT p.*, COALESCE(e.quantidade,0) as estoque FROM produtos p LEFT JOIN estoque e ON e.produto_id = p.id WHERE 1=1'
        params = []
        if q:
            sql += ' AND p.nome LIKE ?'
            params.append(f'%{q}%')
        if cat:
            sql += ' AND p.categoria=?'
            params.append(cat)
        sql += ' ORDER BY p.id DESC'
        rows = conn.execute(sql, params).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/produtos', methods=['POST'])
@login_required
def api_produtos_post():
    d        = request.get_json()
    nome     = d.get('nome','').strip()
    preco    = d.get('preco', 0)
    cat      = d.get('categoria','Outros')
    qtd      = int(d.get('estoque', 0))
    por_peso = 1 if d.get('por_peso') else 0
    if not nome or float(preco) < 0:
        return jsonify({'ok': False, 'msg': 'Nome e preço obrigatórios'}), 400
    with get_db() as conn:
        cur = conn.execute('INSERT INTO produtos (nome,preco,categoria,por_peso) VALUES (?,?,?,?)', (nome, preco, cat, por_peso))
        pid = cur.lastrowid
        conn.execute('INSERT INTO estoque (produto_id, quantidade) VALUES (?,?)', (pid, qtd))
        conn.commit()
    return jsonify({'ok': True, 'msg': 'Produto cadastrado!'})

@app.route('/api/produtos/<int:pid>', methods=['PUT'])
@login_required
def api_produtos_put(pid):
    d        = request.get_json()
    nome     = d.get('nome','').strip()
    preco    = d.get('preco', 0)
    cat      = d.get('categoria')
    qtd      = int(d.get('estoque', 0))
    por_peso = 1 if d.get('por_peso') else 0
    if not nome:
        return jsonify({'ok': False, 'msg': 'Nome obrigatório'}), 400
    with get_db() as conn:
        if cat:
            conn.execute('UPDATE produtos SET nome=?, preco=?, categoria=?, por_peso=? WHERE id=?', (nome, preco, cat, por_peso, pid))
        else:
            conn.execute('UPDATE produtos SET nome=?, preco=?, por_peso=? WHERE id=?', (nome, preco, por_peso, pid))
        conn.execute('''
            INSERT INTO estoque (produto_id, quantidade, atualizado_em)
            VALUES (?, ?, datetime("now","localtime"))
            ON CONFLICT(produto_id) DO UPDATE SET
                quantidade=excluded.quantidade,
                atualizado_em=excluded.atualizado_em
        ''', (pid, qtd))
        conn.commit()
    return jsonify({'ok': True, 'msg': 'Produto atualizado!'})

@app.route('/api/produtos/<int:pid>', methods=['DELETE'])
@login_required
def api_produtos_del(pid):
    with get_db() as conn:
        conn.execute('DELETE FROM produtos WHERE id=?', (pid,))
        conn.commit()
    return jsonify({'ok': True})

# ── API PEDIDOS ────────────────────────────────────────────────
@app.route('/api/pedidos', methods=['GET'])
@login_required
def api_pedidos_get():
    status = request.args.get('status', '').strip()
    q      = request.args.get('q', '').strip()
    with get_db() as conn:
        sql    = '''SELECT p.*, c.nome as cliente_nome FROM pedidos p
                    LEFT JOIN clientes c ON c.id = p.cliente_id WHERE 1=1'''
        params = []
        if status:
            sql += ' AND p.status=?'
            params.append(status)
        if q:
            sql += ' AND (p.mesa LIKE ? OR c.nome LIKE ?)'
            params.extend([f'%{q}%', f'%{q}%'])
        sql += ' ORDER BY p.id DESC'
        rows = conn.execute(sql, params).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/pedidos/<int:pid>/itens', methods=['GET'])
@login_required
def api_pedidos_itens(pid):
    with get_db() as conn:
        pedido = conn.execute('''
            SELECT p.*, c.nome as cliente_nome
            FROM pedidos p LEFT JOIN clientes c ON c.id = p.cliente_id
            WHERE p.id=?
        ''', (pid,)).fetchone()
        if not pedido:
            return jsonify({'ok': False, 'msg': 'Pedido não encontrado'}), 404
        itens = conn.execute('''
            SELECT i.*, pr.nome as produto_nome
            FROM itens_pedido i
            JOIN produtos pr ON pr.id = i.produto_id
            WHERE i.pedido_id=?
        ''', (pid,)).fetchall()
    return jsonify({
        'pedido': dict(pedido),
        'itens':  [dict(i) for i in itens]
    })

@app.route('/api/pedidos', methods=['POST'])
@login_required
def api_pedidos_post():
    d          = request.get_json()
    mesa       = d.get('mesa','').strip()
    cliente_id = d.get('cliente_id') or None
    itens      = d.get('itens', [])
    if not mesa or not itens:
        return jsonify({'ok': False, 'msg': 'Mesa e itens obrigatórios'}), 400
    with get_db() as conn:
        ids          = list({int(item['produto_id']) for item in itens})
        placeholders = ','.join('?' * len(ids))
        prods_map    = {
            r['id']: r for r in conn.execute(
                f'SELECT p.id, p.nome, p.preco, p.por_peso, COALESCE(e.quantidade,0) as estoque '
                f'FROM produtos p LEFT JOIN estoque e ON e.produto_id=p.id '
                f'WHERE p.id IN ({placeholders})', ids
            ).fetchall()
        }
        total = 0
        for item in itens:
            item_pid = int(item['produto_id'])
            prod     = prods_map.get(item_pid)
            if not prod:
                return jsonify({'ok': False, 'msg': 'Produto não encontrado'}), 400
            if prod['por_peso']:
                valor_carne = float(item.get('valor_carne', 0))
                if valor_carne <= 0:
                    return jsonify({'ok': False, 'msg': f'Informe o valor de {prod["nome"]}'}), 400
                total += valor_carne
            else:
                qtd = int(item['quantidade'])
                if prod['estoque'] < qtd:
                    return jsonify({'ok': False, 'msg': f'Estoque insuficiente para {prod["nome"]}'}), 400
                total += prod['preco'] * qtd
        cur       = conn.execute('INSERT INTO pedidos (cliente_id, mesa, total) VALUES (?,?,?)', (cliente_id, mesa, total))
        pedido_id = cur.lastrowid
        for item in itens:
            item_pid = int(item['produto_id'])
            prod     = prods_map[item_pid]
            if prod['por_peso']:
                valor_carne = float(item.get('valor_carne', 0))
                conn.execute(
                    'INSERT INTO itens_pedido (pedido_id,produto_id,quantidade,peso_kg,preco_unit,subtotal) VALUES (?,?,?,?,?,?)',
                    (pedido_id, item_pid, 1, None, prod['preco'], valor_carne)
                )
                # produtos por peso não baixam estoque unitário
            else:
                qtd = int(item['quantidade'])
                conn.execute(
                    'INSERT INTO itens_pedido (pedido_id,produto_id,quantidade,peso_kg,preco_unit,subtotal) VALUES (?,?,?,?,?,?)',
                    (pedido_id, item_pid, qtd, None, prod['preco'], prod['preco']*qtd)
                )
                conn.execute(
                    'UPDATE estoque SET quantidade=quantidade-?, atualizado_em=datetime("now","localtime") WHERE produto_id=?',
                    (qtd, item_pid)
                )
        conn.commit()
    return jsonify({'ok': True, 'msg': 'Pedido registrado!', 'total': total})

@app.route('/api/pedidos/<int:pid>/pagar', methods=['PUT'])
@login_required
def api_pedidos_pagar(pid):
    with get_db() as conn:
        row = conn.execute('SELECT status FROM pedidos WHERE id=?', (pid,)).fetchone()
        if not row:
            return jsonify({'ok': False, 'msg': 'Pedido não encontrado'}), 404
        if row['status'] == 'Pago':
            return jsonify({'ok': False, 'msg': 'Pedido já está pago'}), 400
        conn.execute("UPDATE pedidos SET status='Pago' WHERE id=?", (pid,))
        conn.commit()
    return jsonify({'ok': True, 'msg': 'Pedido marcado como pago!'})

@app.route('/api/pedidos/<int:pid>', methods=['DELETE'])
@login_required
def api_pedidos_del(pid):
    with get_db() as conn:
        itens = conn.execute(
            'SELECT i.produto_id, i.quantidade, i.peso_kg, p.por_peso '
            'FROM itens_pedido i JOIN produtos p ON p.id=i.produto_id WHERE i.pedido_id=?',
            (pid,)
        ).fetchall()
        for item in itens:
            if not item['por_peso'] and item['peso_kg'] is None:
                conn.execute(
                    'UPDATE estoque SET quantidade=quantidade+?, atualizado_em=datetime("now","localtime") WHERE produto_id=?',
                    (item['quantidade'], item['produto_id'])
                )
        conn.execute('DELETE FROM pedidos WHERE id=?', (pid,))
        conn.commit()
    return jsonify({'ok': True})

# ── API ESTOQUE ────────────────────────────────────────────────
@app.route('/api/estoque', methods=['GET'])
@login_required
def api_estoque_get():
    q = request.args.get('q', '').strip()
    with get_db() as conn:
        if q:
            rows = conn.execute('''
                SELECT e.*, p.nome, p.categoria FROM estoque e
                JOIN produtos p ON p.id = e.produto_id
                WHERE p.nome LIKE ? OR p.categoria LIKE ?
                ORDER BY e.quantidade ASC
            ''', (f'%{q}%', f'%{q}%')).fetchall()
        else:
            rows = conn.execute('''
                SELECT e.*, p.nome, p.categoria FROM estoque e
                JOIN produtos p ON p.id = e.produto_id
                ORDER BY e.quantidade ASC
            ''').fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/estoque/<int:pid>', methods=['PUT'])
@login_required
def api_estoque_put(pid):
    d   = request.get_json()
    qtd = int(d.get('quantidade', 0))
    if qtd < 0:
        return jsonify({'ok': False, 'msg': 'Quantidade não pode ser negativa'}), 400
    with get_db() as conn:
        conn.execute(
            'UPDATE estoque SET quantidade=?, atualizado_em=datetime("now","localtime") WHERE produto_id=?',
            (qtd, pid)
        )
        conn.commit()
    return jsonify({'ok': True, 'msg': 'Estoque atualizado!'})

# ── API RELATÓRIOS ─────────────────────────────────────────────
@app.route('/api/relatorios')
@login_required
def api_relatorios():
    with get_db() as conn:
        resumo = conn.execute('''
            SELECT
                (SELECT COUNT(*) FROM clientes) as total_clientes,
                (SELECT COUNT(*) FROM produtos) as total_produtos,
                (SELECT COUNT(*) FROM pedidos) as total_pedidos,
                (SELECT COUNT(*) FROM pedidos WHERE status='Pago') as pagos,
                (SELECT COUNT(*) FROM pedidos WHERE status='Pendente') as pendentes,
                (SELECT COALESCE(SUM(total),0) FROM pedidos) as total_vendas,
                (SELECT COALESCE(SUM(total),0) FROM pedidos WHERE status='Pago') as recebido,
                (SELECT COALESCE(SUM(total),0) FROM pedidos WHERE status='Pendente') as a_receber
        ''').fetchone()
        top_produtos = conn.execute('''
            SELECT p.nome, SUM(i.quantidade) as total_vendido, SUM(i.subtotal) as receita
            FROM itens_pedido i JOIN produtos p ON p.id = i.produto_id
            GROUP BY p.id ORDER BY total_vendido DESC LIMIT 5
        ''').fetchall()
        est_critico = conn.execute('''
            SELECT p.nome, e.quantidade FROM estoque e
            JOIN produtos p ON p.id = e.produto_id
            WHERE e.quantidade <= 5 ORDER BY e.quantidade ASC
        ''').fetchall()
    return jsonify({
        'resumo':       dict(resumo),
        'top_produtos': [dict(r) for r in top_produtos],
        'est_critico':  [dict(r) for r in est_critico]
    })

# ── INICIAR ────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n🔥 Churrascaria do Ronan — Sistema Web")
    print("   Acesse: http://localhost:5000")
    print("   Login: admin / 123\n")
    app.run(debug=True, port=5000)
