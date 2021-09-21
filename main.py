import random
import os
import sys
import time
from os import system, name

class Vue:
    def __init__(self, parent):
        self.parent=parent

    def afficher_menu_initial(self):
        print("BIENVENUE AUX DALEKS")
        rep=input("Que voulez-vous, 1-pour partie, 2-pour score\n")
        self.parent.demande_initiale(rep)

    def afficher_partie(self, partie):
        self.clear()

        niveau = partie.niveau
        score = partie.score
        print("NIVEAU: ", niveau, "    SCORE: ", score, "    NB ZAPPEUR: ", sep=" ")

        matrice = []
        for y in range(partie.dimy):
            ligne = []
            for x in range(partie.dimx):
                ligne.append(" ")
            matrice.append(ligne)

        docx = partie.doc.pos[0]
        docy = partie.doc.pos[1]

        matrice[docy][docx] = "O"

        for dalek in partie.daleks:
            dalekx = dalek.pos[0]
            daleky = dalek.pos[1]

            matrice[daleky][dalekx] = "W"

        for ferrailles in partie.ferrailles:
            ferraillesx = ferrailles.pos[0]
            ferraillesy = ferrailles.pos[1]

            matrice[ferraillesy][ferraillesx] = "F"

        for ligne in matrice:
            print(ligne)

        time.sleep(5)

    def afficher_score(self, parent):
        self.clear()
        print("           HIGH SCORE")

        hs = self.parent.modele.high_score
        hs.sort(reverse=True)
        i = 0
        for high_score in hs:
            i += 1
            print (i," - ", high_score, sep=" ")

        rep=input("appuyer sur une touche pour retourner au menu principal")
        self.clear()
        self.afficher_menu_initial()


    def clear(self):
        if name == 'nt':
            _ = system('cls')

        else:
            _ = system('clear')




class Ferraille:
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos



class Dalek:
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos


class Jeu:
    def __init__(self, parent):
        self.partie = None
        self.parent=parent
        self.nbr_dalek_par_niveau=5
        self.high_score = [100, 3200,123,420]

    def crée_partie(self):
        self.partie = Partie(self)
        self.partie.crée_niveau()


class Partie:
    def __init__(self, parent):
        self.parent = parent
        self.doc = None
        self.dimx = 12
        self.dimy = 8
        self.niveau = 0
        self.daleks = []
        self.ferrailles = []
        self.score = 5

    def crée_niveau(self):
        self.niveau += 1
        nbr_daleks = self.niveau+self.parent.nbr_dalek_par_niveau

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
        if rep == "1":
            self.modele.crée_partie()
            self.vue.afficher_partie(self.modele.partie)
        elif rep == "2":
            self.vue.afficher_score(self, )



if __name__ == '__main__':
    controler = Controleur()
