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
        (WrapTk.ASTERISK[1],        r"\*"),
        (WrapTk.BECOMES[1],         r":="),
        (WrapTk.COLON[1],           r":"),
        (WrapTk.COMMA[1],           r","),
        (WrapTk.DIV[1],             r"/"),
        (WrapTk.DOUBLEDOT[1],       r"\.\."),
        (WrapTk.EQUAL[1],           r"="),
        (WrapTk.GREATER[1],         r"\>"),
        (WrapTk.ID[1],              r"[a-zA-Z]\w*"),
        (WrapTk.LEFTBRACKET[1],     r"\["),
        (WrapTk.LEFTPARENTHESIS[1], r"\("),
        (WrapTk.LESS[1],            r"\<"),
        (WrapTk.MINUS[1],           r"-"),
        (WrapTk.NOTEQUAL[1],        r"\<\>"),
        (WrapTk.NOTGREATER[1],      r"\<="),
        (WrapTk.NOTLESS[1],         r"\>="),
        (WrapTk.NUMERAL[1],         r"\d+"),
        (WrapTk.PERIOD[1],          r"\."),
        (WrapTk.PLUS[1],            r"\+"),
        (WrapTk.RIGHTBRACKET[1],    r"\]"),
        (WrapTk.RIGHTPARENTHESIS[1],r"\)"),
        (WrapTk.SEMICOLON[1],       r";"),
        (WrapTk.COMMENT[1],         r"\(\*|\{"),
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

    def _readLine(self):
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

    def _ignComment(self):
        nbra = 0
        npar = 0
        comment = re.compile("(?P<leftbracket>\{)|(?P<leftparenthesis>\(\*)|(?P<rightbracket>\})|(?P<rightparenthesis>\*\))")
        match = comment.search(self._buffer)
        print "CHIVATO"
        while match:
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
            if ((nbra or npar) and not match):
                if self._readLine():
                    match = comment.search(self._buffer)

        if (not nbra and not npar):
            return True
        else:
            return False

    def yyLex(self):
        if self._fin:
            if self._readLine():
                print "--------"
                print "Linea: ", self._nline, "; Columna: ", self._ncol
                print "BUFFER = ", self._buffer

                match = self._regex.match(self._buffer)
                if match is None:
                    print "## TOKEN_ERROR ##"
                    self._buffer = self._buffer[1:]
                    self._ncol += 1
                    return Token(WrapTk.TOKEN_ERROR[1])

                token = WrapTk.toToken(match.lastgroup)
                value = match.group(match.lastgroup)

                if token != WrapTk.COMMENT[1]:
                    self._ncol += match.end() - match.start()
                    self._buffer = self._buffer[match.end():]

                if token == WrapTk.ID[1]:
                    #print value
                    if st.isReserved(value.lower()):
                        #print "reservedd"
                        return Token(st.getIndex(value))
                    if not st.isIn(value.lower()):
                        st.insert(value.lower())
                    return Token(WrapTk.ID[1], value)
                elif token == WrapTk.NUMERAL[1]:
                    return Token(WrapTk.NUMERAL[1], int(value))
                elif token == WrapTk.COMMENT[1]:
                    if not self._ignComment():
                        return Token(WrapTk.TOKEN_ERROR[1])
                else:
                    return Token(token)
            # Fin if
            else:
                return Token(WrapTk.ENDTEXT[1])
        else:
            print "ERROR: no se ha abierto el fichero de codigo fuente."
            exit(-1)

