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

    def est_en_colison(self):
        for dalek in self.parent.get_daleks():
            if dalek is not self:
                if self.pos == dalek.pos:
                    return True
        return False


class Jeu:
    def __init__(self, parent):
        self.partie = None
        self.parent=parent
        self.nbr_dalek_par_niveau = 0
        self.score = []

    def crée_partie(self):
        self.partie = Partie(self)
        self.partie.crée_niveau()

    def bouger_doc(self, direction):
        self.partie.doc.bouger(direction)
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

    def get_daleks(self):
        return self.daleks

    def colison_daleks(self):
        daleks_mort = []
        daleks_vivent = []
        for dalek in self.daleks:
            if dalek.est_en_colison():
                daleks_mort.append(dalek)
            else:
                daleks_vivent.append(dalek)

        for dalek_mort in daleks_mort:
            self.ferrailles.append(Ferraille(self, dalek_mort.pos))

        self.daleks = daleks_vivent


class Docteur:
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos

    def bouger(self, direction):
        pos_dif = {
            "1": [-1, 1],
            "2": [0, 1],
            "3": [1, 1],
            "4": [-1, 0],
            "5": [0, 0],
            "6": [1, 0],
            "7": [-1, -1],
            "8": [0, -1],
            "9": [1, -1],
        }[direction]

        self.pos[0] += pos_dif[0]
        self.pos[1] += pos_dif[1]




class Controleur:
    def __init__(self):
        self.modele = Jeu(self)
        self.vue = Vue(self)

        self.vue.afficher_menu_initial()

    def demande_initiale(self, rep):
        self.modele.crée_partie()
        self.vue.afficher_partie(self.modele.partie)
        while True:
            print()
            self.modele.bouger_doc("9")
            self.vue.afficher_partie(self.modele.partie)
            import time
            time.sleep(2)


if __name__ == '__main__':
    controler = Controleur()
