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

def choice_word(liste_de_mots): #fonction qui choisi un mot au hasard dans la liste
    mots = read_words(liste_de_mots)
    if mots:
        return random.choice(mots)
    else:
        return None

def display__(mot):
    for len(mot) in mot:
        print("_", end=" ")

#fonction qui lit les scores depusi un fichier texte
def read_scores(fichier = "scores.txt"):
    try:
        with open(fichier, "r") as file:
            lignes = file.readlines()
            scores = {}
            for ligne in lignes:
                nom, score = ligne.strip().split(":")
                scores[nom] = int(score)
            return scores
    except FileNotFoundError:
        print(f"Erreur : le fichier {fichier} est introuvable")
        return {}

#fonction qui ecrit les scores dans un fichier texte
def write_scores(scores, fichier = "scores.txt"):
    with open(fichier, "w") as file:
        for nom, score in scores.items():
            file.write(f"{nom}:{score}\n")

def demander_nom():

    nom = input("Entrez votre nom : ").strip()
    return nom
    if not nom:
        nom = " jouer Anonyme"
    return nom

def play():
