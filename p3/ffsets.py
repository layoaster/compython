#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Clase que almacena first y follow de cada uno de los simbolos no terminales de la gramatica de Pascal-
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

from token import *

class FFSets:

    def __init__(self):
        self._ffs = {}

        self._ffs["program"]                = ([WrapTk.PROGRAM],
                                               [WrapTk.ENDTEXT])

        self._ffs["blockBody"]              = ((WrapTk.CONST, WrapTk.TYPE, WrapTk.VAR, WrapTk.PROCEDURE, WrapTk.BEGIN),
                                               (WrapTk.PERIOD, WrapTk.SEMICOLON))

        self._ffs["constantDefinitionPart"] = ([WrapTk.CONST],
                                               (WrapTk.TYPE, WrapTk.VAR, WrapTk.PROCEDURE, WrapTk.BEGIN))

        self._ffs["constantDefinition"]     = ([WrapTk.ID],
                                               (WrapTk.ID, WrapTk.TYPE, WrapTk.VAR, WrapTk.PROCEDURE, WrapTk.BEGIN))


        self._ffs["typeDefinitionPart"]     = ([WrapTk.TYPE],
                                               (WrapTk.VAR, WrapTk.PROCEDURE, WrapTk.BEGIN))

        self._ffs["typeDefinition"]         = ([WrapTk.ID],
                                               (WrapTk.ID, WrapTk.VAR, WrapTk.PROCEDURE, WrapTk.BEGIN))

        self._ffs["newType"]                = ((WrapTk.ARRAY, WrapTk.RECORD),
                                               [WrapTk.SEMICOLON])

        self._ffs["newArrayType"]           = ([WrapTk.ARRAY],
                                               [WrapTk.SEMICOLON])

        self._ffs["indexRange"]             = ((WrapTk.NUMERAL, WrapTk.ID),
                                               [WrapTk.RIGHTBRACKET])

        self._ffs["newRecordType"]          = ([WrapTk.RECORD],
                                               [WrapTk.SEMICOLON])

        self._ffs["fieldList"]              = ([WrapTk.ID],
                                               [WrapTk.END])

        self._ffs["recordSection"]          = ([WrapTk.ID],
                                               (WrapTk.SEMICOLON, WrapTk.END))

        self._ffs["variableDefinitionPart"] = ([WrapTk.VAR],
                                               (WrapTk.PROCEDURE, WrapTk.BEGIN))

        self._ffs["variableDefinition"]     = ([WrapTk.ID],
                                               (WrapTk.ID, WrapTk.PROCEDURE, WrapTk.BEGIN))

        self._ffs["variableGroup"]          = ([WrapTk.ID],
                                               (WrapTk.SEMICOLON, WrapTk.RIGHTPARENTHESIS))

        self._ffs["procedureDefinition"]    = ([WrapTk.PROCEDURE],
                                               [WrapTk.BEGIN])

        self._ffs["procedureBlock"]         = ((WrapTk.LEFTPARENTHESIS, WrapTk.SEMICOLON),
                                               [WrapTk.SEMICOLON])

        self._ffs["formalParameterList"]    = ((WrapTk.VAR, WrapTk.ID),
                                               [WrapTk.RIGHTPARENTHESIS])

        self._ffs["parameterDefinition"]    = ((WrapTk.VAR, WrapTk.ID),
                                              (WrapTk.SEMICOLON, WrapTk.RIGHTPARENTHESIS))

        self._ffs["statement"]              = ((WrapTk.ID, WrapTk.IF, WrapTk.WHILE, WrapTk.BEGIN),
                                               (WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON))

        self._ffs["statementGroup"]         = ((WrapTk.LEFTBRACKET, WrapTk.PERIOD, WrapTk.BECOMES, WrapTk.LEFTPARENTHESIS),
                                               (WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON))

        self._ffs["procedureStatement"]     = ([WrapTk.LEFTPARENTHESIS],
                                               (WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON))

        self._ffs["actualParameterList"]    = ((WrapTk.PLUS, WrapTk.MINUS, WrapTk.NUMERAL, WrapTk.ID, WrapTk.NOT, WrapTk.LEFTPARENTHESIS),
                                               [WrapTk.RIGHTPARENTHESIS])

        self._ffs["ifStatement"]            = ([WrapTk.IF],
                                               (WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON))

        self._ffs["whileStatement"]         = ([WrapTk.WHILE],
                                               (WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON))

        self._ffs["compoundStatement"]      = ([WrapTk.BEGIN],
                                               (WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON, WrapTk.PERIOD))

        self._ffs["expression"]             = ((WrapTk.PLUS, WrapTk.MINUS, WrapTk.NUMERAL, WrapTk.ID, WrapTk.NOT, WrapTk.LEFTPARENTHESIS),
                                               (WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON, WrapTk.COMMA, WrapTk.RIGHTPARENTHESIS, WrapTk.DO, WrapTk.RIGHTBRACKET, WrapTk.THEN))

        self._ffs["relationalOperator"]     = ((WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS),
                                               (WrapTk.PLUS, WrapTk.MINUS, WrapTk.NUMERAL, WrapTk.ID, WrapTk.NOT, WrapTk.LEFTPARENTHESIS))

        self._ffs["simpleExpression"]       = ((WrapTk.PLUS, WrapTk.MINUS, WrapTk.NUMERAL, WrapTk.ID, WrapTk.NOT, WrapTk.LEFTPARENTHESIS),
                                               (WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON, WrapTk.COMMA, WrapTk.RIGHTPARENTHESIS, WrapTk.DO, WrapTk.RIGHTBRACKET, WrapTk.THEN, WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS))

        self._ffs["signOperator"]           = ((WrapTk.PLUS, WrapTk.MINUS),
                                               (WrapTk.NUMERAL, WrapTk.ID, WrapTk.NOT, WrapTk.LEFTPARENTHESIS))

        self._ffs["additiveOperator"]       = ((WrapTk.PLUS, WrapTk.MINUS, WrapTk.OR),
                                               (WrapTk.NUMERAL, WrapTk.ID, WrapTk.NOT, WrapTk.LEFTPARENTHESIS))

        self._ffs["term"]                   = ((WrapTk.NUMERAL, WrapTk.ID, WrapTk.NOT, WrapTk.LEFTPARENTHESIS),
                                               (WrapTk.PLUS, WrapTk.MINUS, WrapTk.OR, WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON, WrapTk.COMMA, WrapTk.RIGHTPARENTHESIS, WrapTk.DO, WrapTk.RIGHTBRACKET, WrapTk.THEN, WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS))

        self._ffs["multiplyingOperator"]    = ((WrapTk.ASTERISK, WrapTk.DIV, WrapTk.MOD, WrapTk.AND),
                                               (WrapTk.NUMERAL, WrapTk.ID, WrapTk.NOT, WrapTk.LEFTPARENTHESIS))

        self._ffs["factor"]                 = ((WrapTk.NUMERAL, WrapTk.ID, WrapTk.NOT, WrapTk.LEFTPARENTHESIS),
                                               (WrapTk.ASTERISK, WrapTk.DIV, WrapTk.MOD, WrapTk.AND, WrapTk.PLUS, WrapTk.MINUS, WrapTk.OR, WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON, WrapTk.COMMA, WrapTk.RIGHTPARENTHESIS, WrapTk.DO, WrapTk.RIGHTBRACKET, WrapTk.THEN, WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS))

        self._ffs["selector"]               = ((WrapTk.LEFTBRACKET, WrapTk.PERIOD),
                                               (WrapTk.LEFTBRACKET, WrapTk.PERIOD, WrapTk.BECOMES, WrapTk.ASTERISK, WrapTk.DIV, WrapTk.MOD, WrapTk.AND, WrapTk.PLUS, WrapTk.MINUS, WrapTk.OR, WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON, WrapTk.COMMA, WrapTk.RIGHTPARENTHESIS, WrapTk.DO, WrapTk.RIGHTBRACKET, WrapTk.THEN, WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS))

        self._ffs["indexSelector"]          = ([WrapTk.LEFTBRACKET],
                                               (WrapTk.LEFTBRACKET, WrapTk.PERIOD, WrapTk.BECOMES, WrapTk.ASTERISK, WrapTk.DIV, WrapTk.MOD, WrapTk.AND, WrapTk.PLUS, WrapTk.MINUS, WrapTk.OR, WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON, WrapTk.COMMA, WrapTk.RIGHTPARENTHESIS, WrapTk.DO, WrapTk.RIGHTBRACKET, WrapTk.THEN, WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS))

        self._ffs["fieldSelector"]          = ([WrapTk.PERIOD],
                                               (WrapTk.LEFTBRACKET, WrapTk.PERIOD, WrapTk.BECOMES, WrapTk.ASTERISK, WrapTk.DIV, WrapTk.MOD, WrapTk.AND, WrapTk.PLUS, WrapTk.MINUS, WrapTk.OR, WrapTk.ELSE, WrapTk.END, WrapTk.SEMICOLON, WrapTk.COMMA, WrapTk.RIGHTPARENTHESIS, WrapTk.DO, WrapTk.RIGHTBRACKET, WrapTk.THEN, WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS))

        self._ffs["constant"]               = ((WrapTk.ID, WrapTk.NUMERAL),
                                               (WrapTk.SEMICOLON, WrapTk.DOUBLEDOT, WrapTk.RIGHTBRACKET))

    def first(self, noterm):
        """ Devuelve el conjunto FIRST de un simbolo no terminal de la gramatica
        """
        self._tkset = frozenset(self._ffs[noterm][0])
        return self._tkset

    def follow(self, noterm):
        """ Devuelve el conjunto FOLLOW de un simbolo no terminal de la gramatica
        """
        self._tkset = frozenset(self._ffs[noterm][1])
        return self._tkset

p = FFSets()

stop = p.first("program")

stop2 = stop.union((1, 2))

print stop2

stop2 = stop2.union(stop2, (30, 40), stop)

print stop2