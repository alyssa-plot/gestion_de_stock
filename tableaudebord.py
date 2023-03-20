import mysql.connector
from tkinter import messagebox
import tkinter as tk
from tkinter import *

#On se connecte à notre base de données avec nos identifiants
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="azerty",
  database="boutique"
)

mycursor = mydb.cursor()

#Ensuite on va créer notre interface graphique, assez simple et épurée
master = Tk()
master.title("Tableau de bord de la boutique")

liste_produits = Listbox(master, height=10, width=50)
liste_produits.grid(row=0, column=0, rowspan=6, columnspan=2)
mycursor.execute("SELECT * FROM produit")
resultats = mycursor.fetchall()
for resultat in resultats:
  liste_produits.insert(END, resultat)

id_ = Label(master, text="id_")
id_.grid(row=0, column=2)
idtext = Entry(master, width=20)
idtext.grid(row=0, column=4)

nom = Label(master, text="Nom")
nom.grid(row=0, column=3)
nom_text = Entry(master, width=20)
nom_text.grid(row=0, column=5)

description = Label(master, text="Description")
description.grid(row=1, column=2)
description_text = Entry(master, width=20)
description_text.grid(row=1, column=4)

prix = Label(master, text="Prix")
prix.grid(row=1, column=3)
prix_text = Entry(master, width=20)
prix_text.grid(row=1, column=5)

quantite = Label(master, text="Quantité")
quantite.grid(row=2, column=2)
quantite_text = Entry(master, width=20)
quantite_text.grid(row=2, column=4)

categorie = Label(master, text="Catégorie")
categorie.grid(row=2, column=3)
categorie_text = Entry(master, width=20)
categorie_text.grid(row=2, column=5)

#Je vais créer les fonctions ajouter un produit, le modifier ou alors le supprimer reliées à leur touche
def ajouter_produit():
    sql = "INSERT INTO produit (nom, description, prix, quantite, categorie) VALUES (%s, %s, %s, %s, %s)"
    valeurs = (nom_text.get(), description_text.get(), prix_text.get(), quantite_text.get(), categorie_text.get())
    mycursor.execute(sql, valeurs)
    mydb.commit()
    liste_produits.insert(END, valeurs)
    nom_text.delete(0, END)
    description_text.delete(0, END)
    prix_text.delete(0, END)
    quantite_text.delete(0, END)
    categorie_text.delete(0, END)

#création du bouton ajouter produit
add_btn = Button(master, text="Ajouter un produit", command=ajouter_produit)
add_btn.grid(row=3, column=4)

#Ici la fonction pour supprimer un produit
def supprimer_produit():
  id = idtext.get()
  sql = "DELETE FROM produit WHERE id_produit = %s"
  val = (id,)

  mycursor.execute(sql, val)
  mydb.commit()

  idtext.delete(0, END)
  nom_text.delete(0, END)
  description_text.delete(0, END)
  prix_text.delete(0, END)
  quantite_text.delete(0, END)
  categorie_text.delete(0, END)
  liste_produits.delete(0, END)
  mycursor.execute("SELECT * FROM produit")
  resultats = mycursor.fetchall()
  for resultat in resultats:
    liste_produits.insert(END, resultat)

remove_btn = Button(master, text="Supprimer un produit", command=supprimer_produit)
remove_btn.grid(row=3, column=5)

#La fonction pour modifier un produit et une confirmation si vraiment vous souhaitez modifier
def afficher_produits():
  liste_produits.delete(0, END)
  mycursor.execute("SELECT * FROM produit")
  resultats = mycursor.fetchall()
  for resultat in resultats:
    liste_produits.insert(END, resultat)

def clear_entries():
  idtext.delete(0, END)
  nom_text.delete(0, END)
  description_text.delete(0, END)
  prix_text.delete(0, END)
  quantite_text.delete(0, END)
  categorie_text.delete(0, END)

def modifier_produit():
    id_produit = idtext.get()
    nom_produit = nom_text.get()
    description_produit = description_text.get()
    prix_produit = prix_text.get()
    quantite_produit = quantite_text.get()
    categorie_produit = categorie_text.get()

    if id_produit == "":
        messagebox.showerror("Erreur", "Veuillez rentrer l'ID du produit que vous voulez modifier")
        return
    if nom_produit == "" or description_produit == "" or prix_produit == "" or quantite_produit == "" or categorie_produit == "":
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs pour modifier le produit")
        return
    
    resultat = messagebox.askquestion("Confirmation", "Êtes-vous sûr de vouloir modifier ce produit ?")
    if resultat == "yes":
        sql = "UPDATE produit SET nom=%s, description=%s, prix=%s, quantite=%s, categorie=%s, WHERE id_produit = %s"
        val = (nom_produit, description_produit, prix_produit, quantite_produit, categorie_produit, id_produit)
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Modification", "Le produit a été modifié avec succès")
        clear_entries()
        afficher_produits() 

update_btn = Button(master, text="Modifier un produit", command=modifier_produit)
update_btn.grid(row=4, column=4)

master.mainloop()
