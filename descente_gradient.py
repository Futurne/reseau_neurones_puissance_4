import numpy as np
from multiprocessing import Pool
from reseau_neurones import Reseau, Couche

"""""""""""""""""""""""""""""""""
Fonctions permettant la descente de gradient stochastique.
"""""""""""""""""""""""""""""""""
def calculer_dp_derniere_couche(reseau, sortie_voulue):
    """
    Retourne le vecteur correspondant aux derivees partielles
    de la fonction perte par rapport aux valeurs des neurones
    de la derniere couche.
    """
    valeur_sortie = reseau.couches[-1].valeur_neurones
    return 2*(valeur_sortie - sortie_voulue)


def dp_couche_precedente(liste_dp_couche_actuelle, couche):
    """
    Calcul les dp de la fonction perte par rapport aux valeurs des neurones
    de la couche precedente.
    """
    liste_dp_couche_precedente = [] # ieme case = dp(ieme_neurone_couche_precedente)/dp(fonction_perte)
    for numero_neurone_couche_precedente in range(couche.matrice_poids.shape[1]):
        somme = 0
        for numero_neurone_couche_actuelle in range(couche.nbr_neurone):
            derivee_sigmoid = Couche.derivee_sigmoid(couche.valeur_z[numero_neurone_couche_actuelle])
            somme += couche.matrice_poids[numero_neurone_couche_actuelle][numero_neurone_couche_precedente] * derivee_sigmoid * liste_dp_couche_actuelle[numero_neurone_couche_actuelle]
        liste_dp_couche_precedente.append(somme)
    return liste_dp_couche_precedente


def calculer_dp_couche(numero_couche, reseau, liste_dp_couche_actuelle):
    """
    Yield recursivement les valeurs des dp de la fonction perte par rapport aux poids et aux biais
    de chacunes des couches dans l'ordre croissant (de la premiere sous couche
    jusqu'a la derniere couche de sortie).

    Une etape de la recursion fait :
    Calcule les derivees partielles de la fonction perte par rapport aux poids et aux biais de tout les
    neurones de la couche demandee, puis calcule les dp de la fonction perte
    par rapport aux valeurs des neurones de la couche precedente pour pouvoir relancer la fonction sur la couche precedente.
    """
    couche_actuelle = reseau.couches[numero_couche]
    couche_precedente = reseau.couches[numero_couche-1]
    valeur_z_actuels = couche_actuelle.valeur_z

    matrice_dp = np.zeros((couche_actuelle.nbr_neurone, couche_precedente.nbr_neurone))
    vecteur_biais_dp = np.zeros(couche_actuelle.nbr_neurone)
    # rempli la matrice et le vecteur contenant toutes les dp au fur et a mesure

    for num_neurone_actuel in range(matrice_dp.shape[0]):
            # ce produit sert pour le calcul des dp dans la boucle suivante mais est une constante
            produit_temporaire = Couche.derivee_sigmoid(valeur_z_actuels[num_neurone_actuel]) * liste_dp_couche_actuelle[num_neurone_actuel]
            for num_neurone_precedent in range(matrice_dp.shape[1]):
                matrice_dp[num_neurone_actuel, num_neurone_precedent] = couche_precedente.valeur_neurones[num_neurone_precedent]* produit_temporaire
            # la dp du biais est directement le produit temporaire calcule precedemment
            vecteur_biais_dp[num_neurone_actuel] = produit_temporaire

    if numero_couche != 1:
        liste_dp_couche_precedente = dp_couche_precedente(liste_dp_couche_actuelle,couche_actuelle)
        for mat, vec in calculer_dp_couche(numero_couche-1, reseau, liste_dp_couche_precedente): # yield recursivement les valeurs des autres couches
            yield mat, vec

    yield (matrice_dp, vecteur_biais_dp) # puis yield les valeurs qui viennent d'etre calculees (les yields sont donc dans l'ordre croissant des couches)


def gradient(reseau, sortie_voulue):
    """
    Retourne un tableau contenant toutes les dp de la fonction perte evaluee sur la sortie voulue,
    par rapport aux poids et aux biais.

    Le reseau doit avoir deja prit en entree l'entree souhaitee.

    La premiere case du tableau contient la matrice des dp des poids et le vecteur
    des dp des biais de la deuxieme couche (la premiere etant l'entree).
    Les cases suivantes ont les memes contenus pour les couches suivantes.
    """
    liste_dp_derniere_couche = calculer_dp_derniere_couche(reseau, sortie_voulue)
    return [(mat, vec) for mat, vec in calculer_dp_couche(len(reseau.couches)-1, reseau, liste_dp_derniere_couche)]


def calculer_gradient_total(arguments):
    """
    Les arguments doivent etre un tuple de la forme (reseau, liste_entree, liste_sortie).
    Retourne le gradient total etant
    la somme de tout les gradients calcules par couple (entree, sortie).
    """
    reseau, liste_entree, liste_sortie = arguments[0], arguments[1], arguments[2]
    # initialisation des matrices de dp et des vecteurs de dp
    gradient_tot = [[np.zeros((c2.nbr_neurone, c1.nbr_neurone)), np.zeros(c2.nbr_neurone)] for c1, c2 in zip(reseau.couches[:-1], reseau.couches[1:])]
    for entree, sortie_voulue in zip(liste_entree, liste_sortie):
        reseau.calculer_sortie(entree)
        liste_dp = gradient(reseau, sortie_voulue)
        ajouter_dp_gradtotal(liste_dp, gradient_tot)

    return gradient_tot


def gradient_perte_moyenne(reseau, liste_entree, liste_sortie, nbr_process):
    """
    Calcul le gradient de la fonction de perte moyenne sur tous les
    parametres du reseau (poids et biais).
    """
    # initialisation des matrices de dp et des vecteurs de dp
    gradient_moy = [[np.zeros((c2.nbr_neurone, c1.nbr_neurone)), np.zeros(c2.nbr_neurone)] for c1, c2 in zip(reseau.couches[:-1], reseau.couches[1:])]

    taille_sous_liste = len(liste_entree)//nbr_process
    if taille_sous_liste == 0: # cas ou il y a trop peu de donnees par rapport au nbr de process demande
        taille_sous_liste = len(liste_entree) # pas besoin de faire des calculs en parallele => 1 process

    arguments_calcul_gradient = [] # futur liste des arguments pour les process de calcul
    for debut_sous_liste in range(0, len(liste_entree), taille_sous_liste):
        fin_sous_liste = debut_sous_liste + taille_sous_liste
        if fin_sous_liste > len(liste_entree):
            fin_sous_liste = len(liste_entree)
        arguments_calcul_gradient.append((Reseau.copie_reseau(reseau), liste_entree[debut_sous_liste:fin_sous_liste], liste_sortie[debut_sous_liste:fin_sous_liste]))

    pool = Pool(processes=nbr_process)
    liste_gradient = pool.map(calculer_gradient_total, arguments_calcul_gradient) # lance tout les process sur les calculs de gradient_total
    for grad_tot in liste_gradient: # reuni tout les gradient_total dans le gradient_moyen
        ajouter_dp_gradtotal(grad_tot, gradient_moy)

    for mat_grad, vec_grad in gradient_moy: # moyenne le gradient
        mat_grad /= len(liste_entree)
        vec_grad /= len(liste_entree)

    return gradient_moy


def etape_descente_gradient(reseau, liste_entree, liste_sortie, nbr_process, lmbda):
    """
    Soustrait le gradient moyen (calcule grace a la liste entree/sortie donnee)
    a tout les parametres du reseau (soustrait un pourcentage egal au lambda).
    Retourne le gradient de la fonction perte moyenne.
    """
    gradient_moy = gradient_perte_moyenne(reseau, liste_entree, liste_sortie, nbr_process)
    for gradient, couche in zip(gradient_moy, reseau.couches[1:]):
        couche.matrice_poids -= lmbda * gradient[0]
        couche.vecteur_biais -= lmbda * gradient[1]

    return gradient_moy


def descente_gradient_stochastique(reseau, liste_entree, liste_sortie, nombre_etapes, nbr_process=4, lmbda=0.8, print_module=False):
    """
    Effectue autant d'etapes de la descente du gradient que demande,
    mais divise les data donnees pour avoir moins de calcul a faire.
    Il est possible de preciser le nombre de process a utiliser afin de
    faire des calculs en parallele.
    Preciser la valeur du lmbda permet de preciser le taux d'apprentissage entre chaque etape de la descente.
    Il est aussi possible d'afficher le module du gradient afin de voir l'avancee de la methode.
    """
    from random import shuffle
    # rassemble les deux listes ensemble pour melanger les couples
    couple_entree_sortie_shuffled = [(entree, sortie) for entree, sortie in zip(liste_entree, liste_sortie)]
    shuffle(couple_entree_sortie_shuffled)

    liste_echantillon = []
    taille_echantillon = len(liste_entree)//nombre_etapes
    for debut_echantillon in range(0, len(liste_entree), taille_echantillon):
        fin_echantillon = debut_echantillon + taille_echantillon
        if fin_echantillon > len(liste_entree):
            fin_echantillon = len(liste_entree)

        liste_echantillon.append(couple_entree_sortie_shuffled[debut_echantillon:fin_echantillon])

    # desensemble les couples (entree, sortie) pour faire une liste_entree et une liste_sortie
    # pour chaque echantillon
    for numero, echantillon in enumerate(liste_echantillon):
        liste_entree, liste_sortie = [], []
        for entree, sortie in echantillon:
            liste_entree.append(entree)
            liste_sortie.append(sortie)
        liste_echantillon[numero] = [liste_entree, liste_sortie]

    # effectue une etape de la descente de gradient sur chacun des echantillons
    for echantillon in liste_echantillon:
        gradient_moy = etape_descente_gradient(reseau, echantillon[0], echantillon[1], nbr_process, lmbda)
        if print_module:
            print(module_gradient(gradient_moy))

"""""""""""""""""""""""""""""""""
Fonctions pratiques.
"""""""""""""""""""""""""""""""""
def module_gradient(gradient):
    """
    Retourne le module du gradient donne.
    """
    from math import sqrt
    somme = 0
    for mat_grad, vec_grad in gradient:
        for ligne in mat_grad:
            for coordonnees in ligne:
                somme += coordonnees**2
        for coordonnees in vec_grad:
            somme += coordonnees**2

    return sqrt(somme)

def ajouter_dp_gradtotal(liste_dp, grad_total):
    """Ajoute au grad_total la liste des dp calculees."""
    for dp, grad in zip(liste_dp, grad_total):
        grad[0] += dp[0] # matrice des dp par rapport aux poids
        grad[1] += dp[1] # vecteur des dp par rapport aux biais
