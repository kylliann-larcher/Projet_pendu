import random, sys, pygame

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
LARGEUR, HAUTEUR = 900, 600
Screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("image de fond avec pygame")
COULEUR_TEXTE = (255, 255, 255)
COULEUR_PENDU = (255, 0, 0)
ESSAIS_MAX = 8
COULEUR_FOND = (0, 0, 0)  # Noir

pygame.init()  # Initialisation de Pygame
pygame.mixer.init()  # Initialisation du module audio

ARRIERE_PLAN = r"C:\Users\kylli/Desktop\Spe_ia\Projet_pendu\pendu1.jpg"
MUSIQUE_PERDU = r"\Users\kylli\Desktop\Spe_ia\Projet_pendu\perdu.mp3"
MUSIQUE_FOND = r"C:\Users\kylli\Desktop\Spe_ia\Projet_pendu\music.mp3"
MUSIQUE_VICTOIRE = r"C:\Users\kylli\Desktop\Spe_ia\Projet_pendu\victoire.mp3"
IMAGE_MENU = r"C:\Users\kylli\Desktop\Spe_ia\Projet_pendu\menu.JPEG"


# Chargement des médias
menu = pygame.image.load(IMAGE_MENU)  # Charge l'image du menu
image_fond = pygame.image.load(ARRIERE_PLAN)  # Charge l'image d'arrière-plan
pygame.mixer.music.load(MUSIQUE_FOND)        # Charge la musique de fond
son_perdu = pygame.mixer.Sound(MUSIQUE_PERDU)  # Charge la musique de défaite
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
    if erreurs >= 7:
        pygame.draw.line(fenetre, COULEUR_PENDU, (x + 150, y - 80), (x + 130, y - 40), 5)  # Jambe gauche
    if erreurs >= 8:
        pygame.draw.line(fenetre, COULEUR_PENDU, (x + 150, y - 80), (x + 170, y - 40), 5)  # Jambe droite

def gestion_messages(erreurs):
    if erreurs == 5:
        display_text("Ça commence à chauffer !", LARGEUR // 2, 250, centrer=True)
    elif erreurs == 7:
        display_text("Presque perdu !", LARGEUR // 2, 250, centrer=True)
    elif erreurs == 8:
        display_text("Oh non, tu as perdu...", LARGEUR // 2, 250, centrer=True)
        jouer_effet_perdu()
        return False  # Indique que la partie est terminée
    return True
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
        fenetre.blit(menu, (0, 0))  # Affiche l'image d'arrière-plan
        pygame.mixer.music.play(-1)  # Lecture en boucle infinie
        display_text("Menu Principal", LARGEUR // 2, 100, centrer=True)
        display_text("1. Jouer", LARGEUR // 2, 200, centrer=True)
        display_text("2. Ajouter un mot", LARGEUR // 2, 300, centrer=True)
        display_text("Appuyez sur Échap pour quitter", LARGEUR // 2, 500, centrer=True)
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
        #fenetre.fill(COULEUR_FOND)
        fenetre.blit(image_fond, (0, 0))  # Afficher l'image de fond
        display_text("Entrez votre nom :", LARGEUR // 2, 400, centrer=True)
        display_text(nom, LARGEUR // 2, 300, centrer=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Entrée pour valider
                    if nom.strip() == "":
                        return "Joueur Anonyme"
                    return nom.strip()
                elif event.key == pygame.K_BACKSPACE:  # Retour arrière
                    nom = nom[:-1]
                else:
                    nom += event.unicode



# Interface pour ajouter un mot
def ajouter_mot_interface(liste_de_mots):
    mot = ""
    actif = True
    while actif:
        # Nettoie l'écran avant d'afficher
        fenetre.blit(image_fond, (0, 0))  
        
        # Affiche les instructions et le mot en cours de saisie
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
                        # Écrit le mot dans le fichier
                        write_words(liste_de_mots, mot)
                        
                        # Affiche un message de confirmation
                        fenetre.blit(image_fond, (0, 0))  # Efface l'écran
                        display_text("Mot ajouté avec succès !", LARGEUR // 2, HAUTEUR // 2, centrer=True, couleur=(0, 255, 0))
                        pygame.display.flip()
                        
                        # Attend 3 secondes
                        pygame.time.delay(3000)
                        
                        return  # Retour au menu principal après l'ajout
                elif event.key == pygame.K_BACKSPACE:
                    mot = mot[:-1]
                else:
                    mot += event.unicode

def clear_screen(image_fond):
    """Efface l'écran en affichant une image de fond."""
    fenetre.blit(image_fond, (0, 0))

def draw_game_state(mot, lettres_trouvees, lettres_ratees, score_joueur, erreurs):
    """Affiche l'état actuel du jeu à l'écran."""
    draw_hangman(erreurs)
    mot_affiche = display_word(mot, lettres_trouvees)
    display_text(f"Mot : {mot_affiche}", LARGEUR // 2, 100, centrer=True)
    display_text(f"Lettres ratées : {', '.join(lettres_ratees)}", LARGEUR // 2, HAUTEUR - 100, centrer=True)
    display_text(f"Score : {score_joueur}", LARGEUR // 2, 200, centrer=True)
    pygame.display.flip()

def handle_events(lettres_trouvees, lettres_ratees, mot):
    """Gère les événements du joueur, retourne les états mis à jour."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False, None
            elif event.unicode.isalpha():
                lettre = event.unicode.upper()
                if lettre in lettres_trouvees or lettre in lettres_ratees:
                    clear_screen(image_fond)  # Efface l'écran avant d'afficher le message
                    display_text("Lettre déjà essayée.", LARGEUR // 2, HAUTEUR - 50, centrer=True)
                    pygame.display.flip()
                else:
                    return True, lettre
    return True, None

def check_victory(mot, lettres_trouvees, score_joueur):
    """Vérifie si le joueur a gagné."""
    if all(l in lettres_trouvees for l in mot):
        pygame.mixer.Sound(MUSIQUE_VICTOIRE).play()
        display_text("Félicitations, vous avez gagné !", LARGEUR // 2, 300, centrer=True)
        pygame.time.wait(3000)
        return True, score_joueur + 10
    return False, score_joueur

def check_defeat(erreurs, ESSAIS_MAX):
    """Vérifie si le joueur a perdu."""
    if erreurs >= ESSAIS_MAX:
        display_text("Vous avez perdu...", LARGEUR // 2, 400, centrer=True)
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(son_perdu)
        pygame.time.wait(3000)
        return True
    return False

def play_round(mot, lettres_trouvees, lettres_ratees, erreurs, score_joueur, image_fond):
    """Joue un tour du jeu, retourne les états mis à jour."""
    clear_screen(image_fond)
    draw_game_state(mot, lettres_trouvees, lettres_ratees, score_joueur, erreurs)
    jeu_en_cours, lettre = handle_events(lettres_trouvees, lettres_ratees, mot)
    if not jeu_en_cours:
        return False, erreurs, score_joueur
    if lettre:
        if lettre in mot:
            lettres_trouvees.append(lettre)
        else:
            lettres_ratees.append(lettre)
            erreurs += 1
    victoire, score_joueur = check_victory(mot, lettres_trouvees, score_joueur)
    if victoire:
        return False, erreurs, score_joueur
    if check_defeat(erreurs, ESSAIS_MAX):
        return False, erreurs, score_joueur
    return True, erreurs, score_joueur

def play(mots_txt="mots.txt", fichier_scores="scores.txt"):
    """Boucle principale du jeu."""
    while True:
        choix = menu_principal()
        if choix == "jouer":
            mots = read_words(mots_txt)
            if not mots:
                print("Aucun mot à jouer. Ajoutez des mots avant de jouer.")
                continue
            mot = choice_word(mots_txt).upper()
            nom = ask_name_interface()
            scores = read_scores(fichier_scores)
            score_joueur = scores.get(nom, 0)
            lettres_trouvees, lettres_ratees = [], []
            erreurs = 0
            jeu_en_cours = True

            while jeu_en_cours:
                jeu_en_cours, erreurs, score_joueur = play_round(
                    mot, lettres_trouvees, lettres_ratees, erreurs, score_joueur, image_fond
                )
            scores[nom] = score_joueur
            write_scores(scores, fichier_scores)

        elif choix == "ajouter":
            ajouter_mot_interface(mots_txt)

if __name__ == "__main__":
    play()
