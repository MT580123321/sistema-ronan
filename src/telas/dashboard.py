import customtkinter as ctk

def abrir_dashboard(frame, clientes, produtos, pedidos, estoque):
    for widget in frame.winfo_children():
        widget.destroy()

    titulo = ctk.CTkLabel(
        frame,
        text="Dashboard",
        font=("Arial", 30, "bold")
    )
    titulo.pack(pady=20)

    box = ctk.CTkFrame(frame)
    box.pack(pady=20)

    dados = [
        ("Clientes", len(clientes)),
        ("Produtos", len(produtos)),
        ("Pedidos", len(pedidos)),
        ("Estoque", len(estoque))
    ]

    linha = 0
    coluna = 0

    for nome, valor in dados:
        card = ctk.CTkFrame(box, width=250, height=150)
        card.grid(row=linha, column=coluna, padx=20, pady=20)

        ctk.CTkLabel(
            card,
            text=nome,
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        ctk.CTkLabel(
            card,
            text=str(valor),
            font=("Arial", 40)
        ).pack()

        coluna += 1

        if coluna > 1:
            coluna = 0
            linha += 1
