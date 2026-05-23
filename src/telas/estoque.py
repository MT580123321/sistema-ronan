import customtkinter as ctk

def tela_estoque(frame, estoque):
    for widget in frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        frame,
        text="Controle de Estoque",
        font=("Arial", 28, "bold")
    ).pack(pady=20)

    lista = ctk.CTkTextbox(frame, width=800, height=400)
    lista.pack(pady=20)

    for produto, qtd in estoque.items():
        status = "OK"

        if qtd <= 5:
            status = "BAIXO"

        lista.insert(
            "end",
            f"{produto} - Quantidade: {qtd} - Status: {status}\n"
        )
