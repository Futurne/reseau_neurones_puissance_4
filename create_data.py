"""
A pour but de generer / completer un fichier data correspondant
a un ensemble de parties dans des etats differents et puis d'y
associer un coup a jouer.
"""

from puissance4 import jouer_coup, est_jouable, init_grille, botjoues, Arbre, finpartie, init_arbre

def jouer_tout_les_coups(grille):
    """
    L'adversaire joue sur toutes les colonnes possibles.
    Cette fonction itere les 7 nouvelles grilles.
    """
    from copy import deepcopy
    for colonne in range(7):
        grille_copie = deepcopy(grille)
        if est_jouable(grille_copie, colonne):
            jouer_coup(grille_copie, colonne, 1)
            yield grille_copie


def faire_jouer_bot(grille, arbre):
    """
    Fait jouer le bot et retourne le coup.
    """
    return botjoues(arbre)


def generer_data():
    """
    Recupere les grilles initiales,
    fait jouer le bot contre lui-meme
    , recupere les coups du bot pour
    en faire de la nouvelle data.
    """
    numero_grille = 0
    for grille_initiale in convertir("data_initiale"):
        print(numero_grille)
        numero_grille += 1

        arbre = init_arbre(2, grille_initiale) # le bot a besoin de l'arbre pour jouer
        partie_terminee = False
        while not partie_terminee:
            inverser_grille(grille_initiale) # inverse la grille pour avoir une grille valide pour le bot
            coup = faire_jouer_bot(grille_initiale, arbre)
            completer_data(grille_initiale, coup)
            jouer_coup(grille_initiale, coup, 1)

            partie_terminee, vainqueur = finpartie(grille_initiale)

def inverser_grille(grille):
    """
    Inverse les pions des deux joueurs dans la grille.
    """
    for ligne in grille:
        for numero_case, case in enumerate(ligne):
            if case == 1:
                ligne[numero_case] = 0
            elif case == 0:
                ligne[numero_case] = 1

def completer_data(grille, coup, chemin_data="nv_data"):
    """
    Complete le fichier data avec une
    nouvelle grille et le coup.
    """
    desc = ""
    for ligne in grille:
        for case in ligne:
            desc += 'x' if case == 1 else 'y' if case == 0 else 'o'
    desc += ' ' + str(coup) + '\n'
    with open(chemin_data, 'a') as fichier:
        fichier.write(desc)


def convertir(chemin_data):
    """
    iterateur sur les grilles ecrites dans le fichier
    """
    with open(chemin_data,'r') as fichier:
        for ligne in fichier:
            grille = init_grille()
            for numero, element in enumerate(ligne):
                if element in {'x', 'y', 'o'}:
                    grille[numero//7][numero%7] = 1 if element == 'x' else 0 if element == 'y' else None

            yield grille

if __name__ == "__main__":
    generer_data()
