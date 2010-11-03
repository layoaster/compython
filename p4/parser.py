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
from stack import *
from nonterm import *
from parsingtable import *

class SynAn:
    """ Clase Analizador Sintactico:
        Comprueba que la secuencia de tokens de entrada sea acorde con las
        especificaciones de la gramatica de Pascal-
    """

    def __init__(self, verbose):
        """ Constructor de la clase. Atributos:
            _lookahead = token o simbolo de preanalisis
            _scanner = instancia de la clase analizador lexico
            _symbol = simbolo actual (terminal o no terminal) en el tope de la pila 
        """
        self._scanner = None
        self._lookahead = None
        self._symbol = None
        self._tokens = ""
        self._trace = ""
        self._n = 0

    def getTrace(self):
        return self._trace

    def getTokens(self):
        return self._tokens

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
        self._table = ParsingTable()

        self._stack.push(Token(WrapTk.ENDTEXT))
        self._stack.push(NonTerm(WrapNT.PROGRAM))
        self._lookahead = self._scanner.yyLex()
        self._tokens += self._lookahead.getTokLexeme() + "|"
        while not self._stack.isEmpty():
            self._trace += '<input type="hidden" name="trace' + str(self._n) + '" value="' + self._stack.printStack() + '">\n'
            self._symbol = self._stack.top()
            if isinstance(self._symbol, Token):    # Si en el top hay un token
                if self._symbol.getToken() == self._lookahead.getToken():
                    self._stack.pop()
                    self._lookahead = self._scanner.yyLex()
                    self._tokens += self._lookahead.getTokLexeme() + "|"
                else:   # El top es diferente del lookahead
                    raise SynError(SynError.UNEXPECTED_SYM, self._scanner.getPos(), 
                                   " - Found '" + self._lookahead.getLexeme() + "', expected '" + self._symbol.getTokLexeme() + "'")
            else:   	# Si en el top hay un no terminal
                try:
                    rule = self._table.getCell(self._symbol, self._lookahead)
                    self._stack.pop()
                    if rule is not None:  # Si la regla no es epsilon
                        for i in reversed(rule.getProd()):   # Sobrecargar pila
                            self._stack.push(i)    # para hacer push a la lista
                except KeyError:    # La celda esta vacia
                    raise SynError(SynError.NO_VALID_PROD, self._scanner.getPos(),
                                   " - From '" + self._symbol.getName() + "' having '" + self._lookahead.getLexeme() + "' as input token") 
            self._n += 1
        self._tokens = '<input type="hidden" name="tokens" value="' + self._tokens[:-3] + '">\n'
