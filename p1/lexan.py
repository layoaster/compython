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

    __patterns = [
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
    __flags = re.UNICODE | re.MULTILINE | re.IGNORECASE

    __fin = None
    __nline = None
    __ncol = None
    __line = None

    def __init__(self):
        """ Constructor de la clase
        """
        self.__nline = 1
        self.__ncol = 1
        self.__line = []
        self.__fin = False
        #Patrones para los tokens
        
    def openFile(self, fin):
        error = False
        try:
            self.__fin = open(fin, "rU")
        except IOError:
            error = True
        return error

    def yyLex(self):
        if self.__fin:
            for name, rule in __patterns:
                parts.append("(?P<%s>%s)" % (name, rule))
            
            self.__line = self.__fin.readline().decode("utf-8")
            
            self.__line = self.__fin.readline().decode("utf-8")
            self.__nline += 1

            self.__fin.close()
        else:
            print "ERROR: no se ha abierto el fichero de codigo fuente."
            exit(-1)


# --- Programa Principal ---
if __name__ == '__main__':

    analex = LexAn()
    analex.openFile(sys.argv[1])
    analex.yyLex()

