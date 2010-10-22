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
from st import SymbolTable, st
from token import WrapTk, Token

class LexAn:

    _patterns = [
        (WrapTk.COMMENT,         r"\(\*|\{|//"),
        (WrapTk.ASTERISK,        r"\*"),
        (WrapTk.BECOMES,         r":="),
        (WrapTk.COLON,           r":"),
        (WrapTk.COMMA,           r","),
        (WrapTk.DOUBLEDOT,       r"\.\."),
        (WrapTk.EQUAL,           r"="),
        (WrapTk.NOTEQUAL,        r"\<\>"),
        (WrapTk.NOTGREATER,      r"\<="),
        (WrapTk.NOTLESS,         r"\>="),
        (WrapTk.GREATER,         r"\>"),
        (WrapTk.ID,              r"[a-zA-Z]\w*"),
        (WrapTk.LEFTBRACKET,     r"\["),
        (WrapTk.LEFTPARENTHESIS, r"\("),
        (WrapTk.LESS,            r"\<"),
        (WrapTk.MINUS,           r"-"),
        (WrapTk.NUMERAL,         r"\d+"),
        (WrapTk.PERIOD,          r"\."),
        (WrapTk.PLUS,            r"\+"),
        (WrapTk.RIGHTBRACKET,    r"\]"),
        (WrapTk.RIGHTPARENTHESIS,r"\)"),
        (WrapTk.SEMICOLON,       r";")
    ]

    def __init__(self):
        """ Constructor de la clase
        """
        self._nline = 0
        self._ncol = 1
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
            self._ncol += wsmatch.end() - wsmatch.start()
        return True

    def _ignComment(self):
        """ Procesado de comentarios, incluyendo comentarios anidados, multilinea y malformados (sin cerrar)
        """
        comment = re.compile("(?P<leftbracket>\{)|(?P<leftparenthesis>\(\*)|(?P<rightbracket>\})|(?P<rightparenthesis>\*\))|(?P<doublebar>//)")
        match = comment.search(self._buffer)
        if match.lastgroup != "doublebar":
            nbra = 1
            npar = 1
            flag = True
            while (nbra != 0 or npar != 0):
                if flag:
                    nbra = 0
                    npar = 0
                    flag = False
                if match:
                    if match.lastgroup == "leftbracket":
                        nbra += 1
                    if match.lastgroup == "leftparenthesis":
                        npar += 1
                    if match.lastgroup == "rightbracket":
                        nbra -= 1
                    if match.lastgroup == "rightparenthesis":
                        npar -= 1

                    self._buffer = self._buffer[match.end():]
                    match = comment.search(self._buffer)
                else:
                    self._buffer = ""
                    if self._readLine():
                        match = comment.search(self._buffer)
                        if match:
                            print match.lastgroup
                    else:
                        return False
            if len(self._buffer) == 0:
                self._readLine()
            return True
        else:
            self._buffer = ""
            self._readLine()
            return True

    def getPos(self):
        return (self._nline, self._ncol)

    def yyLex(self):
        #if self._fin:
        if self._readLine():
            match = self._regex.match(self._buffer)

            if match is None:
                self._buffer = self._buffer[1:]
                self._ncol += 1
                raise LexError(LexError.UNKNOWN_CHAR, self.getPos())

            token = WrapTk.toToken(match.lastgroup)
            value = match.group(match.lastgroup)

            while token == WrapTk.COMMENT:
                if self._ignComment():
                    #Varios Comentarios bien hehcos separados por espacios
                    self._readLine()
                    match = self._regex.match(self._buffer)
                    if match is None:
                        return Token(WrapTk.ENDTEXT)
                    token = WrapTk.toToken(match.lastgroup)
                    value = match.group(match.lastgroup)
                else:
                    raise LexError(LexError.UNCLOSED_COM, self.getPos())

            self._ncol += match.end() - match.start()
            self._buffer = self._buffer[match.end():]

            if token == WrapTk.ID:
                if st.isReserved(value.lower()):
                    return Token(st.getIndex(value.lower()))
                if not st.isIn(value.lower()):
                    st.insert(value.lower())
                return Token(WrapTk.ID, value.lower())
            elif token == WrapTk.NUMERAL:
                if int(value) > 32767:
                    raise LexError(LexError.INT_OVERFLOW, self.getPos())
                else:
                    return Token(WrapTk.NUMERAL, int(value))
            else:   # Reconocido token valido
                return Token(token)
        else:   # Se ha llegado a fin del fichero
            return Token(WrapTk.ENDTEXT)
        #else:
        #    raise IOError
