# SISTEMA DE GESTÃO DA CHURRASCARIA DO RONAN

## 1. IDENTIFICAÇÃO DA EQUIPE

### Integrantes

* Michel Guido
* Andre Rocha
* Mickael Miranda


# 2. DESCRIÇÃO DO PROJETO

O Sistema de Gestão da Churrascaria do Ronan é uma aplicação web desenvolvida para automatizar os processos administrativos e operacionais da empresa.

O sistema foi criado para centralizar informações relacionadas ao gerenciamento de clientes, produtos, estoque, pedidos e usuários, proporcionando maior controle das operações e melhor organização dos dados.

A solução busca substituir processos manuais por um ambiente informatizado capaz de auxiliar na tomada de decisões e aumentar a produtividade do estabelecimento.

O projeto foi desenvolvido utilizando Python, Flask, SQLite, HTML5, CSS3 e JavaScript, aplicando conceitos de Engenharia de Software, Banco de Dados, Programação Orientada a Objetos e Desenvolvimento Web.



# 3. OBJETIVOS DO PROJETO

## Objetivo Geral

Desenvolver uma solução web capaz de auxiliar a administração da Churrascaria do Ronan por meio da automação de processos internos.

## Objetivos Específicos

* Centralizar informações administrativas;
* Automatizar o controle de estoque;
* Facilitar o gerenciamento de clientes;
* Registrar pedidos de forma organizada;
* Disponibilizar relatórios gerenciais;
* Melhorar a tomada de decisões;
* Reduzir erros operacionais.



# 4. FUNCIONALIDADES IMPLEMENTADAS

## Sistema de Autenticação

* Login de usuários
* Controle de sessão
* Controle de permissões
* Logout seguro

## Gestão de Usuários

* Cadastro de usuários
* Edição de usuários
* Controle de acesso
* Perfis Administrador e Operador

## Gestão de Clientes

* Cadastro
* Consulta
* Atualização
* Exclusão

## Gestão de Produtos

* Cadastro de produtos
* Alteração de informações
* Controle de preços
* Consulta de produtos

## Controle de Estoque

* Entrada de produtos
* Saída de produtos
* Atualização automática de quantidades
* Controle de disponibilidade

## Gestão de Pedidos

* Registro de pedidos
* Associação de produtos
* Controle operacional

## Relatórios

* Relatórios administrativos
* Acompanhamento operacional
* Consultas gerenciais

## Dashboard

* Visão geral do sistema
* Indicadores operacionais
* Acesso rápido aos módulos

---

# 5. ESTRUTURA DO PROJETO


churrascaria-do-ronan/
│
├── app.py
├── run.py
├── requirements.txt
├── README.md
│
├── database/
│   └── schema.sql
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── dashboard.js
│   │   ├── clientes.js
│   │   ├── produtos.js
│   │   ├── estoque.js
│   │   ├── pedidos.js
│   │   ├── relatorios.js
│   │   └── usuarios.js
│   └── logo.png
│
└── templates/
    ├── login.html
    ├── base.html
    └── pages/
        ├── dashboard.html
        ├── clientes.html
        ├── produtos.html
        ├── estoque.html
        ├── pedidos.html
        ├── relatorios.html
        └── usuarios.html




# 6. TECNOLOGIAS UTILIZADAS

## Backend

* Python 3.15
* Flask

## Front-End

* HTML5
* CSS3
* JavaScript

## Banco de Dados

* SQLite

## Segurança

* Werkzeug Security
* Hash de Senhas
* Controle de Sessões

## Ferramentas

* Git
* GitHub
* Visual Studio Code



# 7. ARQUITETURA DO SISTEMA

O sistema foi desenvolvido seguindo uma arquitetura baseada no padrão MVC (Model-View-Controller).

## Model

Responsável pela persistência e manipulação dos dados.

## View

Responsável pela interface gráfica apresentada ao usuário.

## Controller

Responsável pelas regras de negócio e comunicação entre a interface e o banco de dados.

### Benefícios

* Organização do projeto;
* Separação de responsabilidades;
* Facilidade de manutenção;
* Escalabilidade.



# 8. PARADIGMAS DE PROGRAMAÇÃO

## 8.1 Programação Orientada a Objetos (POO)

Aplicada na modelagem das principais entidades do sistema:

* Usuário
* Cliente
* Produto
* Pedido
* Estoque

### Benefícios

* Encapsulamento
* Modularidade
* Reutilização de código
* Facilidade de manutenção



## 8.2 Programação Estruturada

Utilizada no fluxo das regras de negócio.

### Aplicações

* Processamento de pedidos
* Controle de estoque
* Validação de dados
* Geração de relatórios



## 8.3 Programação Modular

O projeto foi dividido em módulos independentes:

* Autenticação
* Usuários
* Clientes
* Produtos
* Estoque
* Pedidos
* Relatórios

### Benefícios

* Organização
* Facilidade de manutenção
* Escalabilidade



# 9. MODELAGEM DO BANCO DE DADOS

## Principais Tabelas

### usuarios

Responsável pela autenticação e controle de acesso.

### clientes

Armazena os dados dos clientes.

### produtos

Armazena os produtos cadastrados.

### estoque

Controla a quantidade disponível de cada produto.

### pedidos

Registra as vendas realizadas.

### itens_pedido

Relaciona produtos aos pedidos.



## Relacionamentos

Cliente → Pedido

Pedido → Itens do Pedido

Produto → Estoque

Produto → Itens do Pedido

Usuário → Sistema



# 10. REQUISITOS FUNCIONAIS

### RF01

Permitir autenticação de usuários.

### RF02

Permitir gerenciamento de usuários.

### RF03

Permitir cadastro de clientes.

### RF04

Permitir cadastro de produtos.

### RF05

Permitir controle de estoque.

### RF06

Permitir registro de pedidos.

### RF07

Permitir emissão de relatórios.

### RF08

Permitir gerenciamento administrativo.



# 11. REQUISITOS NÃO FUNCIONAIS

### RNF01

Interface intuitiva e amigável.

### RNF02

Persistência dos dados em banco relacional.

### RNF03

Controle de acesso por autenticação.

### RNF04

Estrutura modular.

### RNF05

Compatibilidade com navegadores modernos.

### RNF06

Segurança através de hash de senhas.


# 12. SEGURANÇA IMPLEMENTADA

O sistema implementa mecanismos básicos de segurança:

* Autenticação de usuários;
* Controle de acesso por perfil;
* Proteção de rotas administrativas;
* Sessões autenticadas;
* Criptografia de senhas utilizando:

```python
generate_password_hash()
check_password_hash()
```

As senhas não são armazenadas em texto puro, aumentando a segurança dos dados dos usuários.



# 13. DIVISÃO DE RESPONSABILIDADES

## Michel Guido — Arquitetura e Estruturação

* Organização da estrutura do projeto;
* Planejamento da arquitetura;
* Padronização do código;
* Apoio na modelagem do sistema.



## Andre Rocha — Desenvolvimento Backend

* Implementação das regras de negócio;
* Integração com banco de dados;
* Desenvolvimento dos módulos administrativos;
* Controle de estoque;
* Controle de pedidos.



## Mickael Miranda — Interface e Experiência do Usuário

* Desenvolvimento das telas;
* Estrutura HTML;
* Estilização CSS;
* Implementação JavaScript;
* Organização visual da aplicação.



# 14. MELHORIAS IMPLEMENTADAS

Durante o desenvolvimento foram implementadas as seguintes melhorias:

* Sistema de autenticação;
* Dashboard administrativo;
* Controle de usuários;
* Persistência em banco de dados;
* Estrutura modularizada;
* Interface moderna;
* Organização das funcionalidades;
* Controle de acesso;
* Segurança de senhas.



# 15. ROADMAP DE DESENVOLVIMENTO

- [x] Levantamento de requisitos
- [x] Modelagem do sistema
- [x] Estrutura do banco de dados
- [x] Sistema de autenticação
- [x] Dashboard administrativo
- [x] Gestão de usuários
- [x] Gestão de clientes
- [x] Gestão de produtos
- [x] Controle de estoque
- [x] Gestão de pedidos
- [x] Impressão de comandas
- [x] Relatórios administrativos
- [x] Exportação de relatórios
- [x] Controle de acesso por perfil
- [x] Baixa automática de estoque
- [x] Reposição automática de estoque em cancelamentos
- [x] Busca dinâmica de informações
- [x] Interface web responsiva
- [x] Integração com banco de dados SQLite
- [x] Segurança de senhas com hash criptográfico



# 16. INTERFACE DO SISTEMA

O sistema possui uma interface moderna baseada em páginas web responsivas.

## Características

* Dashboard administrativo;
* Navegação intuitiva;
* Interface amigável;
* Formulários organizados;
* Melhor experiência do usuário;
* Estrutura visual profissional.



# 17. USUÁRIOS PADRÃO

## Administrador

```text
Usuário: admin
Senha: ronan2025
```

## Operador

```text
Usuário: garcom
Senha: ronan2025
```



# 18. FLUXO DE FUNCIONAMENTO

1. O usuário realiza login.
2. O sistema valida as credenciais.
3. O usuário acessa o Dashboard.
4. As operações são realizadas através dos módulos.
5. Os dados são armazenados no banco SQLite.
6. Relatórios podem ser gerados em tempo real.



# 19. INSTRUÇÕES DE EXECUÇÃO

## 1. Clonar o Repositório

```bash
git clone 
```

## 2. Acessar a Pasta

```bash
cd churrascaria-do-ronan
```

## 3. Criar Ambiente Virtual

```bash
python -m venv venv
```

## 4. Ativar Ambiente Virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux

```bash
source venv/bin/activate
```

## 5. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 6. Executar o Sistema

```bash
python run.py
```

## 7. Acessar o Sistema

```text
http://127.0.0.1:5000
```



# 20. IMPACTO SOCIAL

O projeto contribui para a transformação digital de pequenos negócios locais, permitindo que empreendedores utilizem recursos tecnológicos para melhorar a gestão administrativa de seus estabelecimentos.

Benefícios sociais:

* Modernização empresarial;
* Redução de desperdícios;
* Organização financeira;
* Maior produtividade;
* Incentivo à utilização de tecnologia na gestão de negócios.



# 21. CONSIDERAÇÕES FINAIS

O Sistema de Gestão da Churrascaria do Ronan representa a aplicação prática dos conhecimentos adquiridos durante o curso de Análise e Desenvolvimento de Sistemas.

A solução desenvolvida busca resolver problemas reais relacionados à administração de pequenos negócios, proporcionando maior controle das operações, melhor organização dos dados e suporte à tomada de decisões.

O projeto demonstra a importância da tecnologia como ferramenta estratégica para modernização e crescimento empresarial.



# 22. LICENÇA

Projeto desenvolvido exclusivamente para fins acadêmicos.

Todos os direitos reservados à equipe desenvolvedora.
