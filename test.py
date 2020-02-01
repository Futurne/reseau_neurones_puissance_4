from reseau_neurones import *
from descente_gradient import *
from time import time
import numpy as np

reseau = Reseau([84, 10, 10, 7])
liste_entree, liste_sortie = [], []
with open("nv_data", 'r') as fichier:
    nbr_data = 0
    for ligne in fichier:
        nbr_data += 1
        liste_entree.append(ligne[:42])
        liste_sortie.append(ligne[43:44])


liste_entree_normalisee, liste_sortie_normalisee = [], []
for entree in liste_entree:
    entree_normalisee = [0 for i in range(84)]
    for numero_c, caractere in enumerate(entree):
        if caractere == 'x':
            entree_normalisee[numero_c] = 1
        elif caractere == 'y':
            entree_normalisee[42+numero_c] = 1
    liste_entree_normalisee.append(entree_normalisee)

for sortie in liste_sortie:
    liste_sortie_normalisee.append([1 if i == int(sortie) else 0 for i in range(7)])

temp1 = time()
for i in range(300):
    print("Descente numero", i)
    accuracy, perte = calculer_accuracy_et_perte_moyenne(reseau, liste_entree_normalisee, liste_sortie_normalisee)
    print("Perte moyenne du reseau : {}".format(perte))
    print("Accuracy du reseau : {}\n".format(accuracy))
    descente_gradient_stochastique(reseau, liste_entree_normalisee, liste_sortie_normalisee, 3, print_module=False, nbr_process=12)

print("Temps total : {} s".format(time() - temp1))

accuracy, perte = calculer_accuracy_et_perte_moyenne(reseau, liste_entree_normalisee, liste_sortie_normalisee)
print("Perte moyenne du reseau : {}".format(perte))
print("Accuracy du reseau : {}".format(accuracy))

"""
for _ in range(140):
    gradient = etape_descente_gradient(reseau, liste_entree_normalisee, liste_sortie_normalisee, lmbda=0.4)
    print(module_gradient(gradient))

for couche in reseau.couches[1:]:
    print("La couche possede {} neurones.".format(couche.nbr_neurone))
    print("Matrice de poids :")
    print(couche.matrice_poids)
    print("Vecteur de biais :")
    print(couche.vecteur_biais)
    print("")
"""
