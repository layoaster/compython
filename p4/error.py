#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Excepciones para manejar los distintos errores de las fases del Compilador para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

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

class Error(Exception, object):
    """ Clase padre de errores """
    __metaclass__ = ABCMeta

    pos = ()
    errno = -1
    info = ""

    def __init__(self, errno, pos, info=""):
        self.errno = errno
        self.pos = pos
        self.info = info

    @abstractmethod
    def printError(self, err):
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
    NO_VALID_PROD  = 1

    _errStrings = ("Unexpected symbol", 
                   "No valid production rule")

    def __init__(self, errno, pos, info=""):
        #super.__init__(errno, pos, info)
        super(SynError, self).__init__(errno, pos, info)

    def printError(self):
        print Colors.WARNING + str(self.pos[0]) + "L" \
              + ", " + str(self.pos[1]) + "C " \
              + Colors.FAIL + "[SYN ERROR] " + Colors.ENDC \
              + " " + self._errStrings[self.errno] + self.info
