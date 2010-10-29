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

        self._table[NonTerm(WrapNT.PROGRAM)] = {Token(WrapTk.PROGRAM) : Production([Token(WrapTk.PROGRAM),
                                                                                    Token(WrapTk.ID),
                                                                                    Token(WrapTk.SEMICOLON),
                                                                                    NonTerm(WrapNT.BLOCKBODY),
                                                                                    Token(WrapTk.PERIOD)])}

        self._table[NonTerm(WrapNT.BLOCKBODY)] = {Token(WrapTk.CONST) : Production([NonTerm(WrapNT.CONSTDEFPART),
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
                                                                                    NonTerm(WrapNT.COMPSTATE)])}

        self._table[NonTerm(WrapNT.CONSTDEFPART)] = {Token(WrapTk.CONST) : Production([Token(WrapTk.CONST),
                                                                                       NonTerm(WrapNT.CONSTDEF),
                                                                                       NonTerm(WrapNT.CONSTDEF2)]),

                                                     Token(WrapTk.TYPE) : None,
                                                     Token(WrapTk.VAR) : None,
                                                     Token(WrapTk.PROCEDURE) : None,
                                                     Token(WrapTk.BEGIN) : None}

        self._table[NonTerm(WrapNT.CONSTDEF)] = {Token(WrapTk.ID) : Production([Token(WrapTk.ID),
                                                                                Token(WrapTk.EQUAL),
                                                                                NonTerm(WrapNT.CONSTANT),
                                                                                Token(WrapTk.SEMICOLON)])}

        self._table[NonTerm(WrapNT.CONSTDEF2)] = {Token(WrapTk.ID) : Production([NonTerm(WrapNT.CONSTDEF),
                                                                                 NonTerm(WrapNT.CONSTDEF2)]),

                                                  Token(WrapTk.TYPE) : None,
                                                  Token(WrapTk.VAR) : None,
                                                  Token(WrapTk.PROCEDURE) : None,
                                                  Token(WrapTk.BEGIN) : None}

        self._table[NonTerm(WrapNT.TYPEDEFPART)] = {Token(WrapTk.TYPE) : Production([Token(WrapTk.TYPE),
                                                                                     NonTerm(WrapNT.TYPEDEF),
                                                                                     NonTerm(WrapNT.TYPEDEF2)]),

                                                    Token(WrapTk.VAR) : None,
                                                    Token(WrapTk.PROCEDURE) : None,
                                                    Token(WrapTk.BEGIN) : None}

        self._table[NonTerm(WrapNT.TYPEDEF)] = {Token(WrapTk.ID) : Production([Token(WrapTk.ID),
                                                                               Token(WrapTk.EQUAL),
                                                                               NonTerm(WrapNT.NEWTYPE),
                                                                               Token(WrapTk.SEMICOLON)])}

        self._table[NonTerm(WrapNT.TYPEDEF2)] = {Token(WrapTk.ID) : Production([NonTerm(WrapNT.TYPEDEF),
                                                                                NonTerm(WrapNT.TYPEDEF2)]),

                                                 Token(WrapTk.VAR) : None,
                                                 Token(WrapTk.PROCEDURE) : None,
                                                 Token(WrapTk.BEGIN) : None}

        self._table[NonTerm(WrapNT.NEWTYPE)] = {Token(WrapTk.ARRAY) : Production([NonTerm(WrapNT.NEWARRAYTYPE)]),

                                                 Token(WrapTk.RECORD) : Production([NonTerm(WrapNT.NEWRECTYPE)])}

        self._table[NonTerm(WrapNT.NEWARRAYTYPE)] = {Token(WrapTk.ARRAY) : Production([Token(WrapTk.ARRAY),
                                                                                       Token(WrapTk.LEFTBRACKET),
                                                                                       NonTerm(WrapNT.INDEXRANGE),
                                                                                       Token(WrapTk.RIGHTBRACKET),
                                                                                       Token(WrapTk.OF),
                                                                                       Token(WrapTk.ID)])}

        self._table[NonTerm(WrapNT.INDEXRANGE)] = {Token(WrapTk.NUMERAL) : Production([NonTerm(WrapNT.CONSTANT),
                                                                                       Token(WrapTk.DOUBLEDOT),
                                                                                       NonTerm(WrapNT.CONSTANT)]),

                                                    Token(WrapTk.ID) : Production([NonTerm(WrapNT.CONSTANT),
                                                                                   Token(WrapTk.DOUBLEDOT),
                                                                                   NonTerm(WrapNT.CONSTANT)])}

        self._table[NonTerm(WrapNT.NEWRECTYPE)] = {Token(WrapTk.RECORD) : Production([Token(WrapTk.RECORD),
                                                                                      NonTerm(WrapNT.RECSECTION),
                                                                                      NonTerm(WrapNT.FIELDLIST),
                                                                                      Token(WrapTk.END)])}

        self._table[NonTerm(WrapNT.FIELDLIST)] = {Token(WrapTk.ID) : Production([Token(WrapTk.SEMICOLON),
                                                                                 NonTerm(WrapNT.RECSECTION),
                                                                                 NonTerm(WrapNT.FIELDLIST)])}

        self._table[NonTerm(WrapNT.FIELDLIST2)] = {Token(WrapTk.SEMICOLON) : Production([Token(WrapTk.SEMICOLON),
                                                                                         NonTerm(WrapNT.RECSECTION),
                                                                                         NonTerm(WrapNT.FIELDLIST)]),

                                                   Token(WrapTk.END) : None}

        self._table[NonTerm(WrapNT.RECSECTION)] = {Token(WrapTk.ID) : Production([Token(WrapTk.ID),
                                                                                  NonTerm(WrapNT.RECSECTION2),
                                                                                  Token(WrapTk.COLON),
                                                                                  Token(WrapTk.ID)])}

        self._table[NonTerm(WrapNT.RECSECTION2)] = {Token(WrapTk.COMMA) : Production([Token(WrapTk.COMMA),
                                                                                      NonTerm(WrapNT.RECSECTION2)]),

                                                   Token(WrapTk.COLON) : None}

        self._table[NonTerm(WrapNT.VARDEFPART)] = {Token(WrapTk.VAR) : Production([Token(WrapTk.VAR),
                                                                                   NonTerm(WrapNT.VARDEF),
                                                                                   NonTerm(WrapNT.VARDEF2)]),

                                                   Token(WrapTk.PROCEDURE) : None,
                                                   Token(WrapTk.BEGIN) : None}

        self._table[NonTerm(WrapNT.VARDEF)] = {Token(WrapTk.ID) : Production([NonTerm(WrapNT.RECSECTION),
                                                                              Token(WrapTk.SEMICOLON)])}

        self._table[NonTerm(WrapNT.VARDEF2)] = {Token(WrapTk.ID) : Production([NonTerm(WrapNT.VARDEF),
                                                                               NonTerm(WrapNT.VARDEF2)]),

                                                Token(WrapTk.PROCEDURE) : None,
                                                Token(WrapTk.BEGIN) : None}

        self._table[NonTerm(WrapNT.VARGROUP)] = {Token(WrapTk.ID) : Production([Token(WrapTk.ID),
                                                                                NonTerm(WrapNT.VARGROUP2),
                                                                                Token(WrapTk.COLON),
                                                                                Token(WrapTk.ID)])}

        self._table[NonTerm(WrapNT.VARGROUP2)] = {Token(WrapTk.COMMA) : Production([Token(WrapTk.COMMA),
                                                                                    NonTerm(WrapNT.VARGROUP2)]),

                                                  Token(WrapTk.COLON) : None}

        self._table[NonTerm(WrapNT.PROCDEF)] = {Token(WrapTk.PROCEDURE) : Production([Token(WrapTk.PROCEDURE),
                                                                                      Token(WrapTk.ID),
                                                                                      NonTerm(WrapNT.PROCBLOCK),
                                                                                      Token(WrapTk.SEMICOLON),
                                                                                      NonTerm(WrapNT.PROCDEF)]),
                                                Token(WrapTk.BEGIN) : None}

    def getCell(self, nterm, tok):
        row = self._table.get(nterm)
        return  self._table[nterm][tok]

#table = ParsingTable()
#lista = table.getCell(NonTerm(WrapNT.BLOCKBODY), Token(WrapTk.PROCEDURE))
#for x in lista.getProd():
    #print x.getName()



