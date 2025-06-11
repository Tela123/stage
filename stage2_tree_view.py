import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import *
#pour la boite des messages
from tkinter import messagebox as mb


r=tk.Tk()
r.title("Formulaire Tree View Mysql")
r.geometry("900x350")

connect = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stage1"
)
conn = connect.cursor()
    
    #recuprer les données de la bd
conn.execute("SELECT * FROM example  ORDER BY nom")

tree=ttk.Treeview(r)
tree['show']='headings'

#style de la page
s=ttk.Style(r)
s.theme_use("winnative")

s.configure(".", font=('Helvetica', 11))
s.configure("Treeview.Heading", foreground='darkblue', font=('Helvetica', 11, "bold", "italic"))

#definir le nombre de colonnes
tree["columns"]=("ID", "Nom", "Prenom","Email", "N° Tél", "Age", "Mot de passe")

#definir la taille de chaque colonne
tree.column("ID", width=45, minwidth=45, anchor=tk.CENTER)
tree.column("Nom", width=135, minwidth=135, anchor=tk.CENTER)
tree.column("Prenom", width=135, minwidth=135, anchor=tk.CENTER)
tree.column("Email", width=135, minwidth=135, anchor=tk.CENTER)
tree.column("N° Tél", width=135, minwidth=135, anchor=tk.CENTER)
tree.column("Age", width=45, minwidth=45, anchor=tk.CENTER)
tree.column("Mot de passe", width=135, minwidth=135, anchor=tk.CENTER)

tree.heading("ID",text="id", anchor=tk.CENTER)
tree.heading("Nom",text="Nom", anchor=tk.CENTER)
tree.heading("Prenom",text="Prenom", anchor=tk.CENTER)
tree.heading("Email",text="Email", anchor=tk.CENTER)
tree.heading("N° Tél", text="N° Tél", anchor=tk.CENTER)
tree.heading("Age", text="Age", anchor=tk.CENTER)
tree.heading("Mot de passe",text="Mot de passe", anchor=tk.CENTER)

i=0
for ro in conn:
    tree.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6]))
    i=i+1
    
hsb=ttk.Scrollbar(r, orient="horizontal")
hsb.configure(command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
hsb.pack(fill=X, side=BOTTOM)

vsb=ttk.Scrollbar(r, orient="vertical")
vsb.configure(command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(fill=Y, side=RIGHT)

tree.pack()

nom=tk.StringVar()
prenom=tk.StringVar()
email=tk.StringVar()
phone=tk.IntVar()
age=tk.IntVar()
mot_de_passe=tk.StringVar()
def ajouter(tree):
    f=Frame(r, width=400, height=370, background="lightgrey")
    f.place(x=100, y=250)
    
    l1=Label(f, text="Nom", width=12, font=('Times', 11, 'bold'))
    e1=Entry(f, textvariable=nom, width=25)
    l1.place(x=50, y=30)
    e1.place(x=170, y=30)
    
    l2=Label(f, text="Prenom", width=12, font=('Times', 11, 'bold'))
    e2=Entry(f, textvariable=prenom, width=25)
    l2.place(x=50, y=70)
    e2.place(x=170, y=70)
    
    l3=Label(f, text="Email", width=12, font=('Times', 11, 'bold'))
    e3=Entry(f, textvariable=email, width=25)
    l3.place(x=50, y=110)
    e3.place(x=170, y=110)
    
    l4=Label(f, text="N° Tél", width=12, font=('Times', 11, 'bold'))
    e4=Entry(f, textvariable=phone, width=25)
    l4.place(x=50, y=150)
    e4.place(x=170, y=150)
    
    l5=Label(f, text="Age", width=12, font=('Times', 11, 'bold'))
    e5=Entry(f, textvariable=age, width=25)
    l5.place(x=50, y=190)
    e5.place(x=170, y=190)
    e5.delete(0, END)
    
    l6=Label(f, text="Mot de passe", width=12, font=('Times', 11, 'bold'))
    e6=Entry(f, textvariable=mot_de_passe, width=25)
    l6.place(x=50, y=220)
    e6.place(x=170, y=220)
    
    def enregistrer():
        nonlocal e1, e2, e3, e4, e5, e6
        usernom=nom.get()
        u_pre=prenom.get()
        u_mail=email.get()
        u_phone=phone.get()
        u_age=age.get()
        u_mdp=mot_de_passe.get()
        conn.execute("INSERT INTO example (nom, prenom, email, mot_de_passe, phone, age) VALUES (%s, %s, %s, %s, %s, %s)",
                       (usernom, u_pre, u_mail, u_mdp, u_phone, u_age ))
        #print(conn.lastrowid)
        connect.commit()
       # tree.insert('', 'end', text="", values=(lastrowid,usernom, u_pre, u_mail, u_mdp, u_phone, u_age))
        tree.insert('', 'end', text="", values=(usernom, u_pre, u_mail, u_mdp, u_phone, u_age))
        mb.showinfo("Succès", "Infos enregistrées.")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        f.destroy()
        
    submibutton=tk.Button(f, text="Ajouter", command=enregistrer)
    submibutton.configure(font=('Times', 11, 'bold'), bg='green', fg='white')
    submibutton.place(x=100, y=280)
    
    cancelbutton=tk.Button(f, text="Effacer", command=f.destroy)
    cancelbutton.configure(font=('Times', 11, 'bold'), bg='red', fg='white')
    cancelbutton.place(x=240, y=280)
    
def supprimer(tree):
    selected_item = tree.selection()
    if not selected_item:
        mb.showwarning("Avertissement", "Veuillez sélectionner un élément à supprimer.")
        return

    selected_item = selected_item[0]
    values = tree.item(selected_item)['values']
    print(values)

    uid = values[0]  # ✅ Ici, on prend le premier élément de la liste des valeurs

    del_query = "DELETE FROM example WHERE id = %s"
    sel_data = (uid,)
    
    try:
        conn.execute(del_query, sel_data)
        connect.commit()
        tree.delete(selected_item)
        mb.showinfo("Succès", "Supprimé avec succès")
    except Exception as e:
        mb.showerror("Erreur", f"Erreur lors de la suppression : {e}")


def modifier(id_utilisateur, nom, prenom, email, phone, age, mot_de_passe):
    # Requête SQL de mise à jour
    sql = """
    UPDATE exemple
    SET nom = %s,
    prenom = %s,
    email = %s,
    phone = %s,
    age = %s,
    mot_de_passe = %s
    WHERE id = %s
        """

    valeurs = (nom, prenom, email, phone, age, mot_de_passe, id_utilisateur)

    conn.execute(sql, valeurs)
    connect.commit()

    if conn.rowcount == 0:
        print("Aucun enregistrement trouvé avec cet ID.")
    else:
        print("Modification effectuée avec succès.")

 
    
insertbutton=tk.Button(r, text="Ajouter", command=lambda:ajouter(tree))
insertbutton.configure(font=('calibri', 14, 'bold'), bg='green', fg='white')
insertbutton.place(x=200, y=260)

updatebutton=tk.Button(r, text="Modifier", command=lambda:modifier(tree))
updatebutton.configure(font=('calibri', 14, 'bold'), bg='blue', fg='white')
updatebutton.place(x=300, y=260)

deletebutton=tk.Button(r, text="Supprimer", command=lambda:supprimer(tree))
deletebutton.configure(font=('calibri', 14, 'bold'), bg='red', fg='white')
deletebutton.place(x=400, y=260)

#tree.column()
r.mainloop()