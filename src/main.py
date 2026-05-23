<<<<<<< HEAD
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BG = "#111111"
SIDE = "#4A0E0E"
CARD = "#1D1D1D"
ACC = "#D35400"
HOVER = "#E67E22"
GOLD = "#D4AF37"

app = ctk.CTk()
app.geometry("1600x920")
app.title("Churrascaria do Ronan")
app.configure(fg_color=BG)

# FUNÇÕES

def clear():
    for w in content.winfo_children():
        w.destroy()


def header(t):
    clear()

    ctk.CTkLabel(
        content,
        text=t,
        font=("Segoe UI", 34, "bold"),
        text_color=GOLD
    ).pack(anchor="w", padx=40, pady=30)


# DASHBOARD

def dashboard():

    header("Dashboard Operacional")

    wrap = ctk.CTkFrame(content, fg_color="transparent")
    wrap.pack(fill="x", padx=30)

    dados = [
        ("Clientes", "0"),
        ("Produtos", "0"),
        ("Pedidos", "0"),
        ("Estoque", "0")
    ]

    for titulo, valor in dados:

        card = ctk.CTkFrame(
            wrap,
            width=290,
            height=180,
            corner_radius=24,
            fg_color=CARD
        )
        card.pack(side="left", padx=15)

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=titulo,
            font=("Segoe UI", 20)
        ).pack(pady=(35, 8))

        ctk.CTkLabel(
            card,
            text=valor,
            font=("Segoe UI", 42, "bold"),
            text_color=GOLD
        ).pack()

    # ÁREA ADMINISTRATIVA

    resumo = ctk.CTkFrame(
        content,
        fg_color=CARD,
        corner_radius=24,
        height=260
    )
    resumo.pack(fill="x", padx=40, pady=40)

    resumo.pack_propagate(False)

    ctk.CTkLabel(
        resumo,
        text="Resumo Administrativo",
        font=("Segoe UI", 26, "bold"),
        text_color=GOLD
    ).pack(anchor="w", padx=30, pady=(30, 10))

    texto = """
Sistema operacional iniciado com sucesso.

• Clientes cadastrados: 0
• Produtos cadastrados: 0
• Pedidos realizados: 0
• Estoque registrado: 0

Nenhuma movimentação encontrada.
"""

    ctk.CTkLabel(
        resumo,
        text=texto,
        justify="left",
        font=("Segoe UI", 18),
        text_color="#DDDDDD"
    ).pack(anchor="w", padx=30)



# TABELAS

def tabela(nome, colunas, vazio):

    header(nome)

    top = ctk.CTkFrame(content, fg_color="transparent")
    top.pack(fill="x", padx=30)

    for c in colunas:

        head = ctk.CTkFrame(
            top,
            fg_color=CARD,
            corner_radius=14,
            height=55
        )
        head.pack(fill="x", pady=5)

        ctk.CTkLabel(
            head,
            text=c,
            font=("Segoe UI", 17, "bold")
        ).pack(side="left", padx=25, pady=15)

    vazio_box = ctk.CTkFrame(
        content,
        fg_color=CARD,
        corner_radius=20,
        height=220
    )
    vazio_box.pack(fill="x", padx=30, pady=30)

    vazio_box.pack_propagate(False)

    ctk.CTkLabel(
        vazio_box,
        text=vazio,
        font=("Segoe UI", 24, "bold"),
        text_color=GOLD
    ).place(relx=0.5, rely=0.5, anchor="center")


# TELAS

def clientes():
    tabela(
        "Clientes",
        ["Nome", "Telefone", "CPF"],
        "0 clientes cadastrados"
    )


def produtos():
    tabela(
        "Produtos",
        ["Produto", "Preço", "Estoque"],
        "0 produtos cadastrados"
    )


def pedidos():
    tabela(
        "Pedidos",
        ["Mesa", "Cliente", "Status"],
        "0 pedidos cadastrados"
    )


def estoque():
    tabela(
        "Estoque",
        ["Item", "Quantidade", "Situação"],
        "0 itens no estoque"
    )


# LOGIN

login = ctk.CTkFrame(app, fg_color=BG)
login.pack(fill="both", expand=True)

box = ctk.CTkFrame(
    login,
    width=620,
    height=680,
    corner_radius=30,
    fg_color=CARD
)
box.place(relx=.5, rely=.5, anchor="center")

box.pack_propagate(False)

ctk.CTkLabel(
    box,
    text="🔥",
    font=("Segoe UI Emoji", 80)
).pack(pady=(40, 10))

ctk.CTkLabel(
    box,
    text="CHURRASCARIA DO RONAN",
    font=("Segoe UI", 30, "bold"),
    text_color=GOLD
).pack()

ctk.CTkLabel(
    box,
    text="Sistema de Gestão Comercial",
    text_color="#BBBBBB",
    font=("Segoe UI", 16)
).pack(pady=10)

u = ctk.CTkEntry(
    box,
    width=360,
    height=56,
    placeholder_text="Usuário"
)
u.pack(pady=12)

s = ctk.CTkEntry(
    box,
    width=360,
    height=56,
    placeholder_text="Senha",
    show="●"
)
s.pack()


# SISTEMA


sys = ctk.CTkFrame(app, fg_color=BG)

def entrar():

    if u.get() == "admin" and s.get() == "123":

        login.pack_forget()

        sys.pack(fill="both", expand=True)

        dashboard()

    else:

        messagebox.showerror(
            "Erro",
            "Usuário ou senha inválidos"
        )

ctk.CTkButton(
    box,
    text="Entrar",
    width=360,
    height=56,
    fg_color=ACC,
    hover_color=HOVER,
    font=("Segoe UI", 18, "bold"),
    command=entrar
).pack(pady=40)

# SIDEBAR

side = ctk.CTkFrame(
    sys,
    width=280,
    fg_color=SIDE
)
side.pack(side="left", fill="y")

side.pack_propagate(False)

content = ctk.CTkFrame(
    sys,
    fg_color=BG
)
content.pack(fill="both", expand=True)

ctk.CTkLabel(
    side,
    text="CHURRASCARIA\nDO RONAN",
    font=("Segoe UI", 26, "bold"),
    text_color=GOLD,
    justify="center"
).pack(pady=35)

menus = [
    ("Dashboard", dashboard),
    ("Clientes", clientes),
    ("Produtos", produtos),
    ("Pedidos", pedidos),
    ("Estoque", estoque)
]

for n, f in menus:

    ctk.CTkButton(
        side,
        text=n,
        width=220,
        height=52,
        fg_color=ACC,
        hover_color=HOVER,
        font=("Segoe UI", 16, "bold"),
        command=f
    ).pack(pady=12)

# BOTÃO SAIR

ctk.CTkButton(
    side,
    text="Sair",
    width=220,
    height=52,
    fg_color="#8B0000",
    hover_color="#AA0000",
    font=("Segoe UI", 16, "bold"),
    command=app.destroy
).pack(side="bottom", pady=30)

app.mainloop()
=======
from produto import Produto
            numero_mesa = int(input("Número da mesa: "))

            comanda = buscar_comanda(numero_mesa)

            # cria somente se não existir
            if comanda is None:
                mesa = Mesa(numero_mesa)
                comanda = Comanda(mesa)
                lista_comandas.append(comanda)

            print("\nCardápio:")

            for i, produto in enumerate(cardapio):
                print(
                    f"{i+1} - {produto.nome} "
                    f"(R$ {produto.preco}) "
                    f"| Estoque: {produto.estoque}"
                )

            escolha = int(input("Escolha o produto: ")) - 1
            quantidade = int(input("Quantidade: "))

            if escolha < 0 or escolha >= len(cardapio):
                print("Produto inválido!")
                continue

            produto = cardapio[escolha]

            pedido = Pedido(produto, quantidade)
            comanda.adicionar_item(pedido)

            salvar_dados(lista_comandas)

            print("Pedido adicionado com sucesso!")

        except ValueError:
            print("Digite apenas números!")

        except Exception as erro:
            print(f"Erro: {erro}")


    # FECHAR MESA
    elif opcao == "2":
        try:
            numero = int(input("Número da mesa para fechar: "))

            comanda = buscar_comanda(numero)

            if comanda:
                print(f"Total da mesa: R$ {comanda.calcular_total():.2f}")
                lista_comandas.remove(comanda)

                salvar_dados(lista_comandas)

                print("Mesa fechada com sucesso!")

            else:
                print("Mesa não encontrada!")

        except ValueError:
            print("Digite apenas números!")


    # RELATÓRIO
    elif opcao == "3":
        ver_relatorio(lista_comandas)


    # SAIR
    elif opcao == "0":
        salvar_dados(lista_comandas)
        print("Saindo do sistema...")
        break


    else:
        print("Opção inválida!")
>>>>>>> 2537dd920b42e569adafa6a79089b16ecda7162b
