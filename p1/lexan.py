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

class LexAn:

    _patterns = [
        ("ASTERISK",        r"\*"),
        ("BECOMES",         r":="),
        ("COLON",           r":"),
        ("COMMA",           r","),
        ("DIV",             r"/"),
        ("DOUBLEDOT",       r"\.\."),
        ("EQUAL",           r"="),
        ("GREATER",         r"\>"),
        ("ID",              r"[a-zA-Z]+\w*"),
        ("LEFTBRACKET",     r"\["),
        ("LEFTPARENTHESIS", r"\("),
        ("LESS",            r"\<"),
        ("MINUS",           r"-"),
        ("NOTEQUAL",        r"\<\>"),
        ("NOTGREATER",      r"\<="),
        ("NOTLESS",         r"\>="),
        ("NUMERAL",         r"\d+"),
        ("PERIOD",          r"\."),
        ("PLUS",            r"\+"),
        ("RIGHTBRACKET",    r"\]"),
        ("RIGHTPARENTHESIS",r"\)"),
        ("SEMICOLON",       r";"),
    ]

    def __init__(self):
        """ Constructor de la clase
        """
        self._nline = 1
        self._ncol = 1
        self._line = ""
        self._fin = None
        self._flags = re.UNICODE | re.IGNORECASE
        
        parts = []
        for name, rule in _patterns:
            parts.append("(?P<%s>%s)" % (name, rule))

        self._regex = re.compile("|".join(parts), self._flags)
        self._wsregex = re.compile("\s*", re.MULTILINE)

    def openFile(self, fin):
        error = False
        try:
            self._fin = open(fin, "rU")
        except IOError:
            error = True
        return error

    def yyLex(self):
        if self._fin:
            if self._line == "":
                self._line = self._fin.readline().decode("utf-8")

            # Ignorar espacios en blanco
            wsmatch = self._wsregex.match(line)
            if wsmatch:
                line = line[wsmatch.end():]

            match = self._regex(line)
            
            #self._line = self.__fin.readline().decode("utf-8")
            self._nline += 1

            self._fin.close()
        else:
            print "ERROR: no se ha abierto el fichero de codigo fuente."
            exit(-1)


# --- Programa Principal ---
if __name__ == '__main__':

    analex = LexAn()
    analex.openFile(sys.argv[1])
    analex.yyLex()

