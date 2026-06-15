-- =============================================
-- CHURRASCARIA DO RONAN — Schema SQL
-- =============================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    nivel TEXT DEFAULT 'admin',
    criado_em TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    cpf TEXT,
    criado_em TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    categoria TEXT DEFAULT 'Outros',
    por_peso INTEGER DEFAULT 0,   -- 1 = vendido por kg, 0 = por unidade
    criado_em TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL UNIQUE,
    quantidade INTEGER DEFAULT 0,
    atualizado_em TEXT DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    mesa TEXT NOT NULL,
    status TEXT DEFAULT 'Pendente',
    total REAL DEFAULT 0,
    criado_em TEXT DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 1,
    peso_kg REAL DEFAULT NULL,       -- preenchido quando por_peso=1
    preco_unit REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);


-- ── CARDÁPIO INICIAL ────────────────────────────────────────
-- Insere apenas se a tabela produtos estiver vazia
INSERT INTO produtos (nome, preco, categoria, por_peso)
SELECT nome, preco, categoria, pp FROM (
  SELECT 'Picanha' AS nome, 89.90 AS preco, 'Carnes' AS categoria, 1 AS pp UNION ALL
  SELECT 'Costela Bovina',       69.90, 'Carnes', 1 UNION ALL
  SELECT 'Fraldinha',            75.90, 'Carnes', 1 UNION ALL
  SELECT 'Maminha',              72.90, 'Carnes', 1 UNION ALL
  SELECT 'Alcatra',              79.90, 'Carnes', 1 UNION ALL
  SELECT 'Linguiça Toscana',     39.90, 'Linguiça', 1 UNION ALL
  SELECT 'Frango (Coxa)',        45.90, 'Frango', 1 UNION ALL
  SELECT 'Cordeiro',             99.90, 'Carnes', 1 UNION ALL
  SELECT 'Arroz Branco',          8.00, 'Acompanhamentos', 0 UNION ALL
  SELECT 'Feijão Tropeiro',      10.00, 'Acompanhamentos', 0 UNION ALL
  SELECT 'Vinagrete',             6.00, 'Acompanhamentos', 0 UNION ALL
  SELECT 'Farofa Especial',       9.00, 'Acompanhamentos', 0 UNION ALL
  SELECT 'Pão de Alho',           5.00, 'Acompanhamentos', 0 UNION ALL
  SELECT 'Maionese da Casa',      7.00, 'Acompanhamentos', 0 UNION ALL
  SELECT 'Cerveja Heineken 600ml',14.00,'Bebidas Alcoólicas', 0 UNION ALL
  SELECT 'Cerveja Brahma 600ml',  12.00,'Bebidas Alcoólicas', 0 UNION ALL
  SELECT 'Caipirinha',            18.00,'Bebidas Alcoólicas', 0 UNION ALL
  SELECT 'Dose de Whisky',        22.00,'Bebidas Alcoólicas', 0 UNION ALL
  SELECT 'Vinho Tinto (taça)',    20.00,'Bebidas Alcoólicas', 0 UNION ALL
  SELECT 'Vinho Branco (taça)',   20.00,'Bebidas Alcoólicas', 0 UNION ALL
  SELECT 'Água Mineral 500ml',    4.00,'Bebidas Não Alcoólicas', 0 UNION ALL
  SELECT 'Refrigerante Lata',     6.00,'Bebidas Não Alcoólicas', 0 UNION ALL
  SELECT 'Suco Natural',         10.00,'Bebidas Não Alcoólicas', 0 UNION ALL
  SELECT 'Água de Coco',          8.00,'Bebidas Não Alcoólicas', 0 UNION ALL
  SELECT 'Limonada Suíça',       12.00,'Bebidas Não Alcoólicas', 0 UNION ALL
  SELECT 'Pudim',                 9.00,'Sobremesas', 0 UNION ALL
  SELECT 'Sorvete (2 bolas)',     8.00,'Sobremesas', 0
) WHERE NOT EXISTS (SELECT 1 FROM produtos LIMIT 1);

INSERT INTO estoque (produto_id, quantidade)
SELECT id, CASE WHEN por_peso = 1 THEN 9999 ELSE 50 END
FROM produtos
WHERE id NOT IN (SELECT produto_id FROM estoque);
