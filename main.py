import random
import os
import sys
import time

class Vue:
    def __init__(self, parent):
        self.parent=parent

    def afficher_menu_initial(self):
        print("BIENVENUE AUX DALEKS")
        rep=input("Que voulez-vous, 1-pour partie, 2-pour score\n")
        self.parent.demande_initiale(rep)


    def afficher_partie(self, partie):
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

    def afficher_score(self, Jeu):
        print("           HIGH SCORE")



        for score in Jeu:
            i = 0
            i += 1
            print (i + score)




class Ferraille:
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos



class Dalek:
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos

    def bouger(self):
        pos_doc = self.parent.get_doc().pos
        pos_doc_x = pos_doc[0]
        pos_doc_y = pos_doc[1]
        pos_x = self.pos[0]
        pos_y = self.pos[1]

        if pos_doc_x > pos_x:
            self.pos[0] += 1
        elif pos_doc_x < pos_x:
            self.pos[0] -= 1

        if pos_doc_y > pos_y:
            self.pos[1] += 1
        elif pos_doc_y < pos_y:
            self.pos[1] -= 1

    def colision_avec_dalek(self, dalek):
        return self.pos == dalek.pos


class Jeu:
    def __init__(self, parent):
        self.partie = None
        self.parent=parent
        self.nbr_dalek_par_niveau=5
        self.score = []

    def crée_partie(self):
        self.partie = Partie(self)
        self.partie.crée_niveau()

    def bouger_doc(self):
        self.partie.bouger_dalek()
        self.partie.colison_daleks()


class Partie:
    def __init__(self, parent):
        self.parent = parent
        self.doc = None
        self.dimx = 12
        self.dimy = 8
        self.niveau = 0
        self.daleks = []
        self.ferrailles = []

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

    def bouger_dalek(self):
        for dalek in self.daleks:
            dalek.bouger()

    def get_doc(self):
        return self.doc

    def colison_daleks(self):
        dalek_survivant = []
        for dalek1 in self.daleks:
            for dalek2 in self.daleks:
                if dalek1 is dalek2:
                    continue


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
        while True:
            self.modele.bouger_doc()
            self.vue.affcher_partie(self.modele.partie)
            import time
            time.sleep(3)



if __name__ == '__main__':
    controler = Controleur()
