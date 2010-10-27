#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
$Id$
Description: Excepciones para manejar los distintos errores de las fases del Compilador para Pascal-.
$Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
$Date$
$Revision$
"""

from token import Token
from abc import ABCMeta, abstractmethod

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

#---------------------

class Error(object):
    """ Clase padre de errores """
    __metaclass__ = ABCMeta

    pos = ()
    errno = -1
    found = None
    expected = None

    def __init__(self, errno, pos, found, expected=None):
        self.errno = errno
        self.pos = pos
        self.found = found
        self.expected = expected
            #print "errno = ", self.errno, "; pos = ", self.pos, "; found = ", self.found, "; expected = ", self.expected
        #self.printError()

    @abstractmethod
    def printError(self):
        pass

# --------------------

class LexError(Error):
    """ Clase hija de errores lexicos """

    # Constantes de errores lexicos
    UNKNOWN_CHAR = 0
    INT_OVERFLOW = 1
    UNCLOSED_COM = 2

    _errStrings = ("Invalid character",
                   "Integer overflow",
                   "Unclosed comment")

    def __init__(self, errno, pos):
        super(LexError, self).__init__(errno, pos)

    #@classmethod
    def printError(self):
        print Colors.WARNING + str(self.pos[0]) + "L" \
              + ", " + str(self.pos[1]) + "C " \
              + Colors.FAIL + "[LEX ERROR] " + Colors.ENDC\
              + " " + self._errStrings[self.errno]

# --------------------

class SynError(Error):
    """ Clase hija de errores sintacticos """

    # Constantes de errores sintacticos
    UNEXPECTED_SYM = 0

    _errStrings = ("Unexpected symbol", )

    def __init__(self, errno, pos, found, expected=None):
        super(SynError, self).__init__(errno, pos, found, expected)
        #print "errno = ", self.errno, "; pos = ", self.pos, "; found = ", self.found, "; expected = ", self.expected
        self.printError()
    
    def printError(self):
        print str(Colors.WARNING + str(self.pos[0]) + "L,").rjust(10),
        print str(str(self.pos[1]) + "C").rjust(3),
        
        print Colors.FAIL + "[SYN ERROR]" + Colors.ENDC \
              , " " + self._errStrings[self.errno] \
              + " - Found '" + self.found.getLexeme() + "'",

        if self.expected is not None:
            print "\b, expected",
            try:
                [a for a in self.expected]
                # Si no lanza una excepcion, es un conjunto de tokens
                for tok in self.expected:
                    print "'" + Token(tok).getLexeme() + "',",
                print "\b\b",
            except TypeError:
                # Se trata de un unico token (syntaxError invocado por match, por ejemplo)
                print "'" + Token(self.expected).getLexeme() + "'",
        # Si expected es none, el error vino por syntaxCheck (no mostramos expected en principio)
        print "\n",
