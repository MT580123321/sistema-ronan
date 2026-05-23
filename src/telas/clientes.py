import customtkinter as ctk
from tkinter import messagebox

def tela_clientes(frame, clientes):
    for widget in frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        frame,
        text="Cadastro de Clientes",
        font=("Arial", 28, "bold")
    ).pack(pady=20)

    nome = ctk.CTkEntry(frame, placeholder_text="Nome", width=300)
    nome.pack(pady=10)

    telefone = ctk.CTkEntry(frame, placeholder_text="Telefone", width=300)
    telefone.pack(pady=10)

    lista = ctk.CTkTextbox(frame, width=700, height=300)
    lista.pack(pady=20)

    def atualizar():
        lista.delete("1.0", "end")

        for cliente in clientes:
            lista.insert("end", f"{cliente}\n")

    def salvar():
        if nome.get() == "" or telefone.get() == "":
            messagebox.showerror("Erro", "Preencha os campos")
            return

        clientes.append(f"{nome.get()} - {telefone.get()}")

        atualizar()

        nome.delete(0, "end")
        telefone.delete(0, "end")

    ctk.CTkButton(
        frame,
        text="Cadastrar",
        command=salvar
    ).pack(pady=10)
