#!/usr/bin/env python
# -*- coding: latin-1 -*-

import sys, traceback
import pdb

import time
import datetime
import pyfirmata
# Démarrer la connection avec Arduino UNO
#  USB: /dev/ttyUSB0 ou /dev/ttyACM0
#  UART: /dev/ttyAMA0

def log(msg):
    a = datetime.datetime.now()
    print "%s : %s" % ( a.strftime("%X"), msg)

def print_error(msg):
    print '-'*60
    print "Erreur : %s " % msg
    print '-'*60
    traceback.print_exc(file=sys.stdout)
    print '-'*60
    sys.exit(1)

class Robot(object):

    DEF_SPEED = 50

    def __init__(self, name):
        log("Creation du Robot : %s " % name)
        self.name = name
        self.board = None
        self.moteur_gauche = None
        self.moteur_droit  = None
        self.direction = None
        self.vitesse = 0
        self.online = False

    def offline(self):
        log("Robot : %s : Offline" % self.name )
        self.board.exit()

    def online(self):
        self.online = True
        if not self.moteur_droit:
            log("Robot : %s : Moteur Droit inexistant")
            self.online = False
        if not self.moteur_gauche:
            log("Robot : %s : Moteur gauche inexistant")
            self.online = False
        if self.online:
            log("Robot : %s : Online" % self.name )

    def set_board(self):
        log("Init Robot : board")
        try:
            self.board = pyfirmata.Arduino('/dev/ttyACM0')
            self.online = True
        except:
            print_error("Pb init board")

    def set_Moteur_Droit(self, pin_sens=0, pin_vitesse=0):
        if self.board:
            self.moteur_droit = Motor("Moteur Droit", self.board, pin_sens, pin_vitesse)
        else:
            log("Set Board First")

    def set_Moteur_Gauche(self, pin_sens, pin_vitesse):
        if self.board:
            self.moteur_gauche = Motor("Moteur Gauche", self.board, pin_sens, pin_vitesse)
        else:
            log("Set Board First")

    def stop(self):
        pass

    def avance(self, vitesse=DEF_SPEED):
        pass

    def recule(self, vitesse=DEF_SPEED):
        pass

    def droite(self):
        pass

    def gauche(self):
        pass

    def __str__(self):
        return """
            Robot Name : {name} direction={d} vitesse={v}
            - Moteur droit  : {m_d}
            - Moteur gauche : {m_g}
        """.format( name=self.name, d=self.direction, v=self.vitesse, m_d=self.moteur_droit, m_g=self.moteur_gauche )

class Motor(object):
    def __init__(self, name, board, pin_direction, pin_vitesse):
        self.board = board
        self.name = name
        self.d_pin = pin_direction
        self.s_pin = pin_vitesse
        self.pwm = None
        self.sens = None
        self.direction = 0
        self.vitesse = 0
        self.mode_test = True
        try:
            log ("Init %s : PWM : %s" % (self.name, self.s_pin))
            self.pwm = self.board.get_pin("d:%s:p" % self.s_pin)

            log ("Init %s : DIR : %s" % (self.name, self.d_pin))
            self.sens = self.board.get_pin("d:%s:o" % self.d_pin)
        except:
            print_error( "PB : Init Motor : %s " % self.name )

    def _write(self):
        self.sens.write(self.direction)
        self.pwm.write(self.vitesse)

    def stop(self):
        self.vitesse = 0
        self._write()

    def run(self, vitesse=0.5, sens=0):
        self.vitesse = vitesse
        self.direction = sens
        self._write()

    def __str__(self):
        return "Moteur : %s d=%s v=%s" % (self.name, self.direction, self.vitesse)



log( "Debut" )

## Creation du robot

R1 = Robot("R1")
R1.set_board()
R1.set_Moteur_Droit(pin_sens=12, pin_vitesse=3)
R1.set_Moteur_Gauche(pin_sens=13,pin_vitesse=11)

print R1

R1.offline()

log("Fin")
