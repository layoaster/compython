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

        self._table[NonTerm(WrapNT.PROGRAM)]      = {Token(WrapTk.PROGRAM)  : Production([Token(WrapTk.PROGRAM),
                                                                                          Token(WrapTk.ID),
                                                                                          Token(WrapTk.SEMICOLON),
                                                                                          NonTerm(WrapNT.BLOCKBODY),
                                                                                          Token(WrapTk.PERIOD)])}

        self._table[NonTerm(WrapNT.BLOCKBODY)]    = {Token(WrapTk.CONST)    : Production([NonTerm(WrapNT.CONSTDEFPART),
                                                                                          NonTerm(WrapNT.TYPEDEFPART),
                                                                                          NonTerm(WrapNT.VARDEFPART),
                                                                                          NonTerm(WrapNT.PROCDEF),
                                                                                          NonTerm(WrapNT.COMPSTATE)]),

                                                     Token(WrapTk.TYPE)     : Production([NonTerm(WrapNT.CONSTDEFPART),
                                                                                          NonTerm(WrapNT.TYPEDEFPART),
                                                                                          NonTerm(WrapNT.VARDEFPART),
                                                                                          NonTerm(WrapNT.PROCDEF),
                                                                                          NonTerm(WrapNT.COMPSTATE)]),

                                                     Token(WrapTk.VAR)      : Production([NonTerm(WrapNT.CONSTDEFPART),
                                                                                          NonTerm(WrapNT.TYPEDEFPART),
                                                                                          NonTerm(WrapNT.VARDEFPART),
                                                                                          NonTerm(WrapNT.PROCDEF),
                                                                                          NonTerm(WrapNT.COMPSTATE)]),

                                                     Token(WrapTk.PROCEDURE): Production([NonTerm(WrapNT.CONSTDEFPART),
                                                                                          NonTerm(WrapNT.TYPEDEFPART),
                                                                                          NonTerm(WrapNT.VARDEFPART),
                                                                                          NonTerm(WrapNT.PROCDEF),
                                                                                          NonTerm(WrapNT.COMPSTATE)]),

                                                     Token(WrapTk.BEGIN)    : Production([NonTerm(WrapNT.CONSTDEFPART),
                                                                                          NonTerm(WrapNT.TYPEDEFPART),
                                                                                          NonTerm(WrapNT.VARDEFPART),
                                                                                          NonTerm(WrapNT.PROCDEF),
                                                                                          NonTerm(WrapNT.COMPSTATE)])}

        self._table[NonTerm(WrapNT.CONSTDEFPART)] = {Token(WrapTk.CONST)     : Production([Token(WrapTk.CONST),
                                                                                           NonTerm(WrapNT.CONSTDEF),
                                                                                           NonTerm(WrapNT.CONSTDEF2)]),
                                                     Token(WrapTk.TYPE)      : None,
                                                     Token(WrapTk.VAR)       : None,
                                                     Token(WrapTk.PROCEDURE) : None,
                                                     Token(WrapTk.BEGIN)     : None}

        self._table[NonTerm(WrapNT.CONSTDEF)]     = {Token(WrapTk.ID)        : Production([Token(WrapTk.ID),
                                                                                           Token(WrapTk.EQUAL),
                                                                                           NonTerm(WrapNT.CONSTANT),
                                                                                           Token(WrapTk.SEMICOLON)])}

        self._table[NonTerm(WrapNT.CONSTDEF2)]    = {Token(WrapTk.ID)        : Production([NonTerm(WrapNT.CONSTDEF),
                                                                                           NonTerm(WrapNT.CONSTDEF2)]),
                                                     Token(WrapTk.TYPE)      : None,
                                                     Token(WrapTk.VAR)       : None,
                                                     Token(WrapTk.PROCEDURE) : None,
                                                     Token(WrapTk.BEGIN)     : None}

        self._table[NonTerm(WrapNT.TYPEDEFPART)]  = {Token(WrapTk.TYPE)      : Production([Token(WrapTk.TYPE),
                                                                                           NonTerm(WrapNT.TYPEDEF),
                                                                                           NonTerm(WrapNT.TYPEDEF2)]),
                                                     Token(WrapTk.VAR)       : None,
                                                     Token(WrapTk.PROCEDURE) : None,
                                                     Token(WrapTk.BEGIN)     : None}

        self._table[NonTerm(WrapNT.TYPEDEF)]      = {Token(WrapTk.ID)        : Production([Token(WrapTk.ID),
                                                                                           Token(WrapTk.EQUAL),
                                                                                           NonTerm(WrapNT.NEWTYPE),
                                                                                           Token(WrapTk.SEMICOLON)])}

        self._table[NonTerm(WrapNT.TYPEDEF2)]     = {Token(WrapTk.ID)        : Production([NonTerm(WrapNT.TYPEDEF),
                                                                                           NonTerm(WrapNT.TYPEDEF2)]),
                                                     Token(WrapTk.VAR)       : None,
                                                     Token(WrapTk.PROCEDURE) : None,
                                                     Token(WrapTk.BEGIN)     : None}

        self._table[NonTerm(WrapNT.NEWTYPE)]      = {Token(WrapTk.ARRAY)     : Production([NonTerm(WrapNT.NEWARRAYTYPE)]),
                                                     Token(WrapTk.RECORD)    : Production([NonTerm(WrapNT.NEWRECTYPE)])}

        self._table[NonTerm(WrapNT.NEWARRAYTYPE)] = {Token(WrapTk.ARRAY)     : Production([Token(WrapTk.ARRAY),
                                                                                           Token(WrapTk.LEFTBRACKET),
                                                                                           NonTerm(WrapNT.INDEXRANGE),
                                                                                           Token(WrapTk.RIGHTBRACKET),
                                                                                           Token(WrapTk.OF),
                                                                                           Token(WrapTk.ID)])}

        self._table[NonTerm(WrapNT.INDEXRANGE)]   = {Token(WrapTk.NUMERAL)   : Production([NonTerm(WrapNT.CONSTANT),
                                                                                           Token(WrapTk.DOUBLEDOT),
                                                                                           NonTerm(WrapNT.CONSTANT)]),

                                                     Token(WrapTk.ID)        : Production([NonTerm(WrapNT.CONSTANT),
                                                                                           Token(WrapTk.DOUBLEDOT),
                                                                                           NonTerm(WrapNT.CONSTANT)])}

        self._table[NonTerm(WrapNT.NEWRECTYPE)]   = {Token(WrapTk.RECORD)    : Production([Token(WrapTk.RECORD),
                                                                                           NonTerm(WrapNT.FIELDLIST),
                                                                                           Token(WrapTk.END)])}

        self._table[NonTerm(WrapNT.FIELDLIST)]    = {Token(WrapTk.ID)        : Production([NonTerm(WrapNT.RECSECTION),
                                                                                           NonTerm(WrapNT.FIELDLIST2)])}

        self._table[NonTerm(WrapNT.FIELDLIST2)]   = {Token(WrapTk.SEMICOLON) : Production([Token(WrapTk.SEMICOLON),
                                                                                           NonTerm(WrapNT.RECSECTION),
                                                                                           NonTerm(WrapNT.FIELDLIST2)]),
                                                     Token(WrapTk.END)       : None}

        self._table[NonTerm(WrapNT.RECSECTION)]   = {Token(WrapTk.ID)        : Production([Token(WrapTk.ID),
                                                                                           NonTerm(WrapNT.RECSECTION2),
                                                                                           Token(WrapTk.COLON),
                                                                                           Token(WrapTk.ID)])}

        self._table[NonTerm(WrapNT.RECSECTION2)]  = {Token(WrapTk.COMMA)     : Production([Token(WrapTk.COMMA),
                                                                                           Token(WrapTk.ID),
                                                                                           NonTerm(WrapNT.RECSECTION2)]),
                                                     Token(WrapTk.COLON)     : None}

        self._table[NonTerm(WrapNT.VARDEFPART)]   = {Token(WrapTk.VAR)       : Production([Token(WrapTk.VAR),
                                                                                           NonTerm(WrapNT.VARDEF),
                                                                                           NonTerm(WrapNT.VARDEF2)]),
                                                     Token(WrapTk.PROCEDURE) : None,
                                                     Token(WrapTk.BEGIN)     : None}

        self._table[NonTerm(WrapNT.VARDEF)]       = {Token(WrapTk.ID)        : Production([NonTerm(WrapNT.RECSECTION),
                                                                                           Token(WrapTk.SEMICOLON)])}

        self._table[NonTerm(WrapNT.VARDEF2)]      = {Token(WrapTk.ID)        : Production([NonTerm(WrapNT.VARDEF),
                                                                                           NonTerm(WrapNT.VARDEF2)]),
                                                     Token(WrapTk.PROCEDURE) : None,
                                                     Token(WrapTk.BEGIN)     : None}

        self._table[NonTerm(WrapNT.VARGROUP)]     = {Token(WrapTk.ID)        : Production([Token(WrapTk.ID),
                                                                                           NonTerm(WrapNT.VARGROUP2),
                                                                                           Token(WrapTk.COLON),
                                                                                           Token(WrapTk.ID)])}

        self._table[NonTerm(WrapNT.VARGROUP2)]    = {Token(WrapTk.COMMA)     : Production([Token(WrapTk.COMMA),
                                                                                           NonTerm(WrapNT.VARGROUP2)]),
                                                     Token(WrapTk.COLON)     : None}

        self._table[NonTerm(WrapNT.PROCDEF)]      = {Token(WrapTk.PROCEDURE) : Production([Token(WrapTk.PROCEDURE),
                                                                                           Token(WrapTk.ID),
                                                                                           NonTerm(WrapNT.PROCBLOCK),
                                                                                           Token(WrapTk.SEMICOLON),
                                                                                           NonTerm(WrapNT.PROCDEF)]),
                                                     Token(WrapTk.BEGIN)     : None}

        self._table[NonTerm(WrapNT.PROCBLOCK)]    = {Token(WrapTk.LEFTPARENTHESIS) : Production([NonTerm(WrapNT.PROCBLOCK2),
                                                                                                 Token(WrapTk.SEMICOLON),
                                                                                                 NonTerm(WrapNT.BLOCKBODY)]),

                                                     Token(WrapTk.SEMICOLON) : Production([NonTerm(WrapNT.PROCBLOCK2),
                                                                                           Token(WrapTk.SEMICOLON),
                                                                                           NonTerm(WrapNT.BLOCKBODY)])}

        self._table[NonTerm(WrapNT.PROCBLOCK2)]   = {Token(WrapTk.LEFTPARENTHESIS) : Production([Token(WrapTk.LEFTPARENTHESIS),
                                                                                                 NonTerm(WrapNT.FORPARAMLIST),
                                                                                                 Token(WrapTk.RIGHTPARENTHESIS)]),
                                                     Token(WrapTk.SEMICOLON) : None}

        self._table[NonTerm(WrapNT.FORPARAMLIST)] = {Token(WrapTk.VAR)       : Production([NonTerm(WrapNT.PARAMDEF),
                                                                                           NonTerm(WrapNT.PARAMDEF2)]),
                                                     Token(WrapTk.ID)        : Production([NonTerm(WrapNT.PARAMDEF),
                                                                                           NonTerm(WrapNT.PARAMDEF2)]),
                                                     Token(WrapTk.RIGHTPARENTHESIS) : None}

        self._table[NonTerm(WrapNT.PARAMDEF)]     = {Token(WrapTk.VAR)       : Production([Token(WrapTk.VAR),
                                                                                           NonTerm(WrapNT.RECSECTION)]),
                                                     Token(WrapTk.ID)        : Production([NonTerm(WrapNT.RECSECTION)])}

        self._table[NonTerm(WrapNT.PARAMDEF2)]    = {Token(WrapTk.SEMICOLON) : Production([Token(WrapTk.SEMICOLON),
                                                                                           NonTerm(WrapNT.PARAMDEF),
                                                                                           NonTerm(WrapNT.PARAMDEF2)]),
                                                     Token(WrapTk.RIGHTPARENTHESIS) : None}

        self._table[NonTerm(WrapNT.STATEMENT)]    = {Token(WrapTk.ID)        : Production([Token(WrapTk.ID),
                                                                                           NonTerm(WrapNT.STATEGROUP)]),

                                                     Token(WrapTk.IF)        : Production([NonTerm(WrapNT.IFSTATE)]),
                                                     Token(WrapTk.WHILE)     : Production([NonTerm(WrapNT.WHILESTATE)]),
                                                     Token(WrapTk.BEGIN)     : Production([NonTerm(WrapNT.COMPSTATE)]),
                                                     Token(WrapTk.ELSE)      : None,
                                                     Token(WrapTk.END)       : None,
                                                     Token(WrapTk.SEMICOLON) : None}

        self._table[NonTerm(WrapNT.STATEGROUP)]   = {Token(WrapTk.LEFTBRACKET) : Production([NonTerm(WrapNT.FACTOR2),
                                                                                             Token(WrapTk.BECOMES),
                                                                                             NonTerm(WrapNT.EXPRESSION)]),

                                                     Token(WrapTk.PERIOD)      : Production([NonTerm(WrapNT.FACTOR),
                                                                                             Token(WrapTk.BECOMES),
                                                                                             NonTerm(WrapNT.EXPRESSION)]),

                                                     Token(WrapTk.BECOMES)     : Production([NonTerm(WrapNT.FACTOR2),
                                                                                             Token(WrapTk.BECOMES),
                                                                                             NonTerm(WrapNT.EXPRESSION)]),

                                                     Token(WrapTk.LEFTPARENTHESIS) : Production([NonTerm(WrapNT.PROCSTATE)]),
                                                     Token(WrapTk.ELSE)        : Production([NonTerm(WrapNT.PROCSTATE)]),
                                                     Token(WrapTk.END)         : Production([NonTerm(WrapNT.PROCSTATE)]),
                                                     Token(WrapTk.SEMICOLON)   : Production([NonTerm(WrapNT.PROCSTATE)])}

        self._table[NonTerm(WrapNT.PROCSTATE)]    = {Token(WrapTk.LEFTPARENTHESIS) : Production([Token(WrapTk.LEFTPARENTHESIS),
                                                                                                 NonTerm(WrapNT.ACTPARAMLIST),
                                                                                                 Token(WrapTk.RIGHTPARENTHESIS)]),
                                                     Token(WrapTk.ELSE)        : None,
                                                     Token(WrapTk.END)         : None,
                                                     Token(WrapTk.SEMICOLON)   : None}

        self._table[NonTerm(WrapNT.ACTPARAMLIST)] = {Token(WrapTk.PLUS)        : Production([NonTerm(WrapNT.EXPRESSION),
                                                                                             NonTerm(WrapNT.EXPRESSION2)]),

                                                     Token(WrapTk.MINUS)       : Production([NonTerm(WrapNT.EXPRESSION),
                                                                                             NonTerm(WrapNT.EXPRESSION2)]),

                                                     Token(WrapTk.NUMERAL)     : Production([NonTerm(WrapNT.EXPRESSION),
                                                                                             NonTerm(WrapNT.EXPRESSION2)]),

                                                     Token(WrapTk.ID)          : Production([NonTerm(WrapNT.EXPRESSION),
                                                                                             NonTerm(WrapNT.EXPRESSION2)]),

                                                     Token(WrapTk.NOT)         : Production([NonTerm(WrapNT.EXPRESSION),
                                                                                             NonTerm(WrapNT.EXPRESSION2)]),

                                                     Token(WrapTk.LEFTPARENTHESIS) : Production([NonTerm(WrapNT.EXPRESSION),
                                                                                                 NonTerm(WrapNT.EXPRESSION2)])}

        self._table[NonTerm(WrapNT.EXPRESSION2)]  = {Token(WrapTk.COMMA)       : Production([Token(WrapTk.COMMA),
                                                                                                 NonTerm(WrapNT.EXPRESSION),
                                                                                                 NonTerm(WrapNT.EXPRESSION2)]),
                                                    Token(WrapTk.RIGHTPARENTHESIS) : None}

        self._table[NonTerm(WrapNT.IFSTATE)]      = {Token(WrapTk.IF)          : Production([Token(WrapTk.IF),
                                                                                             NonTerm(WrapNT.EXPRESSION),
                                                                                             Token(WrapTk.THEN),
                                                                                             NonTerm(WrapNT.STATEMENT),
                                                                                             NonTerm(WrapNT.IFSTATE2)])}

        self._table[NonTerm(WrapNT.IFSTATE2)]     = {Token(WrapTk.ELSE)        : Production([Token(WrapTk.ELSE),
                                                                                             NonTerm(WrapNT.STATEMENT)]),
                                                    #Token(WrapTk.ELSE)        : None,
                                                     Token(WrapTk.END)         : None,
                                                     Token(WrapTk.SEMICOLON)   : None}

        self._table[NonTerm(WrapNT.WHILESTATE)]   = {Token(WrapTk.WHILE)       : Production([Token(WrapTk.WHILE),
                                                                                             NonTerm(WrapNT.EXPRESSION),
                                                                                             Token(WrapTk.DO),
                                                                                             NonTerm(WrapNT.STATEMENT)])}

        self._table[NonTerm(WrapNT.COMPSTATE)]    = {Token(WrapTk.BEGIN)       : Production([Token(WrapTk.BEGIN),
                                                                                             NonTerm(WrapNT.STATEMENT),
                                                                                             NonTerm(WrapNT.STATEMENT2),
                                                                                             Token(WrapTk.END)])}

        self._table[NonTerm(WrapNT.STATEMENT2)]   = {Token(WrapTk.SEMICOLON)   : Production([Token(WrapTk.SEMICOLON),
                                                                                             NonTerm(WrapNT.STATEMENT),
                                                                                             NonTerm(WrapNT.STATEMENT2)]),
                                                     Token(WrapTk.END)         : None}

        self._table[NonTerm(WrapNT.EXPRESSION)]   = {Token(WrapTk.PLUS)        : Production([NonTerm(WrapNT.SIMPLEEXPR),
                                                                                             NonTerm(WrapNT.EXPRGROUP)]),

                                                     Token(WrapTk.MINUS)       : Production([NonTerm(WrapNT.SIMPLEEXPR),
                                                                                             NonTerm(WrapNT.EXPRGROUP)]),

                                                     Token(WrapTk.NUMERAL)     : Production([NonTerm(WrapNT.SIMPLEEXPR),
                                                                                             NonTerm(WrapNT.EXPRGROUP)]),

                                                     Token(WrapTk.ID)          : Production([NonTerm(WrapNT.SIMPLEEXPR),
                                                                                             NonTerm(WrapNT.EXPRGROUP)]),

                                                     Token(WrapTk.NOT)         : Production([NonTerm(WrapNT.SIMPLEEXPR),
                                                                                             NonTerm(WrapNT.EXPRGROUP)]),

                                                     Token(WrapTk.LEFTPARENTHESIS) : Production([NonTerm(WrapNT.SIMPLEEXPR),
                                                                                                 NonTerm(WrapNT.EXPRGROUP)])}

        self._table[NonTerm(WrapNT.EXPRGROUP)]    = {Token(WrapTk.LESS)        : Production([NonTerm(WrapNT.RELATOPER),
                                                                                             NonTerm(WrapNT.SIMPLEEXPR)]),

                                                     Token(WrapTk.EQUAL)       : Production([NonTerm(WrapNT.RELATOPER),
                                                                                             NonTerm(WrapNT.SIMPLEEXPR)]),

                                                     Token(WrapTk.GREATER)     : Production([NonTerm(WrapNT.RELATOPER),
                                                                                             NonTerm(WrapNT.SIMPLEEXPR)]),

                                                     Token(WrapTk.NOTGREATER)  : Production([NonTerm(WrapNT.RELATOPER),
                                                                                             NonTerm(WrapNT.SIMPLEEXPR)]),

                                                     Token(WrapTk.NOTEQUAL)    : Production([NonTerm(WrapNT.RELATOPER),
                                                                                             NonTerm(WrapNT.SIMPLEEXPR)]),

                                                     Token(WrapTk.NOTLESS)     : Production([NonTerm(WrapNT.RELATOPER),
                                                                                             NonTerm(WrapNT.SIMPLEEXPR)]),
                                                     Token(WrapTk.ELSE)        : None,
                                                     Token(WrapTk.END)         : None,
                                                     Token(WrapTk.SEMICOLON)   : None,
                                                     Token(WrapTk.COMMA)       : None,
                                                     Token(WrapTk.RIGHTPARENTHESIS) : None,
                                                     Token(WrapTk.DO)          : None,
                                                     Token(WrapTk.RIGHTBRACKET) : None,
                                                     Token(WrapTk.THEN)        : None}

        self._table[NonTerm(WrapNT.RELATOPER)]    = {Token(WrapTk.LESS)        : Production([Token(WrapTk.LESS)]),
                                                     Token(WrapTk.EQUAL)       : Production([Token(WrapTk.EQUAL)]),
                                                     Token(WrapTk.GREATER)     : Production([Token(WrapTk.GREATER)]),
                                                     Token(WrapTk.NOTGREATER)  : Production([Token(WrapTk.NOTGREATER)]),
                                                     Token(WrapTk.NOTEQUAL)    : Production([Token(WrapTk.NOTEQUAL)]),
                                                     Token(WrapTk.NOTLESS)     : Production([Token(WrapTk.NOTLESS)])}

        self._table[NonTerm(WrapNT.SIMPLEEXPR)]   = {Token(WrapTk.PLUS)        : Production([NonTerm(WrapNT.SIGN),
                                                                                             NonTerm(WrapNT.TERM),
                                                                                             NonTerm(WrapNT.SIMPLEEXPRGROUP)]),

                                                     Token(WrapTk.MINUS)       : Production([NonTerm(WrapNT.SIGN),
                                                                                             NonTerm(WrapNT.TERM),
                                                                                             NonTerm(WrapNT.SIMPLEEXPRGROUP)]),

                                                     Token(WrapTk.NUMERAL)     : Production([NonTerm(WrapNT.SIGN),
                                                                                             NonTerm(WrapNT.TERM),
                                                                                             NonTerm(WrapNT.SIMPLEEXPRGROUP)]),

                                                     Token(WrapTk.ID)          : Production([NonTerm(WrapNT.SIGN),
                                                                                             NonTerm(WrapNT.TERM),
                                                                                             NonTerm(WrapNT.SIMPLEEXPRGROUP)]),

                                                     Token(WrapTk.NOT)         : Production([NonTerm(WrapNT.SIGN),
                                                                                             NonTerm(WrapNT.TERM),
                                                                                             NonTerm(WrapNT.SIMPLEEXPRGROUP)]),

                                                     Token(WrapTk.LEFTPARENTHESIS) : Production([NonTerm(WrapNT.SIGN),
                                                                                                 NonTerm(WrapNT.TERM),
                                                                                                 NonTerm(WrapNT.SIMPLEEXPRGROUP)])}

        self._table[NonTerm(WrapNT.SIGN)]         = {Token(WrapTk.PLUS)        : Production([NonTerm(WrapNT.SIGNOPER)]),
                                                     Token(WrapTk.MINUS)       : Production([NonTerm(WrapNT.SIGNOPER)]),
                                                     Token(WrapTk.NUMERAL)     : None,
                                                     Token(WrapTk.ID)          : None,
                                                     Token(WrapTk.NOT)         : None,
                                                     Token(WrapTk.LEFTPARENTHESIS) : None}

        self._table[NonTerm(WrapNT.SIMPLEEXPRGROUP)] = {Token(WrapTk.PLUS)     : Production([NonTerm(WrapNT.ADDIOPER),
                                                                                             NonTerm(WrapNT.TERM),
                                                                                             NonTerm(WrapNT.SIMPLEEXPRGROUP)]),

                                                        Token(WrapTk.MINUS)    : Production([NonTerm(WrapNT.ADDIOPER),
                                                                                             NonTerm(WrapNT.TERM),
                                                                                             NonTerm(WrapNT.SIMPLEEXPRGROUP)]),

                                                        Token(WrapTk.OR)       : Production([NonTerm(WrapNT.ADDIOPER),
                                                                                             NonTerm(WrapNT.TERM),
                                                                                             NonTerm(WrapNT.SIMPLEEXPRGROUP)]),

                                                        Token(WrapTk.ELSE)     : None,
                                                        Token(WrapTk.END)      : None,
                                                        Token(WrapTk.SEMICOLON) : None,
                                                        Token(WrapTk.COMMA)    : None,
                                                        Token(WrapTk.RIGHTPARENTHESIS) : None,
                                                        Token(WrapTk.DO)       : None,
                                                        Token(WrapTk.RIGHTBRACKET) : None,
                                                        Token(WrapTk.THEN)     : None,
                                                        Token(WrapTk.LESS)     : None,
                                                        Token(WrapTk.EQUAL)    : None,
                                                        Token(WrapTk.GREATER)  : None,
                                                        Token(WrapTk.NOTGREATER) : None,
                                                        Token(WrapTk.NOTEQUAL) : None,
                                                        Token(WrapTk.NOTLESS)  : None}

        self._table[NonTerm(WrapNT.SIGNOPER)]     = {Token(WrapTk.PLUS)        : Production([Token(WrapTk.PLUS)]),
                                                     Token(WrapTk.MINUS)       : Production([Token(WrapTk.MINUS)])}

        self._table[NonTerm(WrapNT.ADDIOPER)]     = {Token(WrapTk.PLUS)        : Production([Token(WrapTk.PLUS)]),
                                                     Token(WrapTk.MINUS)       : Production([Token(WrapTk.MINUS)]),
                                                     Token(WrapTk.OR)          : Production([Token(WrapTk.OR)])}

        self._table[NonTerm(WrapNT.TERM)]         = {Token(WrapTk.NUMERAL)     : Production([NonTerm(WrapNT.FACTOR),
                                                                                             NonTerm(WrapNT.MULTIPLYING)]),

                                                     Token(WrapTk.ID)          : Production([NonTerm(WrapNT.FACTOR),
                                                                                             NonTerm(WrapNT.MULTIPLYING)]),

                                                     Token(WrapTk.NOT)         : Production([NonTerm(WrapNT.FACTOR),
                                                                                             NonTerm(WrapNT.MULTIPLYING)]),

                                                     Token(WrapTk.LEFTPARENTHESIS) : Production([NonTerm(WrapNT.FACTOR),
                                                                                                 NonTerm(WrapNT.MULTIPLYING)])}

        self._table[NonTerm(WrapNT.MULTIPLYING)]  = {Token(WrapTk.ASTERISK)    : Production([NonTerm(WrapNT.MULTIPLYOPER),
                                                                                             NonTerm(WrapNT.FACTOR),
                                                                                             NonTerm(WrapNT.MULTIPLYING)]),

                                                     Token(WrapTk.DIV)         : Production([NonTerm(WrapNT.MULTIPLYOPER),
                                                                                             NonTerm(WrapNT.FACTOR),
                                                                                             NonTerm(WrapNT.MULTIPLYING)]),

                                                     Token(WrapTk.MOD)         : Production([NonTerm(WrapNT.MULTIPLYOPER),
                                                                                             NonTerm(WrapNT.FACTOR),
                                                                                             NonTerm(WrapNT.MULTIPLYING)]),

                                                     Token(WrapTk.AND)         : Production([NonTerm(WrapNT.MULTIPLYOPER),
                                                                                             NonTerm(WrapNT.FACTOR),
                                                                                             NonTerm(WrapNT.MULTIPLYING)]),

                                                     Token(WrapTk.PLUS)        : None,
                                                     Token(WrapTk.MINUS)       : None,
                                                     Token(WrapTk.OR)          : None,
                                                     Token(WrapTk.ELSE)        : None,
                                                     Token(WrapTk.END)         : None,
                                                     Token(WrapTk.SEMICOLON)   : None,
                                                     Token(WrapTk.COMMA)       : None,
                                                     Token(WrapTk.RIGHTPARENTHESIS) : None,
                                                     Token(WrapTk.DO)          : None,
                                                     Token(WrapTk.RIGHTBRACKET) : None,
                                                     Token(WrapTk.THEN)        : None,
                                                     Token(WrapTk.LESS)        : None,
                                                     Token(WrapTk.EQUAL)       : None,
                                                     Token(WrapTk.GREATER)     : None,
                                                     Token(WrapTk.NOTGREATER)  : None,
                                                     Token(WrapTk.NOTEQUAL)    : None,
                                                     Token(WrapTk.NOTLESS)     : None}

        self._table[NonTerm(WrapNT.MULTIPLYOPER)] = {Token(WrapTk.ASTERISK)    : Production([Token(WrapTk.ASTERISK)]),
                                                     Token(WrapTk.DIV)         : Production([Token(WrapTk.DIV)]),
                                                     Token(WrapTk.MOD)         : Production([Token(WrapTk.MOD)]),
                                                     Token(WrapTk.AND)         : Production([Token(WrapTk.AND)])}
    
        self._table[NonTerm(WrapNT.FACTOR)]       = {Token(WrapTk.NUMERAL)     : Production([Token(WrapTk.NUMERAL)]),

                                                     Token(WrapTk.ID)          : Production([Token(WrapTk.ID),
                                                                                             NonTerm(WrapNT.FACTOR2)]),

                                                     Token(WrapTk.LEFTPARENTHESIS) : Production([Token(WrapTk.LEFTPARENTHESIS),
                                                                                                 NonTerm(WrapNT.EXPRESSION),
                                                                                                 Token(WrapTk.RIGHTPARENTHESIS)]),

                                                     Token(WrapTk.NOT)         : Production([Token(WrapTk.NOT),
                                                                                             NonTerm(WrapNT.FACTOR)])}

        self._table[NonTerm(WrapNT.FACTOR2)]      = {Token(WrapTk.LEFTBRACKET) : Production([NonTerm(WrapNT.SELECTOR),
                                                                                             NonTerm(WrapNT.FACTOR2)]),

                                                     Token(WrapTk.PERIOD)      : Production([NonTerm(WrapNT.SELECTOR),
                                                                                             NonTerm(WrapNT.FACTOR2)]),

                                                     Token(WrapTk.BECOMES)     : None,
                                                     Token(WrapTk.ASTERISK)    : None,
                                                     Token(WrapTk.DIV)         : None,
                                                     Token(WrapTk.MOD)         : None,
                                                     Token(WrapTk.AND)         : None,
                                                     Token(WrapTk.PLUS)        : None,
                                                     Token(WrapTk.MINUS)       : None,
                                                     Token(WrapTk.OR)          : None,
                                                     Token(WrapTk.ELSE)        : None,
                                                     Token(WrapTk.END)         : None,
                                                     Token(WrapTk.SEMICOLON)   : None,
                                                     Token(WrapTk.COMMA)       : None,
                                                     Token(WrapTk.RIGHTPARENTHESIS) : None,
                                                     Token(WrapTk.DO)          : None,
                                                     Token(WrapTk.RIGHTBRACKET): None,
                                                     Token(WrapTk.THEN)        : None,
                                                     Token(WrapTk.LESS)        : None,
                                                     Token(WrapTk.EQUAL)       : None,
                                                     Token(WrapTk.GREATER)     : None,
                                                     Token(WrapTk.NOTGREATER)  : None,
                                                     Token(WrapTk.NOTEQUAL)    : None,
                                                     Token(WrapTk.NOTLESS)     : None}

        self._table[NonTerm(WrapNT.SELECTOR)]     = {Token(WrapTk.LEFTBRACKET) : Production([NonTerm(WrapNT.INDEXSELECTOR)]),
                                                     Token(WrapTk.PERIOD)      : Production([NonTerm(WrapNT.FIELDSELECTOR)])}

        self._table[NonTerm(WrapNT.INDEXSELECTOR)] = {Token(WrapTk.LEFTBRACKET): Production([Token(WrapTk.LEFTBRACKET),
                                                                                             NonTerm(WrapNT.EXPRESSION),
                                                                                             Token(WrapTk.RIGHTBRACKET)])}

        self._table[NonTerm(WrapNT.FIELDSELECTOR)] = {Token(WrapTk.PERIOD)     : Production([Token(WrapTk.PERIOD),
                                                                                             Token(WrapTk.ID)])}

        self._table[NonTerm(WrapNT.CONSTANT)]     = {Token(WrapTk.NUMERAL)     : Production([Token(WrapTk.NUMERAL)]),
                                                     Token(WrapTk.ID)          : Production([Token(WrapTk.ID)])}

    def getCell(self, nterm, tok):
        row = self._table.get(nterm)
        return  self._table[nterm][tok]
