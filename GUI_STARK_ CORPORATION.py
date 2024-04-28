import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import ttk

#criando o banco de dados SQL
meubd = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="bancodedados"
)

mycursor = meubd.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS tarefas (id INT AUTO_INCREMENT PRIMARY KEY, descricao VARCHAR(255), data_inicio DATE, data_termino DATE, status VARCHAR(20))")

#criar janela, definir o titulo e o tamanho, definição do redimensionamento
janela = tk.Tk()
janela.title("GUI STARK CORPORATION")
janela.resizable(False, False)

#cores
preto = "#000000"
vermelho = "#ff0015"
branco = "#ffffff"

#criando as funções

def listar_tarefas():
    lista_tarefas_lb.delete(0, tk.END)
    mycursor.execute("SELECT * FROM tarefas")
    for tarefa in mycursor.fetchall():
        lista_tarefas_lb.insert(tk.END, f'{tarefa[1]} - Inicio: {tarefa[2]} - Término: {tarefa[3]} - Status: {tarefa[4]}')

def registrar_tarefas():
    descricao = entry_descricao.get()
    data_inicio = entry_data_inicio.get()
    data_termino = entry_data_termino.get()
    status = combo_status.get()

    # Formatação das datas
    data_inicio_formatada = "-".join(reversed(data_inicio.split("/")))
    data_termino_formatada = "-".join(reversed(data_termino.split("/")))

    if descricao:
        sql = "INSERT INTO tarefas (descricao, data_inicio, data_termino, status) VALUES (%s, %s, %s, %s)"
        val = (descricao, data_inicio_formatada, data_termino_formatada, status)
        mycursor.execute(sql, val)
        meubd.commit()
        messagebox.showinfo("Registrada!", "Tarefa registrada com sucesso")
        listar_tarefas()
    else:
        messagebox.showerror("ERRO!", "Informe alguma tarefa!")

def marcar_concluida():
    tarefas_selecionadas = lista_tarefas_lb.curselection()
    if tarefas_selecionadas:
        for selecionada in tarefas_selecionadas[::-1]:
            tarefa_concluida = lista_tarefas_lb.get(selecionada).split(" - ")[0]
            mycursor.execute("DELETE FROM tarefas WHERE descricao = %s", (tarefa_concluida,))
            meubd.commit()
            messagebox.showinfo("Tarefa Concluída", f"A tarefa {tarefa_concluida} foi concluida")
        listar_tarefas()
    else:
        messagebox.showinfo("ERRO!", "Selecione uma tarefa para ser removida")
        

#criando o frame 1

frame_1 = tk.Frame(janela,bg="#000000")
frame_1.pack(side="left")

label_tarefa = tk.Label(frame_1, text="TAREFAS",bg="#000000",fg="#ffffff")
label_tarefa.pack(fill="x")

lista_tarefas_lb = tk.Listbox(frame_1,width=100,height=20, selectmode="multiple")
lista_tarefas_lb.pack(fill="both",expand=True)

#criando o frame 2

frame_2 = tk.Frame(janela,bg="#000000",padx=5)
frame_2.pack(side="left")

label_descricao = tk.Label(frame_2,text="Descrição:",bg=preto,fg=branco,padx=5)
label_descricao.pack(fill="x")
entry_descricao = tk.Entry(frame_2,width=70)
entry_descricao.pack(fill="x",pady=15)

label_data_inicio = tk.Label(frame_2,text="Data de Inicio:",bg=preto,fg=branco)
label_data_inicio.pack(fill="x")
entry_data_inicio = tk.Entry(frame_2)
entry_data_inicio.pack(fill="x",pady=15)

label_data_termino = tk.Label(frame_2,text="Data de término:",bg=preto,fg=branco)
label_data_termino.pack(fill="x")
entry_data_termino = tk.Entry(frame_2)
entry_data_termino.pack(fill="x",pady=15)

label_status = tk.Label(frame_2,text="Status:",bg=preto,fg=branco)
label_status.pack(fill="x")
combo_status = ttk.Combobox(frame_2,state="readonly")
combo_status['values'] = ('A Fazer', 'Em Andamento', 'Concluído')
combo_status.pack(fill="x",pady=15)
combo_status.current()

botao_registrar_tarefa = tk.Button(frame_2,text="Registrar",bg="#ff0015",command=registrar_tarefas)
botao_registrar_tarefa.pack(fill="x",pady=5)
botao_remover_tarefas_concluidas = tk.Button(frame_2,text="Marcar como concluida", command=marcar_concluida,bg=vermelho)
botao_remover_tarefas_concluidas.pack(fill="x")



janela.mainloop()