import random
import pygame
import sys

# ------------------------------------------- Fonctions utilitaires pour les fichiers -------------------------------------------
# Fonctions pour lire et écrire des mots dans un fichier
def read_words(mots_txt):
    try:
        with open(mots_txt, "r") as file:
            mots = file.readlines()
            return [mot.strip() for mot in mots]
    except FileNotFoundError:
        return []
    
def write_words(mots_txt, mot):
    with open(mots_txt, "a") as file:
        file.write(mot + "\n")

# Fonction pour choisir un mot aléatoire dans une liste de mots
def choice_word(mots_txt):
    mots = read_words(mots_txt)
    if mots:
        return random.choice(mots)
    else:
        return None

# Fonctions pour lire et écrire les scores dans un fichier   
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

# Fonction pour demander le nom du joueur
def ask_name():
    nom = input("Entrez votre nom : ").strip()
    if not nom:
        return "Joueur Anonyme"
    return nom

# --------------------------------------------- Fonctions pour le jeu du pendu -------------------------------------------
# Constantes pour la fenêtre Pygame
LARGEUR, HAUTEUR = 800, 600
COULEUR_FOND = (255, 255, 255)
COULEUR_TEXTE = (0, 0, 0)
COULEUR_PENDU = (255, 0, 0)
ESSAIS_MAX = 6

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("The Hangman Game")
police = pygame.font.Font(None, 48)

#fonction pour dessiner le pendu
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

#fonction pour afficher du texte sur la fenêtre
def display_text(texte, x, y, couleur=COULEUR_TEXTE, centrer=False):
    rendu = police.render(texte, True, couleur)
    rect = rendu.get_rect()
    if centrer:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    fenetre.blit(rendu, rect)
def display_word(mot, lettres_trouvees):
    return " ".join([lettre if lettre in lettres_trouvees else "_" for lettre in mot])

# Fonction principale pour jouer au jeu du pendu

def menu_principal():
    while True:
        fenetre.fill(COULEUR_FOND)
        display_text("Menu Principal", LARGEUR // 2, 100, centrer=True)
        display_text("1. Jouer", LARGEUR // 2, 200, centrer=True)
        display_text("2. Ajouter un mot", LARGEUR // 2, 300, centrer=True)
        display_text("Appuyez sur Échap pour quitter", LARGEUR // 2, 400, centrer=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "jouer"
                elif event.key == pygame.K_2:
                    return "ajouter"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# Interface pour demander un nom
def ask_name_interface():
    nom = ""
    actif = True
    while actif:
        fenetre.fill(COULEUR_FOND)
        display_text("Entrez votre nom :", LARGEUR // 2, 200, centrer=True)
        display_text(nom, LARGEUR // 2, 300, centrer=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Entrée pour valider
                    if nom.strip() == "":
                        nom = "Joueur Anonyme"
                    return nom
                elif event.key == pygame.K_BACKSPACE:  # Retour arrière
                    nom = nom[:-1]
                else:
                    nom += event.unicode


# Interface pour ajouter un mot
def ajouter_mot_interface(liste_de_mots):
    mot = ""
    actif = True
    while actif:
        fenetre.fill(COULEUR_FOND)
        display_text("Entrez un nouveau mot :", LARGEUR // 2, 200, centrer=True)
        display_text(mot, LARGEUR // 2, 300, centrer=True)
        display_text("Appuyez sur Entrée pour valider", LARGEUR // 2, 400, centrer=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    mot = mot.strip().upper()
                    if mot.isalpha():
                        write_words(liste_de_mots, mot)
                        return
                elif event.key == pygame.K_BACKSPACE:
                    mot = mot[:-1]
                else:
                    mot += event.unicode

def play(mots_txt="mots.txt", fichier_scores="scores.txt"):
    while True:
        choix = menu_principal()
        if choix == "jouer":
            mots = read_words(mots_txt)
            if not mots:
                print("Aucun mot à jouer. Ajoutez des mots avant de jouer.")
                continue

            mot = choice_word(mots_txt)
            if mot is None:
                print("Erreur : Aucun mot n'a été sélectionné.")
                return

            mot = mot.upper()
            nom = ask_name_interface()
            scores = read_scores(fichier_scores)
            score_joueur = scores.get(nom, 0)

            lettres_trouvees = []
            lettres_ratees = []
            erreurs = 0
            jeu_en_cours = True

            while jeu_en_cours:
                fenetre.fill(COULEUR_FOND)
                draw_hangman(erreurs)
                mot_affiche = display_word(mot, lettres_trouvees)
                display_text(f"Mot : {mot_affiche}", LARGEUR // 2, 100, centrer=True)
                display_text(f"Lettres ratées : {', '.join(lettres_ratees)}", LARGEUR // 2, 200, centrer=True)
                display_text(f"Score : {score_joueur}", LARGEUR // 2, 300, centrer=True)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        jeu_en_cours = False
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        lettre = event.unicode.upper()
                        if lettre.isalpha() and lettre not in lettres_trouvees and lettre not in lettres_ratees:
                            if lettre in mot:
                                lettres_trouvees.append(lettre)
                            else:
                                lettres_ratees.append(lettre)
                                erreurs += 1

                if "_" not in display_word(mot, lettres_trouvees):
                    display_text("Vous avez gagné !", LARGEUR // 2, 400, centrer=True)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    score_joueur += 10
                    jeu_en_cours = False
                elif erreurs >= ESSAIS_MAX:
                    display_text(f"Vous avez perdu ! Le mot était : {mot}", LARGEUR // 2, 400, centrer=True)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    score_joueur -= 5
                    jeu_en_cours = False

            scores[nom] = score_joueur
            write_scores(scores, fichier_scores)

        elif choix == "ajouter":
            ajouter_mot_interface(mots_txt)

if __name__ == "__main__":
    play()