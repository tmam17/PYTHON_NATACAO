import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import database
import logic

class AppNatacao(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Controlo de Treinos de Natação")
        self.geometry("1000x700")
        self.minsize(900, 650)

        database.criar_base_dados()
        self.criar_widgets()
        self.atualizar_dados_interface()

    def criar_widgets(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_registo = self.tabview.add("📝 Registar & Histórico")
        self.tab_stats = self.tabview.add("📊 Estatísticas & Resumo")
        self.tab_graficos = self.tabview.add("📈 Gráficos de Desempenho")

        self.construir_aba_registo()
        self.construir_aba_stats()
        self.construir_aba_graficos()

    def construir_aba_registo(self):
        frame_form = ctk.CTkFrame(self.tab_registo, corner_radius=10)
        frame_form.pack(side="left", fill="y", padx=(0, 15), pady=10, ipadx=10, ipady=10)

        ctk.CTkLabel(frame_form, text="Registar Novo Treino", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=10, pady=(10, 15))

        ctk.CTkLabel(frame_form, text="Data (AAAA-MM-DD):").pack(anchor="w", padx=10, pady=(0, 2))
        self.entry_data = ctk.CTkEntry(frame_form, width=220)
        self.entry_data.pack(anchor="w", padx=10, pady=(0, 10))
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ctk.CTkLabel(frame_form, text="Distância (metros):").pack(anchor="w", padx=10, pady=(0, 2))
        self.entry_metros = ctk.CTkEntry(frame_form, width=220)
        self.entry_metros.pack(anchor="w", padx=10, pady=(0, 10))

        ctk.CTkLabel(frame_form, text="Duração (minutos):").pack(anchor="w", padx=10, pady=(0, 2))
        self.entry_minutos = ctk.CTkEntry(frame_form, width=220)
        self.entry_minutos.pack(anchor="w", padx=10, pady=(0, 10))

        ctk.CTkLabel(frame_form, text="Calorias (kcal):").pack(anchor="w", padx=10, pady=(0, 2))
        self.entry_calorias = ctk.CTkEntry(frame_form, width=220)
        self.entry_calorias.pack(anchor="w", padx=10, pady=(0, 10))

        ctk.CTkLabel(frame_form, text="Estilo Principal:").pack(anchor="w", padx=10, pady=(0, 2))
        self.combo_estilo = ctk.CTkComboBox(frame_form, values=["Livre / Estilo", "Costas", "Bruços", "Mariposa / Coração", "Misturado"], width=220, state="readonly")
        self.combo_estilo.pack(anchor="w", padx=10, pady=(0, 20))
        self.combo_estilo.set("Livre / Estilo")

        btn_salvar = ctk.CTkButton(frame_form, text="Guardar Treino", command=self.guardar_treino, fg_color="#28a745", hover_color="#218838")
        btn_salvar.pack(fill="x", padx=10, pady=(0, 8))

        btn_apagar = ctk.CTkButton(frame_form, text="Eliminar Selecionado", command=self.eliminar_treino, fg_color="#dc3545", hover_color="#c82333")
        btn_apagar.pack(fill="x", padx=10)

        frame_tabela = ctk.CTkFrame(self.tab_registo, corner_radius=10)
        frame_tabela.pack(side="right", fill="both", expand=True, pady=10)

        ctk.CTkLabel(frame_tabela, text="Histórico de Treinos", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))

        colunas = ("ID", "Data", "Metros", "Minutos", "Calorias", "Estilo")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")

        style = ttk.Style()
        style.theme_use("clam")
        is_dark = (ctk.get_appearance_mode() == "Dark")
        style.configure("Treeview", background="#2b2b2b" if is_dark else "#ffffff", foreground="white" if is_dark else "black", fieldbackground="#2b2b2b" if is_dark else "#ffffff", rowheight=26)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#1f538d")

        for col in colunas:
            self.tabela.heading(col, text=col)
            if col == "ID":
                self.tabela.column(col, width=40, anchor="center")
            else:
                self.tabela.column(col, width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.tabela.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side="right", fill="y", pady=(0, 15), padx=(0, 15))

    def construir_aba_stats(self):
        frame_topo = ctk.CTkFrame(self.tab_stats, fg_color="transparent")
        frame_topo.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(frame_topo, text="Resumo de Desempenho e Carga", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        ctk.CTkButton(frame_topo, text="Atualizar Dados", command=self.atualizar_dados_interface).pack(side="right")

        self.paineis = {}
        periodos = [("Esta Semana", "semana"), ("Este Mês", "mes"), ("Este Ano", "ano")]

        for titulo, chave in periodos:
            frame_box = ctk.CTkFrame(self.tab_stats, corner_radius=10)
            frame_box.pack(fill="x", pady=8, ipady=5)

            ctk.CTkLabel(frame_box, text=f"📊 {titulo}", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))

            sub_frame = ctk.CTkFrame(frame_box, fg_color="transparent")
            sub_frame.pack(fill="x", padx=15, pady=(0, 10))

            lbl_metros = ctk.CTkLabel(sub_frame, text="Distância Total: 0 m")
            lbl_metros.grid(row=0, column=0, sticky="w", padx=10, pady=2)

            lbl_horas = ctk.CTkLabel(sub_frame, text="Tempo Total: 0.0 h")
            lbl_horas.grid(row=0, column=1, sticky="w", padx=10, pady=2)

            lbl_cal = ctk.CTkLabel(sub_frame, text="Calorias: 0 kcal")
            lbl_cal.grid(row=0, column=2, sticky="w", padx=10, pady=2)

            lbl_ritmo = ctk.CTkLabel(sub_frame, text="Ritmo Médio: 0:00 /100m", font=ctk.CTkFont(weight="bold"))
            lbl_ritmo.grid(row=1, column=0, sticky="w", padx=10, pady=(5, 2))

            lbl_media_diaria = ctk.CTkLabel(sub_frame, text="Média Diária: 0 m/dia")
            lbl_media_diaria.grid(row=1, column=1, columnspan=2, sticky="w", padx=10, pady=(5, 2))

            self.paineis[chave] = {
                "metros": lbl_metros,
                "horas": lbl_horas,
                "calorias": lbl_cal,
                "ritmo": lbl_ritmo,
                "media_diaria": lbl_media_diaria
            }

    def construir_aba_graficos(self):
        frame_topo = ctk.CTkFrame(self.tab_graficos, fg_color="transparent")
        frame_topo.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(frame_topo, text="Evolução Gráfica de Treinos", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        ctk.CTkButton(frame_topo, text="Atualizar Gráficos", command=self.atualizar_graficos).pack(side="right")

        self.frame_canvas = ctk.CTkFrame(self.tab_graficos, corner_radius=10)
        self.frame_canvas.pack(fill="both", expand=True)

    def atualizar_graficos(self):
        for widget in self.frame_canvas.winfo_children():
            widget.destroy()

        dados = database.buscar_treinos_grafico_db()

        if not dados:
            ctk.CTkLabel(self.frame_canvas, text="Sem dados suficientes para gerar gráficos. Registre treinos primeiro.", font=ctk.CTkFont(size=13)).pack(pady=80)
            return

        datas = [d[0] for d in dados]
        metros = [d[1] for d in dados]
        ritmos = [(d[2] / d[1]) * 100 if d[1] > 0 else 0 for d in dados]

        is_dark = (ctk.get_appearance_mode() == "Dark")
        bg_color = "#2b2b2b" if is_dark else "#f0f0f0"
        text_color = "white" if is_dark else "black"

        plt.style.use("dark_background" if is_dark else "default")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), tight_layout=True)
        fig.patch.set_facecolor(bg_color)

        ax1.bar(datas, metros, color="#1f538d", alpha=0.85, width=0.6)
        ax1.set_title("Distância por Treino (Metros)", fontsize=11, fontweight="bold", color=text_color)
        ax1.set_xlabel("Data", fontsize=9, color=text_color)
        ax1.set_ylabel("Metros (m)", fontsize=9, color=text_color)
        ax1.tick_params(axis="x", rotation=30)
        ax1.grid(axis="y", linestyle="--", alpha=0.3)

        ax2.plot(datas, ritmos, color="#ff7f0e", marker="o", linewidth=2, markersize=6)
        ax2.set_title("Ritmo Médio (min / 100m)", fontsize=11, fontweight="bold", color=text_color)
        ax2.set_xlabel("Data", fontsize=9, color=text_color)
        ax2.set_ylabel("Minutos por 100m", fontsize=9, color=text_color)
        ax2.tick_params(axis="x", rotation=30)
        ax2.grid(True, linestyle="--", alpha=0.3)

        canvas = FigureCanvasTkAgg(fig, master=self.frame_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def guardar_treino(self):
        data = self.entry_data.get().strip()
        metros = self.entry_metros.get().strip()
        minutos = self.entry_minutos.get().strip()
        calorias = self.entry_calorias.get().strip()
        estilo = self.combo_estilo.get()

        try:
            datetime.strptime(data, "%Y-%m-%d")
            m_val = int(metros)
            min_val = float(minutos)
            c_val = int(calorias)
        except ValueError:
            messagebox.showerror("Erro de Dados", "Verifique os campos!\n- Data no formato AAAA-MM-DD\n- Metros e Calorias inteiros\n- Minutos numéricos.")
            return

        database.inserir_treino_db(data, m_val, min_val, c_val, estilo)
        messagebox.showinfo("Sucesso", "Treino registado com sucesso!")
        self.limpar_formulario()
        self.atualizar_dados_interface()

    def limpar_formulario(self):
        self.entry_data.delete(0, "end")
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_metros.delete(0, "end")
        self.entry_minutos.delete(0, "end")
        self.entry_calorias.delete(0, "end")

    def eliminar_treino(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um treino na tabela para apagar.")
            return

        item = self.tabela.item(selecionado)
        treino_id = item["values"][0]

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja eliminar este treino?"):
            database.eliminar_treino_db(treino_id)
            self.atualizar_dados_interface()
            messagebox.showinfo("Sucesso", "Treino eliminado.")

    def atualizar_dados_interface(self):
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        todos_treinos = database.buscar_todos_treinos_db()
        for t in todos_treinos:
            self.tabela.insert("", "end", values=t)

        stats = logic.obter_estatisticas_periodos()

        for chave, dados in stats.items():
            widgets = self.paineis[chave]
            widgets["metros"].configure(text=f"Distância Total: {dados['metros']:,} m".replace(",", " "))
            widgets["horas"].configure(text=f"Tempo Total: {dados['horas']:.1f} h")
            widgets["calorias"].configure(text=f"Calorias: {dados['calorias']:,} kcal".replace(",", " "))
            widgets["ritmo"].configure(text=f"Ritmo Médio: {dados['ritmo']}")
            widgets["media_diaria"].configure(text=f"Média Diária: {dados['media_diaria']:.0f} m/dia")

        self.atualizar_graficos()
