import random
import pygame

# --- Fonctions utilitaires pour les fichiers ---
def read_words(liste_de_mots):
    try:
        with open(liste_de_mots, "r") as file:
            mots = file.readlines()
            if not mots:
                print(f"Erreur : le fichier {liste_de_mots} est vide.")
                return []
            print(f"Mots lus : {mots}")  # Ajout d'un print pour voir les mots
            return [mot.strip() for mot in mots]
    except FileNotFoundError:
        print(f"Erreur : le fichier {liste_de_mots} est introuvable")
        return []

def write_words(liste_de_mots, mot):
    with open(liste_de_mots, "a") as file:
        file.write(mot + "\n")

def choice_word(liste_de_mots):
    mots = read_words(liste_de_mots)
    if mots:
        return random.choice(mots)
    else:
        return None
    
def read_scores(fichier="scores.txt"):
    try:
        with open(fichier, "r") as file:
            lignes = file.readlines()
            scores = {}
            for ligne in lignes:
                nom, score = ligne.strip().split(":")
                scores[nom] = int(score)
            return scores
    except FileNotFoundError:
        return {}

def write_scores(scores, fichier="scores.txt"):
    with open(fichier, "w") as file:
        for nom, score in scores.items():
            file.write(f"{nom}:{score}\n")

def demander_nom():
    nom = input("Entrez votre nom : ").strip()
    if not nom:
        return "Joueur Anonyme"
    return nom

# --- Configuration globale ---
LARGEUR, HAUTEUR = 800, 600
COULEUR_FOND = (255, 255, 255)
COULEUR_TEXTE = (0, 0, 0)
COULEUR_PENDU = (255, 0, 0)
ESSAIS_MAX = 6

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu du Pendu")
police = pygame.font.Font(None, 48)

def draw_hangman(erreurs):
    x, y = 100, 400
    if erreurs >= 1:
        pygame.draw.line(fenetre, COULEUR_PENDU, (x, y), (x + 200, y), 5)
    if erreurs >= 2:
        pygame.draw.line(fenetre, COULEUR_PENDU, (x + 50, y), (x + 50, y - 200), 5)
    if erreurs >= 3:
        pygame.draw.line(fenetre, COULEUR_PENDU, (x + 50, y - 200), (x + 150, y - 200), 5)
    if erreurs >= 4:
        pygame.draw.line(fenetre, COULEUR_PENDU, (x + 150, y - 200), (x + 150, y - 180), 5)
    if erreurs >= 5:
        pygame.draw.circle(fenetre, COULEUR_PENDU, (x + 150, y - 160), 20, 5)
    if erreurs >= 6:
        pygame.draw.line(fenetre, COULEUR_PENDU, (x + 150, y - 140), (x + 150, y - 80), 5)

def afficher_texte(texte, x, y):
    rendu = police.render(texte, True, COULEUR_TEXTE)
    fenetre.blit(rendu, (x, y))

def display_word(mot, lettres_trouvees):
    return " ".join([lettre if lettre in lettres_trouvees else "_" for lettre in mot])

def play(liste_de_mots="mots.txt", fichier_scores="scores.txt"):
    mots = read_words(liste_de_mots)
    if not mots:
        print("Aucun mot à jouer. Assurez-vous que le fichier mots.txt contient des mots.")
        return
    
    mot = choice_word(liste_de_mots)
    if mot is None:
        print("Erreur : Aucun mot n'a été sélectionné.")
        return
    
    mot = mot.upper() 

    nom = demander_nom()
    scores = read_scores(fichier_scores)
    score_joueur = scores.get(nom, 0)

    lettres_trouvees = []
    lettres_ratees = []
    erreurs = 0
    jeu_en_cours = True

    print(f"Bienvenue, {nom}! Votre score actuel est de {score_joueur}.")

    while jeu_en_cours:
        fenetre.fill(COULEUR_FOND)
        draw_hangman(erreurs)
        mot_affiche = display_word(mot, lettres_trouvees)
        afficher_texte(f"Mot : {mot_affiche}", 300, 100)
        afficher_texte(f"Lettres ratées : {', '.join(lettres_ratees)}", 300, 200)
        afficher_texte(f"Score : {score_joueur}", 300, 300)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_en_cours = False
                break
            elif event.type == pygame.KEYDOWN:
                lettre = event.unicode.upper()
                if lettre.isalpha() and lettre not in lettres_trouvees and lettre not in lettres_ratees:
                    if lettre in mot:
                        lettres_trouvees.append(lettre)
                    else:
                        lettres_ratees.append(lettre)
                        erreurs += 1

        if "_" not in display_word(mot, lettres_trouvees):
            afficher_texte("Vous avez gagné !", 300, 400)
            pygame.display.flip()
            pygame.time.wait(2000)
            score_joueur += 10
            jeu_en_cours = False
        elif erreurs >= ESSAIS_MAX:
            afficher_texte(f"Vous avez perdu ! Le mot était : {mot}", 300, 400)
            pygame.display.flip()
            pygame.time.wait(2000)
            score_joueur -= 5
            jeu_en_cours = False

    scores[nom] = score_joueur
    write_scores(scores, fichier_scores)
    print(f"Merci d'avoir joué, {nom}! Votre nouveau score est de {score_joueur}.")
    pygame.quit()

if __name__ == "__main__":
    play()
