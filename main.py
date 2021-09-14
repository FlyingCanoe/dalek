import random

class Vue:
    def __init__(self, parent):
        self.parant=parent

    def afficher_menu_initial(self):
        print("BIENVENUE AUX DALEKS")
        rep=input("Que voulez-vous, 1-pour partie, 2-pour score\n")
        self.parant.demande_initiale(rep)

class Jeu:
    def __init__(self, parent):
        self.partie = Partie()
        self.parant=parent
        self.nbr_dalek_par_niveau=5

class Partie():
    def __init__(self):
        self.doc=None
        self.largeur=12
        self.hauteur=8
        self.niveau=0
        self.daleks=[]

class Controleur:
    def __init__(self):
        self.modele=Jeu(self)
        self.vue=Vue(self)

        self.vue.afficher_menu_initial()

    def demande_initiale(self, rep):
        print(rep)


if __name__=='__main__':
    controler = Controleur()
