#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Implementación de la fase del Analisis Sintactico basado en el Análisis Sintáctico Descendente No Recursivo.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

from lexan import LexAn
from token import *
from error import *
#from table import *
from stack import *
from nonterm import *
from production import *

class SynAn:
    """ Clase Analizador Sintactico:
        Comprueba que la secuencia de tokens de entrada sea acorde con las
        especificaciones de la gramatica de Pascal-
    """
    def __init__(self):
        """ Constructor de la clase. Atributos:
            _lookahead = token o simbolo de preanalisis
            _scanner = instancia de la clase analizador lexico
        """
        self._scanner = None
        self._lookahead = None
        self._top = None

    def start(self, fin):
        """ Comienzo del analizador sintactico. Se encarga de inicializar el lexico,
            ordenarle abrir el fichero y recoger el primer token de entrada para comenzar
            el analisis
        """
        self._scanner = LexAn()
        try:
            self._scanner.openFile(fin)
        except IOError:
            raise

        self._stack = Stack()
#        self._table = ParsingTable()

        self._stack.push(Token(WrapTk.ENDTEXT))
        self._stack.push(NonTerm(WrapNT.PROGRAM))
        self._stack.push(Token(WrapTk.PERIOD))
#        self._stack.push(<Program>)
        while self._stack.top() != Token(WrapTk.ENDTEXT):
            self._top = self._stack.top()
            self._lookahead = self._scanner.yyLex()
            if isinstance(self._top, Token):    # Si en el top hay un token
                if self._top.getToken() == self._lookahead.getToken():
                    self._stack.pop()
                    print "macheo", self._lookahead.getToken()
                    self._lookahead = self._scanner.yyLex()
                else:       # El top es diferente del lookahead
                    print self._scanner.getPos(),
                    print "Syntax Error:", self._top.getLexeme(), "found",
                    print "-", self._lookahead.getLexeme(), "expected."
                    exit(1)
            else:                   # Si en el top hay un no terminal
                print "futura ampliacion"
                exit(1)
