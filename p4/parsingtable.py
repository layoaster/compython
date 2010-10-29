#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Tabla de Analisis Sintactico del Analizador Sintactico Descendente No Recursivo.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

from nonterm import *
from token import *
from production import *

class ParsingTable:

    def __init__(self):
        self._table = {}

        self._table = {NonTerm(WrapNT.PROGRAM) : {Token(WrapTk.PROGRAM) : Production([Token(WrapTk.PROGRAM),
                                                                                      Token(WrapTk.ID),
                                                                                      Token(WrapTk.SEMICOLON),
                                                                                      NonTerm(WrapNT.BLOCKBODY),
                                                                                      Token(WrapTk.PERIOD)])}}

        self._table = {NonTerm(WrapNT.BLOCKBODY) : {Token(WrapTk.CONST) : Production([NonTerm(WrapNT.CONSTDEFPART),
                                                                                      NonTerm(WrapNT.TYPEDEFPART),
                                                                                      NonTerm(WrapNT.VARDEFPART),
                                                                                      NonTerm(WrapNT.PROCDEF),
                                                                                      NonTerm(WrapNT.COMPSTATE)]),

                                                    Token(WrapTk.TYPE) : Production([NonTerm(WrapNT.CONSTDEFPART),
                                                                                     NonTerm(WrapNT.TYPEDEFPART),
                                                                                     NonTerm(WrapNT.VARDEFPART),
                                                                                     NonTerm(WrapNT.PROCDEF),
                                                                                     NonTerm(WrapNT.COMPSTATE)]),

                                                    Token(WrapTk.VAR) : Production([NonTerm(WrapNT.CONSTDEFPART),
                                                                                    NonTerm(WrapNT.TYPEDEFPART),
                                                                                    NonTerm(WrapNT.VARDEFPART),
                                                                                    NonTerm(WrapNT.PROCDEF),
                                                                                    NonTerm(WrapNT.COMPSTATE)]),

                                                    Token(WrapTk.PROCEDURE) : Production([NonTerm(WrapNT.CONSTDEFPART),
                                                                                          NonTerm(WrapNT.TYPEDEFPART),
                                                                                          NonTerm(WrapNT.VARDEFPART),
                                                                                          NonTerm(WrapNT.PROCDEF),
                                                                                          NonTerm(WrapNT.COMPSTATE)]),

                                                    Token(WrapTk.BEGIN) : Production([NonTerm(WrapNT.CONSTDEFPART),
                                                                                      NonTerm(WrapNT.TYPEDEFPART),
                                                                                      NonTerm(WrapNT.VARDEFPART),
                                                                                      NonTerm(WrapNT.PROCDEF),
                                                                                      NonTerm(WrapNT.COMPSTATE)])}}

        self._table = {NonTerm(WrapNT.CONSTDEFPART) : {Token(WrapTk.CONST) : Production([Token(WrapTk.CONST),
                                                                                      NonTerm(WrapNT.CONSTDEF),
                                                                                      NonTerm(WrapNT.CONSTDEF2)]),

                                                       Token(WrapTk.TYPE) : None}}

    def getCell(self, nterm, tok):

        return self._table.get(nterm)[tok]

table = ParsingTable()
lista = table.getCell(NonTerm(WrapNT.BLOCKBODY), Token(WrapTk.PROCEDURE))
for x in lista.getProd():
    print x.getName()



