#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

from lexan import LexAn
from token import *
from error import *
import st


class SynAn:

    def __init__(self):
        _lookahead = None

    def start(self, fin):
        scanner = LexAn()
        scanner.openFile(fin)
        tok = scanner.yyLex()
        
	cline = 0
        print "ROW\tPOS\tTOKEN\t\t\tSYMBOL TABLE"
        print "---\t---\t-----\t\t\t------------"
        while tok.getToken() != WrapTk.ENDTEXT:
            # Imprimimos linea y posicion
            if scanner.getPos()[0] == cline:
                print "\t", scanner.getPos()[1],
            else:
                cline = scanner.getPos()[0]
                print cline, "\t", scanner.getPos()[1],

            # Imprimimos el tokenID y su valor, si es el caso
            print "\t<" + WrapTk.TokStrings[tok.getToken() - 1] + ",",
            print str(tok.getValue()) + ">",

            # Si es un identificador, mostramos su indice de la ST
            if (tok.getValue() != None and tok.getToken() != WrapTk.NUMERAL):
                print "\t\tST INDEX:", st.st.getIndex(tok.getValue()),
            try:
                tok = scanner.yyLex()
            except LexicalError as e:
                e._printError()
                tok = Token(WrapTk.TOKEN_ERROR)
            print ""
        print "--- ENDTEXT ---"
