import random
import os
import sys
import time
from os import system, name


def check_proximity(pos1, pos2):  # regarde la distance entre les deux objets
    proximity_x = abs(pos1[0] - pos2[0])
    proximity_y = abs(pos1[1] - pos2[1])

    return max(proximity_x, proximity_y)


class AppError(Exception):
    pass


class Vue:
    def __init__(self, parent):
        self.controler = parent

    def afficher_menu_initial(self):
        selection = False
        while not selection:
            self.clear()
            print("BIENVENUE AUX DALEKS")
            rep = input("Que voulez-vous, 1-pour partie, 2-pour score, 3-pour quitter\n")
            if rep == "1" or rep == "2" or rep == "3":
                selection = True
        self.controler.demande_initiale(rep)

    def afficher_difficulte(self):  # affiche le choix de difficulter
        selection = False
        while not selection:
            print("choisir sa difficulté")
            rep = input("1-facile, 2-moyen, 3-difficile\n")
            if rep == "1" or rep == "2" or rep == "3":
                selection = True
        self.controler.changer_difficulter(rep)

    def afficher_partie(self, partie):  # affiche le jeu en son entier
        self.clear()

        niveau = partie.niveau
        score = partie.score
        zappeur = partie.nbzappeur
        teleporteur = partie.nbtp
        print("NIVEAU: ", niveau, "    SCORE: ", score, "    NB ZAPPEUR: ", zappeur,
              "     NB TELEPORTEUR: ", teleporteur, "\n",   sep=" ")  # le HUD du joueur

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

    def afficher_score(self):  # affiche le menu du high score
        self.clear()
        print("           HIGH SCORE\n")

        hs = self.controler.modele.high_score
        hs.sort(reverse=True)  # mets les scores en bon ordre
        i = 0
        for high_score in hs:
            i += 1
            print(i, " - ", high_score, sep=" ")

        input("appuyer sur une touche pour retourner au menu principal")
        self.clear()
        self.afficher_menu_initial()

    def clear(self):  # efface tout ce qui est sur l'écran
        if name == 'nt':
            _ = system('cls')

        else:
            _ = system('clear')

    def game_over(self):  # s'affiche lorsque l'on perd la partie
        self.clear()
        print("               VOUS AVEZ PERDU\n \n \n", "              SCORE: ",
              self.controler.modele.partie.score, sep=" ")
        time.sleep(3)
        self.afficher_menu_initial()

    def get_input():
        return input(":")


class Ferraille:
    def __init__(self, pos):
        self.pos = pos


class Dalek:
    def __init__(self, parent, pos):
        self.partie = parent
        self.pos = pos

    def bouger(self):
        pos_doc = self.partie.get_doc().pos
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

    def est_en_colison_avec(self, obj):
        if obj is not self:
            if self.pos == obj.pos:
                return True
        return False

    def est_en_colison(self):
        doc = self.partie.get_doc()
        if self.est_en_colison_avec(doc):
            self.partie.game_over()

        for dalek in self.partie.get_daleks():
            if self.est_en_colison_avec(dalek):
                return True

        for ferraille in self.partie.ferrailles:
            if self.est_en_colison_avec(ferraille):
                return True
        return False


class Jeu:
    def __init__(self, parent):
        self.partie = None
        self.controler = parent
        self.nbr_dalek_par_niveau = 5
        self.high_score = []
        self.difficulte = 1

    def cree_partie(self):
        self.partie = Partie(self)
        self.partie.cree_niveau()

    def jouer_tour(self, action):
        self.partie.jouer_tour(action)

    def game_over(self):
        self.high_score.append(self.partie.score)
        self.controler.game_over()


class Partie:
    def __init__(self, parent):
        self.jeu = parent
        self.doc = None
        self.dimx = 12
        self.dimy = 8
        self.niveau = 0
        self.daleks = []
        self.ferrailles = []
        self.score = 0
        self.nbzappeur = 0
        self.nbtp = 0

    def cree_niveau(self):  # creation d'un niveau lors d'un changement de niveau ou une nouvelle partie
        self.niveau += 1
        self.nbzappeur += 1
        self.nbtp += 1
        nbr_daleks = self.niveau * self.jeu.nbr_dalek_par_niveau

        posx = random.randrange(self.dimx)
        posy = random.randrange(self.dimy)
        nbr_pos = [[posx, posy]]
        nerreur = 0
        while len(nbr_pos) <= nbr_daleks:
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

    def colison(self):
        self.tuer_daleks_si(Dalek.est_en_colison)

    def jouer_tour(self, action):
        self.doc.action(action)
        self.bouger_dalek()
        self.colison()
        if len(self.daleks) == 0:
            self.cree_niveau()

    def tuer_daleks_si(self, f):
        daleks_mort = []
        daleks_vivant = []
        for dalek in self.daleks:
            if f(dalek):
                daleks_mort.append(dalek)
                self.score += 5
            else:
                daleks_vivant.append(dalek)
        self.daleks = daleks_vivant

        for dalek in daleks_mort:
            ferrail = Ferraille(dalek.pos)
            if ferrail not in self.ferrailles:
                self.ferrailles.append(ferrail)

    def game_over(self):
        self.jeu.game_over()


class Docteur:
    def __init__(self, parent, pos):
        self.partie = parent
        self.pos = pos

    def tp(self):  # le teleporteur
        partie = self.partie
        jeu = partie.jeu

        if partie.nbtp <= 0:
            raise AppError

        partie.nbtp -= 1

        if jeu.difficulte == "1":  # facile
            tp_legal = False
            loop = 0  # nb d'essaie de teleportage

            while not tp_legal:
                dimx = self.partie.dimx
                dimy = self.partie.dimy
                pos = [0, 0]
                pos[0] = random.randrange(dimx)
                pos[1] = random.randrange(dimy)
                self.pos = pos
                tp_legal = True

                for dalek in self.partie.daleks:
                    tp_illegal = check_proximity(self.pos, dalek.pos)

                    if tp_illegal == 0:  # teleporte là où il n'y a pas de daleks
                        tp_legal = False
                    elif tp_illegal == 1 and loop < 70:  # teleporte a une case de distance min, version moins stricte
                        tp_legal = False
                    elif tp_illegal == 2 and loop < 30:  # rend le teleporteur moins stricte si il est impossible de ce teleporter, permettant au teleporteur d'être utiliser à des niveaux suppérieurs
                        tp_legal = False

                for ferraille in self.partie.ferrailles:  # ne teleporte pas où il y a des ferrailles
                    tp_illegal = check_proximity(self.pos, ferraille.pos)
                    if tp_illegal == 0:
                        tp_legal = False
                loop += 1

        elif jeu.difficulte == "2":  # normal
            tp_legal = False
            while not tp_legal:
                dimx = self.partie.dimx
                dimy = self.partie.dimy
                pos = [0, 0]
                pos[0] = random.randrange(dimx)
                pos[1] = random.randrange(dimy)
                self.pos = pos
                tp_legal = True

                for dalek in self.partie.daleks:
                    tp_illegal = check_proximity(self.pos, dalek.pos)
                    if tp_illegal == 0:
                        tp_legal = False
                for ferraille in self.partie.ferrailles:
                    tp_illegal = check_proximity(self.pos, ferraille.pos)
                    if tp_illegal == 0:
                        tp_legal = False

            self.pos = pos
        elif jeu.difficulte == "3":  # difficile
            tp_legal = False

            while not tp_legal:
                dimx = self.partie.dimx
                dimy = self.partie.dimy
                pos = [0, 0]
                pos[0] = random.randrange(dimx)
                pos[1] = random.randrange(dimy)
                self.pos = pos
                tp_legal = True

                for ferraille in self.partie.ferrailles:
                    tp_illegal = check_proximity(self.pos, ferraille.pos)
                    if tp_illegal == 0:
                        tp_legal = False

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
        pos_x = self.pos[0] + pos_dif[0]
        pos_y = self.pos[1] + pos_dif[1]
        pos = [pos_y, pos_x]

        if pos_x == -1:
            raise AppError
        elif pos_x == self.partie.dimx:
            raise AppError
        if pos_y == -1:
            raise AppError
        elif pos_y == self.partie.dimy:
            raise AppError

        for ferraille in self.partie.ferrailles:
            move_illegal = check_proximity(pos, ferraille.pos)
            if move_illegal == 0:
                raise AppError

        self.pos[0] += pos_dif[0]
        self.pos[1] += pos_dif[1]

    def action(self, action):  # les actions performer par le joueur
        try:
            {
                "z": self.zappeur,
                "x": self.tp,
                "1": lambda: self.bouger(action),
                "2": lambda: self.bouger(action),
                "3": lambda: self.bouger(action),
                "4": lambda: self.bouger(action),
                "5": lambda: self.bouger(action),
                "6": lambda: self.bouger(action),
                "7": lambda: self.bouger(action),
                "8": lambda: self.bouger(action),
                "9": lambda: self.bouger(action),
            }[action]()
        except KeyError:
            raise AppError  # si l'input est invalide

    def zappeur(self):
        partie = self.partie

        if partie.nbzappeur <= 0:
            raise AppError

        self.partie.nbzappeur -= 1
        partie.tuer_daleks_si(lambda dalek: 1 == check_proximity(self.pos, dalek.pos))


class Controleur:
    def __init__(self):
        self.modele = Jeu(self)
        self.vue = Vue(self)
        self.vue.afficher_menu_initial()

    def game_over(self):
        self.vue.game_over()

    def demande_initiale(self, rep):
        if rep == "1":  # option commencer partie
            self.vue.afficher_difficulte()
            self.modele.cree_partie()
            while True:
                self.vue.afficher_partie(self.modele.partie)
                try:
                    self.modele.jouer_tour(Vue.get_input())
                except AppError:
                    pass
        elif rep == "2":  # option voir high score
            self.vue.afficher_score()

        elif rep == "3":  # option quitter
            quit()

    def changer_difficulter(self, rep):
        self.modele.difficulte = rep


if __name__ == '__main__':
    controler = Controleur()
