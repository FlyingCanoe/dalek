import random
import os
import sys


class Vue:
    def __init__(self, parent):
        self.parent=parent

    def afficher_menu_initial(self):
        print("BIENVENUE AUX DALEKS")
        rep=input("Que voulez-vous, 1-pour partie, 2-pour score\n")
        self.parent.demande_initiale(rep)

    def affcher_partie(self, partie):
        matrice = []
        for y in range(partie.dimy):
            ligne = []
            for x in range(partie.dimx):
                ligne.append("-")
            matrice.append(ligne)

        docx = partie.doc.pos[0]
        docy = partie.doc.pos[1]

        matrice[docy][docx] = "O"

        for dalek in partie.daleks:
            dalekx = dalek.pos[0]
            daleky = dalek.pos[1]

            matrice[daleky][dalekx] = "W"

        for ligne in matrice:
            print(ligne)


class Dalek:
    def __init__(self, parant, pos):
        self.parant = parant
        self.pos = pos


class Jeu:
    def __init__(self, parent):
        self.partie = None
        self.parent=parent
        self.nbr_dalek_par_niveau=5

    def crée_partie(self):
        self.partie = Partie(self)
        self.partie.crée_niveau()


class Partie:
    def __init__(self, parent):
        self.parant = parent
        self.doc=None
        self.dimx=12
        self.dimy=8
        self.niveau=0
        self.daleks=[]
        self.ferrailles = []

    def crée_niveau(self):
        self.niveau += 1
        nbr_daleks = self.niveau+self.parant.nbr_dalek_par_niveau

        posx = random.randrange(self.dimx)
        posy = random.randrange(self.dimy)
        nbr_pos = [[posx, posy]]
        nerreur = 0
        while len(nbr_pos) <= nbr_daleks + 1:
            posx = random.randrange(self.dimx)
            posy = random.randrange(self.dimy)
            if [posx, posy] not in nbr_pos:
                nbr_pos.append([posx, posy])
            else:
                nerreur += 1
        posdoc = nbr_pos.pop(0)
        self.doc = Docteur(self, posdoc)

        for pos in nbr_pos:
            self.daleks.append(Dalek(self, pos))

        self.ferrailles = []


class Docteur:
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos


class Controleur:
    def __init__(self):
        self.modele = Jeu(self)
        self.vue = Vue(self)

        self.vue.afficher_menu_initial()

    def demande_initiale(self, rep):
        self.modele.crée_partie()
        self.vue.affcher_partie(self.modele.partie)


if __name__ == '__main__':
    controler = Controleur()
