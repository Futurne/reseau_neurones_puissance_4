"""
Permet la creation et l'entrainement d'un reseau de neurone grace a la descente de gradient stochastique.
"""
from math import exp
import numpy as np


"""""""""""""""""""""""""""""""""
Objets correspondant a la structure d'un reseau de neurone.
"""""""""""""""""""""""""""""""""
class Couche:
    def __init__(self, matrice_poids, vecteur_biais):
        """
        La matrice de poids doit etre une matrice de type np.array.
        """
        self.matrice_poids = matrice_poids
        self.nbr_neurone = matrice_poids.shape[0]
        self.vecteur_biais = vecteur_biais
        self.valeur_neurones = np.zeros(self.nbr_neurone)
        self.valeur_z = None  # correspond a la valeur intermediaire des neurones avant la sigmoid

    def sortie(self, entree):
        """Retourne la valeur des neurones de la couche dans un np.array."""
        self.valeur_z = np.dot(self.matrice_poids, entree) - self.vecteur_biais
        Couche.sigmoid(self.valeur_z, self.valeur_neurones)
        return self.valeur_neurones

    def sigmoid(vecteur_z, valeur):
        """
        Effectue le produit entre la matrice et le vecteur entree et soustrait les biais,
        puis fait la sigmoid de chacunes des valeurs.
        C'est la fonction d'activation du neurone.
        """
        for i in range(vecteur_z.size):
            valeur[i] = 1/(1+exp(-vecteur_z[i]))

    def derivee_sigmoid(valeur):
        """Retourne l'evaluation de la derivee de la sigmoid en la valeur donnee."""
        return exp(-valeur)*(1/(1+exp(-valeur)))**2


class Reseau:
    def __init__(self, nombre_neurones):
        """nombre_neurones est un tableau qui contient le nombre de neurones de chaque couche."""
        self.couches = []
        # valeur2 : nbr neurones dans la couche actuelle
        # valeur1 : nbr neurones dans la couche precedente
        self.couches.append(Couche(np.ones((nombre_neurones[0], 1)), None)) # premiere couche : couche d'entree
        for valeur1, valeur2 in zip(nombre_neurones[:-1], nombre_neurones[1:]):
            self.ajouter_random_couche(valeur2, valeur1)

    def calculer_sortie(self, entree):
        """
        Renvoie la sortie du reseau de neurone.
        La taille de l'entree doit correspondre au nombre de neurone
        dans la premier couche lors de la creation du neurone.
        entree doit aussi etre du type 'np.array'.
        """
        self.couches[0].valeur_neurones = np.array(entree) # copie et ajoute les valeurs de l'entree a la premiere couche
        for couche in self.couches[1:]:
            entree = couche.sortie(entree)
        return entree

    def ajouter_random_couche(self, nb_lignes, nb_colonnes, min_val=-2, max_val=2):
        """
        Ajoute a la liste des couches une couche possedant le nbr
        de lignes et de colonnes demandees, avec des valeurs de poids
        et de biais aleatoire.
        """
        from random import random
        mat_poids = np.zeros((nb_lignes, nb_colonnes))
        vec_biais = np.zeros(nb_lignes)

        ecart = max_val-min_val
        for ligne in mat_poids:
            for numero_poids in range(len(ligne)):
                ligne[numero_poids] = min_val + random()*ecart

        for numero_biais in range(len(vec_biais)):
            vec_biais[numero_biais] = min_val + random()*ecart

        self.couches.append(Couche(mat_poids, vec_biais))

    def copie_reseau(reseau):
        """
        Retourne un reseau identique mais qui utilise
        une nouvelle zone de la mémoire.
        Permet de simuler plusieurs reseau en meme temps afin de
        faire des calculs en parallele.
        """
        liste_couche = []
        liste_mat_poids, liste_vec_biais = [], []
        for couche in reseau.couches:
            liste_mat_poids.append(couche.matrice_poids)
            liste_vec_biais.append(couche.vecteur_biais)

        for mat_poids, vec_biais in zip(liste_mat_poids, liste_vec_biais):
            liste_couche.append(Couche(mat_poids, vec_biais))

        # cree un reseau vide et y colle les nouvelles couches
        nv_reseau = Reseau([1])
        nv_reseau.couches = liste_couche
        return nv_reseau


"""""""""""""""""""""""""""""""""
Fonctions pratiques.
"""""""""""""""""""""""""""""""""
def calculer_perte_moyenne(reseau, liste_entree, liste_sortie):
    """
    Calcul la perte moyenne entre la sortie du reseau et la sortie esperee.
    """
    perte_moyenne = 0
    for entree, sortie_voulue in zip(liste_entree, liste_sortie):
        sortie = reseau.calculer_sortie(entree)
        perte_moyenne += sum([(val1-val2)**2 for val1, val2 in zip(sortie, sortie_voulue)])

    return perte_moyenne / len(liste_entree)


def calculer_accuracy_et_perte_moyenne(reseau, liste_entree, liste_sortie):
    """
    Calcul l'accuracy moyenne et la perte moyenne entre la sortie du reseau et la sortie esperee.
    """
    perte_moyenne = 0
    accuracy_moyenne = 0
    for entree, sortie_voulue in zip(liste_entree, liste_sortie):
        sortie = reseau.calculer_sortie(entree)
        perte_moyenne += sum([(val1-val2)**2 for val1, val2 in zip(sortie, sortie_voulue)])

        max_proba, numero = 0, 0
        for numero_neurone, valeur_neurone in enumerate(sortie):
            if valeur_neurone > max_proba:
                max_proba = valeur_neurone
                numero = numero_neurone
        accuracy_moyenne += 1 if sortie_voulue[numero] == 1 else 0

    return accuracy_moyenne/len(liste_entree), perte_moyenne/len(liste_entree)
