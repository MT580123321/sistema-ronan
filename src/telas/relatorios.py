import customtkinter as ctk

def tela_relatorios(frame, clientes, produtos, pedidos):
    for widget in frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        frame,
        text="Relatórios",
        font=("Arial", 28, "bold")
    ).pack(pady=20)

    texto = ctk.CTkTextbox(frame, width=800, height=400)
    texto.pack(pady=20)

    texto.insert("end", "===== RELATÓRIO =====\n\n")
    texto.insert("end", f"Clientes: {len(clientes)}\n")
    texto.insert("end", f"Produtos: {len(produtos)}\n")
    texto.insert("end", f"Pedidos: {len(pedidos)}\n")
