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
    
#main
if __name__ == "__main__":
    passwords = load_passwords()
    print("Bienvenue dans le gestionnaire de mots de passe !")
    action = ""
    while(action != "fin"):
        action = input("Que voulez-vous faire ? (lire/ajouter/supprimer/fin) ").lower()

        if action == "ajouter":
            service = input("Service : ")
            password = generate_password()
            passwords[service] = encrypt_password(password).decode()
            save_passwords(passwords)
            print(f"Le mot de passe pour {service} est {password}")

        elif action == "lire":
            for service in passwords:
                print(service)

            service = input("Service : ")
            if service in passwords:
                encrypted_password = passwords[service]
                print(f"Le mot de passe pour {service} est {decrypt_password(encrypted_password.encode())}")
            else:
                print("Service introuvable")

        elif action == "supprimer":
            for service in passwords:
                print(service)

            service = input("Service : ")
            if service in passwords:
                del passwords[service]
                save_passwords(passwords)
                print(f"Le mot de passe pour {service} a été supprimé")
            else:
                print("Service introuvable")

        
        