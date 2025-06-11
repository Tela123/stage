import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import *
#pour la boite des messages
from tkinter import messagebox as mb

# Connexion à MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="stage1"
    )

def afficher():
    for item in tree.get_children():
        tree.delete(item)
    cnx = connect_db()
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM example")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    cursor.close()
    cnx.close()

def ajouter():
    nom = nom_var.get()
    prenom = prenom_var.get()
    genre = genre_var.get()
    email=email_var.get()
    phone=phone_var.get()
    age=age_var.get()
    mdp=mdp_var.get()

    if not (nom and prenom and genre):
        mb.showwarning("Champs vides", "Veuillez remplir tous les champs.")
        return

    cnx = connect_db()
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO example (nom, prenom, sexe, email, phone, age,mot_de_passe) VALUES (%s, %s, %s,%s, %s, %s, %s)", (nom, prenom, genre,email,phone,age,mdp))
    cnx.commit()
    cursor.close()
    cnx.close()
    afficher()
    vider()

def supprimer():
    selected = tree.selection()
    if not selected:
        mb.showwarning("Sélection", "Veuillez sélectionner une ligne à supprimer.")
        return
    item = tree.item(selected[0])
    id = item['values'][0]
    cnx = connect_db()
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM example WHERE id = %s", (id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    afficher()

def remplir_champs(event):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        values = item['values']
        nom_var.set(values[1])
        prenom_var.set(values[2])
        genre_var.set(values[3])
        email_var.set(values[4])
        phone_var.set(values[5])
        age_var.set(values[6])
        mdp_var.set(values[7])

def modifier():
    selected = tree.selection()
    if not selected:
        mb.showwarning("Sélection", "Veuillez sélectionner une ligne à modifier.")
        return
    item = tree.item(selected[0])
    id = item['values'][0]

    cnx = connect_db()
    cursor = cnx.cursor()
    cursor.execute("""
        UPDATE example SET nom = %s, prenom = %s, sexe = %s, email = %s, phone = %s, age = %s, mot_de_passe = %s WHERE id = %s
    """, (nom_var.get(), prenom_var.get(), genre_var.get(), email_var.get(), phone_var.get(), age_var.get(), mdp_var.get(), id))
    cnx.commit()
    cursor.close()
    cnx.close()
    afficher()
    vider()

def vider():
    nom_var.set("")
    prenom_var.set("")
    genre_var.set("")
    email_var.set("")
    phone_var.set("")
    age_var.set("")
    mdp_var.set("")
    recherche_var.set("")
    
def afficher(terme="", champ="nom"):
    for item in tree.get_children():
        tree.delete(item)

    cnx = connect_db()
    cursor = cnx.cursor()

    if terme:
        requete = f"SELECT * FROM example WHERE {champ} LIKE %s"
        cursor.execute(requete, (f"{terme}%",))
    else:
        cursor.execute("SELECT * FROM example")

    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    cursor.close()
    cnx.close()

def rechercher(event):
    valeur = recherche_var.get()
    champ = attribut_var.get()
    afficher(valeur, champ)

# Interface Tkinter
root = tk.Tk()
root.title("CRUD Tkinter avec MySQL et Combobox")

tk.Label(root, text="Nom").grid(row=0, column=0)
nom_var = tk.StringVar()
tk.Entry(root, textvariable=nom_var).grid(row=0, column=1)

tk.Label(root, text="Prénom").grid(row=1, column=0)
prenom_var = tk.StringVar()
tk.Entry(root, textvariable=prenom_var).grid(row=1, column=1)

tk.Label(root, text="genre").grid(row=2, column=0)
genre_var = tk.StringVar()
genre_cb = ttk.Combobox(root, textvariable=genre_var, values=["Masculin", "Féminin"])
genre_cb.grid(row=2, column=1)

tk.Label(root, text="Email").grid(row=3, column=0)
email_var = tk.StringVar()
tk.Entry(root, textvariable=email_var).grid(row=3, column=1)

tk.Label(root, text="N° Tél").grid(row=4, column=0)
phone_var = tk.StringVar()
tk.Entry(root, textvariable=phone_var).grid(row=4, column=1)

tk.Label(root, text="Age").grid(row=5, column=0)
age_var = tk.StringVar()
tk.Entry(root, textvariable=age_var).grid(row=5, column=1)

tk.Label(root, text="Mot de Passe").grid(row=6, column=0)
mdp_var = tk.StringVar()
tk.Entry(root, textvariable=mdp_var).grid(row=6, column=1)

frame_recherche = tk.Frame(root)
frame_recherche.grid(row=0, column=2)

#tk.Label(root, text="Recherche :").grid(row=0, column=2)
recherche_var = tk.StringVar()
entry_recherche = tk.Entry(root, textvariable=recherche_var, width=40)
entry_recherche.grid(row=0, column=3)
entry_recherche.bind("<KeyRelease>", rechercher)

attribut_var = tk.StringVar(value="nom")
choix_menu = ttk.Combobox(frame_recherche, textvariable=attribut_var, values=["nom", "email","prenom","sexe"], width=10, state="readonly")
choix_menu.grid(row=0, column=3)

tk.Button(root, text="Ajouter", bg='green', font=('Times',11, 'bold', 'italic'), fg='white',  command=ajouter).grid(row=7, column=0)
tk.Button(root, text="Modifier", bg='blue', font=('Times',11, 'bold', 'italic'), fg='white', command=modifier).grid(row=7, column=1)
tk.Button(root, text="Supprimer", bg='red', font=('Helvetica',11, 'bold', 'italic'), fg='white',  command=supprimer).grid(row=7, column=2)
tk.Button(root, text="Vider", bg='grey', font=('Franklin',11, 'bold', 'italic'), fg='white',  command=vider).grid(row=7, column=3)

columns = ("id", "nom", "prenom", "genre", "email", "n° Tel", "age", "password")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.grid(row=9, column=0, columnspan=8)

tree.bind("<<TreeviewSelect>>", remplir_champs)
s=ttk.Style(root)
s.theme_use("winnative")

afficher()
root.mainloop()
