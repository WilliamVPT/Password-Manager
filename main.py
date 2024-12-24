from time import sleep
from tkinter import messagebox
from tkinter.messagebox import *
from cryptography.fernet import Fernet
import json
import secrets
import string
import os
import tkinter as tk

# Générer ou charger une clé
def load_or_generate_key(filename='key.key'):
    if not os.path.exists(filename):
        key = Fernet.generate_key()
        with open(filename, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(filename, 'rb') as key_file:
            key = key_file.read()
    return key

key = load_or_generate_key()
cipher_suite = Fernet(key)

#génération du mot de passe
def generate_password(length=20):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

#crypter/décrypter
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

#sauvegarde/chargement
def save_passwords(data, filename='passwords.json'):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_passwords(filename='passwords.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
def ajouter():
    passwords = load_passwords()

    def valider():
        service = entry.get().strip()
        if not service:
            showinfo("Erreur", "Veuillez saisir un service")
            return
        
        password = generate_password()
        passwords[service] = encrypt_password(password).decode()
        save_passwords(passwords)
        showinfo("Mot de passe ajouté", f"Le mot de passe pour '{service}' est : {password}")
        f_ajout.destroy()

    # Interface pour ajouter un mot de passe
    f_ajout = tk.Toplevel()  # Utilisez Toplevel pour éviter les conflits avec Tk
    f_ajout.title("Ajout de mot de passe")

    # Champ de saisie
    tk.Label(f_ajout, text="Nom du service :").pack()
    entry = tk.Entry(f_ajout)  # Directement sans StringVar
    entry.pack()

    # Bouton de validation
    tk.Button(f_ajout, text="Valider", command=valider).pack()

    # Met le focus sur le champ de saisie
    entry.focus()

    f_ajout.mainloop()

def lire():
    def afficher_mdp(service):
        f_aff_mdp = tk.Toplevel()
        encrypted_password = passwords.get(service)
        value = tk.StringVar()
        if encrypted_password:
            value.set(decrypt_password(encrypted_password.encode()))
            tk.Label(f_aff_mdp, text=f"Le mot de passe pour '{service}' est : ").pack()
            tk.Entry(f_aff_mdp, textvariable=value).pack()
                     
        else:
            tk.Label(f_aff_mdp, text=f"Le mot de passe pour '{service}' est introuvable").pack()

        f_lire.destroy()
        
        
    passwords = load_passwords()

    # Fenêtre Tkinter pour afficher les services
    f_lire = tk.Tk()
    f_lire.title("Lire un mot de passe")

    # Liste des services
    for service in passwords.keys():
        tk.Button(f_lire, text=service, command=lambda s=service: afficher_mdp(s)).pack()

    f_lire.mainloop()

def supprimer():
    def supprimer_mdp(service):
        # Demander une confirmation avant de supprimer le mot de passe
        confirmation = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer le mot de passe pour '{service}' ?")
        
        if confirmation:  # Si l'utilisateur confirme la suppression
            del passwords[service]
            save_passwords(passwords)
            showinfo("Suppression", f"Le mot de passe pour '{service}' a été supprimé")
            f_suppr.destroy()  # Ferme la fenêtre après suppression

    f_suppr = tk.Tk()
    f_suppr.title("Suppression de mot de passe")

    passwords = load_passwords()
    for service in passwords:
        tk.Button(f_suppr, text=service, command=lambda s=service: supprimer_mdp(s)).pack()

    f_suppr.mainloop()

    
#main
if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title("Gestionnaire de mots de passe")
    passwords = load_passwords()
    tk.Label(fenetre, text="Bienvenue dans le gestionnaire de mots de passe !").pack()
  
    tk.Button(fenetre, text="Ajouter", command=ajouter).pack()
    tk.Button(fenetre, text="Lire", command=lire).pack()
    tk.Button(fenetre, text="Supprimer", command=supprimer).pack()
    fenetre.mainloop() 