#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Modulo del Analizador Lexico para Pascal-.
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
        (WrapTk.ID,              r"[a-zA-Z]\w*"),
        (WrapTk.LEFTPARENTHESIS, r"\("),
        (WrapTk.MINUS,           r"-"),
        (WrapTk.NUMERAL,         r"\d+"),
        (WrapTk.PLUS,            r"\+"),
        (WrapTk.RIGHTPARENTHESIS,r"\)"),
        (WrapTk.SLASH,           r"\/")
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
        return (self._nline, self._tokstart)

    def yyLex(self):
        if self._readLine():
            match = self._regex.match(self._buffer)

            if match is None:
                self._buffer = self._buffer[1:]
                self._ncol += 1
                LexError(LexError.UNKNOWN_CHAR, self.getPos())
                return Token(WrapTk.TOKEN_ERROR)

            token = WrapTk.toToken(match.lastgroup)
            value = match.group(match.lastgroup)

            self._ncol += match.end()
            self._buffer = self._buffer[match.end():]

            if token == WrapTk.ID:
                return Token(WrapTk.ID, value.lower())
            elif token == WrapTk.NUMERAL:
                if int(value) > 32767:
                    LexError(LexError.INT_OVERFLOW, self.getPos())
                    return Token(WrapTk.TOKEN_ERROR)
                else:
                    return Token(WrapTk.NUMERAL, int(value))
            else:   # Reconocido token valido
                return Token(token)
        else:   # Se ha llegado a fin del fichero
            return Token(WrapTk.ENDTEXT)
