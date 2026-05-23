import customtkinter as ctk

def tela_produtos(frame, produtos):
    for widget in frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        frame,
        text="Cadastro de Produtos",
        font=("Arial", 28, "bold")
    ).pack(pady=20)

    nome = ctk.CTkEntry(frame, placeholder_text="Produto", width=300)
    nome.pack(pady=10)

    preco = ctk.CTkEntry(frame, placeholder_text="Preço", width=300)
    preco.pack(pady=10)

    lista = ctk.CTkTextbox(frame, width=700, height=300)
    lista.pack(pady=20)

    def atualizar():
        lista.delete("1.0", "end")

        for produto in produtos:
            lista.insert("end", f"{produto}\n")

    def salvar():
        produtos.append(f"{nome.get()} - R$ {preco.get()}")

        atualizar()

        nome.delete(0, "end")
        preco.delete(0, "end")

    ctk.CTkButton(
        frame,
        text="Cadastrar Produto",
        command=salvar
    ).pack(pady=10)
