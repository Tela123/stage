#importe les biblio

# pour le graphisme
import tkinter as tk
#pour la boite des messages
from tkinter import messagebox
#pour la connexion à la bd
import mysql.connector

# Fonction d'enregistrement utilisateur: je recupere via get les infos
def enregistrer():
    nom = nom_entry.get()
    prenom = prenom_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    phone = phone_entry.get()
    age = age_entry.get()

#je controle que les champs sont remplis
    if not (nom and prenom and email and password and phone and age):
        messagebox.showwarning("Erreur", "Tous les champs sont requis.")
        return

#je verifie que l'age estvun nombre
    if not age.isdigit():
        messagebox.showerror("Erreur age", "l'age doit etre un nombre.")
        return
#je me connecte à la bd
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="stage1"
        )
        cursor = conn.cursor()
        
        #j'enregistre dans la bd
        cursor.execute("INSERT INTO example (nom, prenom, email, mot_de_passe, phone, age) VALUES (%s, %s, %s, %s, %s, %s)",
                       (nom, prenom, email, password, phone, int(age)))
        conn.commit()
        conn.close()
        #message de validation
        messagebox.showinfo("Succès", "Inscription réussie.")
        #delete permet de vider les champs de saisie apres une validation
        nom_entry.delete(0, tk.END)
        prenom_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        #je gere les cas d'erreurs avec les exception
    except mysql.connector.IntegrityError:
        messagebox.showerror("Erreur ", "email deja utilise")
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur MySQL", f"{err}")

# Fenêtre principale
root = tk.Tk()
root.title("Formulaire Inscription")
root.geometry("400x500")

tk.Label(root, text="Nom").pack(pady=3)
nom_entry = tk.Entry(root)
nom_entry.pack()

tk.Label(root, text="Prénom").pack(pady=3)
prenom_entry = tk.Entry(root)
prenom_entry.pack()

tk.Label(root, text="Email").pack(pady=3)
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Mot de passe").pack(pady=3)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Label(root, text="N° TEL").pack(pady=3)
phone_entry = tk.Entry(root)
phone_entry.pack()

tk.Label(root, text="Age").pack(pady=3)
age_entry = tk.Entry(root)
age_entry.pack()

tk.Button(root, text="S'inscrire", command=enregistrer, bg="green", fg="white").pack(pady=15)

root.mainloop()