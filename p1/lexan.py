#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import sys
import string
import re
from st import SymbolTable, st
from token import WrapTk, Token

class LexAn:

    _patterns = [
        (WrapTk.ASTERISK,        r"\*"),
        (WrapTk.BECOMES,         r":="),
        (WrapTk.COLON,           r":"),
        (WrapTk.COMMA,           r","),
        (WrapTk.DIV,             r"/"),
        (WrapTk.DOUBLEDOT,       r"\.\."),
        (WrapTk.EQUAL,           r"="),
        (WrapTk.GREATER,         r"\>"),
        (WrapTk.ID,              r"[a-zA-Z]\w*"),
        (WrapTk.LEFTBRACKET,     r"\["),
        (WrapTk.LEFTPARENTHESIS, r"\("),
        (WrapTk.LESS,            r"\<"),
        (WrapTk.MINUS,           r"-"),
        (WrapTk.NOTEQUAL,        r"\<\>"),
        (WrapTk.NOTGREATER,      r"\<="),
        (WrapTk.NOTLESS,         r"\>="),
        (WrapTk.NUMERAL,         r"\d+"),
        (WrapTk.PERIOD,          r"\."),
        (WrapTk.PLUS,            r"\+"),
        (WrapTk.RIGHTBRACKET,    r"\]"),
        (WrapTk.RIGHTPARENTHESIS,r"\)"),
        (WrapTk.SEMICOLON,       r";"),
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
        error = False
        try:
            self._fin = open(fin, "rU")
        except IOError:
            error = True
        return error

    def readLine(self):
        while self._buffer == "":
            self._buffer = self._fin.readline()#.decode("utf-8")
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

    def yyLex(self):
        if self._fin:
            if self.readLine():
                print "--------"
                print "Linea: ", self._nline, "; Columna: ", self._ncol
                print "BUFFER = ", self._buffer

                match = self._regex.match(self._buffer)
                if match is None:
                    print "## TOKEN_ERROR ##"
                    self._buffer = self._buffer[1:]
                    self._ncol += 1
                    return Token(WrapTk.TOKEN_ERROR)

                self._ncol += match.end() - match.start()
                self._buffer = self._buffer[match.end():]
                token = WrapTk.toToken(match.lastgroup)
                value = match.group(match.lastgroup)
                if token == WrapTk.ID:
                    #print value
                    if st.isReserved(value.lower()):
                        #print "reservedd"
                        return Token(st.getIndex(value))
                    if not st.isIn(value.lower()):
                        st.insert(value.lower())
                    return Token(WrapTk.ID, value)
                elif token == WrapTk.NUMERAL:
                    return Token(WrapTk.NUMERAL, int(value))
                else:
                    return Token(token)
            # Fin if
            else:
                return Token(WrapTk.ENDTEXT)
        else:
            print "ERROR: no se ha abierto el fichero de codigo fuente."
            exit(-1)

