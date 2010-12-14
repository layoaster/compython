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

    def __init__(self, errno, pos, found=None, expected=None):
        self.errno = errno
        self.pos = pos
        self.found = found
        self.expected = expected

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
        self.printError()

    def printError(self):
        print str(Colors.WARNING + str(self.pos[0]) + "L,").rjust(10),
        print str(str(self.pos[1]) + "C").rjust(3),

        print Colors.FAIL + "[LEX ERROR] " + Colors.ENDC\
              + self._errStrings[self.errno]

# --------------------

class SynError(Error):
    """ Clase hija de errores sintacticos """

    # Constantes de errores sintacticos
    UNEXPECTED_SYM = 0

    _errStrings = ("Unexpected symbol", )

    def __init__(self, errno, pos, found, expected=None):
        super(SynError, self).__init__(errno, pos, found, expected)
        self.printError()
    
    def printError(self):
        print str(Colors.WARNING + str(self.pos[0]) + "L,").rjust(10),
        print str(str(self.pos[1]) + "C").rjust(3),
        
        print Colors.FAIL + "[SYN ERROR]" + Colors.ENDC \
              + " " + self._errStrings[self.errno] \
              + " - Found '" + self.found.getLexeme() + "'",

        if self.expected is not None:
            print "\b, expected",
            try:
                [a for a in self.expected]
                # Si no lanza una excepcion, es un conjunto de tokens
                for tok in self.expected:
                    print "'" + Token(tok).getTokLexeme() + "',",
                print "\b\b",
            except TypeError:
                # Se trata de un unico token (syntaxError invocado por match, por ejemplo)
                print "'" + Token(self.expected).getTokLexeme() + "'",
        # Si expected es None, el error vino por syntaxCheck (no mostramos expected en principio)
        print "\n",
        
# --------------------
        
class SemError(Error):
    """ Clase hija de errores sintacticos """

    # Constantes de errores semanticos
    # Errores de ambito 
    UNDECLARED_TYPE  = 0
    REC_DEFINITION   = 1
    REDEFINED_ID     = 2
    UNDECLARED_ID    = 3
    MAX_LVL_ACHIEVED = 4
    WARN_UNUSED_ID   = 5
    # Errores de tipo
    INVALID_KIND     = 6
    INVALID_RANGE    = 7
    BAD_ASSIG_TYPES  = 8
    BAD_PARAM_NUMBER = 9
    BAD_PARAM_TYPE   = 10
    READ_INT_EXPCT   = 11
    WRITE_EXPR_EXPCT = 12
    BOOL_EXPR_EXPCT  = 13
    CONF_EXPR_TYPES  = 14
    NOT_ARRAY_TYPE   = 15
    NOT_RECORD_TYPE  = 16
    ILLEGAL_INDEX    = 17
    
    # Cadenas de texto que describen cada uno de los posibles errores semanticos encontrados
    _errStrings = ("Undeclared type", 
                   "Recursive array definition of type",
                   "Redefined identifier",
                   "Undeclared identifier",
                   "Internal compiler error - Maximum scope nesting level reached",
                   "Identifier declared but never used",
                   
                   "Invalid identifier kind",
                   "Invalid array range",
                   "Non-conformant assignment types",
                   "Non-conformant number of parameters on call to",
                   "Unexpected parameter type, got ",
                   "Integer variable expected as parameter on call to 'read'",
                   "Integer expression expected as parameter on call to 'write'",
                   "Boolean expression expected, but got",
                   "Conflicting types while evaluating expression",
                   "Not an array type",
                   "Not a record type"
                   "Illegal indexing value")

    def __init__(self, errno, pos, found=None):
        super(SemError, self).__init__(errno, pos, found)
        self.printError()
    
    def printError(self):
        print str(Colors.WARNING + str(self.pos[0]) + "L,").rjust(10),
        print str(str(self.pos[1]) + "C").rjust(3),
        
        if self.errno != self.WARN_UNUSED_ID:
            print Colors.FAIL + "[SEM ERROR]" + Colors.ENDC \
                + " " + self._errStrings[self.errno],
        else:
            print Colors.HEADER + " [WARNING] " + Colors.ENDC \
                + " " + self._errStrings[self.errno],
              
        if self.found is not None:
            if isinstance(self.found, Token):
                print "'" + self.found.getLexeme() + "'"
            else:
                print "'" + self.found + "'"
        else:
            print "\n",
