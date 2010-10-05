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
import st
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
        for name, rule in _patterns:
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

    def yyLex(self, st):
        if self._fin:
            while self._buffer == "":
                self._buffer = self._fin.readline().decode("utf-8")
                if self._buffer == "": # EOF
                    return Token(WrapTk.ENDTEXT)
                self._nline += 1

                # Ignorar espacios en blanco
                wsmatch = self._wsregex.match(self._buffer)
                if wsmatch:
                    self._buffer = self._buffer[wsmatch.end():]

            match = self._regex(self._buffer)
            if match is None:
                print "Linea ", self._nline, "- TOKEN_ERROR; buffer: ", self._buffer
                return Token(WrapTk.TOKEN_ERROR)

            self._ncol = match.start()
            token = WrapTk.toToken(match.lastgroup)
            value = match.group(match.lastgroup)
            if token == WrapTk.ID:
                if st.isReserved(value):
                    return Token(token)
                if not st.isIn(value):
                    st.insert(value)
                return Token(WrapTk.ID, value)
            elif token == WrapTk.NUMERAL:
                return Token(WrapTk.NUMERAL, int(value))

        else:
            print "ERROR: no se ha abierto el fichero de codigo fuente."
            exit(-1)

