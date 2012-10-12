#!/usr/bin/env python2
#-*- coding:utf8-*-
    
import os
import threading
import subprocess

from time import *

BOTS_PATH = "../bots/"
ROUND_TIMEOUT = 0.01


class Match(threading.Thread):
    def __init__(self, bots):
        """ Initialise l'arene
        bots doit contenir la liste des bots (nom du programme) qui vont s'affronter

        arguments: bots"""
        self.import_bots(bots)
        self.scores = [0]*len(bots)
        self.error=0
        threading.Thread.__init__(self)

    def import_bots(self, bots):
        """Description de import_bots
        Verifie que les noms des bots correspondent bien a des programmes
        arguments: bots"""
        self.bots = list()
        for b in bots:
            if not os.path.exists(BOTS_PATH+b):
                raise ValueError("Could not find bot '{bot}'".format(bot = b))
            else:
                self.bots.append(b)

    def pret(self):
        """Description de pret
        Verifie que les joueurs sont prèts
    
        arguments: arg"""
        if self.p[0].stdout.readline()!="OK\n":
            # Pas très joli tout ça!
            # Faut changer le nom de l'erreur
            # et géré le cas où il y aura plus de joueurs
            raise ValueError("Le bot {bot} n'arrive pas à ce préparer".format(bot = self.bots[0]))
        if self.p[1].stdout.readline()!="OK\n":
            raise ValueError("Le bot {bot} n'arrive pas à ce préparer".format(bot = self.bots[1]))

    def feu(self):
        """Description de feu
        Envoie aux bots le message de depart
    
        arguments: arg"""
        self.p[0].stdin.write("A\n")
        self.p[1].stdin.write("A\n")

    def partez(self):
        """Description de partez
        Fait jouer une partie du jeu des prisonniers
    
        arguments: """
        # Lecteur du choix des bots
        r1 = self.p[0].stdout.readline().rstrip()
        r2 = self.p[1].stdout.readline().rstrip()

        # On determine le gagnant
        if r1=="C" and r2=="C":
            self.scores[0]+=5
            self.scores[1]+=5
        elif r1=="C" and r2=="T":
            self.scores[0]+=0
            self.scores[1]+=10
        elif r1=="T" and r2=="C":
            self.scores[0]+=10
            self.scores[1]+=0
        elif r1=="T" and r2=="T":
            self.scores[0]+=1
            self.scores[1]+=1
        else:
            raise ValueError("Les réponses ne correspondent pas à la question... Voila ce qu'on me demande de traiter: r1= {r1}, r2 = {r2}".format(r1 = r1, r2 = r2))

        # Envoie de la reponse des autres
        self.p[0].stdin.write(r2+'\n')
        self.p[1].stdin.write(r1+'\n')

    def run(self):
        """ Boucle principale qui va faire affronter les bots """
        self.p = list()

        self.p.append(subprocess.Popen("./start", stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         cwd=os.path.abspath(BOTS_PATH+self.bots[0]+"/")))
        self.p.append(subprocess.Popen("./start", stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         cwd=os.path.abspath(BOTS_PATH+self.bots[1]+"/")))
        self.pret()
        self.feu()

        # On boucle le jeu pendant 50 tours
        for k in range(50):
            self.partez()

        # Message de fin de jeu
        self.p[0].stdin.write("Q\n")
        self.p[1].stdin.write("Q\n")




if __name__ == '__main__':

    bots = ["AlwaysT", "AlwaysC", "Random"]
    #bots = ["Random"]
    c1 = bots[0]
    c2 = bots[1]

    for b1 in bots:
        for b2 in bots:
            match = Match([b1,b2])
            match.start()
            match.join(ROUND_TIMEOUT*200)
            if match.isAlive():
                print "Failed to answer in time"
            else:
                print "{b1} vs {b2}: score {scores}".format(b1 = b1, b2 = b2, scores = str(match.scores))
                if(match.scores[1]>match.scores[0]):
                    print "{b2} wins\n".format(b2 = b2)
                elif(match.scores[1]<match.scores[0]):
                    print "{b1} wins\n".format(b1 = b1)
                else:
                    print "Draw\n"


