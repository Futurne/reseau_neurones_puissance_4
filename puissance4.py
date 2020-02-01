"""
Grille : n nb_colonnes, m nb_lignes
"""
nb_colonnes=7
nb_lignes=6

#import pygame
#from pygame.locals import *
from random import randint
from copy import deepcopy as cp



def init_grille():
    return [[None for _ in range(nb_colonnes)] for _ in range(nb_lignes)]

#La grille est implémentée dans le même sens qu'une grille classique.
#None signifie case vide.
#0 signifie joueur 0, 1 joueur 1.
def iter_case(grille):
    '''Rebvoie un iterateur sur tous les indices des cases de la grille'''
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            yield i,j

def valuation(liste):
    if liste.count(None) == 4 or (liste.count(0) > 0 and liste.count(1) > 0) :
        return 0
    
    return 10**liste.count(0) -10**liste.count(1)

def bloc_4(grille):
    for ligne in lignes(grille):
        for i in range(len(ligne)-3):
            yield(ligne[i:i+4])
    for ligne in colonnes(grille):
        for i in range(len(ligne)-3):
            yield(ligne[i:i+4])
    for ligne in diagonales(grille):
        for i in range(len(ligne)-3):
            yield(ligne[i:i+4])
    for ligne in antidiagonales(grille):
        for i in range(len(ligne)-3):
            yield(ligne[i:i+4])
def compteur(grille):
    score = 0
    for bloc in bloc_4(grille):
        score += valuation(bloc)
    return score

class Arbre:
    def __init__(self,grille, dernier_joueur):
        self.grille = grille
        self.fils = []
        self.est_finie = False
        self.dernier_joueur = dernier_joueur
        self.score = 'penis'
        self.coup_precedent = 'penis'
        self.coup_precedentbis = 'penis2'

    def prochains_coup(self):
        if not self.est_finie:
            for colonne in range(nb_colonnes):
                if est_jouable(self.grille, colonne):
                    grille2 = cp(self.grille)
                    jouer_coup(grille2, colonne, 1-self.dernier_joueur)
                    self.fils.append(Arbre(grille2, 1-self.dernier_joueur))
                    self.fils[-1].est_finie = finpartie(grille2)[0]
                    self.fils[-1].coup_precedent = colonne
                    self.fils[-1].coup_precedentbis = self.coup_precedent 
def hauteur(arbre):
    """renvoies hauteur de l'arbre qui compte les espaces entre les poteaux"""
    if arbre.fils ==[]:
        return 0
    else:
        return 1+max([hauteur(fils) for fils in arbre.fils])

def concatenate(Liste):
    L=[]
    for element in Liste:
        L += element
    return L

def feuilles(arbre):
    if   len(arbre.fils) == 0 :
        return [arbre]
    else:
        return concatenate([feuilles(fils) for fils in arbre.fils])

def mise_a_jour(arbre):
    """fonction recursive qui prend en entrée un arbre dans l'etat ou c'est a l'adversaire de jouer et qui met a jour la totalité des scores de l'arbre"""
    if hauteur(arbre) == 1:
        for feuille in feuilles(arbre):
            feuille.score = compteur(feuille.grille)
        arbre.score = min([feuille.score for feuille in arbre.fils])
    elif hauteur(arbre) == 0:
        arbre.score = 10**6
    elif hauteur(arbre) >=2 :
        for fils in arbre.fils:
            for petit_fils in fils.fils:
                mise_a_jour(petit_fils)
            L = [petit_fils.score for petit_fils in fils.fils]
            if L == []:
                fils.score = -10**6
            else:
                fils.score = max(L)
        arbre.score = min([fils.score for fils in arbre.fils])
    return arbre.score, arbre.coup_precedent
    
def botjoues(arbre):
    from multiprocessing import Pool

    for feuille in feuilles(arbre):
        feuille.prochains_coup()
    for feuille in feuilles(arbre):
        feuille.prochains_coup()

    pool = Pool(7)
    tab_minimum = pool.map(mise_a_jour, arbre.fils)
    maxi, coup = tab_minimum[0][0], tab_minimum[0][1]
    for val in tab_minimum:
        if val[0] > maxi:
            maxi, coup = val[0], val[1]
    return coup
    #for fils in arbre.fils:
     #   mise_a_jour(fils)
    """produit une erreure si arbre n'a pas de fils
    maxi = max([val[0] for val in tab_minimum])
    for fils in arbre.fils:
        if fils.score == maxi:
            fils_optimal = fils
    return fils_optimal.coup_precedent"""
    
        
def est_jouable(grille,colonne):
    return grille[0][colonne] is None

def jouer_coup(grille,colonne,joueur):
    #joueur, c'est 0 ou 1.
    if est_jouable(grille,colonne):           
        for i in range(nb_lignes-1,-1,-1):
            if grille[i][colonne] is None :
                 grille[i][colonne]=joueur
                 break
    else:
        raise ValueError

def afficher(grille):
    def f(a):
        if a is None :
            return " "
        if a==0:
            return 'O'
        return 'X'
    for ligne in grille:
        print(list(f(a) for a in ligne))
def init_arbre(n, grille=None):
    if grille is None:
        grille = init_grille()
    arbre = Arbre(grille,1)
    for i in range(2*n):
        for feuille in feuilles(arbre):
            feuille.prochains_coup()
    return arbre
    
def partie2joueurs(n):
    grille=init_grille()
    joueur=0
    partie_termine = False
    arbre = init_arbre(n)
    while not partie_termine:
        print(grille)
        try:
            if joueur == 1:
                colonne = int(input("Quel colonne pour le n°"+str(joueur)+" ? "))
                jouer_coup(grille,colonne,joueur)
                partie_termine, vainqueur = finpartie(grille)
                joueur=1-joueur
                print(grille)
                for fils in arbre.fils:
                    for petit_fils in fils.fils:
                        if petit_fils.coup_precedent == colonne and petit_fils.coup_precedentbis == coup_bot:
                            arbre = petit_fils
                  
            else :
                coup_bot = botjoues(arbre)
                print(coup_bot)
                jouer_coup(grille,coup_bot,joueur)
                partie_termine, vainqueur = finpartie(grille)
                joueur=1-joueur
                print(grille)
                
        except:
            print("COUP IMPOSSIBLE, RECOMMENCER")
    print(grille)
    print(vainqueur, ' a gagné')
    
def colonne(grille,i):
    """iterateur sur la colonne i de la grille en descendant"""
    for ligne in grille:
        yield ligne[i]

def colonnes(grille):
    """renvoies un iterateur sur les colonnes sous forme de liste """
    for i in range(nb_colonnes):
        yield list(colonne(grille, i))

def diagonale(grille,c):
    """c caractérise une diagonale de part l'invariant: c = i-j"""
    for ligne in range(nb_lignes):
        for colonne in range(nb_colonnes):
            if ligne - colonne == c:
                yield grille[ligne][colonne]
def diagonales(grille):
    """ renvoies un iterateur sur les diagonales sous forme de liste"""
    for valeur in range(-nb_colonnes+1, nb_lignes):
        yield list(diagonale(grille, valeur))


def antidiagonale(grille,c):
    """c caractérise une antidiagonale de part l'invariant: c = i+j"""
    for ligne in range(nb_lignes):
        for colonne in range(nb_colonnes):
            if ligne + colonne == c:
                yield grille[ligne][colonne]

def antidiagonales(grille):
    """ renvoies un iterateur sur les antidiagonales sous forme de liste"""
    for valeur in range(0, nb_lignes+ nb_colonnes-1):
        yield list(antidiagonale(grille, valeur))        

def lignes(grille):
    for ligne in grille:
        yield ligne

def finpartie(grille):
    for ligne in grille:
        compteur = 0
        valeur = ligne[0]
        for element in ligne:
            if element == valeur and valeur is not None:
                compteur += 1
                if compteur == 4:
                    return True, valeur
            else:
                compteur = 1
                valeur = element
    for i in range(nb_colonnes):
        compteur = 0
        valeur = grille[0][i]
        for element in colonne(grille,i):                         
            if element == valeur and valeur is not None:
                compteur += 1
                # print(compteur)
                if compteur == 4:
                    return True, valeur
            else:
                compteur = 1
                valeur = element
    
    for c in range(-nb_colonnes+1, nb_lignes):
        compteur = 0
        valeur = grille[0][i]
        for element in diagonale(grille,c):                         
            if element == valeur and valeur is not None:
                compteur += 1
                # print(compteur)
                if compteur == 4:
                    return True, valeur
            else:
                compteur = 1
                valeur = element
    
    for c in range(0, nb_lignes+ nb_colonnes-1):
        compteur = 0
        valeur = grille[0][i]
        for element in antidiagonale(grille,c):                         
            if element == valeur and valeur is not None:
                compteur += 1
                # print(compteur)
                if compteur == 4:
                    return True, valeur
            else:
                compteur = 1
                valeur = element
        
    
    return False,'penis'
 
 

 
def affiche2(grille):
    #Initialisation de la bibliothèque Pygame
    pygame.init()
    
    #Création de la fenêtre
    fenetre = pygame.display.set_mode((842, 1046))
    NaineNoire = pygame.image.load("LaNaineNoire.png").convert()
    Rouge = pygame.image.load("cerclerouge.png").convert_alpha()
    Bleu = pygame.image.load("cerclebleu.png").convert_alpha()
    fenetre.blit(NaineNoire, (0,0))
    def coordonnee(ligne, colonne):
        return (60*colonne +100 , 60*ligne + 100 )
    
    for ligne in range(nb_lignes):
        for colonne in range(nb_colonnes):
            if grille[ligne][colonne] == 0:
                fenetre.blit(Bleu, coordonnee(ligne, colonne))
            elif grille[ligne][colonne] == 1:
                fenetre.blit(Rouge, coordonnee(ligne, colonne))
    pygame.display.flip()
                
if __name__ == "__main__":
    partie2joueurs(2)    

