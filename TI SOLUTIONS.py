import tkinter as tk
from tkinter import ttk, messagebox

class HelpDeskApp:
    def __init__(self, root):
        # Configuração inicial da janela
        self.root = root
        self.root.title("💻 IT HelpDesk")
        self.root.geometry("1000x650")
        self.root.configure(bg="#ecf0f1")

        # Lista de chamados
        self.chamados = []
        self.next_id = 1

        # Barra de menu
        self._build_topbar()

        # Área principal
        self.main_area = tk.Frame(self.root, bg="#ecf0f1")
        self.main_area.pack(expand=True, fill="both")

        # Tela inicial → Dashboard
        self._dashboard()

    # ----------------------------
    # Barra superior (menu)
    # ----------------------------
    def _build_topbar(self):
        top = tk.Frame(self.root, bg="#2c3e50", height=60)
        top.pack(side="top", fill="x")

        tk.Label(top, text="🛠️ IT HelpDesk",
                 bg="#2c3e50", fg="white", font=("Arial", 18, "bold")).pack(side="left", padx=15)

        menu_frame = tk.Frame(top, bg="#2c3e50")
        menu_frame.pack(side="right", padx=10)

        botoes = [
            ("📊 Dashboard", self._dashboard),
            ("➕ Abrir", self._abrir_chamado),
            ("📋 Listar", self._listar_chamados),
            ("✏️ Editar", self._editar_chamado),
            ("❌ Excluir", self._excluir_chamado),
            ("🚪 Sair", self._sair),
        ]

        for txt, cmd in botoes:
            b = tk.Button(menu_frame, text=txt, command=cmd,
                          bg="#34495e", fg="white", relief="flat",
                          font=("Arial", 12), padx=10, pady=5)
            b.pack(side="left", padx=5)

    def _clear_window(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    # ----------------------------
    # Dashboard
    # ----------------------------
    def _dashboard(self):
        self._clear_window()
        tk.Label(self.main_area, text="📊 Painel de Controle",
                 font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=20)

        cards = tk.Frame(self.main_area, bg="#ecf0f1")
        cards.pack(pady=20)

        abertos = sum(1 for c in self.chamados if c["status"] == "Aberto")
        andamento = sum(1 for c in self.chamados if c["status"] == "Em andamento")
        fechados = sum(1 for c in self.chamados if c["status"] == "Fechado")

        card_data = [
            ("🟢 Abertos", abertos, "#27ae60"),
            ("🟡 Em Andamento", andamento, "#f39c12"),
            ("🔴 Fechados", fechados, "#e74c3c"),
        ]

        for i, (titulo, valor, cor) in enumerate(card_data):
            f = tk.Frame(cards, bg=cor, width=200, height=100)
            f.grid(row=0, column=i, padx=15)
            tk.Label(f, text=titulo, bg=cor, fg="white",
                     font=("Arial", 14, "bold")).pack(pady=10)
            tk.Label(f, text=str(valor), bg=cor, fg="white",
                     font=("Arial", 16, "bold")).pack()

    # ----------------------------
    # Abrir chamado
    # ----------------------------
    def _abrir_chamado(self):
        self._clear_window()
        tk.Label(self.main_area, text="➕ Novo Chamado",
                 font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=20)

        form = tk.Frame(self.main_area, bg="#ecf0f1")
        form.pack(pady=10)

        tk.Label(form, text="Título:", bg="#ecf0f1").grid(row=0, column=0, sticky="e")
        titulo_entry = tk.Entry(form, width=40)
        titulo_entry.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Descrição:", bg="#ecf0f1").grid(row=1, column=0, sticky="ne")
        desc_entry = tk.Text(form, width=40, height=5)
        desc_entry.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Importância:", bg="#ecf0f1").grid(row=2, column=0, sticky="e")
        importancia_combo = ttk.Combobox(form, values=["Baixa 🟢", "Média 🟡", "Alta 🔴"])
        importancia_combo.grid(row=2, column=1, pady=5)

        def salvar():
            titulo = titulo_entry.get().strip()
            desc = desc_entry.get("1.0", tk.END).strip()
            importancia = importancia_combo.get()

            if not titulo or not desc or not importancia:
                messagebox.showwarning("Erro", "Preencha todos os campos!")
                return

            chamado = {
                "id": self.next_id,
                "titulo": titulo,
                "descricao": desc,
                "status": "Aberto",
                "importancia": importancia
            }
            self.chamados.append(chamado)
            self.next_id += 1

            messagebox.showinfo("Sucesso", f"Chamado {chamado['id']} criado!")
            self._listar_chamados()

        tk.Button(self.main_area, text="💾 Salvar Chamado", command=salvar,
                  bg="#27ae60", fg="white", font=("Arial", 12)).pack(pady=15)

    # ----------------------------
    # Listar chamados (com cores 🎨)
    # ----------------------------
    def _listar_chamados(self):
        self._clear_window()
        tk.Label(self.main_area, text="📋 Lista de Chamados",
                 font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=20)

        colunas = ("ID", "Título", "Status", "Importância")
        tree = ttk.Treeview(self.main_area, columns=colunas, show="headings", height=15)

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="center")

        # Configura estilos para linhas coloridas
        tree.tag_configure("alta", background="#f8d7da")   # vermelho claro
        tree.tag_configure("media", background="#fff3cd")  # amarelo claro
        tree.tag_configure("baixa", background="#d4edda")  # verde claro

        prioridade_ordem = {"Alta 🔴": 1, "Média 🟡": 2, "Baixa 🟢": 3}
        chamados_ordenados = sorted(
            self.chamados,
            key=lambda c: prioridade_ordem.get(c["importancia"], 99)
        )

        # Insere os chamados com cor
        for c in chamados_ordenados:
            if "Alta" in c["importancia"]:
                tag = "alta"
            elif "Média" in c["importancia"]:
                tag = "media"
            else:
                tag = "baixa"

            tree.insert("", "end", values=(c["id"], c["titulo"], c["status"], c["importancia"]), tags=(tag,))

        tree.pack(padx=20, pady=10, fill="x")

        # Botão detalhes
        def ver_detalhes():
            item = tree.selection()
            if not item:
                messagebox.showwarning("Atenção", "Selecione um chamado!")
                return
            cid = int(tree.item(item[0])["values"][0])
            chamado = next(c for c in self.chamados if c["id"] == cid)

            win = tk.Toplevel(self.root)
            win.title(f"Chamado {cid} - Detalhes")
            win.geometry("500x400")
            win.config(bg="#ecf0f1")

            tk.Label(win, text=f"🆔 Chamado {cid}",
                     font=("Arial", 14, "bold"), bg="#ecf0f1").pack(pady=10)
            tk.Label(win, text=f"📌 Título: {chamado['titulo']}",
                     font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
            tk.Label(win, text=f"⚡ Importância: {chamado['importancia']}",
                     font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
            tk.Label(win, text=f"📊 Status: {chamado['status']}",
                     font=("Arial", 12), bg="#ecf0f1").pack(pady=5)

            tk.Label(win, text="📝 Descrição:", font=("Arial", 12, "bold"),
                     bg="#ecf0f1").pack(pady=5)
            text = tk.Text(win, wrap="word", height=10, width=50)
            text.insert("1.0", chamado["descricao"])
            text.config(state="disabled")
            text.pack(padx=10, pady=5)

            tk.Button(win, text="Fechar", command=win.destroy).pack(pady=10)

        tk.Button(self.main_area, text="🔍 Ver Detalhes", command=ver_detalhes,
                  bg="#2980b9", fg="white", font=("Arial", 12)).pack(pady=10)

    # ----------------------------
    # Editar chamado
    # ----------------------------
    def _editar_chamado(self):
        self._clear_window()
        tk.Label(self.main_area, text="✏️ Editar Chamado",
                 font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=20)

        tk.Label(self.main_area, text="ID do chamado:", bg="#ecf0f1").pack()
        id_entry = tk.Entry(self.main_area, width=10)
        id_entry.pack(pady=5)

        form_frame = tk.Frame(self.main_area, bg="#ecf0f1")
        form_frame.pack(pady=10)

        def carregar():
            try:
                cid = int(id_entry.get())
            except ValueError:
                messagebox.showerror("Erro", "Digite um ID válido!")
                return

            chamado = next((c for c in self.chamados if c["id"] == cid), None)
            if not chamado:
                messagebox.showerror("Erro", "Chamado não encontrado!")
                return

            for w in form_frame.winfo_children():
                w.destroy()

            titulo_var = tk.StringVar(value=chamado["titulo"])
            tk.Label(form_frame, text="Título:", bg="#ecf0f1").pack()
            titulo_entry = tk.Entry(form_frame, textvariable=titulo_var, width=50)
            titulo_entry.pack(pady=5)

            tk.Label(form_frame, text="Descrição:", bg="#ecf0f1").pack()
            desc_entry = tk.Text(form_frame, width=50, height=5)
            desc_entry.insert(tk.END, chamado["descricao"])
            desc_entry.pack()

            tk.Label(form_frame, text="Status:", bg="#ecf0f1").pack(pady=5)
            status_combo = ttk.Combobox(form_frame, values=["Aberto", "Em andamento", "Fechado"])
            status_combo.set(chamado["status"])
            status_combo.pack()

            tk.Label(form_frame, text="Importância:", bg="#ecf0f1").pack(pady=5)
            importancia_combo = ttk.Combobox(form_frame, values=["Baixa 🟢", "Média 🟡", "Alta 🔴"])
            importancia_combo.set(chamado["importancia"])
            importancia_combo.pack()

            def salvar_edicao():
                chamado["titulo"] = titulo_var.get()
                chamado["descricao"] = desc_entry.get("1.0", tk.END).strip()
                chamado["status"] = status_combo.get()
                chamado["importancia"] = importancia_combo.get()
                messagebox.showinfo("Sucesso", f"Chamado {cid} atualizado!")
                self._listar_chamados()

            tk.Button(form_frame, text="💾 Salvar Alterações", command=salvar_edicao,
                      bg="#27ae60", fg="white", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.main_area, text="Carregar Chamado", command=carregar,
                  bg="#2980b9", fg="white", font=("Arial", 12)).pack(pady=10)

    # ----------------------------
    # Excluir chamado
    # ----------------------------
    def _excluir_chamado(self):
        self._clear_window()
        tk.Label(self.main_area, text="❌ Excluir Chamado",
                 font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=20)

        tk.Label(self.main_area, text="ID do chamado:", bg="#ecf0f1").pack()
        id_entry = tk.Entry(self.main_area, width=10)
        id_entry.pack(pady=5)

        def excluir():
            try:
                cid = int(id_entry.get())
            except ValueError:
                messagebox.showerror("Erro", "Digite um ID válido!")
                return

            chamado = next((c for c in self.chamados if c["id"] == cid), None)
            if not chamado:
                messagebox.showerror("Erro", "Chamado não encontrado!")
                return

            if messagebox.askyesno("Confirmação", f"Deseja realmente excluir o chamado {cid}?"):
                self.chamados.remove(chamado)
                messagebox.showinfo("Sucesso", f"Chamado {cid} excluído!")
                self._listar_chamados()

        tk.Button(self.main_area, text="🗑️ Excluir", command=excluir,
                  bg="#e74c3c", fg="white", font=("Arial", 12)).pack(pady=10)

    # ----------------------------
    # Sair
    # ----------------------------
    def _sair(self):
        if messagebox.askyesno("Confirmação", "Deseja sair do sistema?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HelpDeskApp(root)
    root.mainloop()