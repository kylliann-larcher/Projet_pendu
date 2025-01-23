import random

def read_words(liste_de_mots):
    try:
        with open(liste_de_mots,"r") as file: #ouvre le fichier en mode lecture
            mots = file.readlines() #lit toutes lingnes
            return  [mot.strip()for mot in mots] #supprime les espaces et les retours a la ligne
    except FileNotFoundError:
        print(f"Erreur : le fichier {liste_de_mots} est introuvable")
        return[]

def write_words(liste_de_mots, mot):
    with open(liste_de_mots,"a") as file: #ouvre le fichier en mode ecriture
        file.write(mot + "\n") #ecrit le mot et un retour a la ligne

def choice_word(liste_de_mots):
    mots = read_words(liste_de_mots)
    if mots:
        return random.choice(mots)
    else:
        return None

def display__(mot):
    for len(mot) in mot:
        print("_", end=" ")


  