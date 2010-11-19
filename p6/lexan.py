#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Modulo del Analizador Lexico para expresiones aritmeticas (+, -, *, /, - (unario)) parentizadas.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import sys
import string
import re
from error import LexError
from token import WrapTk, Token

class LexAn:

    _patterns = [
        (WrapTk.ASTERISK,        r"\*"),
        (WrapTk.LEFTPARENTHESIS, r"\("),
        (WrapTk.LETTER,          r"[a-zA-Z]"),
        (WrapTk.RIGHTPARENTHESIS,r"\)"),
        (WrapTk.VERTICALBAR,     r"\|")
    ]

    def __init__(self):
        """ Constructor de la clase
        """
        self._nline = 0
        self._ncol = 1
        self._tokstart = 1
        self._buffer = ""
        self._fin = None
        self._flags = re.UNICODE | re.IGNORECASE

        parts = []
        for name, rule in self._patterns:
            parts.append("(?P<%s>%s)" % (WrapTk.toStr(name), rule))

        self._regex = re.compile("|".join(parts), self._flags)
        self._wsregex = re.compile("\s*", re.MULTILINE)

    def openFile(self, fin):
        """ Abre el fichero para lectura (con modo de saltos de linea universales). Si se crea
            una excepcion de tipo IOError, se lanza hacia la clase llamante
        """
        try:
            self._fin = open(fin, "rU")
        except IOError:
            raise

    def _readLine(self):
        """ Lee una linea del fichero y la inserta en el buffer, ignorando lineas en blanco
        """
        while self._buffer == "":
            self._buffer = self._fin.readline()
            if self._buffer == "": # EOF
                return False
            self._nline += 1
            self._ncol = 1
            self._buffer = self._buffer.rstrip()

        # Ignorar espacios en blanco
        wsmatch = self._wsregex.match(self._buffer)
        if wsmatch:
            self._buffer = self._buffer[wsmatch.end():]
            self._ncol += wsmatch.end()
            self._tokstart = self._ncol
        return True

    def getPos(self):
        """ Retorna la linea y columna en la que se situa el ultimo token obtenido
        """
        return (self._nline, self._tokstart)

    def yyLex(self):
        if self._readLine():
            match = self._regex.match(self._buffer)

            if match is None:
                self._buffer = self._buffer[1:]
                self._ncol += 1
                raise LexError(LexError.UNKNOWN_CHAR, self.getPos())    

            token = WrapTk.toToken(match.lastgroup)
            value = match.group(match.lastgroup)

            self._ncol += match.end()
            self._buffer = self._buffer[match.end():]

            if token == WrapTk.LETTER:
                return Token(WrapTk.LETTER, value.lower())
            else:   # Reconocido token valido
                return Token(token)
        else:   # Se ha llegado a fin del fichero
            return Token(WrapTk.ENDTEXT)
