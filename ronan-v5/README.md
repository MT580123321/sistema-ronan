# 🔥 Churrascaria do Ronan — Sistema Web (100% completo)

Sistema de gestão comercial para churrascaria. Flask + SQLite + autenticação com hash bcrypt.

## Como rodar

```bash
pip install -r requirements.txt
python run.py
```

Acesse: http://localhost:5000  
Login padrão: **admin** / **123**

## Funcionalidades completas

- **Login seguro** — senhas armazenadas com hash (werkzeug/scrypt), nunca texto puro
- **Trocar senha** — botão 🔑 na sidebar, qualquer usuário pode alterar a própria senha
- **Usuários** — tela exclusiva para admin: cadastrar, remover e redefinir senha de outros usuários; níveis admin e operador
- **Dashboard** — visão geral de vendas, pedidos, estoque crítico e últimos pedidos
- **Clientes** — cadastro e remoção (com proteção: não remove se tiver pedidos); busca em tempo real
- **Produtos** — cadastro, edição completa (nome, preço, categoria, estoque) e remoção; busca + filtro por categoria
- **Pedidos** — criação com múltiplos itens, baixa automática de estoque, marcar como pago, cancelar (restaura estoque); filtro por status/mesa/cliente; **detalhes dos itens** e **impressão de comanda**
- **Estoque** — ajuste manual de quantidades, alertas ESGOTADO/CRÍTICO/BAIXO/OK; busca por produto ou categoria
- **Relatórios** — resumo financeiro, top 5 produtos, estoque crítico, exportação .txt
